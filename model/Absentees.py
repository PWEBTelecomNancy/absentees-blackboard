__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from google.appengine.ext import db


class Absentees(db.Model):
    student_name = db.StringProperty(required=True)
    student_email = db.StringProperty(required=True)
    student_group = db.StringProperty(required=True)
    class_title = db.StringProperty(required=True)
    teacher_name = db.StringProperty(required=True)
    start_hour = db.StringProperty(required=True)
    end_hour = db.StringProperty(required=True)
    class_date = db.StringProperty(required=True)
    justification_bool = db.BooleanProperty(required=True)
    justification_text = db.StringProperty


def get_absentees_for_class(class_title, teacher_name, class_date, start_hour, end_hour):
    result = db.GqlQuery("SELECT * FROM Absentees WHERE class_title=:class_title AND teacher_name=:teacher_name AND "
                         "class_date=:class_date AND start_hour=:start_hour AND end_hour=:end_hour",
                         class_title=class_title, teacher_name=teacher_name, class_date=class_date,
                         start_hour=start_hour, end_hour=end_hour)
    result = list(result)
    return result


def get_all_absentees():
    query = Absentees.all()
    return query.fetch(limit=None)