__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *
from model.Accounts import *


class MembersAdminHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.page_name = "administration"

    def get(self):
        if self.is_connected() and get_is_admin_from_id(self.request.cookies.get('user_id').split('|')[0]):
            query = Accounts.all()
            accounts = query.fetch(limit=None)

            self.render("administration_members.html", accounts=accounts)

        else:
            self.render("message.html", title="Access forbidden",
                        text="It seems you're not an administrator nor a connected user")
