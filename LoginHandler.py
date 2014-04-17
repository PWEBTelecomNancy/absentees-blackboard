__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from BaseHandler import *


class LoginHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.page_name = "login"

    def get(self):
        self.render('login.html')
