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
		code = self.request.get('code')
		state = self.request.get('state') 
		cid = '539287248398-hsq5ikfp43tem0edsfr2hl02otp01d6t.apps.googleusercontent.com'
		sec = 'l_5sBiVk8S4MRdxj7CSOjN5L'
		redirect = 'https://python-gae-quickstart-164103.appspot.com/oauth'
		gt = 'authorization_code'
		head = {'Content-Type': 'application/x-www-form-urlencoded'}

		data={'code':code,'client_id':cid,'client_secret':sec,'redirect_uri':redirect,'grant_type':gt}
		result = urlfetch.fetch(url='https://www.googleapis.com/oauth2/v4/token',payload=urllib.urlencode(data),method=urlfetch.POST,headers=head)





class MainPage(webapp2.RequestHandler):
	def get(self):
		title = 'OAuth 2.0 Implementation'
		course = 'CS 496'
		description = 'By clicking on the following link, you are authorizing access to your name and email from Google. Click on the link below to authorize Google to give me that information. After clicking the link, we will display your full name, the URL we used to access your Google+ Account and the randomly generated token used to authorize access.'
		redirect_url = 'https://accounts.google.com/o/oauth2/v2/auth'
		link = 'Go To (<a href="{}">Google</a>)'.format(redirect_url)
		greeting = '{} \n {} \n {} \n {}'.format(title, course, description, link)
		self.response.write('<html><body>{}</body></html>'.format(greeting))
		#path = os.path.join(os.path.dirname(__file__), 'index.html')
		#self.response.out.write(path)

	def post(self):
		headers = {'Content-Type': 'application/x-www-form-urlencoded'}
		PARAMS = {
                'code': code,
                'client_id': client_id,
                'client_secret': client_secret,
          }
          try:
          	result = urlfetch.fetch(
          		url=HTTP_REQUEST_URL,
                payload=urllib.urlencode(PARAMS),
                method=urlfetch.POST/GET/DELETE/...,
                headers=headers
                )
          except urlfetch.Error as e:
          	logging.debug(e)

          self.response.write(json.loads(result.content))



app = webapp2.WSGIApplication([
	('/', MainPage),
	('/oauth', OauthHandler)
], debug=True)