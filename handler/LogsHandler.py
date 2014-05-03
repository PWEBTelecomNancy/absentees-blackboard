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

            all_logs = get_all_logs()
            filtered_logs = None

            if date:
                logging.error("date search")

            if author_req:
                logging.error("Author search")

                if filtered_logs is None:
                    filtered_logs = all_logs

                new_list = list()
                for log in filtered_logs:
                    logging.error(log.author)
                    if author_req.upper() in log.author.upper():
                        new_list.append(log)
                filtered_logs = new_list

            if category_req:
                logging.error("cat search")

                if filtered_logs is None:
                    filtered_logs = all_logs

                new_list = list()
                for log in filtered_logs:
                    if category_req.upper() in log.category.upper():
                        new_list.append(log)
                filtered_logs = new_list

            if desc_req:
                logging.error("desc search")

                if filtered_logs is None:
                    filtered_logs = all_logs

                new_list = list()
                for log in filtered_logs:
                    if desc_req in log.description:
                        new_list.append(log)
                filtered_logs = new_list


            self.render("administration_logs.html", all_logs=new_list,
                       search_date=date_req, search_author=author_req,
                       search_category=category_req, search_desc=desc_req)