import inspect
import flask_mailman
from flask_mailman import EmailMessage
print('module:', flask_mailman.__file__)
print('signature:', inspect.signature(EmailMessage))
print('html attrs:', [a for a in dir(EmailMessage) if 'html' in a.lower()])
