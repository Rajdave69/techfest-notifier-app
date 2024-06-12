import requests

headers = {'content-type': 'application/json'}
body = {'title': 'hi', 'body': 'bye', 'image_url': ''}
requests.post("http://127.0.0.1:8381/api/send-notification/", data=body, headers=headers)