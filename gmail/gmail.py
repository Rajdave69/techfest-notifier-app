import os
import pickle
# Gmail API utils
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
# for encoding/decoding messages in base64
from base64 import urlsafe_b64decode, urlsafe_b64encode
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

import email
import base64

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


class GMAIL:

    def __init__(self):
        self.service = self.gmail_authenticate()

    def gmail_authenticate(self):
        creds = None
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('./gmail/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # save the credentials for the next run
            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)
        return build('gmail', 'v1', credentials=creds)

    def get_email(self, msg_id):

        try:
            message_list = self.service.users().messages().get(userId='me', id=msg_id, format='raw').execute()

            msg_raw = base64.urlsafe_b64decode(message_list['raw'].encode('ASCII'))
            msg_str = email.message_from_bytes(msg_raw)

            content_type = msg_str.get_content_maintype()

            if content_type == 'multipart':
                for part in msg_str.get_payload():
                    if part.get_content_maintype() == 'text':
                        body = part.get_payload(decode=True).decode('utf-8')
                        break
            else:
                body = msg_str.get_payload(decode=True).decode('utf-8')

            return {'subject': msg_str['subject'], 'sender': msg_str['from'], 'body': body,
                    'timestamp': msg_str['Date'], 'id': msg_id}

        except HttpError as error:
            print(f'An error occurred: {error}')

    def search_emails(self):
        result = self.service.users().messages().list(userId='me', labelIds="UNREAD").execute()
        number_result = result['resultSizeEstimate']

        final_list = []

        if number_result > 0:
            message_ids = result['messages']

            for ids in message_ids:
                final_list.append(ids['id'])
                self.get_email(self.service, ids['id'])

            return final_list

    def mark_read(self, msg_id):

        try:
            self.service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': 'UNREAD'}).execute()
            print("success")
        except HttpError as error:
            print(error, "could not mark as READ")

# print(search_messages(service))
