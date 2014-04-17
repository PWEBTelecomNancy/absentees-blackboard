from HomeHandler import *
from StudentsListHandler import *
from ClassAbsenteesHandler import *
from ClassTodayHandler import *
from LoginHandler import *
from SignupHandler import *

app = webapp2.WSGIApplication([
                                  ('/', HomeHandler),
                                  ('/login', LoginHandler),
                                  ('/signup', SignupHandler),
                                  ('/students_list', StudentsListHandler),
                                  ('/class_absentees', ClassAbsenteesHandler),
                                  ('/class_today', ClassTodayHandler)
                              ], debug=True)
