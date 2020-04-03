from google.appengine.ext import ndb

class Task (ndb.Model):
	title = ndb.StringProperty()
	due = ndb.DateTimeProperty()
