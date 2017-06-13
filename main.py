#!/usr/bin/env python

import webapp2
import userHandlers
import reviewHandler

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Hello, mon')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/users', userHandlers.UsersHandler),
    ('/reviews', reviewHandler.ReviewsHandler),
    ('/reviews/(.*)', reviewHandler.ReviewsHandler)
], debug=True)
