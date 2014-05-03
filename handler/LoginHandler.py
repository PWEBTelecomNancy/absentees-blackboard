__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *


class LoginHandler(BaseHandler):
    def __init__(self, request=None, response=None):
        super(LoginHandler, self).__init__()
        self.initialize(request, response)
        self.page_name = "login"

    def get(self):
        if self.is_connected():
            self.redirect('/')

        self.render('login.html')

    def post(self):
        username_present = False
        password_present = False
        username = ""
        password = ""

        if self.request.get('login'):
            username_present = True
            username = self.request.get('login')

        if self.request.get('password'):
            password_present = True
            password = self.request.get('password')

        if not username_present or not password_present:
            self.render('login.html', error_message="Incorrect login")

        else:
            user_id = user_connexion(username, password)
            if user_id:
                #Set connexion cookie
                self.response.headers.add_header('Set-Cookie', "user_id=" + id_cookie_generation(user_id)
                                                 + "; Path = '/'")
                self.redirect('/')

            else:
                self.render('login.html', error_message="Incorrect login")
