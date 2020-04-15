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


class Display (webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {}

        #owner of taskboard
        user = users.get_current_user()
       

        #current taskboard
        current_tb_key = ndb.Key (urlsafe=self.request.get('key_name'))
        current_tb = current_tb_key.get()
        owner_user = current_tb.creator
        member_users = ndb.get_multi (current_tb.invited_users)


        # fetching total users to list for radiobutton in display page
        total_user = User.query()
        total_user = total_user.fetch()
        
        

        template_values = {
			'current_tb': current_tb,
			'current_tb_key': current_tb_key.urlsafe(),
			'owner_user': owner_user,
            'total_user': total_user,
            'user': user,
            'member_users': member_users,
            

    	}

        template = JINJA_ENVIRONMENT.get_template ('display.html')
        self.response.write (template.render (template_values))



    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        msg =''
        added_user=''
        template_values={}
        current_tb_key = ndb.Key (urlsafe=self.request.get('current_tb_key'))
        current_tb= current_tb_key.get()
        user = users.get_current_user()
        member_users = ndb.get_multi (current_tb.invited_users)
        total_user = User.query()
        total_user = total_user.fetch()
        exits = False
        b = self.request.get('button')
        owner_user = self.request.get('owner_user')
        if owner_user:
            owner_user = ndb.Key(urlsafe= owner_user)
        


        if b == 'Invite':
            if user.email() == current_tb.creator.get().email_address:
                added_user_key = self.request.get('added_user')
                added_user_key = ndb.Key(urlsafe=added_user_key)
                added_user = added_user_key.get()
                current_tb.invited_users.append(added_user_key)
                current_tb.put()
                added_user.taskBoards.append(current_tb_key)
                added_user.put()
                self.redirect('/display?key_name=' + str(current_tb_key.urlsafe()))
            else:
                self.redirect('/')

        elif b == 'Add':
            exists = False
            task = Task()
            if len(self.request.get('title').strip()) > 0:
                if(current_tb.tasks !=None):
                    for task1 in current_tb.tasks:
                        if task1.get().title == self.request.get('title'):
                            exists = True
                            msg = "Title is already exists"

                if exists == False:
                    task.title = self.request.get('title')

                    # if str(datetime.datetime.today()) > task_due:
                    #    

                    task.due_date = datetime.strptime(self.request.get('due_date'), "%Y-%m-%d")
                    task.checked = False
                    if self.request.get('assign_user') != 'None':
                        assigned_user_key = self.request.get('assign_user')
                        assigned_user_key = ndb.Key(urlsafe=assigned_user_key)
                        task.assigned_to = assigned_user_key
                    task_key =task.put()
                    current_tb.tasks.append(task_key)
                    current_tb.put()
                    msg = "Task added"

                    template_values = {
                        'msg':msg,
                        'key_name' : current_tb_key.urlsafe(),
                        'current_tb_key' : current_tb_key.urlsafe(),
                        'current_tb':current_tb,
                        'user':user,
                        'owner_user': owner_user,
                        'member_users':member_users,
                        'total_user':total_user
                        
                    }
                    template = JINJA_ENVIRONMENT.get_template ('display.html')
                    self.response.write (template.render (template_values))
                else:
                    template_values = {
                        'msg':msg,
                        'key_name' : current_tb_key.urlsafe(),
                        'current_tb_key' : current_tb_key.urlsafe(),
                        'current_tb':current_tb,
                        'user':user,
                        'owner_user': owner_user,
                        'member_users':member_users,
                        'total_user':total_user
                        
                    }
                    template = JINJA_ENVIRONMENT.get_template ('display.html')
                    self.response.write (template.render (template_values))

        elif b == 'Rename':
            Name = self.request.get('Name')
            current_tb.name = Name
            current_tb.put()
            msg = ''
            template_values = {
            'msg':msg,
            'key_name' : current_tb_key.urlsafe(),
            'current_tb_key' : current_tb_key.urlsafe(),
            'current_tb':current_tb,
            'user':user,
            'owner_user': owner_user,
            'member_users':member_users,
            'total_user':total_user
                        
            }
            template = JINJA_ENVIRONMENT.get_template ('display.html')
            self.response.write (template.render (template_values))



        #delete button
        if self.request.get('button') == 'Delete':
            task_key = self.request.get('task_key')
            task_key = ndb.Key(urlsafe = task_key)
            task_key.delete()
            current_tb.tasks.remove(task_key)
            current_tb.put()
            template_values = {
                'msg':msg,
                'key_name' : current_tb_key.urlsafe(),
                'current_tb_key' : current_tb_key.urlsafe(),
                'current_tb':current_tb,
                'user':user,
                'owner_user': owner_user,
                'member_users':member_users,
                'total_user':total_user
                        
            }
            template = JINJA_ENVIRONMENT.get_template ('display.html')
            self.response.write (template.render (template_values))

        #checked tasks
        checked_value = self.request.get('completed')
        
        if checked_value:
            #it is checked
            checked_task_key = ndb.Key(urlsafe = checked_value)
            checked_task = checked_task_key.get()
            checked_task.checked = True
            checked_task.completion_date = datetime.now()
            checked_task.put()
            template_values = {
                'msg':msg,
                'key_name' : current_tb_key.urlsafe(),
                'current_tb_key' : current_tb_key.urlsafe(),
                'current_tb':current_tb,
                'user':user,
                'owner_user': owner_user,
                'member_users':member_users,
                'total_user':total_user
                        
            }
            template = JINJA_ENVIRONMENT.get_template ('display.html')
            self.response.write (template.render (template_values))
        # else:
        #     self.redirect('/')



       
           




