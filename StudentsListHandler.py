__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from BaseHandler import *
import logging
from XMLAnalyser import XMLAnalyser
from google.appengine.api import memcache

class StudentsListHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.pageName = "students_list"
        pass

    def get(self):
        self.render("groupchoice.html")

    def post(self):
        group_to_find = self.request.get("group_name")


        groups = memcache.get("group_list")

        if groups is None:
            logging.error("CACHE MISS StudentsListHandler l. 24")
            parser = XMLAnalyser()
            groups = parser.get_members()
            memcache.set("group_list", groups)

        to_display = dict()
        for key in groups:
            if group_to_find in key:
                to_display[key] = groups[key]


        if len(to_display) > 0:
            self.render("groupdisplay.html", group_name = group_to_find, groups = to_display)
        else:
            self.render("message.html", title = "No such group", subtitle = "", argument = group_to_find)
