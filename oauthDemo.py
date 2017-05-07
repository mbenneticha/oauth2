#!/usr/bin/env python
import os
import urllib

from google.appengine.ext import ndb
#from google.appengine.ext import template
from google.appengine.api import users
#from google.appengine.api import urlfetch

import webapp2
import jinja2
import json
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class OauthHandler(webapp2.RequestHandler):
	def get(self):
		#logging.debug('The contents of the GET request are:' + repr(self.request.GET))

class MainPage(webapp2.RequestHandler):
	def get(self):
		#self.response.write("hello, good-bye, adele.")
		guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
		greetings = greetings_query.fetch(10)

		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'user': user,
			'greetings': greetings,
			'guestbook_name': urllib.quote_plus(guestbook_name),
			'url': url,
			'url_linktext': url_linktext,
		}

		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))



		#template_values = {
		#'displayName': content_dict["displayName"],
		#'newURL': content_dict["url"]
		#}
		#path = os.path.join(os.path.dirname(__file__), 'index.html')
		#self.response.out.write(template.render(path, template_values))
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