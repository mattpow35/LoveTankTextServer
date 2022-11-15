# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "AC7e552889981f23f2dab7d4e11f440d93"
auth_token = '68aa6533885d7e12a0fee192c1cb00e2'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+18609796457',
                     to='+13854211240'
                 )

print(message.sid)


