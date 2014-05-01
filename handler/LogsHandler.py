__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *
from model.Logs import *


class LogsHandler(BaseHandler):
    def __init__(self, response=None, request=None):
        self.initialize(response, request)
        self.page_name = "administration"

    def get(self):
        # If the user isn't connected nor isn't administrator => error message
        if not (self.is_connected() and
                    get_is_admin_from_id(
                            self.request.cookies.get('user_id').split('|')[0])):
            self.error(404)
            self.render("message.html", title="Access forbidden",
                        text="It seems you're not an administrator nor a connected user.")

        else:
            all_logs = Logs.query().order(-Logs.date_time).fetch()

            self.render("administration_logs.html", all_logs=all_logs)

    def post(self):
        # If the user isn't connected nor isn't administrator => error message
        if not (self.is_connected() and get_is_admin_from_id(self.request.cookies.get('user_id').split('|')[0])):
            self.render("message.html", title="Access forbidden",
                        text="It seems you're not an administrator nor a connected user.")

        else:
            all_logs = Logs.query().order(-Logs.date_time).fetch()

            self.write("To be coded.")