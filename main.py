from handler.HomeHandler import *
from handler.StudentsListHandler import *
from handler.ClassAbsenteesHandler import *
from handler.ClassTodayHandler import *
from handler.LoginHandler import *
from handler.SignupHandler import *
from handler.LogoutHandler import *
from handler.ClassWeekHandler import *
from handler.AdministrationHandler import *
from handler.MembersAdminHandler import *
from handler.AbsenteesAdminHandler import *
from handler.LogsHandler import *
from handler.ParametersHandler import *
from handler.AbsenteesMonitorHandler import *
from handler.ProfileHandler import *
from handler.ShowAbsenteeHandler import *

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
                                  ('/admin_absentees', AbsenteesAdminHandler),
                                  ('/show_absentee', ShowAbsenteeHandler),
                                  ('/logs', LogsHandler),
                                  ('/parameters', ParametersHandler),
                                  ('/absentees_monitor', AbsenteesMonitorHandler),
                                  ('/profile', ProfileHandler)
                              ], debug=True)
