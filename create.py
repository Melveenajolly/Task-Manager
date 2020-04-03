import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb

from taskboard import TaskBoard

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True
)


class Create(webapp2.RequestHandler):
     
    def get(self):
       
        
        self.response.headers['Content-Type'] = 'text/html'
        
        user = users.get_current_user()
        error_msg = ''
        type_error = ''
        
        if user:
            template_values = {
                'error_msg' : error_msg,
                'type_error' : type_error 
               
            }
            template = JINJA_ENVIRONMENT.get_template('create.html')
            self.response.write(template.render(template_values))

           
        else:
            self.response.write("You are not logged in!")


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {}

        user = users.get_current_user()
        
        if self.request.get('button') == 'Create':
            if user:
                usr = ndb.Key("User", user.user_id()).get()
               
                task_board = TaskBoard()
                task_board.name = self.request.get('taskboard_name')
                task_board.creator = usr.key
                
                task_board.put()
                usr.taskBoards.append(task_board.key)
                usr.put()
                self.redirect('/create')
        if self.request.get('button') == 'Back':
        	self.redirect('/')

        template = JINJA_ENVIRONMENT.get_template('create.html')
        self.response.write(template.render(template_values))
               



