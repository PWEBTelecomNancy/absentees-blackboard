__author__ = 'Mael Beuget, Pierre Monnin & Thibaut Smith'

from handler.BaseHandler import *
from model.Parameters import *
import time


class ParametersHandler(BaseHandler):
    def __init__(self, response=None, request=None):
        super(ParametersHandler, self).__init__()
        self.initialize(response, request)
        self.page_name = "administration"

    def get(self):
        query = Parameters.all()
        parameters = query.fetch(limit=None)

        if parameters is None or len(parameters) == 0:
            p = Parameters(name="ADE Project", value="TELECOM Nancy")
            p.put()
            query = Parameters.all()
            parameters = query.fetch(limit=None)
            time.sleep(1)

        self.render("administration_parameters.html", parameters=parameters)

    def post(self):
        query = Parameters.all()
        parameters = query.fetch(limit=None)

        for param in parameters:
            name = param.name
            value = self.request.get(name)

            Parameters.delete(param)
            Parameters(name=name, value=value).put()

        time.sleep(1)
        self.redirect('/parameters')
