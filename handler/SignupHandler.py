__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

import re

from handler.BaseHandler import *
from model.Accounts import *


class SignupHandler(BaseHandler):
    user_regexp = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    password_regexp = re.compile(r"^.{3,40}$")
    email_regexp = re.compile(r"^[\S]+@(etu\.)?univ-lorraine\.fr$")

    def __init__(self, request=None, response=None):
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
        name = self.request.get('name').upper()
        error_messages = []

        if not self.valid_username(username):
            error_messages.append("Please enter a username (more than 3 characters).")

        if used_username(username):
            error_messages.append("This username is already used")

        if not self.valid_password(password):
            error_messages.append("Please enter a valid password (more than 3 characters)")

        if not self.valid_email(email):
            error_messages.append("Please enter a valid email address")

        if not self.valid_name(name):
            error_messages.append("Please enter your name in the following format: Lastname and Firstname")

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

    def valid_username(self, username):
        return self.user_regexp.match(username)

    def valid_password(self, password):
        return self.password_regexp.match(password)

    def valid_email(self, email):
        return self.email_regexp.match(email)

    def valid_name(self, name):
        check = True
        if check is None:
            check = False

        if len(name.split(' ')) != 2:
            check = False

        return check