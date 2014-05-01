__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *
from model.Logs import *


class LogsHandler(BaseHandler):
    def __init__(self, response=None, request=None):
        self.initialize(response, request)
        self.page_name = "administration"

    def get(self):
        all_logs = Logs.query().order(-Logs.date_time).fetch()


        self.render("administration_logs.html", all_logs=all_logs)
