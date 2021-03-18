import main
import os
import time
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkfd
import tkinter.messagebox as msgbox


opb = os.path.basename

class MainMenu(tk.Menu):
    def __init__(self):
        super().__init__(root, bg='white', activebackground='red', bd=2)

        self.crt_items()
        root.config(menu = self)
        root.update()
        root.bind_all('<Control-o>', self.op)
        #self.pack()

    def crt_items(self):
        self.filemn = filemn = tk.Menu(self, tearoff=0, bg='white', activebackground='red', bd=2)
        ac = filemn.add_command
        ac(label = 'Open', command = self.op)
        ac(label = "New", command = self.new)
        filemn.add_separator()
        ac(label = 'Save', command = self.save, state = 'disabled')
        ac(label = 'Reopen', command = self.reo, state = 'disabled')
        filemn.add_separator()
        ac(label = 'Close', command = self.close, state = 'disabled')
        ac(label = 'Exit', command = self.master.destroy)

        self.operationmn = operations = tk.Menu(self, tearoff=0, bg= 'white', activebackground = 'red', bd=2)
        ac = operations.add_command
        ac(label = 'Decode', command = self.de, state = 'disabled')
        ac(label = 'Encode', command = self.en, state = 'disabled')

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
        with open(fn,'r') as f:
            org = f.read()
        me = MainEditor(org, fn = fn)
        note.add(me, opb(fn))
        note.select(me)
        self.filemn.entryconfigure(3, state = 'normal')
        self.filemn.entryconfigure(4, state = 'normal')
        self.filemn.entryconfigure(6, state = 'normal')
        self.operationmn.entryconfigure(0, state = 'normal')
        self.operationmn.entryconfigure(1, state = 'normal')

    def new(self):
        me = MainEditor('', fn = None)
        note.add(me, 'new')
        note.select(me)
        self.filemn.entryconfigure(3, state = 'normal')
        self.filemn.entryconfigure(6, state = 'normal')
        self.operationmn.entryconfigure(0, state = 'normal')
        self.operationmn.entryconfigure(1, state = 'normal')

    def close(self):
        selected = note.select()
        if selected:
            note.forget(selected)
            selected = note.select()
            if selected:
                return
        self.filemn.entryconfigure(3, state = 'disabled')
        self.filemn.entryconfigure(4, state = 'disabled')
        self.filemn.entryconfigure(6, state = 'disabled')
        self.operationmn.entryconfigure(0, state = 'disabled')
        self.operationmn.entryconfigure(1, state = 'disabled')

    def reo(self):
        me = note.iselect()
        if not me:
            return
        with open(me.fn, 'r') as f:
            org = f.read()

    def de(self):
        note.iselect().decode()

    def en(self):
        content = note.iselect().encode()
        TopShow(content)

    def save(self):
        fn = tkfd.asksaveasfilename(title = 'Save to The File', initialdir = os.getcwd())
        me = note.iselect()
        if me.fn is None:
            me.fn = fn
            note.add(me, opb(fn))
        with open(fn, 'w') as f:
            f.write(me.read())
        msgbox.showinfo('Success!', 'Succeed in Saving The content into FILE %s' % fn)

    def usage(self):
        pass

    def details(self):
        pass


class MainEditor(tk.Frame):
    _instance = {}

    def __init__(self, content, fn = 'new'):
        super().__init__(note)
        self.crt_items(content)
        self.fn = fn
        self._instance[str(self)] = self


    def crt_items(self, content):
        self.text = text = tk.Text(self)
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

        self.text.delete('1.0', 'end')
        self.text.insert('1.0', text)

    def encode(self):
        r = main.encode(self.text.get('1.0', 'end'))
        return r

    def read(self):
        return self.text.get('1.0', 'end')

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
    text = tk.Text(top)
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


root = tk.Tk()
root.title()
root.geometry('600x300')
mainmenu = MainMenu()
note = MainNote()
root.mainloop()
