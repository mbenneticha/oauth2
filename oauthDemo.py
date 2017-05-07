#!/usr/bin/env python
from google.appengine.ext import ndb
#from google.appengine.api import urlfetch
import logging
import webapp2
#import urllib
import json

class OauthHandler(webapp2.RequestHandler):
	def get(self):
		logging.debug('The contents of the GET request are:' + repr(self.request.GET))

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write("hello, good-bye, adele.")
		template_values = {
		'displayName': content_dict["displayName"],
		'newURL': content_dict["url"]
		}
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))
		#data_to_post = {
		#'message': result.content
		#}
		#encoded_data = urllib.urlencode(data_to_post)
		#send encoded application response to application-3
		#result = urlfetch.fetch(url_app_3, encoded_data, method='POST')

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/oauth', OauthHandler)
], debug=True)