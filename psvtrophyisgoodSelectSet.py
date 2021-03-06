
from Tkinter import *

import os
#import ParseTRPDB Fuck trophy_local.db..
import ParseTRPSFM

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

import psvtrophyisgoodSelectSet_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", lambda: os._exit(0))
    root.resizable(0, 0)
    top = psvtrophyisgood (root)
    psvtrophyisgoodSelectSet_support.init(root, top)
    root.mainloop()

w = None
def create_psvtrophyisgood(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    top = psvtrophyisgood (w)
    psvtrophyisgoodSelectSet_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_psvtrophyisgood():
    global w
    w.destroy()
    w = None


class psvtrophyisgood:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("457x368+487+146")
        top.title("psvtrophyisgood")



        self.selectFrame = LabelFrame(top)
        self.selectFrame.place(relx=0.0, rely=0.0, relheight=0.99, relwidth=1.0)
        self.selectFrame.configure(relief=GROOVE)
        self.selectFrame.configure(text='''Select trophy set''')
        self.selectFrame.configure(width=440)

        self.trophySetSelector = ScrolledListBox(self.selectFrame)
        self.trophySetSelector.place(relx=0.02, rely=0.0, relheight=0.9,relwidth=0.96)
        self.trophySetSelector.configure(background="white")
        self.trophySetSelector.configure(font="TkFixedFont")
        self.trophySetSelector.configure(highlightcolor="#d9d9d9")
        self.trophySetSelector.configure(selectbackground="#c4c4c4")
        self.trophySetSelector.configure(width=440)
        a = 0
        for file in os.listdir(os.path.dirname(os.path.realpath(__file__))+"/trophyDownloaded/data"):
            if file != "sce_trop":
                if not os.path.isfile(file):
                    if not file.startswith("."):
                        ParseTRPSFM.init(os.path.dirname(os.path.realpath(__file__))+"/trophyDownloaded/conf/"+file+"/TROP.SFM")
                        title = ParseTRPSFM.getSetInfo()["title"].replace("[","(") + " ["+file+"]"
                        self.trophySetSelector.insert(a,title)
            a += 1


        self.selectSet = Button(self.selectFrame)
        self.selectSet.place(relx=0.02, rely=0.9, height=26, width=187)
        self.selectSet.configure(activebackground="#d9d9d9")
        self.selectSet.configure(command=lambda: psvtrophyisgoodSelectSet_support.selectSet(self.trophySetSelector.get(ACTIVE)))
        self.selectSet.configure(text='''Select Trophy Set''')

        self.importSet = Button(self.selectFrame)
        self.importSet.place(relx=0.7, rely=0.9, height=26, width=117)
        self.importSet.configure(activebackground="#d9d9d9")
        self.importSet.configure(command=psvtrophyisgoodSelectSet_support.importSet)
        self.importSet.configure(text='''Import Set''')
        self.importSet.configure(width=117)

        self.exportSet = Button(self.selectFrame)
        self.exportSet.place(relx=0.45, rely=0.9, height=26, width=107)
        self.exportSet.configure(activebackground="#d9d9d9")
        self.exportSet.configure(command=lambda: psvtrophyisgoodSelectSet_support.exportSet(self.trophySetSelector.get(ACTIVE)))
        self.exportSet.configure(text='''Export Set''')
        self.exportSet.configure(width=107)












# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)

        #self.configure(yscrollcommand=_autoscroll(vsb),
        #    xscrollcommand=_autoscroll(hsb))
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = Pack.__dict__.keys() | Grid.__dict__.keys() \
                  | Place.__dict__.keys()
        else:
            methods = Pack.__dict__.keys() + Grid.__dict__.keys() \
                  + Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        return func(cls, container, **kw)
    return wrapped

class ScrolledListBox(AutoScroll, Listbox):
    '''A standard Tkinter Text widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

if __name__ == '__main__':
    vp_start_gui()



