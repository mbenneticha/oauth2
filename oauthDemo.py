#!/usr/bin/env python
import os
import urllib

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import urlfetch

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
		user = users.get_current_user()
		if user:
			nickname = user.nickname()
			logout_url = users.create_logout_url('/')
			greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format( nickname, logout_url)
		else:
			login_url = users.create_login_url('/')
			greeting = '<a href="{}">Sign in</a>'.format(login_url)

		self.response.write('<html><body>{}</body></html>'.format(greeting))
		logging.debug('The contents of the GET request are:' + repr(self.request.GET))



class MainPage(webapp2.RequestHandler):
	def get(self):
		title = 'OAuth 2.0 Implementation'
		course = 'CS 496'
		description = 'By clicking on the following link, you are authorizing access to your name and email from Google. Click on the link below to authorize Google to give me that information. After clicking the link, we will display your full name, the URL we used to access your Google+ Account and the randomly generated token used to authorize access.'
		redirect_url = 'https://python-gae-quickstart-164103.appspot.com/oauth'
		link = 'Go To (<a href="{}">Google</a>)'.format(redirect_url)
		greeting = '{} \n {} \n {} \n {}'.format(title, course, description, link)
		self.response.write('<html><body>{}</body></html>'.format(greeting))
		#path = os.path.join(os.path.dirname(__file__), 'index.html')
		#self.response.out.write(path)



app = webapp2.WSGIApplication([
	('/', MainPage),
	('/oauth', OauthHandler)
], debug=True)