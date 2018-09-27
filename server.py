import os
import sys
import gammu
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

# Helpers
def auth_token_valid(token = None):
    return os.getenv('AUTH_TOKEN') == token

def ressource_protected():
    return 'AUTH_TOKEN' in os.environ

# Gammu stuff
# Taken from https://gammu.readthedocs.io/en/latest/python/examples.html and adapted

def send_sms(number, message_text):
    try:
        # Create object for talking with phone
        state_machine = gammu.StateMachine()
        state_machine.ReadConfig()

        # Connect to the phone
        state_machine.Init()

        # Prepare message data
        # We tell that we want to use first SMSC number stored in phone
        message = {
                'Text': text,
                'SMSC': {'Location': 1},
                'Number': number
                }

        # Actually send the message
        state_machine.SendSMS(message)
        return {"status": "Successfully send!"}
    except Exception as e:
        return {"error": "An error occured while sending SMS"}

@app.route('/send_sms/')
def sms_request():
    params = request.args.to_dict()
    auth_token = params['auth_token']
    phone_number = params['phone_number']
    message_text = params['message_text']

    if not ressource_protected():
        return '{"error": "Service not setup entirely!"}', 403
    elif not auth_token_valid(auth_token):
        return '{"error": "Authentication not successfull!"}', 403
    else:
        return {"foo": auth_token, "phone_number": phone_number, "message_text": message_text}, 200
        # status = send_sms(phone_number, message_text)
        # return status, 200

if __name__ == '__main__':
    # Set to false if FLASK_ENV=production????
    # Otherwise set to false or sth bad might happen...
    app.run(debug=True)
