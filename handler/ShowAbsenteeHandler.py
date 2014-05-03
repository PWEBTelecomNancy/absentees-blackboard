__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *
from model.Absentees import *
from model.Logs import *


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
                log_sentence = None

                #Update absentee entry
                absentee = get_absentee_from_id(self.request.get('id'))

                if self.request.get('justified'):
                    absentee.justification_bool = True
                    log_sentence = "%(admin)s accepted the absence of %(student)s. (%(lesson)s from " \
                                   "%(hour_start)s to %(hour_end)s"
                else:
                    absentee.justification_bool = False
                    log_sentence = "%(admin)s refused the absence of %(student)s. (%(lesson)s from " \
                                   "%(hour_start)s to %(hour_end)s"

                if self.request.get('justification') and self.request.get('justification') != "":
                    absentee.justification_text = self.request.get('justification')
                else:
                    absentee.justification_text = "/"

                absentee.put()
                user_id = self.request.cookies.get('user_id').split('|')[0]
                account = get_account_from_id(user_id)

                log_sentence = log_sentence % {'admin': account.name,
                                               'student': absentee.student_name,
                                               'lesson': absentee.class_title,
                                               'hour_start': absentee.start_hour,
                                               'hour_end': absentee.end_hour
                }

                # I don't know why, the date won't accept the same way
                log_sentence = log_sentence + " on the " + absentee.class_date + ".)"
                Logs(
                    date_time=self.date_details.now(),
                    category="absentee control",
                    author=account.name,
                    description=log_sentence
                ).put()

                #Redirect to correct page
                self.redirect('/show_absentee?id=' + self.request.get('id'))

            else:
                self.render("message.html", title="Invalid URL", text="It seems you're using an invalid URL")

        else:
            self.render("message.html", title="Access forbidden",
                        text="It seems you're not an administrator nor a connected user")
