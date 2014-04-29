__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from google.appengine.ext import db


class Logs(db.Model):
    date_time = db.DateTimeProperty(required=True)
    category = db.StringProperty(required=True)
    author = db.StringProperty(required=True)
    description = db.StringProperty(required=True)
