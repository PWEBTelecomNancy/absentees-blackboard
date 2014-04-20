__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

import os
import webapp2
import jinja2
from Accounts import *

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class BaseHandler(webapp2.RequestHandler):
    page_name = "home"

    def is_connected(self):
        if self.request.cookies.get('user_id'):
            user_id = str(self.request.cookies.get('user_id'))

            if user_id and user_id != "":
                return check_cookie(user_id)
            else:
                return False

        else:
            return False


    @staticmethod
    def render_str(template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        if self.is_connected():
            user_id = self.request.cookies.get('user_id').split('|')[0]
            username = get_username_from_id(user_id)
            is_teacher = get_is_teacher_from_id(user_id)
            is_admin = get_is_admin_from_id(user_id)

            self.write(self.render_str(template, connected=True, username=username, is_teacher=is_teacher,
                                       is_admin=is_admin, pageName=self.page_name, **kw))
        else:
            self.write(self.render_str(template, connected=False, pageName=self.page_name, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
