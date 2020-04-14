from google.appengine.ext import ndb

class Task (ndb.Model):
	title = ndb.StringProperty()
	due_date = ndb.DateProperty()
	completion_date =  ndb.DateTimeProperty()
	checked = ndb.BooleanProperty(default=False)
	assigned_to = ndb.KeyProperty(kind ="User")

