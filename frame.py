import os
#import time
import codecs
import chardet
from PIL import Image, ImageTk
from string import ascii_letters, punctuation

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkf
import tkinter.filedialog as tkfd
import tkinter.messagebox as msgbox
from tkinter.scrolledtext import ScrolledText as SText

from . import main


opb = os.path.basename
imgpath = os.path.join(os.path.dirname(__file__), \
        'favicon.jpg')


class MainMenu(tk.Menu):
    def __init__(self, root):
        super().__init__(root, bg='white', activebackground='red', bd=2)

        self.crt_items()

        # all event to bind
        root.bind_all('<Control-o>', self.open)
        root.bind_all('<Control-O>', self.open)
        root.bind_all('<Control-h>', self.details)
        root.bind_all('<Control-H>', self.details)
        root.bind_all('<Control-n>', self.new)
        root.bind_all('<Control-N>', self.new)
        root.bind_all('<Control-f>', self.fontconfigure)
        root.bind_all('<Control-F>', self.fontconfigure)
        root.bind_all('<Control-Shift-a>', self.about)
        root.bind_all('<Control-Shift-A>', self.about)
        root.bind_all('<Control-Shift-Q>', lambda e: self.master.destroy())
        root.bind_all('<Control-Shift-q>', lambda e: self.master.destroy())

        # init the image show
        self.img = ImageTk.PhotoImage(Image.open(imgpath).resize((128, 128)))

        # change the icon image (False means not use default)
        root.iconphoto(False, self.img)

        # show the menu widget
        root.config(menu = self)

        MainEditor.mainmenu = self
        MainEditor.root = root

        self.font = tkf.nametofont('TkDefaultFont').copy()

    def crt_items(self):
        "Create all items"
        # File Menu
        # Open New | Save SaveAs Reopen | Close Exit
        self.filemn = filemn = tk.Menu(self, tearoff=0, bg='white', activebackground='red', bd=2)
        ac = filemn.add_command
        ac(label = 'Open', command = self.open, accelerator = 'Ctrl+o')
        ac(label = "New", command = self.new, accelerator = 'Ctrl+n')
        filemn.add_separator()
        ac(label = 'Save', command = self.save, state = 'disabled', accelerator = 'Ctrl+s')
        ac(label = 'Save As', command = self.saveas, state = 'disabled', accelerator = 'Ctrl+Shift+s')
        ac(label = 'Reopen', command = self.reopen, state = 'disabled', accelerator = 'Ctrl+r')
        filemn.add_separator()
        ac(label = 'Close', command = self.close, state = 'disabled', accelerator = 'Ctrl+q')
        ac(label = 'Exit', command = self.master.destroy, accelerator = 'Ctrl+Shift+q')

        # Openrations Menu
        # Decode Encode
        self.operationmn = operations = tk.Menu(self, tearoff=0, bg= 'white', activebackground = 'red', bd=2)
        ac = operations.add_command
        ac(label = 'Decode', command = self.decode, state = 'disabled', accelerator = 'Ctrl+d')
        ac(label = 'Encode', command = self.encode, state = 'disabled', accelerator = 'Ctrl+e')

        # Configure Menu
        # Font
        cfgmn = tk.Menu(self, tearoff=0, bg='white', activebackground='red', bd=2)
        cfgmn.add_command(label = 'Font', command=self.fontconfigure, accelerator = 'Ctrl+f')

        # Help Menu
        # About Details
        helpmn = tk.Menu(self, tearoff = 0, bg='white', activebackground='red', bd=2)
        ac = helpmn.add_command
        ac(label = 'About', command = self.about, accelerator = "Ctrl+Shift+a")
        ac(label = 'Details', command = self.details, accelerator = "Ctrl+h")

        # add all Menu in
        self.add_cascade(label = 'File', menu = filemn)
        self.add_cascade(label = 'Openrations', menu = operations)
        self.add_cascade(label = 'Configure', menu = cfgmn)
        self.add_cascade(label = 'Help', menu = helpmn)

        self.update()

    def open(self, event = None):
        "Open The file"
        # use tkinter.filedialog to ask the file to open
        fn = tkfd.askopenfilename(title = 'Open The File', initialdir = os.getcwd())

        # if user haven't choose any file, do nothing 
        if not fn:
            return

        org = Open(fn)

        # The file can not use text mode !
        if org is None:
            msgbox.showwarning('Error File Format', 'Your file is not in a right' \
                    ' format the can change into text, check if it can open corretly')
            return

        # create the editor frame to edit the content
        me = MainEditor(self.note, org, fn = fn)
        self.note.add(me, opb(fn))
        self.note.select(me)

        self.unlock('open')

    def unlock(self, type):

        if type == 'open':
            # unlock the operations
            self.filemn.entryconfigure(3, state = 'normal') # Save
            self.filemn.entryconfigure(4, state = 'normal') # Save As
            self.filemn.entryconfigure(5, state = 'normal') # Reopen
            self.filemn.entryconfigure(7, state = 'normal') # Close
            self.operationmn.entryconfigure(0, state = 'normal') # Decode
            self.operationmn.entryconfigure(1, state = 'normal') # Encode

        elif type == 'new':
            # unlock the operations for save (new)
            self.filemn.entryconfigure(3, state = 'normal')
            self.filemn.entryconfigure(5, state = 'normal')
            self.filemn.entryconfigure(7, state = 'normal')
            self.operationmn.entryconfigure(0, state = 'normal')
            self.operationmn.entryconfigure(1, state = 'normal')

        elif type == 'close':
            # disable all the not needed menu operations
            # so user's won't do some meaningless things
            self.filemn.entryconfigure(3, state = 'disabled')
            self.filemn.entryconfigure(4, state = 'disabled')
            self.filemn.entryconfigure(5, state = 'disabled')
            self.filemn.entryconfigure(7, state = 'disabled')
            self.operationmn.entryconfigure(0, state = 'disabled')
            self.operationmn.entryconfigure(1, state = 'disabled')

        elif type == 'saveas':
            # change the state if the *new* file is save into a real file
            self.filemn.entryconfigure(3, state = 'normal') # Save
            self.filemn.entryconfigure(5, state = 'normal') # Reopen

    def new(self, event = None):
        me = MainEditor(self.note, '', fn = None)
        self.note.add(me, 'new')
        self.note.select(me)

        self.unlock('new')

    def close(self, event = None):
        "Close the tab that is selected (showed)"
        # get the instance to have the widget totally forget
        selected = self.note.iselect()
        if selected:
            # remove the instance from the dict in the class
            selected.close()
            # remove the tab !
            self.note.forget(selected)

            # Check if there is still some tab, 
            # if no tabs here, lock some operations
            selected = self.note.select()
            if selected:
                return

        self.unlock('close')

    def reopen(self, event = None):
        "reopen the file that is selected by the frame"
        # get the instance of the frame
        me = self.note.iselect()

        # no frame (no file opened)
        if not me or me.fn is None:
            return

        org = Open(me.fn)

        if org is None:
            msgbox.showwarning('Error File Format', 'Your file is not in a right' \
                    ' format the can change into text, check if it can open corretly')
            return

        # set the frame's content and show it
        me.set(org)

    def decode(self, event = None):
        "Decode the content of the frame"
        self.note.iselect().decode()

    def encode(self, event = None):
        "Encode the content of the frame and show it"
        content = self.note.iselect().encode()
        TopShow(content)

    def save(self, event = None):
        me = self.note.iselect()

        # no frame (no file opened)
        if not me or me.fn is None:
            return self.saveas()

        with codecs.open(me.fn, 'w') as f:
            f.write(me.read())

    def saveas(self, event = None):
        fn = tkfd.asksaveasfilename(title = 'Save to The File', initialdir = os.getcwd())
        if not fn:
            return
        me = self.note.iselect()
        if me.fn is None:
            me.fn = fn
            self.note.add(me, opb(fn))
        with codecs.open(fn, 'w') as f:
            f.write(me.read())
        msgbox.showinfo('Success!', 'Succeed in Saving The content into FILE %s' % fn)

        self.unlock('saveas')

    def fontconfigure(self, e = None):
        top = FontConfigure(self.master, self)

        def changefont(family, size):
            self.font.config(family = family, size = size)
            top.quit()

        top.fonthandler(changefont)
        top.mainloop()

    def about(self, event = None):
        "Create a new windows to show the info of the 'Diary Coder'"
        top = tk.Toplevel()
        top.geometry(f'+{ self.master.winfo_x() }+{ self.master.winfo_y() }')
        top.columnconfigure(0, weight = 3)
        top.rowconfigure(0, weight = 2)
        tk.Label(top, image = self.img).grid(row = 0, column = 0)
        for i, text in enumerate(self._about):
            tk.Label(top, text = text).grid(row = i + 1, column = 0)

        top.resizable(0, 0)

    _about = ("Powered by PYTHON3 - Tkinter",
            "Author: Jeef Coroutine Fu from Chengdu, China",
            "report at jeefy163@163.com or jeefyol@outlook.com",
            "Thank you for using this!"
            )

    def details(self, event = None):
        __import__('webbrowser').open('https://jeefy.herukuapp.com/docs/chencode/diary-encoder')


class MainEditor(tk.Frame):
    _instance = {}
    _fns = {}
    mainmenu = None
    root = None

    def __new__(self, note, content, fn = 'new'):
        # Use the same instance of the file
        # The same filename create a same instance
        # if the filename is the same, 
        # __init__ method would not be called
        self.exists = False

        if fn in self._fns:
            self.exists = True
            return self._fns[fn]

        r = super().__new__(self)
        self._fns[fn] = r
        return r

    def __init__(self, note, content, fn = 'new'):
        "note is the master of each frame"
        if not self.exists:
            super().__init__(note)
            self.crt_items(content)
            self.fn = fn
            # use to get the instance by the frame name
            # just for classmethod - getinstance
            # it's used when note called iselect()
            self._instance[str(self)] = self
            self.binds()


    def crt_items(self, content):
        "Create all Items"
        self.content = content
        self.text = text = SText(self)
        text['font'] = self.mainmenu.font
        text.insert('1.0', content)
        # it left some space between the Notebook and the text widget
        # it also can use place for it
        #text.place(relwidth = 0.98, relheight = 0.98, relx = 0.01, rely = 0.01)
        text.pack(fill='both', expand='yes', padx=5, pady=5)

    def decode(self):
        "Decode the codes and rewrite the content into the result"
        org = main.decode(self.text.get('1.0', 'end').strip())
        """
        try:
            org = main.decode(self.text.get('1.0', 'end'))
        except main.DecodeError as e:
            msgbox.showwarning('Error Format', 'Not a Right format to decode %s' % e.args[1])
            print(e)
            return
        """
        # notice that org is a tuple (can not just insert into the Text widget)
        # so use a text simply change into a well-looked text
        text = ''
        for o in org:
            if len(o) == 1:
                text += o
            else:
                text += o + ' '
        text = text.strip()
        self.set(text)

    def encode(self):
        "return the encode result of the content (to show on a top level)"
        r = main.encode(self.text.get('1.0', 'end'))
        return r

    def set(self, content):
        "Set the content into the param content (delete all first)"
        self.text.delete('1.0', 'end')
        self.text.insert('1.0', content)

    def read(self):
        "Get all content in the text widget"
        return self.text.get('1.0', 'end')

    @property
    def changed(self):
        return self.content == self.read()

    def binds(self):
        "Bind all events"
        self.bind_all('<Control-A>', self.selectAll)
        self.bind_all('<Control-C>', self.copy)
        self.bind_all('<Control-V>', self.paste)
        self.bind_all('<Control-Q>', self.mainmenu.close)
        self.bind_all('<Control-S>', self.mainmenu.save)
        self.bind_all('<Control-E>', self.mainmenu.encode)
        self.bind_all('<Control-D>', self.mainmenu.decode)
        self.bind_all('<Control-Shift-S>', self.mainmenu.saveas)
        self.bind_all('<Control-a>', self.selectAll)
        self.bind_all('<Control-c>', self.copy)
        self.bind_all('<Control-v>', self.paste)
        self.bind_all('<Control-q>', self.mainmenu.close)
        self.bind_all('<Control-s>', self.mainmenu.save)
        self.bind_all('<Control-e>', self.mainmenu.encode)
        self.bind_all('<Control-d>', self.mainmenu.decode)
        self.bind_all('<Control-Shift-s>', self.mainmenu.saveas)

    def selectAll(self, event):
        "The Event call when pressed Ctrl-a (select all content)"
        self.text.tag_add('sel', '1.0', 'end')

    def copy(self, event):
        ("Put the Selected text into a clipboard\n"
        "If there's nothing selected, so do nothing")

        try:
            select = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(select)
        # update so taht can use for next time
        self.root.update()

    def paste(self, event):
        try:
            text = self.root.clipboard_get()
        except tk.TclError:
            return
        #self.text.insert('insert', text)
        try:
            self.text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass

    def close(self):
        ("Delete all instance saved in the dict, \nso it wouldn't "
                "return a forgotten widget instance to show again\n"
                "Avoid can not open a file again"
                )
        self._fns.pop(self.fn)
        self._instance.pop(str(self))

    @classmethod
    def getinstance(cls, name):
        "Return the instance by the frame's name (str(self) is the name)"
        return cls._instance.get(name)

class MainNote(ttk.Notebook):
    def __init__(self, root):
        super().__init__(root)
        # it's just a complex way to fill all the places
        # it would be better if use pack method
        #root.rowconfigure(0, weight = 3)
        #root.columnconfigure(0, minsize = root.winfo_screenheight(), weight = 3)
        #self.grid(row = 0, column = 0, sticky = tk.NSEW)
        self.pack(fill='both', expand='yes')

    def add(self, frame, text, **kwargs):
        if getattr(frame, 'exists', None):
            return
        super().add(frame, text = text)
        self.update()

    def iselect(self):
        "return the instance of the selected tab's frame"
        return MainEditor.getinstance(self.select())

def TopShow(content):
    ("Show it with the toplevel\n"
            "Use Ctrl-A to select all content\n"
            "Ctrl-C to copy all selected content into clipboard\n"
            "Ctrl-V to paste all copied content when in the editing windows\n"
            )
    top = tk.Toplevel()
    top.geometry('300x300')
    # it might be better to have a free size
    # this is just for avoiding changing the windows size
    # so that the widgets cannot change itself automatically
    #top.resizable(0,0)
    text = SText(top)
    text.insert('1.0', content)
    text['state'] = 'disabled'

    def copy(event):
        t = text.get(tk.SEL_FIRST, tk.SEL_LAST)
        root.clipboard_clear()
        root.clipboard_append(t)
        root.update()
    
    def selectAll(event):
        text.tag_add('sel', '1.0', 'end')

    # Bind Copy and SelectAll
    top.bind_all('<Control-a>', selectAll)
    top.bind_all('<Control-c>', copy)
    top.bind_all('<Control-A>', selectAll)
    top.bind_all('<Control-C>', copy)

    def saveinto():
        fn = tkfd.asksaveasfilename(initialdir = os.getcwd())
        if not fn:
            return
        with open(fn, 'w') as f:
            f.write(content)

        msgbox.showinfo('Success', 'Save into %s Succeed!' % fn)

    btn = tk.Button(top, text = 'Save', command = saveinto)
    btn.pack(side = tk.BOTTOM)
    text.pack(side = tk.TOP, fill = 'both', expand = 'yes')
    #top.mainloop()

def Open(filename):
    # open with bytes mode, so can use 
    # chardet.detect to detect the encoding of the file
    # use codecs to decode the content (bytes)
    with codecs.open(filename, 'rb') as f:
        org = f.read()

    encoding = chardet.detect(org)['encoding']
    if encoding is None:
        del org
        return None
    try:
        return codecs.decode(org, encoding)
    except Exception:
        del org
        return None

class FontConfigure(tk.Toplevel):
    def __init__(self, master, mainmenu):
        # the master is the root tk instance!
        super().__init__(master)

        self.fontfamilies = set(tkf.families(master))
        self.font = mainmenu.font.copy()

        self.family = self.dfn = self.font['family']
        self.size = self.font['size']
        self.fontfamilies.add(self.dfn)
        self.fontfamilies = sorted(self.fontfamilies)

        # size is width:500 height:400
        # place it in the center of the screen
        x = master.winfo_screenwidth() // 2 - 250
        y = master.winfo_screenheight() // 2 - 200
        self.geometry('500x400+{}+{}'.format(x, y))

        # set to not resizable so that the windows size won't change
        # if the font family changed (only work when set the size first)
        self.resizable(0,0)

        self.left()
        self.right()

    def left(self):
        # create left widgets

        # the main frame of the left
        frame = tk.Frame(self)
        # take the left place of the Toplevel
        frame.pack(fill = 'y', side = 'left')

        # apply button
        self.btn = tk.Button(frame, {tk.Pack: dict(side = 'bottom'), \
                'text': 'Apply', 'command': self.apply})

        # font size scale
        tk.Scale(frame, {tk.Pack: dict(side = 'bottom', fill='x', anchor='w'), \
                'from_':8, 'to':25, 'orient':'horizontal', \
                'tickinterval':2, 'command':self.cfontsize, \
                'label': 'Font Size'}).set(self.font['size'])

        # label for name
        tk.Label(frame, {tk.Pack: dict(side='top', anchor='w'), 'text': 'Font Families'})
        # fontboxframe
        fbf = tk.Frame(frame, {tk.Pack: dict(side='top', expand='yes', fill='both')} )

        sb = tk.Scrollbar(fbf)
        sb.pack(side='right', fill='y')

        self.libox = listbox = tk.Listbox(fbf, {tk.Pack: \
                dict(fill='both', expand='yes')}, bg='white', yscrollcommand=sb.set)
        sb.configure(command=listbox.yview)

        # insert all font falilies into the listbox
        for i, fml in enumerate(self.fontfamilies):
            listbox.insert(i, fml)

        # bind the event so the fontconfigure can knoew the changes of the font falilies
        listbox.bind('<ButtonRelease-1>', self.pfont)
        listbox.bind('<KeyRelease-Up>', self.pfont)
        listbox.bind('<KeyRelease-Down>', self.pfont)

        listbox.pack()

        # activate has no use to select the content
        i = self.fontfamilies.index(self.dfn)
        listbox.see(i)
        listbox.activate(i)
        listbox.focus_get()
        listbox.update()


    def pfont(self, event = None):
        # change the font falily of the text
        # it would automayically change if the font config change
        selected = self.libox.curselection()
        self.family = family = self.libox.get(selected[0])

        self.font.config(family = family)

    def right(self):
        # right widget
        # maybe it can be wrapped into a frame
        # but there's only a Text widget to Pack

        # font show frame
        #fontshowf = tk.Frame(self, {tk.Pack : dict(side = 'right', fill = 'y')} )
        text = tk.Text(self, font = self.font)
        text.insert('1.0', ascii_letters[:26] + '\n')
        text.insert('2.0', ascii_letters[26:] + '\n\n')
        text.insert('3.0', punctuation)
        text.pack(fill = 'both', expand = 'yes')

    def fonthandler(self, func):
        ("Save the font handler\nNotice that the func would"
                "be called with to arguments\n"
                "The first is the font family, "
                "the second is the font size"
                )
        self.fthdl = func

    def apply(self):
        "Call the fonthandler when click the Apply button\n" \
                "With The argument font_family and font_size"
        self.fthdl(self.family, self.size)
        self.destroy()

    def cfontsize(self, size):
        "The command to change the size of the font "\
                "when the Scale widget has changed it's number"
        self.size = self.font['size'] = size


def _main():
    # Init the root Tk windows
    root = tk.Tk()

    # set the windows into a fit size and put it in center of the screen
    wins = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('600x300+{}+{}'.format(wins[0] // 2 - 300, wins[1] // 2 - 150))

    root.title('Diary Coder')

    # init all widgets (parents)
    MainMenu(root).note = MainNote(root)

    # start the program
    root.mainloop()
