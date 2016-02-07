import tkinter as tk
import config as config

#creates a window of type Type and when the okay is pressed verify is run to test if acceptable

conf = config.config() #create an instance of config

def create_linked_entry(root, Label):
    frame = tk.Frame(root)
    string = tk.StringVar()
    tk.Label(frame, text=Label).grid(row=0, column=0)
    tk.Entry(frame, textvariable=string).grid(row=1, column=0)
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
        if self.verify: #we need to verify (verify is not None)
            erno = self.verify(self.string.get()) #test the string and return true if success
            if erno.equals(None):           #safer way of handling
                return(self.string.get())
    def start(self):
        self.diag.mainloop()

class Uname_and_pass_widget:
    def __init__(self):
        self.diag = tk.Tk()
        interval =  create_linked_entry(self.diag, 'interval')
        interval[0].grid(row=0,column=0)
        self.interval = interval[1]
        #TODO: read interval from config file and put it in the bar
        uname = create_linked_entry(self.diag, 'Username')
        uname[0].grid(row=1,column=0)
        self.uname=uname[1]
        self.uname.set(conf.get_username())
        upass = create_linked_entry(self.diag, 'Password')
        upass[0].grid(row=2,column=0)
        #TODO: make password characters represented with * here
        self.upass=upass[1]
        self.upass.set(conf.get_password())
        bframe = tk.Frame(self.diag) #holds buttons
        tk.Button(bframe, text="Okay", command=self.okay).grid(row=0,column=0)
        tk.Button(bframe, text="Test", command=self.test).grid(row=0,column=1)
        bframe.grid(row=3, column=0)

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
