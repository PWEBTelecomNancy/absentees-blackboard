__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *


class HomeHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        super(HomeHandler, self).__init__()
        self.initialize(request, response)
        self.page_name = "home"

    def get(self):
        self.render('home.html')
