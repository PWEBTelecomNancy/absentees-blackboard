__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *
from model.Accounts import *
import logging
import util


class ProfileHandler(BaseHandler):
    current_user = None

    def get(self):
        if self.is_connected():
            self.current_user = get_connected_user(self.request.cookies['user_id'])

            self.render("profile.html",
                        user=self.current_user,
                        new_login=self.current_user.login,
                        new_email_address=self.current_user.email_address,
                        new_name=self.current_user.name)
        else:
            self.redirect('/')

    def post(self):
        if self.is_connected():
            self.current_user = get_connected_user(self.request.cookies['user_id'])

            username = self.request.get('login')
            old_password = self.request.get('old_password')
            email = self.request.get('email')
            name = self.request.get('name').upper()
            password = self.request.get('password')
            password_confirmation = self.request.get('password_confirmation')

            error_messages = []

            if not util.valid_username(username):
                error_messages.append("Please enter a valid username (more than 3 characters).")

            if used_username(username) and username != self.current_user.login:
                error_messages.append("This username is already used")

            if not util.valid_password(old_password):
                error_messages.append("Please enter a valid password (more than 3 characters, less than 40)")

            if password and password_confirmation:
                if not util.valid_password(old_password):
                    error_messages.append("Please enter a valid new password (more than 3 characters, less than 40)")
                if password != password_confirmation:
                    error_messages.append("The two new password you entered are not equals.")

            if not util.valid_email(email):
                error_messages.append("Please enter a valid email address")

            if not util.valid_name(name):
                error_messages.append("Please enter your name in the following format: \"lastname firstname\", like \"John Doe\".")

            # Check the password
            key_to_check = user_connexion(self.current_user.login, old_password)
            if key_to_check is not None:
                if key_to_check == self.current_user.key().id():
                    # We have the right user
                    pass
                else:
                    error_messages.append("An unexpected error occurred. Please try again.")
            else:
                error_messages.append("You entered the wrong password.")

            if len(error_messages) > 0:
                # Errors have been found
                self.render('profile.html',
                            error_messages=error_messages,
                            user=self.current_user,
                            new_login=username,
                            new_email_address=email,
                            new_name=name)

            else:
                # No error! Update time
                # Update the user
                self.current_user.login = username
                self.current_user.email_address = email
                self.current_user.name = name

                if password != "" and password == password_confirmation:
                    # The user is changing password
                    passhash = password_hash(password)
                    self.current_user.password = passhash
                else:
                    # The user is not changing password
                    pass

                self.current_user.put()

                self.render('profile.html',
                            updated=True,
                            user=self.current_user,
                            new_login=username,
                            new_email_address=email,
                            new_name=name)

        else:
            self.redirect('/')
