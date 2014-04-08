from HomeHandler import *
from StudentsListHandler import *

app = webapp2.WSGIApplication([
                                  ('/', HomeHandler),
                                  ('/students_list', StudentsListHandler)
                              ], debug=True)
