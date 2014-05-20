from handler.HomeHandler import *
from handler.StudentsListHandler import *
from handler.ClassAbsenteesHandler import *
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
from handler.FlushHandler import *

app = webapp2.WSGIApplication([
                                  ('/', HomeHandler),
                                  ('/login', LoginHandler),
                                  ('/signup', SignupHandler),
                                  ('/logout', LogoutHandler),
                                  ('/students/list/?', StudentsListHandler),
                                  ('/students/absentees/?', ClassAbsenteesHandler),
                                  ('/timetable/weekly/?', ClassWeekHandler),
                                  ('/administration/?', AdministrationHandler),
                                  ('/administration/members/?', MembersAdminHandler),
                                  ('/administration/absentees/?', AbsenteesAdminHandler),
                                  ('/administration/show_absentee/?', ShowAbsenteeHandler),
                                  ('/administration/logs/?', LogsHandler),
                                  ('/administration/parameters/?', ParametersHandler),
                                  ('/students/absentees/monitor/?', AbsenteesMonitorHandler),
                                  ('/profile', ProfileHandler),
                                  ('/preload', FlushHandler)
                              ], debug=True)
