from HomeHandler import *
from StudentsListHandler import *
from ClassAbsenteesHandler import *
from ClassTodayHandler import *
from LoginHandler import *
from SignupHandler import *
from LogoutHandler import *
from ClassWeekHandler import *

app = webapp2.WSGIApplication([
                                  ('/', HomeHandler),
                                  ('/login', LoginHandler),
                                  ('/signup', SignupHandler),
                                  ('/logout', LogoutHandler),
                                  ('/students_list', StudentsListHandler),
                                  ('/class_absentees', ClassAbsenteesHandler),
                                  ('/class_today', ClassTodayHandler),
                                  ('/class_week', ClassWeekHandler)
                              ], debug=True)
