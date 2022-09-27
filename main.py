#Importing the modules used
import tkinter as tk
import tkinter.messagebox as tk_msg
import datetime as dt

class window():
    '''This class serves as the UI and contains methods that both create UI elements using TKinter and handles input from the user.'''
    def __init__(self,root) -> None:
        '''The initializer
        
        This method creates many key attibutes and objects used by later methods.
        It also takes in a TK object inorder to create the UI for the user.'''

        #Setting up our tk window
        self.root = root
        self.create_frame()

        #Creating a data object that holds and handles all the actual infomation contained within the logger.
        self.tasks = Data()
        #Loading any data from the save.txt file
        self.tasks.load()

        #configuration attribuites that are used to control the UI
        self.per_page = 20
        self.current_page = 0
        self.total_page = self.tasks.data.__len__()//self.per_page

        #a dictionary that will hold the TKinter IntVars linked to each task.
        self.val_vars = {}

        #Start creating the UI
        self.show()
    
    def create_frame(self):
        '''A short-cut method that adds a frame to the window and assignes it the grid geomatry.'''
        self.frame = tk.Frame(self.root)
        self.frame.grid()
    
    def show(self):
        '''A method to draw our UI'''
        #First we loop through the list of tasks that is held in the data object.
        #here i is our incrementer whilst k & v are the key-value pair from the dictionary that is used to store the task data.
        for i,(k,v) in enumerate(self.tasks.data.items()):
            #To stop the UI becoming too long we split the list of tasks in to pages.
            #Fistly we check to see if we have filled the current page with tasks.
            if i >= (self.current_page+1)*self.per_page:
                #If this page is full, we end the loop to save time.
                break
            elif i < self.current_page*self.per_page:
                #If we are looking at a task that is on a previous page we skip it to save time.
                continue
            else:
                #If the task is on this page we create and store a TK.IntVar of the value
                self.val_vars[i] = tk.IntVar(value=v)
                #and we create an custom entry object that handles the UI elements and interactions for each tracked task.
                entry(k,self.val_vars[i],self.frame,i+2,self)
        
        #A button to allow users to add tasks to be tracked
        self.add_task_button = tk.Button(self.frame,text='Add Task',width=20,command=self.add_task_on_click)
        self.add_task_button.grid(row=1,column=0)

        #A button to allow users to remove tasks from being tracked.
        self.del_task_button = tk.Button(self.frame,text='Del Task',width=20,command=self.del_task_on_click)
        self.del_task_button.grid(row=1,column=2)

        #A button that allows the user to move to the next page
        self.next_page_button = tk.Button(self.frame,text='===>',width=15,command=self.next)
        self.next_page_button.grid(row=0,column=2)

        #A button to take the user back to a previous page
        self.prev_page_button = tk.Button(self.frame,text='<===',width=15,command=self.prev)
        self.prev_page_button.grid(row=0,column=0)

        #A label that returns the current page number to the user.
        self.page_no = tk.IntVar(value=self.current_page+1)
        self.page_no_label = tk.Label(self.frame,textvariable=self.page_no)
        self.page_no_label.grid(row=0,column=1)

        #This set of if statements control the state of the page buttons.
        if self.current_page == 0 and self.total_page != 0:
            #If the user is on the first page, then there are no previous pages and the button should be unclickable
            self.prev_page_button.config(state='disabled')
            self.next_page_button.config(state='active')
        elif self.current_page == self.total_page and self.total_page != 0:
            #If the user is on the last page, then there are no more pages and the next page button should be unclickable
            self.next_page_button.config(state='disabled')
            self.prev_page_button.config(state='active')
        elif self.total_page == 0:
            #If we have only one page then both buttons need to be disabled
            self.next_page_button.config(state='disabled')
            self.prev_page_button.config(state='disabled')
        else:
            #and if we have pages both before and after the current page then both buttons need to be useable.
            self.next_page_button.config(state='active')
            self.prev_page_button.config(state='active')                

    def add_task_on_click(self):
        '''Creates a new window and call the pop_up method with the 'add' key to create the UI elements needed to add a new task.
        
        The method called when the add task button is clicked.'''
        pop_up_window = tk.Toplevel(self.root)
        pop_up_window.grid()
        self.pop_up(pop_up_window,'add')

    def del_task_on_click(self):
        '''Creates a new window and call the pop_up method with the 'del' key to create the UI elements needed to delete a task.
        
        The method called when the delete task button is clicked.'''
        pop_up_window = tk.Toplevel(self.root)
        pop_up_window.grid()
        self.pop_up(pop_up_window,'del')

    def next(self):
        '''Moves the user to the next page.
        
        This method is called by when the next page button is clicked.'''
        self.current_page += 1
        self.update()

    def prev(self):
        '''Moves the user to the previous page.
        
        This method is called by when the previous page button is clicked.'''
        self.current_page -= 1
        self.update()
    
    def update(self):
        '''Re-draws all elements of the UI.
        
        Destroys and re-creates all the UI elements.
        Called when the page number changes or tasks are added/removed/updated.'''
        self.frame.destroy()
        self.create_frame()
        self.show()
        self.tasks.save()
    
    def pop_up(self,win,a):
        '''Creates a small pop-up window used to obtain input from the user.
        
        Takes in a TK TopLevel object (win) and a key (a) that determines what UI elemets to create and what actions buttons do.'''

        def yes_on_click():
            '''A method for the adding/deleting an inputed task.'''
            #get the data inputed by the user
            ans = box.get()
            #preform the actions needed to process the input correctly
            if a == 'add':
                #When adding a task we also need to get the inputted frequency for the task.
                freq = int(freq_box.get())
                #We also need to pass this data to the data object's add_task method to add a task to our list of tasks.
                self.tasks.add_task(ans,freq)
            elif a == 'del':
                #When deleting a task we just call the data object's del_task method, passing though the key(name) of the task to delete.
                self.tasks.del_task(ans)
            #as the list of tasks has changed, we call update and close the pop-up.
            self.update()
            win.destroy()
        
        def no_on_click():
            '''A method for closing the pop-up without passing any inputed data.'''
            win.destroy()

        #define the strings that are used by UI elements shared by different pop-up configurations.
        if a == 'add':
            #The strings for adding a task
            label_str = 'New Task:'
            yes_str = 'Add Task'
        elif a == 'del':
            #The strings for deleting a task
            label_str = 'Task:'
            yes_str = 'Delete Task'
        else:
            #placeholder strings to prevent errors should a key not be passed.
            label_str = 'label'
            yes_str = 'yes'

        #Creating the UI elements of the pop-up
        ans = None
        frame = tk.Frame(win)
        frame.grid()

        #A label informing the user what the need to enter
        label = tk.Label(frame,text = label_str)
        label.grid(row=0, column = 0)

        #An entry box for the user to enter the name of a task
        box = tk.Entry(frame)
        box.grid(row=0,column=1)

        #Creating any additional elements needed.
        if a == 'add':
            #When adding a task we also need to know how often the task need to be repeated.
            #A label informing the user that we also need to know how frequently the task needs to be preformed
            freq_label = tk.Label(frame,text = 'Period:')
            freq_label.grid(row=1, column=0)

            #an entry box for that value
            freq_box = tk.Entry(frame)
            freq_box.grid(row=1,column=1)


        #A button to complete the task
        yes_button = tk.Button(frame,text=yes_str,command=yes_on_click)
        yes_button.grid(row = 2,column= 1)

        #A button to cancel the task
        no_button = tk.Button(frame,text='Cancel',command=no_on_click)
        no_button.grid(row = 2,column=0)

        return ans
        
class entry():
    '''An object to handle the UI elements and interations for a single task.'''
    def __init__(self,k,v,frame,row,master) -> None:
        #Converting all our inputs into attributes
        self.key = k
        self.val = v
        self.frame = frame
        self.row = row
        self.master = master

        #creating the UI elements of the entry.
        self.create_entry()
    
    def create_entry(self):
        '''A method that creates the UI elements needed to see the status of a task and take action regarding that task.'''
        #Create a button with the name of the task.
        self.key_button = tk.Button(self.frame,text=self.key,width=25,command=self.on_click)
        self.key_button.grid(row=self.row,column=0)

        #A label to show the user how long their streak is and the condition of the task. (Done/Needs doing/Broken streak)
        self.value_label = tk.Label(self.frame,textvariable=self.val,width=10)
        self.value_label.grid(row=self.row,column=1)

        #A button to pause a task should that be needed. i.e. the user is on holiday and doesn't want to loose the streak.
        self.pause_button = tk.Button(self.frame,text = 'Pause', width=25, command = self.pause_on_click)
        self.pause_button.grid(row = self.row, column = 2)

        #call the method used to check the condition of a task.
        self.done()
    
    def on_click(self):
        '''A method to increment a streak.
        
        This method is called when the button with the task's name is clicked.'''
        #First we update the task as it existes in the data object
        self.master.tasks.update_task(self.key)
        #Then we write the data into the save.txt file
        self.master.tasks.save()
        #Then we update the entry object. This saves us from having to re-draw the page by calling the update method.
        self.val.set(self.master.tasks.get_task(self.key)[0])

        #As the value of the entry and data has changed, we need to re-evaluate the task's condition
        self.done()
    
    def pause_on_click(self):
        '''A method to pause a task from being tracked'''
        #First we update the task in the data object
        self.master.tasks.pause_task(self.key)
        #Then we update the save.txt file.
        self.master.tasks.save()

        #Finally, we re-evaluate the task's condition.
        self.done()
    
    def done(self):
        '''Evaluates the condtion of the assigned task.
        
        This method compares the current date and time to the one on the task to determine the state of the task.'''

        #First we get the current date and time using python's datetime module
        now = dt.date.today()
        #we get the task and frequency of the task from the data object
        task,freq = self.master.tasks.get_task(self.key)[1:3]

        #Now we check the condition.
        if self.master.tasks.get_task(self.key)[3] == 'true':
            #if the task is paused we set the label to a blue, showing that the task is paused.
            self.value_label.config(bg='#0092ff')
        elif (now - task) < freq:
            #if the time since the task was last done is less than the task's period
            #we set the label to a green, showing that this task is done.
            self.value_label.config(bg='#00ff00')
        elif (now - task) == freq:
            #if the time since last completion is the same a the frequency, then we set the labe to an orange.
            #This shows that the task need to be done today or the sreak will be broken
            self.value_label.config(bg='#ff8000')
        elif (now - task) > freq:
            #If the time since the task was last done is greater than the period
            #we set the label to red.
            self.value_label.config(bg='#ff0000')
            #And we set the streak to zero in both the data object and the entry itself to save calling update
            self.master.tasks.set_task(self.key,0)
            self.val.set(0)
            
class Data():
    '''This object holds the data on tasks and contains the methods used to manipulate it.'''
    def __init__(self) -> None:
        #Set up the dictionaries that hold all the data on the tasks.
        self.data = {}
        self.timestamps = {}
        self.freq = {}
        self.paused = {}

    def save(self):
        '''Save the current task data to save.txt'''
        #open the save.txt in write mode, overwriting any existing data
        with open('save.txt','w') as file:
            #all the dicts that hold the data share their key, thus we only need to iterate on one to be able to get all the needed data.
            for k,v in self.data.items():#k is the shared key and v is the size of the streak.
                #We've iterated on data and just call the values from the other dicts.
                t = self.timestamps[k]#t is time when the task was last completed
                f = self.freq[k]#f is the task's period
                p = self.paused[k]#p is the boolean of if the task is paused or not
                #we then format the string that will be written into the file for that task.
                #we use a new line to seperate tasks and the pipe char to seperate the data values for each task.
                line = '{0}|{1}|{2}|{3}|{4}\n'.format(k,v,t,f,p)
                #and the we write the task to the save.txt file.
                file.write(line)
    
    def load(self):
        '''A method to load data from the save.txt file.'''
        #opening the save.txt file in read mode
        with open('save.txt','r') as file:
            #we read the file and split on the newline char to get a list of tasks.
            lines = file.read().split('\n')
            #as our formating creates a trailing newline, we need to remove the last term of the list to prevent errors.
            del lines[-1]
            #then we itterate over each task.
            for line in lines:
                #by spliting on the pipe char, we get a list of data values for each task.
                #instead of a list we put each data value into its own variable
                k,v,t,f,p = line.split('|')#k,v,t,f,p have the same meanings as in the save method
                t = t.split('-')#the timestamp need to be broken into year,month,day
                f = f.split(' ')#the period has a trailing days 

                #Adding the data to the relevent dicts
                self.data[k] = int(v)#the value is saved in save.txt as a string but, in the dict as an int
                self.timestamps[k] = dt.date(int(t[0]),int(t[1]),int(t[2]))#python's datetime.date object takes year,month&day as ints.
                self.freq[k] = dt.timedelta(days=int(f[0]))#datetime.timedelta object also needs an int as input.
                self.paused[k] = p
    
    def add_task(self,task:str,freq:int=1):
        '''The method to handle the addition of a task.
        
        Takes in a name for the task(task) to be used as a key and the task's period(freq)
        if only a name is passed, then a default period of one day is used.'''
        #new tasks have a streak of zero
        self.data[task] = 0
        #The inital timestamp is arbitray
        #The 01/01/2000 was chosen due to sounding nice and being long ago enough that any new task would be red.
        self.timestamps[task] = dt.date(2000,1,1)
        #The inputed period is converted to a timedelta object
        self.freq[task] = dt.timedelta(days=freq)
        #A new task is not created paused.
        self.paused[task] = 'false'
    
    def update_task(self,task:str):
        '''A method to update a task and increment its streak.
        
        Takes in the name(task) of the task being updated.'''
        #The streak is incremented by one
        self.data[task] += 1
        #the time of last completion is set to the current date, using date.today()
        self.timestamps[task] = dt.date.today()
        #If a task is being updated it is not paused
        self.paused[task] = 'false'
    
    def set_task(self,task:str,val:int):
        '''sets a task to a fixed value.
        
        takes in a task's name(task) and a value to set it to (val).'''
        self.data[task] = val
    
    def pause_task(self,task):
        '''A method to pause a tasks.
        
        Takes in the name(task) of the task to be paused'''
        self.paused[task] = 'true'

    
    def del_task(self,task:str):
        '''A method that deletes a given task'''
        #we got, dict by dict, an delete the inputed task.
        del self.data[task]
        del self.timestamps[task]
        del self.freq[task]
        del self.paused[task]
    
    def get_task(self,task:str):
        '''A short-hand method for getting all the data attributed to a task.'''
        return self.data[task], self.timestamps[task], self.freq[task], self.paused[task]

#The code to run the task_logger.
#create the root TK window
root = tk.Tk()
#initialize the window
app = window(root)
#start the TK.mainloop
root.mainloop()