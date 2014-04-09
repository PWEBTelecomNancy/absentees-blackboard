from HomeHandler import *
from StudentsListHandler import *
from ClassAbsenteesHandler import *

app = webapp2.WSGIApplication([
                                  ('/', HomeHandler),
                                  ('/students_list', StudentsListHandler),
                                  ('/class_absentees', CourHandler)
                              ], debug=True)
