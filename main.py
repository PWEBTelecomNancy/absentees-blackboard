from HomeHandler import *
from TestHandler import *

app = webapp2.WSGIApplication([
                                  ('/', HomeHandler),
                                  ('/test', TestHandler)
                              ], debug=True)
