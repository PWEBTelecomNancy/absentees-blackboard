from HomeHandler import *

app = webapp2.WSGIApplication([
                                  ('/', HomeHandler)
                              ], debug=True)
