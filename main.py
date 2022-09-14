import tkinter as tk
import tkinter.messagebox as tk_msg
import datetime as dt

class window():
    def __init__(self,root) -> None:
        self.root = root
        self.create_frame()

        self.tasks = Data()
        self.tasks.load()

        self.per_page = 20
        self.current_page = 0
        self.total_page = self.tasks.data.__len__()//self.per_page

        self.val_vars = {}

        self.show()
    
    def create_frame(self):
        self.frame = tk.Frame(self.root)
        self.frame.grid()
    
    def show(self):
        for i,(k,v) in enumerate(self.tasks.data.items()):
            if i >= (self.current_page+1)*self.per_page:
                break
            elif i < self.current_page*self.per_page:
                continue
            else:
                self.val_vars[i] = tk.IntVar(value=v)
                entry(k,self.val_vars[i],self.frame,i+2,self)
        
        self.add_task_button = tk.Button(self.frame,text='Add Task',width=20,command=self.add_task_on_click)
        self.add_task_button.grid(row=1,column=0)

        self.del_task_button = tk.Button(self.frame,text='Del Task',width=20,command=self.del_task_on_click)
        self.del_task_button.grid(row=1,column=2)

        self.next_page_button = tk.Button(self.frame,text='===>',width=15,command=self.next)
        self.next_page_button.grid(row=0,column=2)

        self.prev_page_button = tk.Button(self.frame,text='<===',width=15,command=self.prev)
        self.prev_page_button.grid(row=0,column=0)

        self.page_no = tk.IntVar(value=self.current_page+1)
        self.page_no_label = tk.Label(self.frame,textvariable=self.page_no)
        self.page_no_label.grid(row=0,column=1)

        if self.current_page == 0 and self.total_page != 0:
            self.prev_page_button.config(state='disabled')
            self.next_page_button.config(state='active')
        elif self.current_page == self.total_page and self.total_page != 0:
            self.next_page_button.config(state='disabled')
            self.prev_page_button.config(state='active')
        elif self.total_page == 0:
            self.next_page_button.config(state='disabled')
            self.prev_page_button.config(state='disabled')
        else:
            self.next_page_button.config(state='active')
            self.prev_page_button.config(state='active')                

    def add_task_on_click(self):
        pop_up_window = tk.Toplevel(self.root)
        pop_up_window.grid()
        self.pop_up(pop_up_window,'add')

    def del_task_on_click(self):
        pop_up_window = tk.Toplevel(self.root)
        pop_up_window.grid()
        self.pop_up(pop_up_window,'del')

    def next(self):
        self.current_page += 1
        self.update()

    def prev(self):
        self.current_page -= 1
        self.update()
    
    def update(self):
        self.frame.destroy()
        self.create_frame()
        self.show()
        self.tasks.save()
    
    def pop_up(self,win,a):

        def yes_on_click():
            ans = box.get()
            if a == 'add':
                freq = int(freq_box.get())
                self.tasks.add_task(ans,freq)
            elif a == 'del':
                self.tasks.del_task(ans)
            self.update()
            win.destroy()
        
        def no_on_click():
            win.destroy()

        if a == 'add':
            label_str = 'New Task:'
            yes_str = 'Add Task'
        elif a == 'del':
            label_str = 'Task:'
            yes_str = 'Delete Task'
        else:
            label_str = 'label'
            yes_str = 'yes'

        ans = None
        frame = tk.Frame(win)
        frame.grid()

        label = tk.Label(frame,text = label_str)
        label.grid(row=0, column = 0)

        box = tk.Entry(frame)
        box.grid(row=0,column=1)

        if a == 'add':
            freq_label = tk.Label(frame,text = 'Period:')
            freq_label.grid(row=1, column=0)

            freq_box = tk.Entry(frame)
            freq_box.grid(row=1,column=1)


        yes_button = tk.Button(frame,text=yes_str,command=yes_on_click)
        yes_button.grid(row = 2,column= 1)

        no_button = tk.Button(frame,text='Cancel',command=no_on_click)
        no_button.grid(row = 2,column=0)

        return ans
        
    
class entry():
    def __init__(self,k,v,frame,row,master) -> None:
        self.key = k
        self.val = v
        self.frame = frame
        self.row = row
        self.master = master

        self.create_entry()
    
    def create_entry(self):
        self.key_button = tk.Button(self.frame,text=self.key,width=25,command=self.on_click)
        self.key_button.grid(row=self.row,column=0)

        self.value_label = tk.Label(self.frame,textvariable=self.val,width=10)
        self.value_label.grid(row=self.row,column=1)

        self.pause_button = tk.Button(self.frame,text = 'Pause', width=25, command = self.pause_on_click)
        self.pause_button.grid(row = self.row, column = 2)

        self.done()
    
    def on_click(self):
        self.master.tasks.update_task(self.key)
        self.master.tasks.save()
        self.val.set(self.master.tasks.get_task(self.key)[0])

        self.done()
    
    def pause_on_click(self):
        self.master.tasks.pause_task(self.key)
        self.master.tasks.save()

        self.done()
    
    def done(self):
        now = dt.date.today()
        task,freq = self.master.tasks.get_task(self.key)[1:3]

        if self.master.tasks.get_task(self.key)[3] == 'true':
            self.value_label.config(bg='#0092ff')
        elif (now - task) < freq:
            self.value_label.config(bg='#00ff00')
        elif (now - task) == freq:
            self.value_label.config(bg='#ff8000')
        elif (now - task) > freq:
            self.value_label.config(bg='#ff0000')
            self.master.tasks.set_task(self.key,0)
            self.val.set(0)
            
class Data():
    def __init__(self) -> None:
        self.data = {}
        self.timestamps = {}
        self.freq = {}
        self.paused = {}

    def save(self):
        with open('save.txt','w') as file:
            for k,v in self.data.items():
                t = self.timestamps[k]
                f = self.freq[k]
                p = self.paused[k]
                line = '{0}|{1}|{2}|{3}|{4}\n'.format(k,v,t,f,p)
                file.write(line)
    
    def load(self):
        with open('save.txt','r') as file:
            lines = file.read().split('\n')
            del lines[-1]
            for line in lines:
                k,v,t,f,p = line.split('|')
                t = t.split('-')
                f = f.split(' ')
                self.data[k] = int(v)
                self.timestamps[k] = dt.date(int(t[0]),int(t[1]),int(t[2]))
                self.freq[k] = dt.timedelta(days=int(f[0]))
                self.paused[k] = p
    
    def add_task(self,task:str,freq:int=1):
        self.data[task] = 0
        self.timestamps[task] = dt.date(2000,1,1)
        self.freq[task] = dt.timedelta(days=freq)
        self.paused[task] = 'false'
    
    def update_task(self,task:str):
        self.data[task] += 1
        self.timestamps[task] = dt.date.today()
        self.paused[task] = 'false'
    
    def set_task(self,task:str,val:int):
        self.data[task] = val
        self.timestamps[task] = dt.date(2000,1,1)
    
    def pause_task(self,task):
        self.paused[task] = 'true'

    
    def del_task(self,task:str):
        del self.data[task]
        del self.timestamps[task]
        del self.freq[task]
        del self.paused[task]
    
    def get_task(self,task:str):
        return self.data[task], self.timestamps[task], self.freq[task], self.paused[task]

root = tk.Tk()
app = window(root)
root.mainloop()