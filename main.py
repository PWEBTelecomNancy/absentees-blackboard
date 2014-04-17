from HomeHandler import *
from StudentsListHandler import *
from ClassAbsenteesHandler import *
from ClassTodayHandler import *

app = webapp2.WSGIApplication([
                                  ('/', HomeHandler),
                                  ('/students_list', StudentsListHandler),
                                  ('/class_absentees', ClassAbsenteesHandler),
                                  ('/class_today', ClassTodayHandler)
                              ], debug=True)
