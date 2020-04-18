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
        total_task_count = 0
        completed_task = 0
        active_task = 0
        completed_today = 0

        #owner of taskboard
        user = users.get_current_user()
        board_msg = ''
        board_msg= self.request.get('board_msg')
    
        add_msg = self.request.get('add_msg')
        

       

        #current taskboard
        current_tb_key = ndb.Key (urlsafe=self.request.get('key_name'))
        current_tb = current_tb_key.get()
        owner_user = current_tb.creator
        member_users = ndb.get_multi (current_tb.invited_users)
        total_task = ndb.get_multi(current_tb.tasks)

        for i in total_task:
            total_task_count = total_task_count + 1
            if i.checked == True:
                completed_task = completed_task + 1
            if i.checked == False:
                active_task = active_task + 1
            if i.completion_date != None:
                if i.completion_date.strftime("%Y-%m-%d") == datetime.now().strftime("%Y-%m-%d"):
                    completed_today = completed_today + 1

            




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
            'total_task_count':total_task_count,
            'completed_task':completed_task,
            'active_task':active_task,
            'completed_today':completed_today,
            'board_msg':board_msg,
            'add_msg':add_msg,
            
            

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
                if self.request.get('added_user') != 'None':
                    added_user_key = self.request.get('added_user')
                    added_user_key = ndb.Key(urlsafe=added_user_key)
                    added_user = added_user_key.get()
                    current_tb.invited_users.append(added_user_key)
                    current_tb.put()
                    added_user.taskBoards.append(current_tb_key)
                    added_user.put()
                    self.redirect('/display?key_name=' + str(current_tb_key.urlsafe()))
                elif self.request.get('added_user') == 'None':
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
                            add_msg = "Title is already exists"

                if exists == False:
                    task.title = self.request.get('title')

                    # if str(datetime.datetime.today()) > task_due:
                    #    
                    today_date = datetime.today().strftime("%Y-%m-%d")
                    today = datetime.strptime(today_date,"%Y-%m-%d")
                    task.due_date = datetime.strptime(self.request.get('due_date'), "%Y-%m-%d")
                    self.response.write(today_date)
                    self.response.write("----------")
                    self.response.write(datetime.strptime(self.request.get('due_date'), "%Y-%m-%d"))
                    task.checked = False
                    if self.request.get('assign_user') != 'None':
                        assigned_user_key = self.request.get('assign_user')
                        assigned_user_key = ndb.Key(urlsafe=assigned_user_key)
                        task.assigned_to = assigned_user_key
                    if task.due_date >= today:
                        task_key =task.put()
                        current_tb.tasks.append(task_key)
                        current_tb.put()
                        add_msg = "Task added"
                        
                    else:
                        add_msg = "Enter a valid due date"
                    self.redirect('/display?key_name=' + str(current_tb_key.urlsafe())+'&add_msg=' +add_msg)

                    # template_values = {
                    #     'msg':msg,
                    #     'key_name' : current_tb_key.urlsafe(),
                    #     'current_tb_key' : current_tb_key.urlsafe(),
                    #     'current_tb':current_tb,
                    #     'user':user,
                    #     'owner_user': owner_user,
                    #     'member_users':member_users,
                    #     'total_user':total_user
                        
                    # }
                    # template = JINJA_ENVIRONMENT.get_template ('display.html')
                    # self.response.write (template.render (template_values))
                else:
                    self.redirect('/display?key_name=' + str(current_tb_key.urlsafe())+'&add_msg=' +add_msg)
            else:
                add_msg = 'Invalid title'
                self.redirect('/display?key_name=' + str(current_tb_key.urlsafe())+'&add_msg=' +add_msg)
        


        elif b == 'Rename':
            if len(self.request.get('Name').strip()) > 0:
                Name = self.request.get('Name')
                current_tb.name = Name
                current_tb.put()
                msg = ''
        #redirect ckeyyumbol if else um redirect cheyyuka
                self.redirect('/display?key_name=' + str(current_tb_key.urlsafe()))
            else:
                self.redirect('/display?key_name=' + str(current_tb_key.urlsafe()))

            # template_values = {
            # 'msg':msg,
            # 'key_name' : current_tb_key.urlsafe(),
            # 'current_tb_key' : current_tb_key.urlsafe(),
            # 'current_tb':current_tb,
            # 'user':user,
            # 'owner_user': owner_user,
            # 'member_users':member_users,
            # 'total_user':total_user
                        
            # }
            # template = JINJA_ENVIRONMENT.get_template ('display.html')
            # self.response.write (template.render (template_values))

        







        #delete button
        if self.request.get('button') == 'Delete':
            task_key = self.request.get('task_key')
            task_key = ndb.Key(urlsafe = task_key)
            
            current_tb.tasks.remove(task_key)
            current_tb.put()
            task_key.delete()
            self.redirect('/display?key_name=' + str(current_tb_key.urlsafe()))
            
            # template_values = {
            #     'msg':msg,
            #     'key_name' : current_tb_key.urlsafe(),
            #     'current_tb_key' : current_tb_key.urlsafe(),
            #     'current_tb':current_tb,
            #     'user':user,
            #     'owner_user': owner_user,
            #     'member_users':member_users,
            #     'total_user':total_user
                        
            # }
            # template = JINJA_ENVIRONMENT.get_template ('display.html')
            # self.response.write (template.render (template_values))

        #checked tasks
        checked_value = self.request.get('completed')
        
        if checked_value:
            #it is checked
            checked_task_key = ndb.Key(urlsafe = checked_value)
            checked_task = checked_task_key.get()
            checked_task.checked = True
            checked_task.completion_date = datetime.now()
            checked_task.put()
            self.redirect('/display?key_name=' + str(current_tb_key.urlsafe()))
            # template_values = {
            #     'msg':msg,
            #     'key_name' : current_tb_key.urlsafe(),
            #     'current_tb_key' : current_tb_key.urlsafe(),
            #     'current_tb':current_tb,
            #     'user':user,
            #     'owner_user': owner_user,
            #     'member_users':member_users,
            #     'total_user':total_user
                        
            # }
            # template = JINJA_ENVIRONMENT.get_template ('display.html')
            # self.response.write (template.render (template_values))

        #remove user
        if self.request.get('button') == 'Remove':

            if self.request.get('removed_user') != 'None':
                removed_user_key_1 = self.request.get('removed_user')
                removed_user_key = ndb.Key(urlsafe= removed_user_key_1)
                removed_user = removed_user_key.get()
                #making the tasks of removed user unassigned
                tasks = ndb.get_multi(current_tb.tasks)
                for task1 in tasks:
                    
                    if task1.assigned_to == removed_user_key.get().key:
                        task1.assigned_to = None
                        task1.put()
                #removing from invited user list
                current_tb.invited_users.remove(removed_user_key)
                current_tb.put()
                member_users = ndb.get_multi (current_tb.invited_users)
                #remove current task board from removed users taskboard list
                removed_user.taskBoards.remove(current_tb_key)
                removed_user.put()
                msg = ''
                self.redirect('/display?key_name=' + str(current_tb_key.urlsafe()))
                # template_values = {
                #     'msg':msg,
                #     'key_name' : current_tb_key.urlsafe(),
                #     'current_tb_key' : current_tb_key.urlsafe(),
                #     'current_tb':current_tb,
                #     'user':user,
                #     'owner_user': owner_user,
                #     'member_users':member_users,
                #     'total_user':total_user
                                
                # }
                # template = JINJA_ENVIRONMENT.get_template ('display.html')
                # self.response.write (template.render (template_values))
            if self.request.get('removed_user') == 'None':
                self.redirect('/display?key_name=' + str(current_tb_key.urlsafe()))

        #Removing the task board
        if  self.request.get('button') == 'Remove the Task Board':
            tasks = ndb.get_multi(current_tb.tasks)
            if len(member_users) == 0 and len(tasks) ==0:
                ou = owner_user.get()
                ou.taskBoards.remove(current_tb_key)
                ou.put()
                current_tb_key.delete()
                
                self.redirect('/')
            else:
                board_msg = 'Delete all the tasks and and remove all members to remove the task board '
                self.redirect('/display?key_name=' + str(current_tb_key.urlsafe())+'&board_msg=' +board_msg)


        if self.request.get('button') == 'Back to home':
            self.redirect('/')



        



       
           




