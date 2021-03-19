from . import main
import os
import time
import codecs
import chardet
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkfd
import tkinter.messagebox as msgbox
from tkinter.scrolledtext import ScrolledText as SText


opb = os.path.basename

class MainMenu(tk.Menu):
    def __init__(self):
        super().__init__(root, bg='white', activebackground='red', bd=2)

        self.crt_items()
        root.config(menu = self)
        root.update()
        root.bind_all('<Control-o>', self.op)
        root.bind_all('<Control-O>', self.op)
        root.bind_all('<Control-n>', self.new)
        root.bind_all('<Control-N>', self.new)
        root.bind_all('<Control-Shift-Q>', lambda e: self.master.destroy())
        root.bind_all('<Control-Shift-q>', lambda e: self.master.destroy())

    def crt_items(self):
        self.filemn = filemn = tk.Menu(self, tearoff=0, bg='white', activebackground='red', bd=2)
        ac = filemn.add_command
        ac(label = 'Open', command = self.op, accelerator = 'Ctrl+o')
        ac(label = "New", command = self.new, accelerator = 'Ctrl+n')
        filemn.add_separator()
        ac(label = 'Save', command = self.save, state = 'disabled', accelerator = 'Ctrl+s')
        ac(label = 'Save As', command = self.saveas, state = 'disabled', accelerator = 'Ctrl+Shift+s')
        ac(label = 'Reopen', command = self.reo, state = 'disabled', accelerator = 'Ctrl+r')
        filemn.add_separator()
        ac(label = 'Close', command = self.close, state = 'disabled', accelerator = 'Ctrl+q')
        ac(label = 'Exit', command = self.master.destroy, accelerator = 'Ctrl+Shift+q')

        self.operationmn = operations = tk.Menu(self, tearoff=0, bg= 'white', activebackground = 'red', bd=2)
        ac = operations.add_command
        ac(label = 'Decode', command = self.de, state = 'disabled', accelerator = 'Ctrl+d')
        ac(label = 'Encode', command = self.en, state = 'disabled', accelerator = 'Ctrl+e')

        helpmn = tk.Menu(self, tearoff = 0, bg='white', activebackground='red', bd=2)
        ac = helpmn.add_command
        ac(label = 'Usage', command = self.usage)
        ac(label = 'Details', command = self.details)

        self.add_cascade(label = 'File', menu = filemn)
        self.add_separator()
        self.add_cascade(label = 'Openrations', menu = operations)
        self.add_separator()
        self.add_cascade(label = 'Help', menu = helpmn)

    def op(self, event = None):
        self._latest_fn = fn = tkfd.askopenfilename(title = 'Open The File', initialdir = os.getcwd())
        if not fn:
            msgbox.showwarning("No File Chosen!", "You cancled to choose a file!")
            return
        with codecs.open(fn,'rb') as f:
            org = f.read()
        encoding = chardet.detect(org)['encoding']
        org = codecs.decode(org, encoding)
        me = MainEditor(org, fn = fn)
        note.add(me, opb(fn))
        note.select(me)
        self.filemn.entryconfigure(3, state = 'normal')
        self.filemn.entryconfigure(4, state = 'normal')
        self.filemn.entryconfigure(5, state = 'normal')
        self.filemn.entryconfigure(7, state = 'normal')
        self.operationmn.entryconfigure(0, state = 'normal')
        self.operationmn.entryconfigure(1, state = 'normal')

    def new(self, event = None):
        me = MainEditor('', fn = None)
        note.add(me, 'new')
        note.select(me)
        self.filemn.entryconfigure(3, state = 'normal')
        self.filemn.entryconfigure(5, state = 'normal')
        self.filemn.entryconfigure(7, state = 'normal')
        self.operationmn.entryconfigure(0, state = 'normal')
        self.operationmn.entryconfigure(1, state = 'normal')

    def close(self, event = None):
        selected = note.select()
        if selected:
            note.forget(selected)
            selected = note.select()
            if selected:
                return
        self.filemn.entryconfigure(3, state = 'disabled')
        self.filemn.entryconfigure(4, state = 'disabled')
        self.filemn.entryconfigure(5, state = 'disabled')
        self.filemn.entryconfigure(7, state = 'disabled')
        self.operationmn.entryconfigure(0, state = 'disabled')
        self.operationmn.entryconfigure(1, state = 'disabled')

    def reo(self, event = None):
        me = note.iselect()
        if not me:
            return
        with codecs.open(me.fn,'rb') as f:
            org = f.read()
        encoding = chardet.detect(org)['encoding']
        org = codecs.decode(org, encoding)
        me.set(org)

    def de(self, event = None):
        note.iselect().decode()

    def en(self, event = None):
        content = note.iselect().encode()
        TopShow(content)

    def save(self, event = None):
        me = note.iselect()
        if me.fn is None:
            self.saveas()
        with codecs.open(me.fn, 'w') as f:
            f.write(me.read())


    def saveas(self, event = None):
        fn = tkfd.asksaveasfilename(title = 'Save to The File', initialdir = os.getcwd())
        if not fn:
            return msgbox.showwarning('No File chosen', 'You Cancled to save the CONTENT!')
        me = note.iselect()
        if me.fn is None:
            me.fn = fn
            note.add(me, opb(fn))
        with codecs.open(fn, 'w') as f:
            f.write(me.read())
        msgbox.showinfo('Success!', 'Succeed in Saving The content into FILE %s' % fn)

    def usage(self):
        pass

    def details(self):
        pass


class MainEditor(tk.Frame):
    _instance = {}
    _fns = {}

    def __new__(self, content, fn = 'new'):
        self.exists = False
        if fn in self._fns:
            self.exists = True
            return self._fns[fn]
        r = super().__new__(self)
        self._fns[fn] = r
        return r

    def __init__(self, content, fn = 'new'):
        if not self.exists:
            super().__init__(note)
            self.crt_items(content)
            self.fn = fn
            self._instance[str(self)] = self
            self.binds()


    def crt_items(self, content):
        self.content = content
        self.text = text = SText(self)
        text.insert('1.0', content)
        text.place(relwidth = 0.98, relheight = 0.98, relx = 0.01, rely = 0.01)

    def decode(self):
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
        r = main.encode(self.text.get('1.0', 'end'))
        return r

    def set(self, content):
        self.text.delete('1.0', 'end')
        self.text.insert('1.0', content)

    def read(self):
        return self.text.get('1.0', 'end')

    @property
    def changed(self):
        return self.content == self.read()

    def binds(self):
        self.bind_all('<Control-A>', self.selectAll)
        self.bind_all('<Control-C>', self.copy)
        self.bind_all('<Control-V>', self.paste)
        self.bind_all('<Control-Q>', mainmenu.close)
        self.bind_all('<Control-S>', mainmenu.save)
        self.bind_all('<Control-E>', mainmenu.en)
        self.bind_all('<Control-D>', mainmenu.de)
        self.bind_all('<Control-Shift-S>', mainmenu.saveas)
        self.bind_all('<Control-a>', self.selectAll)
        self.bind_all('<Control-c>', self.copy)
        self.bind_all('<Control-v>', self.paste)
        self.bind_all('<Control-q>', mainmenu.close)
        self.bind_all('<Control-s>', mainmenu.save)
        self.bind_all('<Control-e>', mainmenu.en)
        self.bind_all('<Control-d>', mainmenu.de)
        self.bind_all('<Control-Shift-s>', mainmenu.saveas)

    def selectAll(self, event):
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

    @classmethod
    def getinstance(cls, name):
        return cls._instance.get(name)

class MainNote(ttk.Notebook):
    def __init__(self):
        super().__init__(root)
        root.rowconfigure(0, weight = 3)
        root.columnconfigure(0, minsize = root.winfo_screenheight(), weight = 3)
        self.grid(row = 0, column = 0, sticky = tk.NSEW)
        self.cid = 0

    def add(self, frame, text, **kwargs):
        if getattr(frame, 'exists', None):
            print('exists')
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


def _main():
    global root, mainmenu, note
    root = tk.Tk()
    wins = root.winfo_screenwidth(), root.winfo_screenheight()
    root.title('Diary Coder')
    root.geometry('600x300+{}+{}'.format(wins[0] // 2 - 300, wins[1] // 2 - 150))
    mainmenu = MainMenu()
    note = MainNote()
    root.mainloop()
