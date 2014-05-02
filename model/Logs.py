__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from google.appengine.ext import ndb


class Logs(ndb.Model):
    date_time = ndb.DateTimeProperty(required=True)
    category = ndb.StringProperty(required=True)
    author = ndb.StringProperty(required=True)
    description = ndb.StringProperty(required=True)

def get_all_logs():
    return Logs.query().order(-Logs.date_time).fetch()