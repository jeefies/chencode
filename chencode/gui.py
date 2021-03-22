import os
import codecs
import chardet
import hashlib
import tkinter as tk
import tkinter.filedialog as tkfd
import tkinter.messagebox as msgbox
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText as SText
from PIL import Image, ImageTk

from . import encode, decode, DecodeError

class MainMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master, bg = 'white', activebackground = 'red')
        self.crt_items()
        self.binds()
        master.config(menu = self)

    def crt_items(self):
        filemn = tk.Menu(self, tearoff = 0, bg = 'white', activebackground = 'red')
        filemn.add_command(label = 'Open', command = self.open, accelerator = 'Ctrl+o')
        filemn.add_command(label = 'New', command = self.new, accelerator = 'Ctrl+n')
        filemn.add_separator()
        filemn.add_command(label = 'Save', command = self.save, accelerator = 'Ctrl+s')
        filemn.add_command(label = 'Save As', command = self.saveas, accelerator = 'Ctrl+Shift+s')
        filemn.add_separator()
        filemn.add_command(label = 'Close', command = self.close, accelerator = 'Ctrl+q')
        filemn.add_command(label = 'Reopen', command = self.reopen, accelerator = 'Ctrl+r')
        filemn.add_separator()
        filemn.add_command(label = 'Quit', command = self.master.quit, accelerator = 'Ctrl+Shift+q')
        self.add_cascade(label = 'File', menu = filemn)

        opemn = tk.Menu(self, tearoff = 0, bg = 'white', activebackground = 'red')
        opemn.add_command(label = 'Encode', command = self.encode, accelerator = 'Ctrl+e')
        opemn.add_command(label = 'Decode', command = self.decode, accelerator = 'Ctrl+d')
        self.add_cascade(label = 'Operations', menu = opemn)

    def binds(self):
        self.master.bind_all("<Control-o>", self.open)
        self.master.bind_all("<Control-O>", self.open)
        self.master.bind_all("<Control-s>", self.save)
        self.master.bind_all("<Control-S>", self.save)
        self.master.bind_all("<Control-Shift-s>", self.saveas)
        self.master.bind_all("<Control-Shift-S>", self.saveas)
        self.master.bind_all("<Control-q>", self.close)
        self.master.bind_all("<Control-Q>", self.close)
        self.master.bind_all("<Control-r>", self.reopen)
        self.master.bind_all("<Control-R>", self.reopen)
        self.master.bind_all("<Control-Shift-r>", self.master.quit)
        self.master.bind_all("<Control-Shift-R>", self.master.quit)
        self.master.bind_all("<Control-e>", self.encode)
        self.master.bind_all("<Control-E>", self.encode)
        self.master.bind_all("<Control-d>", self.decode)
        self.master.bind_all("<Control-D>", self.decode)
        self.master.bind_all("<Control-Shift-q>", lambda e: self.master.quit())
        self.master.bind_all("<Control-Shift-Q>", lambda e: self.master.quit())
        self.master.bind_all("<Control-n>", self.new)
        self.master.bind_all("<Control-N>", self.new)

    def open(self, event = None):
        fn = tkfd.askopenfilename(initialdir = os.getcwd())
        if not fn:
            return
        content = Open(fn)
        if content is None:
            msgbox.showwarning('Type Error', 'Your File Format is not right for edit!')
            return
        me = MainEditor(self.note, content, fn)
        self.note.add(me, os.path.basename(fn))
        self.note.select(me)

    def new(self, event = None):
        me = MainEditor(self.note, '', None)
        self.note.add(me, 'new')
        self.note.select(me)

    def save(self, event = None):
        me = self.note.iselect()
        if me.fn is None:
            self.saveas()
        with codecs.open(me.fn, 'w') as f:
            f.write(me.read())
        msgbox.showinfo("Success!", "Succeeded in Saving The content into %s" % me.fn)

    def saveas(self, event = None):
        fn = tkfd.asksaveasfilename(initialdir = os.getcwd())
        if not fn:
            return
        me = self.note.iselect()
        if me.fn is None:
            me.fn = fn
            me._fn[fn] = me
            self.note.add(me, os.path.basename(fn))
        with codecs.open(fn, 'w') as f:
            f.write(me.read())

    def close(self, event = None):
        me = self.note.iselect()
        if me.changed:
            print('changed')
            r = msgbox.askyesnocancel('Save The changed',\
                    'You have changed the file content, need save?')
            if r:
                self.save()
            if r is None:
                return
        me.close()
        self.note.forget(me)

    def reopen(self, event = None):
        me = self.note.iselect()
        with codecs.open(me.fn, 'w') as f:
            me.set(f.read())

    def encode(self, event = None):
        content = self.note.iselect().encode()
        Topshow(content)

    def decode(self, event = None):
        self.note.iselect().decode()

class MainNote(ttk.Notebook):
    def __init__(self, master):
        ttk.Style().configure('MainNote.TNotebook', background = 'white')
        super().__init__(master, style = 'MainNote.TNotebook')
        self.pack(fill = 'both', expand = 'yes')

    def add(self, frame, text, **kwargs):
        if getattr(frame, 'exists', None):
            print('exists')
            return
        super().add(frame, text = text, **kwargs)
        self.update()

    def iselect(self):
        return MainEditor.getinstance(self.select())

class MainEditor(tk.Frame):
    _instance = {}
    _fn = {}

    def __new__(self, master, content, fn = None):
        self.exists = False
        if fn is None:
            return super().__new__(self)
        if fn in self._fn:
            self.exists = True
            return self._fn[fn]
        r = super().__new__(self)
        self._fn[fn] = r
        return r

    def __init__(self, master, content, fn):
        if not self.exists:
            super().__init__(master)
            self.md5 = hashlib.md5(codecs.encode(content)).hexdigest()
            self.crt_items(content)
            self.fn = fn

        self._instance[str(self)] = self

    def crt_items(self, content):
        self.text = text = SText(self)
        text.pack(fill = 'both', expand = 'yes')
        text.insert('1.0', content)
        text.update()
        self.update()

    def close(self):
        self._fn.pop(self.fn)
        self._instance.pop(str(self))

    def encode(self):
        return encode(self.read())

    def decode(self):
        try:
            r = decode(self.read())
        except DecodeError as e:
            msgbox.showwarning('Decode Error', 'Error code at %s' % e.args[1])
            return
        text = ''
        for i in r:
            text += i
            if len(i) != 1:
                text += ' '
        self.set(text)

    @classmethod
    def getinstance(cls, text):
        return cls._instance.get(text)

    def read(self):
        return self.text.get('1.0', 'end')

    def set(self, text):
        self.text.delete('1.0', 'end')
        self.text.insert('1.0', text)

    @property
    def changed(self):
        return hashlib.md5(codecs.encode(self.read()))\
                .hexdigest() == self.md5
        #r = hashlib.md5(codecs.encode(self.read()))\.hexdigest()
        #print(r)
        #return r

def Open(filename):
    with codecs.open(filename, 'rb') as f:
        content = f.read()

    encoding = chardet.detect(content)['encoding']
    if encoding is None:
        return None
    return codecs.decode(content, encoding)

def Topshow(content):
    top = tk.Toplevel()

    def save(e = None):
        fn = tkfd.asksaveasfilename(initialdir = os.getcwd())
        if not fn:
            return
        with codecs.open(fn, 'w') as f:
            f.write(content)
        msgbox.showinfo('Success!', 'Succeed in saving to file %s' % os.path.basename(fn))


    text = SText(top)
    text.insert('1.0', content)

    text.pack(side = 'top', fill = 'both', expand = 'yes')

    tk.Button(top, text = 'Save', command = save).pack(side = 'bottom', anchor = 'w')

    top.update()


def _main():
    root = tk.Tk()

    root.title('Diary Coder')
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry('600x300+%s+%s' % (w // 2 - 300, h // 2 - 150))

    mainmenu = MainMenu(root)
    mainnote = MainNote(root)
    mainmenu.note = mainnote

    root.mainloop()
