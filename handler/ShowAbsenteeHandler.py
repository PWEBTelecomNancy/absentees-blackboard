__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *
from model.Absentees import *


class ShowAbsenteeHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.page_name = "administration"

    def get(self):
        if self.is_connected() and get_is_admin_from_id(self.request.cookies.get('user_id').split('|')[0]):
            if self.request.get('id') and self.request.get('id') != "":
                absentee = get_absentee_from_id(self.request.get('id'))

                self.render("administration_absentee_show.html", absentee=absentee)

            else:
                self.render("message.html", title="Invalid URL", text="It seems you're using an invalid URL")
        else:
            self.render("message.html", title="Access forbidden",
                        text="It seems you're not an administrator nor a connected user")

    def post(self):
        if self.is_connected() and get_is_admin_from_id(self.request.cookies.get('user_id').split('|')[0]):
            if self.request.get('id') and self.request.get('id') != "":
                #Update absentee entry
                absentee = get_absentee_from_id(self.request.get('id'))

                if self.request.get('justified'):
                    absentee.justification_bool = True
                else:
                    absentee.justification_bool = False

                if self.request.get('justification') and self.request.get('justification') != "":
                    absentee.justification_text = self.request.get('justification')
                else:
                    absentee.justification_text = "/"

                absentee.put()

                #Redirect to correct page
                self.redirect('/show_absentee?id=' + self.request.get('id'))

            else:
                self.render("message.html", title="Invalid URL", text="It seems you're using an invalid URL")

        else:
            self.render("message.html", title="Access forbidden",
                        text="It seems you're not an administrator nor a connected user")
