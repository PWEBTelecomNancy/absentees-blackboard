__author__ = 'Pierre Monnin & Thibaut Smith'

from BaseHandler import *


class HomeHandler(BaseHandler):
    def get(self):
        self.render('home.html')
