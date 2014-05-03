__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

import re

from handler.BaseHandler import *
from model.Absentees import *
from model.ADECommunicator import *


class AbsenteesMonitorHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        super(AbsenteesMonitorHandler, self).__init__()
        self.initialize(request, response)
        self.page_name = "absentees_monitor"

    def get(self):
        if self.is_connected():
            self.render("absentees_monitor.html")

        else:
            self.render("message.html", title="Access forbidden",
                        text="It seems you're not a connected user")

    def post(self):
        if self.is_connected():
            if self.request.get('class_title'):
                absentees = get_absentees_from_class_title(self.request.get('class_title'))
                self.render("absentees_monitor_results.html", absentees=absentees,
                            search_object=self.request.get('class_title'))

            else:
                group_re = re.compile(self.request.get('group_name'))
                absentees = []
                communicator = ADECommunicator()
                student_groups = communicator.get_students_groups()

                for group in student_groups:
                    if group_re.match(group):
                        absentees.extend(get_absentees_from_group_name(group))

                self.render("absentees_monitor_results.html", search_object=self.request.get('group_name'),
                            absentees=absentees)

        else:
            self.render("message.html", title="Access forbidden",
                        text="It seems you're not a connected user")