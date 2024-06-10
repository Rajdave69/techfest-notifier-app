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

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
our_email = 'muhammedrayan.official@gmail.com'

def gmail_authenticate():
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

def get_message(service, msg_id):

    try:
        message_list=service.users().messages().get(userId='me', id=msg_id, format='raw').execute()

        msg_raw = base64.urlsafe_b64decode(message_list['raw'].encode('ASCII'))

        msg_str = email.message_from_bytes(msg_raw)

        content_types = msg_str.get_content_maintype()
        
        #how it will work when is a multipart or plain text

        if content_types == 'multipart':
            part1, part2 = msg_str.get_payload()
            print("This is the message body, html:")
            print(part1.get_payload())
            return part1.get_payload()
        else:
            print("This is the message body plain text:")
            print(msg_str.get_payload())
            return msg_str.get_payload()


    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

def search_messages(service):
    result = service.users().messages().list(userId='me', labelIds="UNREAD").execute()
    number_result = result['resultSizeEstimate']

    final_list = []

    if number_result>0:
        message_ids = result['messages']

        for ids in message_ids:
            final_list.append(ids['id'])
            # call the function that will call the body of the message
            get_message(service, ids['id'] )
            
        return final_list

def mark_read(abc):
    pass

service = gmail_authenticate()

print('')
print(search_messages(service))
