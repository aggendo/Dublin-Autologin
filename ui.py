import tkinter as tk
import config as config

#creates a window of type Type and when the okay is pressed verify is run to test if acceptable

conf = config.config() #create an instance of config

# FIXME: make create_linked_entry a class
# TODO:

 
def realtime_text_wrap(event):
    entry=event.widget
    # FIXME: make this a global method, to prevent function object creation
    # for every label.
    pad = 0
    pad += int(str(entry['bd']))
    pad += int(str(entry['padx']))
    pad *= 2
    entry.configure(wraplength = event.width - pad)

#returns a frame containing the widgets and a StringVar arguments are fed to the Entry
def create_linked_entry(root, Label, arguments={}, helpfultext=None):
    frame = tk.LabelFrame(root, relief=tk.GROOVE, borderwidth=2, text=Label, bd=2, pady=4, labelanchor=tk.N, padx=4)
    string = tk.StringVar()
    tk.Grid.columnconfigure(frame, 0, weight=1)
    #tk.Grid.rowconfigure(frame, 0, weight=1)
    #tk.Grid.rowconfigure(frame, 1, weight=1)
    if(helpfultext): #is helpful text not null
        helptext = tk.Label(frame, text=helpfultext, anchor=tk.W, justify=tk.LEFT, bd=2)
        helptext.bind("<Configure>", realtime_text_wrap) #allows the wrap to resize with the window
        helptext.grid(row=1, column=0, sticky='ew')
    
    tk.Entry(frame, textvariable=string, **arguments).grid(row=2, column=0, sticky='ew')
    #name = tk.Label(frame, text=Label)
    #name.grid(row=0, column=0, sticky='nsew')
    return((frame, string))

class prompt_something:
    def __init__(self, Type, Label, Cancel=False, verify=None):
        self.verify=verify
        self.Type = Type
        self.diag = tk.Tk()
        ent = create_linked_entry(self.diag, Label)
        ent[0].grid()
        self.string=ent[1]
        bframe = tk.Frame(self.diag) #holds buttons
        tk.Button(bframe, text="Okay", command=self.okay).grid(row=0,column=0)
        if(Cancel):
            tk.Button(bframe, text="Cancel", command=self.cancel).grid(row=1,column=0)
        bframe.grid(row=1, column=0)

    def cancel(self):
        self.diag.destroy()
        return(None) #nothing changes

    def okay(self):
        if self.verify: #we need to verify that (verify is not None)
            erno = self.verify(self.string.get()) #test the string and return true if success
            if erno.equals(None):           #safer way of handling
                return(self.string.get())
    def start(self):
        self.diag.mainloop()



class Uname_and_pass_widget:

    def what_size(self, event):
        height = self.intframe.winfo_reqheight() + self.unameframe.winfo_reqheight() + self.upassframe.winfo_reqheight() + self.bheight
        self.diag.minsize(300, height)
        self.diag.maxsize(500, height)
    
    
    def __init__(self):
        self.diag = tk.Tk()
        self.diag.wm_title=('AutoLogin Settings')
        #args holds the common properties for the linked entries
        args={}
        args['width']=32
        #make everything resizable
        tk.Grid.columnconfigure(self.diag, 0, weight=1, pad=3)
        #tk.Grid.rowconfigure(self.diag, 0, weight=1)
        #tk.Grid.rowconfigure(self.diag, 1, weight=1)
        #tk.Grid.rowconfigure(self.diag, 2, weight=1)
        interval =  create_linked_entry(self.diag, 'interval')
        interval[0].grid(row=0,column=0, sticky='nsew', padx=3)
        self.interval = interval[1]
        self.intframe = interval[0]
        #TODO: read interval from config file and put it in the bar
        helptext="put your username here exactly as you would enter it to log in normally WITHOUT the @dublinschool.org at the end of it"
        uname = create_linked_entry(self.diag, 'Username', helpfultext=helptext)
        uname[0].grid(row=1,column=0, sticky='nsew', padx=3)
        self.uname=uname[1]
        self.unameframe = uname[0]
        self.uname.set(conf.get_username())
        args['show']='*' #we change for the password box to only show ****s
        upass = create_linked_entry(self.diag, 'Password', arguments=args)
        upass[0].grid(row=2,column=0, sticky='nsew', padx=3)
        #TODO: make password characters represented with * here
        self.upass=upass[1]
        self.upassframe = upass[0]
        self.upass.set(conf.get_password())
        bframe = tk.Frame(self.diag) #holds buttons
        tk.Button(bframe, text="Okay", command=self.okay, width=10).grid(row=0,column=0)
        unimportant_button = tk.Button(bframe, text="Test", command=self.test, width=10)
        unimportant_button.grid(row=0,column=1)
        self.bheight = unimportant_button.winfo_reqheight()+6
        bframe.grid(row=3, column=0, sticky=tk.E, padx=3, pady=3)
        height = self.intframe.winfo_reqheight() + self.unameframe.winfo_reqheight() + self.upassframe.winfo_reqheight() + self.bheight #get what the height should be
        self.diag.geometry("300x"+str(height)) #set default window size
        self.diag.minsize(300, 0)
        self.diag.update()
        self.what_size('blah')#make the window the right size in the beginning
        self.diag.bind("<Configure>", self.what_size)

    def okay(self):
        if(self.test()):
            conf.set_username(self.uname.get()) #save username and password
            conf.set_password(self.upass.get())
            self.diag.destroy()
        else:
            pass #TODO: tell that it was not successful

    def test(self):
        return(True)#test login here
    
    def start(self):
        self.diag.mainloop()

diag = Uname_and_pass_widget()
diag.start()
