from google.appengine.ext import ndb
from task import Task
from user import User

class TaskBoard (ndb.Model):
	name = ndb.StringProperty()
	creator = ndb.KeyProperty(kind ="User")
	tasks = ndb.KeyProperty(kind ="Task", repeated=True)
	invited_users  =  ndb.KeyProperty(kind ="User", repeated=True)
	