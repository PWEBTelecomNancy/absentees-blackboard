__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from BaseHandler import *


class SignupHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.page_name = "signup"

    def get(self):
        self.render('signup.html')

    def post(self):
        username_present = False
        password_present = False
        email_present = True

        if self.request.post('login'):
            username_present = True

        if self.request.post('password'):
            password_present = True

        if self.request.post('email'):
            email_present = True

        if not username_present or not password_present:
            pass
            # We display again the same form with error message

        else:
            pass
            # It's okay we can add it to the base and connect the user