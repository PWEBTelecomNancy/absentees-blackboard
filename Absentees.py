__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from google.appengine.ext import db


class Absentees(db.Model):
    student_name = db.StringProperty(required=True)
    student_group = db.StringProperty(required=True)
    class_title = db.StringProperty(required=True)
    start_hour = db.TimeProperty(required=True)
    end_hour = db.TimeProperty(required=True)
    class_date = db.DateProperty(required=True)
    justification_bool = db.BooleanProperty(required=True)
    justification_text = db.StringProperty


