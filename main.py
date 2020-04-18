import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from user import User
from display import Display
from taskboard import TaskBoard
from edit import Edit


JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True
)

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		
		url = ''
		url_string = ''
		welcome = 'Welcome back'
		search_url = ''
		search_url_string = ''
		taskBoards = ''
		
		user = users.get_current_user()

		myuser = None
		if user:
			url = users.create_logout_url(self.request.uri)
			url_string = 'logout'
			myuser =''
			myuser_key = ndb.Key('User',  user.user_id() )
			myuser = myuser_key.get()
			# if myuser:
			# 	taskBoards = ndb.get_multi (myuser.taskBoards)
			


			if  myuser == None:
				welcome = 'Welcome to the Task Mangement System'
				myuser = User(id = user.user_id(), email_address = user.email())
				myuser.put()
				taskBoards = ndb.get_multi (myuser.taskBoards)


			taskBoards = ndb.get_multi (myuser.taskBoards)			




		else:

			url = users.create_login_url(self.request.uri)
			url_string = 'login'



        #passing to html page
		template_values = {
		    'url'  : url,
		    'url_string' : url_string,
		    'myuser' : myuser,
		    'user': user,
		    'taskBoards' : taskBoards,
		    'welcome' : welcome,
		    
		}

		template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(template.render(template_values))


	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		template_values = {}

		user = users.get_current_user()
        
		if self.request.get('button') == 'Create':
			if user:
				usr = ndb.Key("User", user.user_id()).get()
               
				task_board = TaskBoard()
				if len(self.request.get('taskboard_name').strip()) > 0:
					task_board.name = self.request.get('taskboard_name')
					task_board.creator = usr.key
	                
					task_board.put()
					usr.taskBoards.append(task_board.key)
					usr.put()
					self.redirect('/')
				else:
					self.redirect('/')
			else:
				self.redirect('/')

		if self.request.get('button') == 'Back':
			self.redirect('/')

		
               

# starts the web application we specify the full routing table here as well
app = webapp2.WSGIApplication([
	('/', MainPage),
	('/display', Display),
	('/edit', Edit)
	
], debug=True)
	
	