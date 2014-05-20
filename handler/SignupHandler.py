__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

import re

from handler.BaseHandler import *
from model.Accounts import *
import util


class SignupHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        super(SignupHandler, self).__init__()
        self.initialize(request, response)
        self.page_name = "signup"

    def get(self):
        if self.is_connected():
            self.redirect('/')

        self.render('signup.html')

    def post(self):
        username = self.request.get('login')
        password = self.request.get('password')
        email = self.request.get('email')
        name = self.request.get('name')
        error_messages = []

        if not util.valid_username(username):
            error_messages.append("Please enter a valid username (more than 3 characters).")

        if used_username(username):
            error_messages.append("This username is already used")

        if not util.valid_password(password):
            error_messages.append("Please enter a valid password (more than 3 characters, less than 40)")

        if not util.valid_email(email):
            error_messages.append("Please enter a valid email address")

        if not util.valid_name(name):
            error_messages.append("Please enter your name in the following format: \"lastname firstname\", like \"John Doe\".")

        if len(error_messages) > 0:
            self.render('signup.html',
                        error_messages=error_messages, username=username,
                        email=email, name=name)

        else:
            #Put the account in datastore
            passhash = password_hash(password)
            account = Accounts(login=username, password=passhash,
                               email_address=email, is_admin=False,
                               is_teacher=False, name=name)
            account.put()

            #Set a cookie for the login and redirect to home
            self.response.headers.add_header('Set-Cookie', "user_id=" + id_cookie_generation(account.key().id())
                                             + "; Path='/'")
            self.redirect('/')
