import os
#import time
import codecs
import chardet
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
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
        root.bind_all('<Control-Shift-a>', self.about)
        root.bind_all('<Control-Shift-A>', self.about)
        root.bind_all('<Control-N>', self.new)
        root.bind_all('<Control-Shift-Q>', lambda e: self.master.destroy())
        root.bind_all('<Control-Shift-q>', lambda e: self.master.destroy())

        # init the image show
        self.img = ImageTk.PhotoImage(Image.open(imgpath).resize((128, 128)))

        # change the icon image (False means not use default)
        root.iconphoto(False, self.img)

        # show the menu widget
        root.config(menu = self)

        MainEditor.mainmenu = self

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

        # Help Menu
        # About Details
        helpmn = tk.Menu(self, tearoff = 0, bg='white', activebackground='red', bd=2)
        ac = helpmn.add_command
        ac(label = 'About', command = self.about, accelerator = "Ctrl+Shift+a")
        ac(label = 'Details', command = self.details, accelerator = "Ctrl+h")

        # add all Menu in
        self.add_cascade(label = 'File', menu = filemn)
        self.add_cascade(label = 'Openrations', menu = operations)
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

        # unlock the operations
        self.filemn.entryconfigure(3, state = 'normal') # Save
        self.filemn.entryconfigure(4, state = 'normal') # Save As
        self.filemn.entryconfigure(5, state = 'normal') # Reopen
        self.filemn.entryconfigure(7, state = 'normal') # Close
        self.operationmn.entryconfigure(0, state = 'normal') # Decode
        self.operationmn.entryconfigure(1, state = 'normal') # Encode

    def new(self, event = None):
        me = MainEditor(self.note, '', fn = None)
        self.note.add(me, 'new')
        self.note.select(me)
        self.filemn.entryconfigure(3, state = 'normal')
        self.filemn.entryconfigure(5, state = 'normal')
        self.filemn.entryconfigure(7, state = 'normal')
        self.operationmn.entryconfigure(0, state = 'normal')
        self.operationmn.entryconfigure(1, state = 'normal')

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

        # disable all the not needed menu operations
        # so user's won't do some meaningless things
        self.filemn.entryconfigure(3, state = 'disabled')
        self.filemn.entryconfigure(4, state = 'disabled')
        self.filemn.entryconfigure(5, state = 'disabled')
        self.filemn.entryconfigure(7, state = 'disabled')
        self.operationmn.entryconfigure(0, state = 'disabled')
        self.operationmn.entryconfigure(1, state = 'disabled')

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
        self.note.iselect().decode()

    def encode(self, event = None):
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

    def about(self, event = None):
        top = tk.Toplevel()
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

    def __new__(self, note, content, fn = 'new'):
        self.exists = False
        if fn in self._fns:
            self.exists = True
            return self._fns[fn]
        r = super().__new__(self)
        self._fns[fn] = r
        return r

    def __init__(self, note, content, fn = 'new'):
        if not self.exists:
            super().__init__(note)
            self.crt_items(content)
            self.fn = fn
            self._instance[str(self)] = self
            self.binds()


    def crt_items(self, content):
        "Create all Items"
        self.content = content
        self.text = text = SText(self)
        text.insert('1.0', content)
        text.place(relwidth = 0.98, relheight = 0.98, relx = 0.01, rely = 0.01)

    def decode(self):
        "Decode the codes and rewrite the content into the result"
        try:
            org = main.decode(self.text.get('1.0', 'end'))
        except:
            msgbox.showwarning('Error Format', 'Not a Right format to decode')
            return
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
        try:
            select = self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            return
        root.clipboard_clear()
        root.clipboard_append(select)
        root.update()

    def paste(self, event):
        text = root.clipboard_get()
        #self.text.insert('insert', text)
        try:
            self.text.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            pass

    def close(self):
        self._fns.pop(self.fn)
        self._instance.pop(str(self))

    @classmethod
    def getinstance(cls, name):
        return cls._instance.get(name)

class MainNote(ttk.Notebook):
    def __init__(self, root):
        super().__init__(root)
        root.rowconfigure(0, weight = 3)
        root.columnconfigure(0, minsize = root.winfo_screenheight(), weight = 3)
        self.grid(row = 0, column = 0, sticky = tk.NSEW)
        self.cid = 0

    def add(self, frame, text, **kwargs):
        if getattr(frame, 'exists', None):
            return
        super().add(frame, text = text)
        self.update()
        cid = self.cid
        self.cid -= 1
        return cid

    def iselect(self):
        return MainEditor.getinstance(self.select())

def TopShow(content):
    top = tk.Toplevel()
    top.geometry('300x300')
    top.resizable(0,0)
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
    btn.pack(side = tk.BOTTOM, fill = 'y')
    text.pack(side = tk.TOP)
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
