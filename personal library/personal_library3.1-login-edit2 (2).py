from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (
         bytes, dict, int, list, object, range, str,
         ascii, chr, hex, input, next, oct, open,
         pow, round, super,
         filter, map, zip)
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import requests
import ast
import pickle
from PIL import Image, ImageTk

def main2():
    watchedlist = []
    to_watchlist = []
    watched_movie_b = []
    remove_watched_movie_b = []
    to_watch_movie_b = []
    add_to_watchedlist_b = []
    remove_to_watch_movie_b = []

    if os.path.isfile('watchlist') and os.path.getsize('watchlist')>0:
        with open('watchlist','rb') as r:
            to_watchlist = pickle.load(r)
        while '-' in to_watchlist:
            for i in to_watchlist:
                if i == '-':
                    to_watchlist.remove(i)
        
    if os.path.isfile('watched') and os.path.getsize('watched'):
        with open('watched','rb') as r:
            watchedlist = pickle.load(r)
        while '-' in watchedlist:
            for i in watchedlist:
                if i == '-':
                    watchedlist.remove(i)

    class Master(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)
            self.title('Personal movie library')
            self.geometry("1920x1080+0+0")
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
            self.protocol("WM_DELETE_WINDOW", self.on_closing)
            masterframe = tk.Frame(self)
            masterframe.grid(column=0, row=0, sticky = "nsew")
            masterframe.grid_rowconfigure(0, weight=1)
            masterframe.grid_columnconfigure(0, weight=1)
            sw = ScrolledWindow(masterframe)
            self.frames = {}
            for F in (MainMenu, SearchBox, WatchedList, ToWatchList):
                ttk.Style(master=self).configure("TButton", font="Times 30",relief='raised', foreground="black", background="black")
                ttk.Style(master=self).configure("TLabelframe.Label", font="Times 30 bold")
                ttk.Style(master=self).configure("TLabel", font="Times 25")
                frame = F(sw.scrollwindow, self)
                self.frames[F] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame(MainMenu)

        def show_frame(self, cont):
            frame = self.frames[cont]
            frame.tkraise()

        def on_closing(self):
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.destroy()


    class MainMenu(ttk.LabelFrame):

        def __init__(self, parent, masterframe):
            ttk.LabelFrame.__init__(self, parent, text="MAIN MENU", labelanchor='n')
            self.grid_columnconfigure(0, weight=1, minsize=1920)
            for x in range(14):
                self.grid_rowconfigure(x, weight=1)

            with open(creds) as f:
                data = f.readlines()
                uname = data[0].rstrip()
            welcome_label = ttk.Label(self, text='Welcome {}!'.format(uname))
            welcome_label.grid(row=0, sticky = 'n')

            new_movie = ttk.Button(self, text='Search new movie', command=lambda: masterframe.show_frame(SearchBox))
            new_movie.grid(row=1, sticky = 'n')

            watchedlist_b = ttk.Button(self, text='Show watched list', command=lambda: masterframe.show_frame(WatchedList))
            watchedlist_b.grid(row=2, sticky = 'n')

            to_watchlist_b = ttk.Button(self, text='Show to watch list', command=lambda: masterframe.show_frame(ToWatchList))
            to_watchlist_b.grid(row=3, sticky = 'n')

            xit = ttk.Button(self, text='Exit', command=exit)
            xit.grid(row=4, sticky = 'n')

    class SearchBox(ttk.LabelFrame):

        def __init__(self, parent, masterframe):
            ttk.LabelFrame.__init__(self, parent, text="Find new movie", labelanchor='n')
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=0)
            self.grid_rowconfigure(1, weight=1)
            self.grid_rowconfigure(2, weight=1)
            self.grid_rowconfigure(3, weight=1)
            entry = tk.Entry(self, font='Arial 20', width=20)
            entry.grid(row=0, sticky='n')
            entry.config(relief='solid')
            button = ttk.Button(self,  text='Search', command=lambda: ShowInfo(parent, entry.get(), masterframe) and entry.delete(0,'end'))
            button.grid(row=1, sticky='n')
            back_buttonImage = Image.open('back.png')
            self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
            back_to_main = ttk.Button(self,  text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT, command=lambda: masterframe.show_frame(MainMenu))
            back_to_main.grid(row=2, sticky='n')

        def reset(self):
            app.destroy()
            main2()
            
    class WatchedList(ttk.LabelFrame):
        def __init__(self, parent, masterframe):
            ttk.LabelFrame.__init__(self, parent, text="Watched movies")
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            if len(watchedlist) != 0:
                self.grid_columnconfigure(10, minsize=900)
                self.grid_rowconfigure(len(watchedlist)+1, minsize=880)
                for x in range(len(watchedlist)):
                    self.grid_rowconfigure(x, weight=1)
                for x in range(len(watchedlist)):
                    watched_movie_b.append(ttk.Button(self, text='{}'.format(watchedlist[x]), command=lambda b=x: ShowInfo(parent, watchedlist[b], masterframe)))
                    watched_movie_b[x].grid(row=x, column=0, sticky='w', columnspan=10)
                    remove_watched_movie_b.append(ttk.Button(self, text='Remove', command=lambda b=x: self.remove_movie(b)))
                    remove_watched_movie_b[x].grid(row=x, column=10, sticky='w')
                back_buttonImage = Image.open('back.png')
                self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
                back_to_main = ttk.Button(self, text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT, command=self.reset)
                back_to_main.grid(row=len(watchedlist)+1, column=0, sticky='n')
            else:
                self.grid_columnconfigure(0, minsize=900)
                self.grid_rowconfigure(1, minsize=880)
                no_movies = ttk.Label(self, text='No movies in watched list', font='Arial 30', anchor=tk.W)
                no_movies.grid(row=0, column=0)
                back_buttonImage = Image.open('back.png')
                self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
                back_to_main = ttk.Button(self, text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT, command=self.reset)
                back_to_main.grid(row=1, column=0, sticky='n')
                
        def remove_movie(self,x):
            watchedlist[x] = '-'
            with open('watched', 'wb') as w:
                pickle.dump(watchedlist, w)
            watched_movie_b[x].grid_forget()
            remove_watched_movie_b[x].grid_forget()

        def reset(self):
            app.destroy()
            main2()

    class ToWatchList(ttk.LabelFrame):

        def __init__(self, parent, masterframe):
            ttk.LabelFrame.__init__(self, parent, text="Watchlist")
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            if len(to_watchlist) != 0:
                self.grid_columnconfigure(11, minsize=900)
                self.grid_rowconfigure(len(to_watchlist)+1, minsize=880)
                self.grid_columnconfigure(0, weight=1)
                for x in range(len(to_watchlist)):
                    self.grid_rowconfigure(x, weight=1)            
                for x in range(len(to_watchlist)):
                    to_watch_movie_b.append(ttk.Button(self, text='{}'.format(to_watchlist[x]), command=lambda b=x: ShowInfo(parent, to_watchlist[b], masterframe)))
                    to_watch_movie_b[x].grid(row=x, column=0, sticky='w', columnspan=10)
                    add_to_watchedlist_b.append(ttk.Button(self, text='Add to watched list', command=lambda b=x: self.add_to_watched(b)))
                    add_to_watchedlist_b[x].grid(row=x, column=10, sticky='w')
                    remove_to_watch_movie_b.append(ttk.Button(self, text='Remove', command=lambda b=x: self.remove_movie_from_watchlist(b)))
                    remove_to_watch_movie_b[x].grid(row=x, column=11, sticky='w')
                back_buttonImage = Image.open('back.png')
                self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
                back_to_main = ttk.Button(self, text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT, command=self.reset)
                back_to_main.grid(row=len(to_watchlist)+1, column=0, sticky='n')
            else:
                self.grid_columnconfigure(0, minsize=900)
                self.grid_rowconfigure(1, minsize=880)
                no_movies = ttk.Label(self, text='No movies in watchlist', font='Arial 30', anchor=tk.W)
                no_movies.grid(row=0, column=0)
                back_buttonImage = Image.open('back.png')
                self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
                back_to_main = ttk.Button(self, text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT, command=self.reset)
                back_to_main.grid(row=1, column=0, sticky='n')

        def add_to_watched(self,x):
            watchedlist.append(to_watchlist[x])
            to_watchlist[x] = '-'
            self.remove_movie_from_watchlist(x)
            with open('watched', 'wb') as w:
                pickle.dump(watchedlist, w)
            to_watch_movie_b[x].grid_forget()
            add_to_watchedlist_b[x].grid_forget()
            remove_to_watch_movie_b[x].grid_forget()
                
        def remove_movie_from_watchlist(self, x):
            to_watchlist[x] = '-'
            with open('watchlist', 'wb') as w:
                pickle.dump(to_watchlist, w)
            to_watch_movie_b[x].grid_forget()
            add_to_watchedlist_b[x].grid_forget()
            remove_to_watch_movie_b[x].grid_forget()

        def reset(self):
            app.destroy()
            main2()

    class ShowInfo(ttk.LabelFrame):

        def __init__(self, parent, name, masterframe):
            ttk.LabelFrame.__init__(self, parent, text="Movie info", labelanchor='n')
            self.grid(row=0, column=0, sticky="nsew")
            self.tkraise()
            for x in range(30):
                self.grid_rowconfigure(x, weight=1)
            self.tkraise()

            title = name
            try:
                res = requests.get('http://www.omdbapi.com/?t='+title+'&apikey=6a32ca26')
                d = res.text
                details = ast.literal_eval(d)
                t = details['Title']
                y = details['Year']
                rt = details['Runtime']
                gen = details['Genre']
                direct = details['Director']
                write = details['Writer']
                act = details['Actors']
                pl = details['Plot']
                rate = self.allratings(details['Ratings'])
                self.m1 = Movie(t, y, rt, gen, direct, write, act, pl, rate)
                movie_name = self.m1.title
                year = self.m1.year
                runtime = self.m1.runtime
                genre = self.m1.genre
                director = self.m1.director
                writers = self.m1.writers
                actors = self.m1.actors
                plot = self.m1.plot
                rating = self.m1.ratings
                label1 = ttk.Label(self, text='Title:', font='Times 30 bold')
                label1.grid(row=0, column=0, sticky='w')
                title = ttk.Label(self, text='{}'.format(movie_name))
                title.grid(row=0,column=1, sticky='w')
                label2 = ttk.Label(self, text='Year:', font='Times 30 bold')
                label2.grid(row=1, column=0, sticky='w')
                year = ttk.Label(self, text='{}'.format(year))
                year.grid(row=1,column=1, sticky='w')
                label3 = ttk.Label(self, text='Runtime:', font='Times 30 bold')
                label3.grid(row=2, column=0, sticky='w')
                runtime = ttk.Label(self, text='{}'.format(runtime))
                runtime.grid(row=2,column=1, sticky='w')
                label4 = ttk.Label(self, text='Genre:', font='Times 30 bold')
                label4.grid(row=3, column=0, sticky='w')
                genre = ttk.Label(self, text='{}'.format(genre))
                genre.grid(row=3,column=1, sticky='w')
                label5 = ttk.Label(self, text='Director:', font='Times 30 bold')
                label5.grid(row=4, column=0, sticky='w')
                direct = ttk.Label(self, text='{}'.format(director))
                direct.grid(row=4,column=1, sticky='w')
                label6 = ttk.Label(self, text='Writers:', font='Times 30 bold')
                label6.grid(row=5, column=0, sticky='w')
                if len(writers) < 88 :
                    ar=6
                    write = ttk.Label(self, text='{}'.format(writers))
                    write.grid(row=5,column=1, sticky='w')
                elif len(writers) > 88 and len(writers) < 172:
                    ar=7
                    write1 = ttk.Label(self, text='{}'.format(writers[:88]+'-'))
                    write1.grid(row=5,column=1, sticky='w')
                    write2 = ttk.Label(self, text='{}'.format(writers[88:]))
                    write2.grid(row=6,column=1, sticky='w')
                else:
                    ar=8
                    write1 = ttk.Label(self, text='{}'.format(writers[:88]+'-'))
                    write1.grid(row=5,column=1, sticky='w')
                    write2 = ttk.Label(self, text='{}'.format(writers[88:172]+'-'))
                    write2.grid(row=6,column=1, sticky='w')
                    write3 = ttk.Label(self, text='{}'.format(writers[172:]))
                    write3.grid(row=7,column=1, sticky='w')
                label7 = ttk.Label(self, text='Actors:', font='Times 30 bold')
                label7.grid(row=ar, column=0, sticky='w')
                act = ttk.Label(self, text='{}'.format(actors))
                act.grid(row=ar,column=1, sticky='w')
                label8 = ttk.Label(self, text='Plot:', font='Times 30 bold')
                label8.grid(row=ar+1, column=0, sticky='w')
                if len(plot) < 93:
                    rr=ar+2
                    pl = ttk.Label(self, text='{}'.format(plot))
                    pl.grid(row=ar+1,column=1, sticky='w')
                elif len(plot) > 93 and len(plot) < 186:
                    rr=ar+3
                    pl1 = ttk.Label(self, text='{}'.format(plot[:93])+'-')
                    pl1.grid(row=ar+1,column=1, sticky='w')
                    pl2 = ttk.Label(self, text='{}'.format(plot[93:]))
                    pl2.grid(row=ar+2,column=1, sticky='w')
                else:
                    rr=ar+4
                    pl1 = ttk.Label(self, text='{}'.format(plot[:93])+'-')
                    pl1.grid(row=ar+1,column=1, sticky='w')
                    pl2 = ttk.Label(self, text='{}'.format(plot[93:186]+'-'))
                    pl2.grid(row=ar+2,column=1, sticky='w')
                    pl3 = ttk.Label(self, text='{}'.format(plot[186:]))
                    pl3.grid(row=ar+3,column=1, sticky='w')
                label9 = ttk.Label(self, text='Ratings:', font='Times 30 bold')
                label9.grid(row=rr, column=0, sticky='w')
                rating = ttk.Label(self, text='{}'.format(rating))
                rating.grid(row=rr,column=1, sticky='w')
                add_to_watchedlist = ttk.Button(self, text='Add to watched list', command=lambda: self.add_to_watched_list(movie_name))
                add_to_watchedlist.grid(row=rr+2,column=1, sticky='n')
                add_to_watchlist = ttk.Button(self, text='Add to watchlist', command=lambda: self.add_to_watchlist(movie_name))
                add_to_watchlist.grid(row=rr+3, column=1, sticky='n')
                back_to_main = ttk.Button(self,  text='Back to main menu', command=self.reset)
                back_to_main.grid(row=rr+4, column=1, sticky='n')
                search_new = ttk.Button(self,  text='New search', command=lambda: masterframe.show_frame(SearchBox))
                search_new.grid(row=rr+5, column=1, sticky='n')
            except:
                errorlabel = ttk.Label(self, text='Movie not found', font='Times 30 bold')
                errorlabel.grid(column =0, row=0, sticky='n')
                back_buttonImage = Image.open('back.png')
                self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
                back_to_main = ttk.Button(self, text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT, command=lambda: masterframe.show_frame(MainMenu))
                back_to_main_error.grid(column=0, row=1, sticky='n')
            
        def add_to_watched_list(self, new_movie_watched=''):
            watchedlist.append(new_movie_watched)
            with open('watched', 'wb') as w:
                pickle.dump(watchedlist, w)
            

        def add_to_watchlist(self, new_movie_to_watchlist=''):
            to_watchlist.append(new_movie_to_watchlist)
            with open('watchlist', 'wb') as w:
                pickle.dump(to_watchlist, w)
            
        def allratings(self, rate):
            global ratings
            ratings = ''
            for i in range(len(rate)):
                ratings += rate[i]['Source'] + " :" + " " + rate[i]['Value'] + "    "
            return ratings

        def reset(self):
            app.destroy()
            main2()

    class Movie(object):
        def __init__(self, title, year, runtime, genre, director, writers, actors, plot, rating):
            self.title = title
            self.year = year
            self.runtime = runtime
            self.genre = genre
            self.director = director
            self.writers = writers
            self.actors = actors
            self.plot = plot
            self.ratings = rating


    class ScrolledWindow(tk.Frame,object):

        def __init__(self, parent, *args, **kwargs):

            super().__init__(parent, *args, **kwargs)
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.parent = parent


            self.yscrlbr = ttk.Scrollbar(self.parent)
            self.yscrlbr.grid(column = 1, row = 0, sticky = 'ns')

            self.canv = tk.Canvas(self.parent)
            self.canv.config(relief = 'flat', width = 10, heigh = 10, bd = 2)

            self.canv.grid(column = 0, row = 0, sticky = 'nsew')
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)

            self.yscrlbr.config(command = self.canv.yview)

            self.scrollwindow = ttk.Frame(self.parent)

            self.canv.create_window(0, 0, window = self.scrollwindow, anchor = 'nw')

            self.canv.config(yscrollcommand = self.yscrlbr.set, scrollregion = (0, 0, 100, 100))

            self.yscrlbr.lift(self.scrollwindow)
            self.scrollwindow.bind('<Configure>', self._configure_window)
            self.scrollwindow.bind('<Enter>', self._bound_to_mousewheel)
            self.scrollwindow.bind('<Leave>', self._unbound_to_mousewheel)

            return

        def _bound_to_mousewheel(self, event):
            self.canv.bind_all("<MouseWheel>", self._on_mousewheel)

        def _unbound_to_mousewheel(self, event):
            self.canv.unbind_all("<MouseWheel>")

        def _on_mousewheel(self, event):
            self.canv.yview_scroll(int(-1*(event.delta/120)), "units")

        def _configure_window(self, event):
            size = (self.scrollwindow.winfo_reqwidth(), self.scrollwindow.winfo_reqheight())
            self.canv.config(scrollregion='0 0 %s %s' % size)
            if self.scrollwindow.winfo_reqwidth() != self.canv.winfo_width():
                self.canv.config(width = self.scrollwindow.winfo_reqwidth())
            if self.scrollwindow.winfo_reqheight() != self.canv.winfo_height():
                self.canv.config(height = self.scrollwindow.winfo_reqheight())
        
        
    app = Master()
    app.mainloop()
    try:
        app.destroy()
    except tk.TclError:
        pass

#Login

creds = 'signup.txt'


def signup():
    global pwordE
    global nameE
    global roots

    roots = tk.Tk()
    roots.title('Signup')
    roots.geometry('250x105+600+350')
    intruction = tk.Label(roots, text='Create a new account\n')
    intruction.grid(row=0, column=0, sticky='E')

    nameL = tk.Label(roots, text='New Username: ')
    pwordL = tk.Label(roots, text='New Password: ')
    nameL.grid(row=1, column=0, sticky='W')
    pwordL.grid(row=2, column=0, sticky='W')

    nameE = tk.Entry(roots)
    pwordE = tk.Entry(roots, show='*')
    nameE.grid(row=1, column=1)
    pwordE.grid(row=2, column=1)

    signupButton = ttk.Button(roots, text='Signup', command=FSSignup)
    signupButton.grid(columnspan=2, sticky='W')
    roots.mainloop()



def FSSignup():
    with open(creds, 'w') as f:
        f.write(nameE.get())
        f.write('\n')
        f.write(pwordE.get())
        f.close()

    roots.destroy()
    main2()



def login():
    global nameEL
    global pwordEL
    global rootA

    rootA = tk.Tk()
    rootA.title('Login')
    rootA.geometry('200x130+600+350')

    intruction = tk.Label(rootA, text='Please Login\n')
    intruction.grid(sticky='E')

    nameL = tk.Label(rootA, text='Username: ')
    pwordL = tk.Label(rootA, text='Password: ')
    nameL.grid(row=1, sticky='W')
    pwordL.grid(row=2, sticky='W')

    nameEL = tk.Entry(rootA)
    pwordEL = tk.Entry(rootA, show='*')
    nameEL.grid(row=1, column=1)
    pwordEL.grid(row=2, column=1)

    loginB = ttk.Button(rootA, text='Login', command=checkLogin)
    loginB.grid(columnspan=2, sticky='W')

    rmuser = ttk.Button(rootA, text='Delete User', command=delUser)
    rmuser.grid(columnspan=2, sticky='W')
    rootA.mainloop()


def checkLogin():
    with open(creds) as f:
        data = f.readlines()
        uname = data[0].rstrip()
        pword = data[1].rstrip()

    if nameEL.get() == uname and pwordEL.get() == pword:
        rootA.destroy()
        main2()

    else:
        r = tk.Tk()
        r.title('Error')
        r.geometry('100x50+600+350')
        rlbl = tk.Label(r, text='\n[!] Invalid Login')
        nameEL.delete(0,'end')
        pwordEL.delete(0,'end')
        rlbl.pack()
        r.mainloop()


def delUser():
    os.remove(creds)
    os.remove('watched')
    os.remove('watchlist')
    rootA.destroy()
    signup()


if os.path.isfile(creds):
    login()
    
else:
    signup()

if __name__ == '__main2__' :
    main2()
