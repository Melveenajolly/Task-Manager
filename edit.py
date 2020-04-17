import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb

from taskboard import TaskBoard
from user import User
from datetime import datetime
from task import Task

JINJA_ENVIRONMENT = jinja2.Environment (
    loader=jinja2.FileSystemLoader (os.path.dirname (__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Edit (webapp2.RequestHandler):

    def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		user =users.get_current_user()
    	
		if user:
		
			current_tb_key = ndb.Key (urlsafe=self.request.get('current_tb_key'))
			current_tb = current_tb_key.get()
			task_key = ndb.Key (urlsafe=self.request.get('task_key'))
			task = task_key.get()
			owner_user = current_tb.creator
			member_users = ndb.get_multi (current_tb.invited_users)
			
        
			template_values = {
			'current_tb': current_tb,
			'current_tb_key': current_tb_key.urlsafe(),
			'task_key': task_key.urlsafe(),
			'task': task
			}
			template = JINJA_ENVIRONMENT.get_template('edit.html')
			self.response.write(template.render(template_values))


		# else:
		# 	url = users.create_login_url(self.request.uri)
		# 	self.redirect(url)


    def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		template_values = {}
		exists = False

		current_tb_key = ndb.Key (urlsafe=self.request.get('current_tb_key'))
		current_tb = current_tb_key.get()
		task_key = ndb.Key (urlsafe=self.request.get('task_key'))
		task = task_key.get()
		owner_user = current_tb.creator
		member_users = ndb.get_multi (current_tb.invited_users)
		msg =''
		# owner_user_key = ndb.Key (urlsafe=self.request.get('owner_user'))
		# owner_user =owner_user_key.get()
		if self.request.get('button') == 'Update':
			if len(self.request.get('title').strip()) == 0:
				error_msg = 'Invalid title'
				exists =True
			else:
				exists = False
	            
	            
	                if(current_tb.tasks !=None):
	                    for task1 in current_tb.tasks:
	                        if task1.get().title == self.request.get('title'):
	                        	if task1 != task_key:
		                            exists = True
		                            msg = "Title is already exists"

	                if exists == False:
	                    task.title = self.request.get('title')

	                      

	                    task.due_date = datetime.strptime(self.request.get('due_date'), "%Y-%m-%d")
	                    
	                    if self.request.get('assign_user') != 'None':
	                        assigned_user_key = self.request.get('assign_user')
	                        assigned_user_key = ndb.Key(urlsafe=assigned_user_key)
	                        task.assigned_to = assigned_user_key
	                    elif self.request.get('assign_user') == 'None':
	                    	task.assigned_to = None

	                    task_key =task.put()
	                    
	                    msg = "Task editted"

				
		template_values = {
			'current_tb': current_tb,
			'current_tb_key': current_tb_key.urlsafe(),
			'task_key': task_key.urlsafe(),
			'task': task,
			'owner_user':owner_user,
			'member_users':member_users,
			'msg':msg

		}
		
		template = JINJA_ENVIRONMENT.get_template ('edit.html')
		self.response.write (template.render (template_values))
		

