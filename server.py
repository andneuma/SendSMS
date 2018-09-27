import os
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions

app = FlaskAPI(__name__)

# Helpers
def auth_token_valid(token = None):
    return os.getenv('AUTH_TOKEN') == token

def ressource_protected():
    return 'AUTH_TOKEN' in os.environ


@app.route('/send_sms/')
def send_sms():
    params = request.args.to_dict()

    if not ressource_protected():
        return '{"error": "Service not setup entirely!"}', 403
    elif not auth_token_valid(params['auth_token']):
        return '{"error": "Authentication not successfull!"}', 403
    else:
        try:
            # send_sms()
            # return None, 200
            return 'Worked!'
        except:
            return {"error": "An error occured while sending SMS"}

if __name__ == '__main__':
    app.run(debug=True)
