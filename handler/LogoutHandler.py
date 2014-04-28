__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *


class LogoutHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        self.initialize(request, response)

    def get(self):
        self.response.headers.add_header('Set-Cookie', "user_id=; Path='/'")
        self.redirect('/')
