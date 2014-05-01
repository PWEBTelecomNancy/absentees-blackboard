__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *
from model.Absentees import *


class AbsenteesAdminHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.page_name = "administration"

    def get(self):
        if self.is_connected() and get_is_admin_from_id(self.request.cookies.get('user_id').split('|')[0]):
            absentees = get_all_absentees()

            self.render("administration_absentees.html", absentees=absentees)

        else:
            self.render("message.html", title="Access forbidden",
                        text="It seems you're not an administrator nor a connected user")

    def post(self):
        if self.is_connected() and get_is_admin_from_id(self.request.cookies.get('user_id').split('|')[0]):
            date = self.request.get('date')
            class_title = self.request.get('class_title')
            student_name = self.request.get('student_name')

            absentees = get_absentees_from_criteria(date, class_title, student_name)

            self.render("administration_absentees.html", absentees=absentees)

        else:
            self.render("message.html", title="Access forbidden",
                        text="It seems you're not an administrator nor a connected user")