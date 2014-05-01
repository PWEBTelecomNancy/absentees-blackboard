__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *


class AbsenteesMonitorHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.page_name = "absentees_monitor"

    def get(self):
        if self.is_connected():
            self.render("absentees_monitor.html")

        else:
            self.render("message.html", title="Access forbidden",
                        text="It seems you're not a connected user")

    def post(self):
        if self.is_connected():
            if self.request.get('class_title'):
                self.response.out.write("Class name")

            else:
                self.response.out.write("Group name")

        else:
            self.render("message.html", title="Access forbidden",
                        text="It seems you're not a connected user")