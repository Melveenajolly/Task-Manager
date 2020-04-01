from google.appengine.ext import ndb

class User (ndb.Model):
	email_address = ndb.StringProperty()