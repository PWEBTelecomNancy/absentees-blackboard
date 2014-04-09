__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from google.appengine.ext import db


class Accounts(db.Model):
    login = db.StringProperty(required=True)
    password = db.StringProperty(required=True)
    is_admin = db.BooleanProperty(required=True)
    is_teacher = db.BooleanProperty(required=True)
    email_address = db.StringProperty(required=True)
