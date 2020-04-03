import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb

from taskboard import TaskBoard

JINJA_ENVIRONMENT = jinja2.Environment (
    loader=jinja2.FileSystemLoader (os.path.dirname (__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Display (webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {}
        user = users.get_current_user ()
        key = ndb.Key (urlsafe=self.request.get('key_name'))
        current_tb = key.get ()

        template_values = {
			'current_tb': current_tb,
			'key': key.urlsafe(),
			'user': user

    	}

        template = JINJA_ENVIRONMENT.get_template ('display.html')
        self.response.write (template.render (template_values))

