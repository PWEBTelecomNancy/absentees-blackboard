import logging

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
            all_logs = get_all_logs()

            self.render("administration_logs.html", all_logs=all_logs,
                        search_date="", search_author="", search_category="",
                        search_desc="")

    def post(self):
        # If the user isn't connected nor isn't administrator => error message
        if not (self.is_connected() and get_is_admin_from_id(self.request.cookies.get('user_id').split('|')[0])):
            self.render("message.html", title="Access forbidden",
                        text="It seems you're not an administrator nor a connected user.")

        else:
            date_req = self.request.get('date', None)
            author_req = self.request.get('author', None)
            category_req = self.request.get('category', None)
            desc_req = self.request.get('desc', None)

            date = None
            if date_req is not None and date_req != "":
                try:
                    date_tab = date_req.split('/')
                    date = datetime.datetime(date_req[2], date_req[1], date_req[0])

                except Exception:
                    date = self.date_details
                    date_req = ""

            all_logs = None

            if date_req and author_req and category_req and desc_req:
                logging.error("Full search")
                all_logs = Logs().query(Logs.date_time == date,
                                        Logs.author == author_req,
                                        Logs.category == category_req,
                                        Logs.description == desc_req)\
                    .order(-Logs.date_time).fetch()
            elif date:
                logging.error("date search")
                all_logs = Logs().query(Logs.date_time == date).order(-Logs.date_time).fetch()
            elif author_req:
                logging.error("Author search")
                all_logs = Logs().query(Logs.author == author_req).order(-Logs.date_time).fetch()
            elif category_req:
                logging.error("cat search")
                logging.error(category_req)
                all_logs = Logs().query(Logs.category == category_req).order(-Logs.date_time).fetch()
            elif desc_req:
                logging.error("desc search")
                all_logs = Logs().query(Logs.description == desc_req).order(-Logs.date_time).fetch()
            else:
                all_logs = get_all_logs()

            self.render("administration_logs.html", all_logs=all_logs,
                       search_date=date_req, search_author=author_req,
                       search_category=category_req, search_desc=desc_req)