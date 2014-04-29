__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *


class ParametersHandler(BaseHandler):
    def __init__(self, response=None, request=None):
        self.initialize(response, request)
        self.page_name = "administration"

    def get(self):
        self.render("administration_parameters.html")
