# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC2a9d7ad0292a5a1645f25a94224ca3db'
auth_token = '7d1c7264bc12eaddcc2473e752e97d6c'
client = Client(account_sid, auth_token)

service = client.messaging.services.create(friendly_name='friendly_name')

print(service.sid)