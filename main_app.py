from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from api.app import app as backend
from web.app import app as frontend
from flask_mailman import Mail
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

orig_SMTP_SSL_init = smtplib.SMTP_SSL.__init__
def patched_SMTP_SSL_init(self, *args, **kwargs):
    kwargs.pop('keyfile', None)
    kwargs.pop('certfile', None)
    orig_SMTP_SSL_init(self, *args, **kwargs)
smtplib.SMTP_SSL.__init__ = patched_SMTP_SSL_init

orig_starttls = smtplib.SMTP.starttls
def patched_starttls(self, *args, **kwargs):
    kwargs.pop('keyfile', None)
    kwargs.pop('certfile', None)
    return orig_starttls(self, *args, **kwargs)
smtplib.SMTP.starttls = patched_starttls

app = Flask(__name__)

backend.config['MAIL_SERVER'] = 'smtp.gmail.com'
backend.config['MAIL_PORT'] = 587
backend.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
backend.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_APP_PASSWORD')
backend.config['MAIL_USE_TLS'] = True
backend.config['MAIL_USE_SSL'] = False
backend.config['MAIL_DEFAULT_TO_SET'] = os.environ.get('EMAIL_USER')

mail = Mail(backend)

app.wsgi_app = DispatcherMiddleware(
    frontend.wsgi_app,
    {
        '/api': backend.wsgi_app
    }
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)