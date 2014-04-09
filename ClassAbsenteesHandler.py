from BaseHandler import *


class CourHandler(BaseHandler):

    def __init__(self, request=None, response=None):
        self.initialize(request, response)
        self.pageName = "class_absentees"

    def get(self):
        class_parameters = {'class_name': 'PWEB', 'time': ' 10:10 - 12:00', 'teacher': 'Mr Charoy', 'type': 'CM',
                          'room': '2.42', 'nb_students': '18'}
        self.render('class_absentees.html', **class_parameters)