from BaseHandler import *


class CourHandler(BaseHandler):

    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.pageName = "cour"
        pass

    def get(self):
        cour = {'matiere': 'PWEB','heure':'10:10 - 12:00','prof':'Mr Charoy', 'typecour':'CM','salle':'2.42','nb_eleve':'18'}
        self.render('cour.html',cour=cour)