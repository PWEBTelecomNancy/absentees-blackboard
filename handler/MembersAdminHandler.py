__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

import time
import datetime

from handler.BaseHandler import *
from model.Accounts import *
from model.Logs import *


class MembersAdminHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        super(MembersAdminHandler, self).__init__()
        self.initialize(request, response)
        self.page_name = "administration"

    def get(self):
        if self.is_connected() and get_is_admin_from_id(self.request.cookies.get('user_id').split('|')[0]):
            accounts = get_all_accounts()
            error_messages = []
            infos_messages = []

            if self.request.get('action') and self.request.get('user'):
                action = self.request.get('action')
                user = self.request.get('user')
                now = datetime.datetime.now()
                author = get_username_from_id(self.request.cookies.get('user_id').split('|')[0])

                if action == "delete":
                    if delete_user_from_login(user):
                        infos_messages.append("User " + user + " has been deleted")
                        Logs(date_time=now, category="members_deletion", author=author, description=author + " deleted"
                             + " account " + user).put()
                    else:
                        error_messages.append("Error while deleting user " + user + ". Please try again")

                elif action == "grant_admin":
                    if grant_admin_from_login(user):
                        infos_messages.append("Admin privileges have been granted to user " + user)
                        Logs(date_time=now, category="members_privileges", author=author, description=author+" granted"
                             + " admin privileges to " + user).put()
                    else:
                        error_messages.append("Error while granting admin privileges to user " + user)

                elif action == "remove_admin":
                    if remove_admin_from_login(user):
                        infos_messages.append("Admin privileges have been removed from user " + user)
                        Logs(date_time=now, category="members_privileges", author=author, description=author+" removed"
                             + " admin privileges from " + user).put()
                    else:
                        error_messages.append("Error while removing admin privileges from user " + user)

                elif action == "grant_teacher":
                    if grant_teacher_from_login(user):
                        infos_messages.append("Teacher privileges have been granted to user " + user)
                        Logs(date_time=now, category="members_privileges", author=author, description=author+" granted"
                             + " teacher privileges to " + user).put()
                    else:
                        error_messages.append("Error while granting teacher privileges to user " + user)

                elif action == "remove_teacher":
                    if remove_teacher_from_login(user):
                        infos_messages.append("Teacher privileges have been removed from user " + user)
                        Logs(date_time=now, category="members_privileges", author=author, description=author+" removed"
                             + " teacher privileges from " + user).put()
                    else:
                        error_messages.append("Error while removing teacher privileges from user " + user)

                else:
                    error_messages.append("It seems you are using an invalid URL. No action will be done.")

                time.sleep(1)
                accounts = get_all_accounts()
                self.render("administration_members.html", accounts=accounts, error_messages=error_messages,
                            infos_messages=infos_messages)

            elif self.request.get('action') and not self.request.get('user') or self.request.get('user')\
                    and not self.request.get('action'):
                error_messages.append("It seems you are using an invalid URL. No action will be done.")
                self.render("administration_members.html", accounts=accounts, error_messages=error_messages)

            else:
                self.render("administration_members.html", accounts=accounts)

        else:
            self.render("message.html", title="Access forbidden",
                        text="It seems you're not an administrator nor a connected user")

    def post(self):
        if self.is_connected() and get_is_admin_from_id(self.request.cookies.get('user_id').split('|')[0]):
            login = self.request.get('login')
            email = self.request.get('email')
            ade_name = self.request.get('ade_name')

            accounts = get_accounts_corresponding_login(login)
            accounts.extend(get_accounts_corresponding_email(email))
            accounts.extend(get_accounts_corresponding_ade_name(ade_name))

            self.render("administration_members.html", accounts=accounts)

        else:
            self.render("message.html", title="Access forbidden",
                        text="It seems you're not an administrator nor a connected user")