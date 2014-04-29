__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *


class AbsenteesAdminHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.page_name = "administration"

    def get(self):
        self.render("administration_absentees.html")
