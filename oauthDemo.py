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

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.
    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


# [START greeting]
class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END greeting]


# [START main_page]

class OauthHandler(webapp2.RequestHandler):
	def get(self):
		logging.debug('The contents of the GET request are:' + repr(self.request.GET))

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

# [START guestbook]
class Guestbook(webapp2.RequestHandler):
	def post(self):
		# We set the same parent key on the 'Greeting' to ensure each
		# Greeting is in the same entity group. Queries across the
		# single entity group will be consistent. However, the write
		# rate to a single entity group should be limited to
		# ~1/second.
		guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		greeting = Greeting(parent=guestbook_key(guestbook_name))

		if users.get_current_user():
			greeting.author = Author( identity=users.get_current_user().user_id(), email=users.get_current_user().email())
			greeting.content = self.request.get('content')
			greeting.put()
		query_params = {'guestbook_name': guestbook_name}
		self.redirect('/?' + urllib.urlencode(query_params))
# [END guestbook]



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
	('/sign', Guestbook)
	#('/oauth', OauthHandler)
], debug=True)