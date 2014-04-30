__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *


class AbsenteesMonitorHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.page_name = "absentees_monitor"

    def get(self):
        self.render("absentees_monitor.html")
