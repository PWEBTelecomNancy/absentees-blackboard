from HomeHandler import *
from StudentsListHandler import *
from CourHandler import *

app = webapp2.WSGIApplication([
                                  ('/', HomeHandler),
                                  ('/students_list', StudentsListHandler),
                                  ('/cour',CourHandler)
                              ], debug=True)
