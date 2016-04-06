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
def create_linked_entry(root, Label, arguments={}, helpfultext=None, slider=False):
    frame = tk.LabelFrame(root, relief=tk.GROOVE, borderwidth=2, text=Label, bd=2, pady=4, labelanchor=tk.N, padx=4)
    string = tk.StringVar() #keep this out here since it is used by both
    tk.Grid.columnconfigure(frame, 0, weight=1)
    if(helpfultext): #is helpful text not null
        helptext = tk.Label(frame, text=helpfultext, anchor=tk.W, justify=tk.LEFT, bd=2)
        helptext.bind("<Configure>", realtime_text_wrap) #allows the wrap to resize with the window
        helptext.grid(row=1, column=0, sticky='ew')
    if not slider:
        tk.Entry(frame, textvariable=string, **arguments).grid(row=2, column=0, sticky='ew')
        return((frame, string, None))
    else:
        tk.Label(frame, textvariable=string, **arguments).grid(row=2, column=0, sticky='ew')
        pos = tk.Scale(frame, showvalue=False, from_=0, to=170, orient=tk.HORIZONTAL)
        pos.grid(row=3, column=0, sticky='ew')
        return((frame, string, pos))


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

    #usage: returns a string to display what the interval is set to
    #do bar: sets if we should move the bar to the value
    def compute_int_string(self, do_Bar=False):
        mins=0
        newMins=0 #this stores the "rounded" minutes after it is to the nearest 5 minutes
        hours=0
        seconds=0
        inter = self.interval.get() #get in terms of 2hrs + room for seconds (170)
        if(inter==0):#never
            self.intString.set("never")
            return("never")
        inter = inter-50 #make the number negative if you are adjusting in terms of seconds
        #the number is 50 because we do not want the script to run ever second so the min is 10
        if(inter>0): #we are dealing with minutes
            fracHour = float(inter)/60.0 #fraction of an hour
            if(fracHour<1.0): #we want to return the time in minutes
                mins = int(fracHour*60)
            else:
                mins = int((fracHour-1)*60)
                hours = 1
                if(fracHour>1.90): #basicly 2hrs
                    self.intString.set("2hrs")
                    if(do_Bar):
                        self.interval.set(170)
                    return("120m")
            if mins>15 or hours==1:
                minL = range(0, 55, 5)
                maxL = range(5, 60, 5)
                for i in range(11):
                    Min=minL[i]
                    Max=maxL[i]
                    if mins<Max and mins>Min:#its in that range
                        if Max-mins>mins-Min: #if it is closer to max
                            newMins=Max
                        else: #set to min
                            newMins=Min
                        break;
                    if(mins==Max): #does not need else if because will never be run if above true
                        newMins=Max
                    elif(mins==Min):
                        newMins=Min
            else:
                newMins=mins
            if hours: #more than an hour
                self.intString.set("1hr "+str(newMins)+"m")
                if do_Bar:
                    self.interval.set(60+50+newMins)
                return(str(60+newMins)+"m")
            else:
                self.intString.set(str(newMins)+"m")
                if do_Bar:
                    self.interval.set(50+newMins)
                return(str(newMins)+"m")
        else:
            inter=inter+50 #make it positive again
            minL = range(0, 45, 5)
            maxL = range(5, 50, 5)
            for i in range(9):
                Min=minL[i]
                Max=maxL[i]
                if inter<Max and inter>Min:#its in that range
                    if Max-interz>mins-inter: #if it is closer to max
                        seconds=Max
                    else: #set to min
                        seconds=Min
                    break;
                if(inter==Max): #does not need else if because will never be run if above true
                    seconds=Max
                elif(inter==Min):
                    seconds=Min
            seconds = seconds+10 #we actually want the min to be 10 so shift up ten
            if(do_Bar):
                self.interval.set(inter)
            self.intString.set(str(seconds)+"s")
            return(str(seconds)+"s")
    
    def __init__(self):
        self.diag = tk.Tk()
        self.diag.wm_title=('AutoLogin Settings')
        #args holds the common properties for the linked entries
        args={}
        args['width']=32
        #make everything resizable
        tk.Grid.columnconfigure(self.diag, 0, weight=1, pad=3)
        interval =  create_linked_entry(self.diag, 'interval', slider=True)
        interval[0].grid(row=0,column=0, sticky='nsew', padx=3)
        self.interval = interval[2]
        self.intString = interval[1]
        self.intframe = interval[0]
        self.interval.configure(command=self.compute_int_string)
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
if __name__=="__main__":
    diag = Uname_and_pass_widget()
    diag.start()
