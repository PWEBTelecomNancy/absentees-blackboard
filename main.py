from HomeHandler import *
from StudentsListHandler import *
from ClassAbsenteesHandler import *
from ClassTodayHandler import *
from LoginHandler import *
from SignupHandler import *
from LogoutHandler import *
from ClassWeekHandler import *
from AdministrationHandler import *
from MembersAdminHandler import *
from AbsenteesAdminHandler import *

app = webapp2.WSGIApplication([
                                  ('/', HomeHandler),
                                  ('/login', LoginHandler),
                                  ('/signup', SignupHandler),
                                  ('/logout', LogoutHandler),
                                  ('/students_list', StudentsListHandler),
                                  ('/class_absentees', ClassAbsenteesHandler),
                                  ('/class_today', ClassTodayHandler),
                                  ('/class_week', ClassWeekHandler),
                                  ('/admin', AdministrationHandler),
                                  ('/admin_members', MembersAdminHandler),
                                  ('/admin_absentees', AbsenteesAdminHandler)
                              ], debug=True)
