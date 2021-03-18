from tkinter import *
from tkinter import messagebox as box



def main_menu():
    window = Tk()
    window.title('Juke Box')
    window.geometry('800x480')
    window.configure(background = 'black')

    label = Label(window, text = 'Juke-Box', fg = 'light green', bg = 'black', font = (None, 30), height = 2)
    label.pack(side = TOP)

    Jam = Button(window, text = 'The Jam', width = 25, height = 2)
    Jam.pack(pady = 10, padx = 25, anchor = 'n')

    Roses = Button(window, text = 'The Stone Roses', width = 25, height = 2)
    Roses.pack(pady = 10, padx = 25, anchor = 'w')

    Smiths = Button(window, text = 'The Smiths', width = 25, height = 2)
    Smiths.pack(pady = 10, padx = 25, anchor = 'w')

    Wedding = Button(window, text = 'The Wedding Pressent', width = 25, height = 2)
    Wedding.pack(pady = 10, padx = 25, anchor = 'w')

    Blondie = Button(window, text = 'Blondie', width = 25, height = 2)
    Blondie.pack(pady = 10, padx = 25, anchor = 'w')

    Clash = Button(window, text = 'Clash', width = 25, height = 2)
    Clash.pack(pady = 10, padx = 25, anchor = 'w')

    Madness = Button(window, text = 'Madness', width = 25, height = 2)
    Madness.pack(pady = 10, padx = 25, anchor = 'n')

    Pistols = Button(window, text = 'The Sex Pistols', width = 25, height = 2)
    Pistols.pack(pady = 10, padx = 25, anchor = 'n')

    window.mainloop()



main_menu()