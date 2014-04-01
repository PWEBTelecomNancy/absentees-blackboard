__author__ = 'Pierre Monnin & Thibaut Smith'

from BaseHandler import *


class HomeHandler(BaseHandler):
    def get(self):
        self.response.out.write("Welcome on the frogidel project : absentees-blackboard!")
