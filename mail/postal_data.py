import json

with open('mail/mail_client_settings.json', 'r') as file:
  data = json.load(file)

MAIL = data['MAIL']
PASSWORD = data['PASSWORD']
PASSWORD_MAIL_APP = data['PASSWORD_MAIL_APP']
