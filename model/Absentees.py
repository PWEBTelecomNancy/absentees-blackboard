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
    justification_text = db.StringProperty(required=True)


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


def get_absentees_from_criteria(date, class_title, student_name):
    if date != "" and class_title == "" and student_name == "":
        query = db.GqlQuery("SELECT * FROM Absentees WHERE class_date=:date", date=date)

    elif date == "" and class_title != "" and student_name == "":
        query = db.GqlQuery("SELECT * FROM Absentees WHERE class_title=:class_title", class_title=class_title)

    elif date == "" and class_title == "" and student_name != "":
        query = db.GqlQuery("SELECT * FROM Absentees WHERE student_name=:student_name", student_name=student_name)

    elif date != "" and class_title != "" and student_name == "":
        query = db.GqlQuery("SELECT * FROM Absentees WHERE class_date=:date AND class_title=:class_title", date=date,
                            class_title=class_title)

    elif date == "" and class_title != "" and student_name != "":
        query = db.GqlQuery("SELECT * FROM Absentees WHERE class_title=:class_title AND student_name=:student_name",
                            class_title=class_title, student_name=student_name)

    elif date != "" and class_title == "" and student_name != "":
        query = db.GqlQuery("SELECT * FROM Absentees WHERE class_date=:date AND student_name=:student_name", date=date,
                            student_name=student_name)

    elif date != "" and class_title != "" and student_name != "":
        query = db.GqlQuery("SELECT * FROM Absentees WHERE class_date=:date AND class_title=:class_title "
                            "AND student_name=:student_name", date=date, class_title=class_title,
                            student_name=student_name)

    result = query.fetch(limit=None)
    return result


def get_absentee_from_id(abs_id):
    return Absentees.get_by_id(int(abs_id))


def get_absentees_from_class_title(class_title):
    query = db.GqlQuery("SELECT * FROM Absentees WHERE class_title=:class_title", class_title=class_title)
    return query.fetch(limit=None)

def get_absentees_from_student_name(student_n):
    query = db.GqlQuery("SELECT * FROM Absentees WHERE student_name=:std_n",std_n = student_n)
    return query.fetch(limit=None)

def get_absentees_from_group_name(group_name):
    query = db.GqlQuery("SELECT * FROM Absentees WHERE student_group=:group_name", group_name=group_name)
    return query.fetch(limit=None)