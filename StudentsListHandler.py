__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from BaseHandler import *
from ADECommunicator import *

class StudentsListHandler(BaseHandler):
    ade_communicator = None

    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.page_name = "students_list"
        self.ade_communicator = ADECommunicator()

    def get(self):
        self.render("groupchoice.html")

    def post(self):
        group_to_find = self.request.get("group_name")
        groups = self.ade_communicator.get_students_groups()

        to_display = dict()
        for key in groups:
            if group_to_find in key:
                to_display[key] = groups[key]

        if len(to_display) > 0:
            self.render("groupdisplay.html", group_name=group_to_find, groups=to_display)
        else:
            self.render("message.html", title="No such group", subtitle="", argument=group_to_find)
