from google.appengine.ext import ndb
from task import Task
from user import User

class TaskBoard (ndb.Model):
	users = ndb.StructuredProperty(User, repeated=True)
	tasks = ndb.StructuredProperty(Task, repeated=True)