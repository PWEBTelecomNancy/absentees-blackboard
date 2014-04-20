__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

import re

from BaseHandler import *
from Accounts import *
from google.appengine.ext import db


class SignupHandler(BaseHandler):
    user_regexp = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    password_regexp = re.compile(r"^.{3,40}$")
    email_regexp = re.compile(r"^[\S]+@(etu\.)?univ-lorraine\.fr$")

    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.page_name = "signup"

    def get(self):
        self.render('signup.html')

    def post(self):
        username = self.request.get('login')
        password = self.request.get('password')
        email = self.request.get('email')
        error_messages = []

        if not self.valid_username(username):
            error_messages.append("Please enter a username (more than 3 characters).")

        if self.used_username(username):
            error_messages.append("This username is already used")

        if not self.valid_password(password):
            error_messages.append("Please enter a valid password (more than 3 characters)")

        if not self.valid_email(email):
            error_messages.append("Please enter a valid email address")

        if len(error_messages) > 0:
            self.render('signup.html', error_messages=error_messages, username=username, email=email)

        else:
            #Put the account in datastore
            passhash = password_hash(password)
            account = Accounts(login=username, password=passhash, email_address=email, is_admin=False, is_teacher=False)
            account.put()

            #Set a cookie for the login and redirect to home
            self.response.headers.add_header('Set-Cookie', "user_id=" + id_cookie_generation(account.key().id())
                                             + "; Path='/'")
            self.redirect('/')

    def valid_username(self, username):
        return self.user_regexp.match(username)

    def used_username(self, username):
        result = db.GqlQuery("SELECT * FROM Accounts WHERE login=:username", username=username)
        print result.count()
        return result.count() != 0

    def valid_password(self, password):
        return self.password_regexp.match(password)

    def valid_email(self, email):
        return self.email_regexp.match(email)