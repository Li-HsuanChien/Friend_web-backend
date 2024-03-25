from django.conf import settings
from mailjet_rest import Client

mailjet = Client(auth=(settings.MJ_APIKEY_PUBLIC, settings.MJ_APIKEY_PRIVATE), version='v3.1')

def send_confirmation_email(email, token_id, user_id):
    data = {
    'Messages': [
                    {
                            "From": {
                                    "Email": "lpc5553@psu.edu",
                                    "Name": "friendweb"
                            },
                            "To": [
                                    {
                                            "Email": email,
                                            "Name": "User"
                                    }
                            ],
                            "Subject": "Confirm you email account for friend web!",
                            "TextPart": "Want to join your friends on the web?",
                            "HTMLPart": """<strong>Please confirm your email address by directing to this link!!</strong><br/><br/>
<a href="https://li-hsuanchien.github.io/Friend_web-frontend/public/verify/{}">Click here to verify your email</a>""".format(str(token_id))
                    }
            ]
    }    
    result = mailjet.send.create(data=data)
    print (result.status_code, result.json())

def send_password_email(email, token_id, user_id):
    data = {
    'Messages': [
                    {
                            "From": {
                                    "Email": "lpc5553@psu.edu",
                                    "Name": "friendweb"
                            },
                            "To": [
                                    {
                                            "Email": email,
                                            "Name": "User"
                                    }
                            ],
                            "Subject": "Reset your password for Friend-Web!",
                            "TextPart": "Forgot your password?",
                            "HTMLPart": """<strong>Please reset your password by directing to this link!!</strong><br/><br/>
<a href="https://li-hsuanchien.github.io/Friend_web-frontend/public/reset-password/{}">Click here to reset your password</a>""".format(str(token_id))
                    }
            ]
    }    
    result = mailjet.send.create(data=data)
    print (result.status_code, result.json())