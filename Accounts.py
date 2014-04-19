__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from google.appengine.ext import db
import hashlib
import random
import string

class Accounts(db.Model):
    login = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    is_admin = db.BooleanProperty(required=True)
    is_teacher = db.BooleanProperty(required=True)
    email_address = db.StringProperty(required=True)


def salt_generation():
    return ''.join(random.choice(string.letters) for i in range(5))


def password_hash(password):
    salt = salt_generation()
    return str(hashlib.sha256(password + salt).hexdigest()) + '|' + salt