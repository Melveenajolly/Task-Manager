from google.appengine.ext import ndb
from task import Task
from user import User

class TaskBoard (ndb.Model):
	name = ndb.StringProperty()
	creator = ndb.KeyProperty(kind ="User")
	tasks = ndb.StructuredProperty(Task, repeated=True)
	