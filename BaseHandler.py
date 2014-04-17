__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

import os
import webapp2
import jinja2


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class BaseHandler(webapp2.RequestHandler):
    page_name = "home"

    @staticmethod
    def render_str(template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, pageName=self.page_name, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)
