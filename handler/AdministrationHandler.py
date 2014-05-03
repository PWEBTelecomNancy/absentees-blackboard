__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *


class AdministrationHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        super(AdministrationHandler, self).__init__()
        self.initialize(request, response)
        self.page_name = "administration"

    def get(self):
        #If the user isn't connected nor isn't administrator => error message
        if not (self.is_connected() and get_is_admin_from_id(self.request.cookies.get('user_id').split('|')[0])):
            self.render("message.html", title="Access forbidden",
                        text="It seems you're not an administrator nor a connected user")

        else:
            self.render('administration_main.html')
