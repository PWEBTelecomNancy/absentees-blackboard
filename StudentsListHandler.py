__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from BaseHandler import *

class StudentsListHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.pageName = "students_list"

    def get(self):
        self.render("groupchoice.html")