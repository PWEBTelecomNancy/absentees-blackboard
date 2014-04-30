__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *
from model.ADECommunicator import *


class StudentsListHandler(BaseHandler):
    """
    Display a list of students.
    The lists are flattened and the sublists' names are discarded.
    """
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

        # Flatten lists
        members = [item for middle_list in to_display for item in to_display[middle_list]]
        members = sorted(members)

        #Uniq list
        temp = members
        members = []
        uniq_mail = []

        for m in temp:
            if m['mail'] not in uniq_mail:
                members.append(m)
                uniq_mail.append(m['mail'])

        if len(to_display) > 0:
            self.render("groupdisplay.html", group_name=group_to_find, groups=members)
        else:
            self.render("message.html", title="No such group", subtitle="", argument=group_to_find)
