__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from google.appengine.ext import db


class Parameters(db.Model):
    key = db.StringProperty(required=True)
    value = db.StringProperty(required=True)
