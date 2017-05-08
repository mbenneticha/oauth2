#!/usr/bin/env python
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
import os
import urllib
import webapp2
import json
import logging
import random
import string
import httplib



class OauthHandler(webapp2.RequestHandler):
	def get(self):
		code = self.request.get('code')
		state = self.request.get('state')
		data = { 'client_id':'539287248398-hsq5ikfp43tem0edsfr2hl02otp01d6t.apps.googleusercontent.com',
			'client_secret':'l_5sBiVk8S4MRdxj7CSOjN5L',
			'redirect_uri':'https://python-gae-quickstart-164103.appspot.com/oauth',
			'grant_type':'authorization_code'}
			#,head = {'Content-Type': 'application/x-www-form-urlencoded'}
		data['code'] = str(code)
		post_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
		enc = urllib.urlencode(data)
		res = urlfetch.fetch('https://www.googleapis.com/oauth2/v4/token', enc, urlfetch.POST, post_headers)
		json_res = json.loads(res.content)
		self.response.write(json_res)
		get_headers = {'Authorization': 'Bearer ' + json_res['access_token']}
		res2 = urlfetch.fetch('https://www.googleapis.com/plus/v1/people/me', headers=get_headers)
		json_res2 = json.loads(res2.content)
		self.response.write(json_res2)
		n = json_res2['name']
		template_values = {
			'at': 'Here is your special verification code from me and your profile link to Google+. This was just a test of using OAuth to secure some of your info',
			'user_fname': n['givenName'],
			'user_lname': n['familyName'],
			'user_URL': json_res2['url'],
			'secret': state
			}
		path = os.path.join(os.path.dirname(__file__), 'sign_in.html')
		self.response.write(template.render(path, template_values))



class MainPage(webapp2.RequestHandler):
	def get(self):
		template_values = {
			'mt': 'CS 496 OAuth 2.0 Implementation',
			'ex': 'By clicking on the following link, you are authorizing access to your name and email from Google. Click on the link below to authorize Google to give me that information. After clicking the link, we will display your full name, the URL we used to access your Google+ Account and the randomly generated token used to authorize access.',
			'msg': 'Go to Google.'
		}
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.write(template.render(path, template_values))

	def post(self):
		state_secret = ''
		for i in range (0,20):
			state_secret += random.choice(string.letters)
		self.redirect(str('https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=539287248398-hsq5ikfp43tem0edsfr2hl02otp01d6t.apps.googleusercontent.com&redirect_uri=https://python-gae-quickstart-164103.appspot.com/oauth&scope=email&access_type=offline&state='+str(state_secret)))



app = webapp2.WSGIApplication([
	('/', MainPage),
	('/oauth', OauthHandler)
], debug=True)