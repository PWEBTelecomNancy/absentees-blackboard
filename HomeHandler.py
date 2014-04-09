__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from BaseHandler import *


class HomeHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.pageName = "home"
        pass

    def get(self):
        self.render('home.html')
