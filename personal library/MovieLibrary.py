#from __future__ import (absolute_import, division,
                        #print_function, unicode_literals)
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import requests
import ast
import pickle


def main():
    watched_list = []
    to_watch_list = []
    watched_movie_buttons = []
    remove_watched_movie_buttons = []
    to_watch_movie_buttons = []
    add_to_watched_list_buttons = []
    remove_to_watch_movie_buttons = []

    if os.path.isfile('watchlist') and os.path.getsize('watchlist') > 0:
        with open('watchlist', 'rb') as r:
            to_watch_list = pickle.load(r)
        while '-' in to_watch_list:
            for i in to_watch_list:
                if i == '-':
                    to_watch_list.remove(i)

    if os.path.isfile('watched') and os.path.getsize('watched'):
        with open('watched', 'rb') as r:
            watched_list = pickle.load(r)
        while '-' in watched_list:
            for i in watched_list:
                if i == '-':
                    watched_list.remove(i)

    class Master(tk.Tk):
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)
            self.title('Personal movie library')

            self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(),self.winfo_screenheight()))
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
            self.protocol("WM_DELETE_WINDOW", self.on_closing)
            masterframe = ttk.Frame(self)
            masterframe.grid(column=0, row=0, sticky="n")
            masterframe.grid_rowconfigure(0, weight=1)
            masterframe.grid_columnconfigure(0, weight=1)
            sw = ScrolledWindow(masterframe)
            self.frames = {}
            for frame_module in (MainMenu, SearchBox, WatchedList, ToWatchList):
                ttk.Style(master=self).configure("TButton", font="Times 20", relief='raised', foreground="black",
                                                 background="white")
                ttk.Style(master=self).configure("TLabelframe.Label", font="Times 30 bold")
                ttk.Style(master=self).configure("TLabel", font="Times 20")
                frame = frame_module(sw.scrollwindow, self)
                self.frames[frame_module] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            self.show_frame(MainMenu)

        def show_frame(self, content):
            frame = self.frames[content]
            frame.tkraise()

        def on_closing(self):
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.destroy()
                exit(0)

    class MainMenu(ttk.LabelFrame):
        def __init__(self, parent, masterframe):
            ttk.LabelFrame.__init__(self, parent, text="MAIN MENU", labelanchor='n')

            self.grid_columnconfigure(0, weight=1, minsize= self.winfo_screenwidth())

            for x in range(14):
                self.grid_rowconfigure(x, weight=1)

            with open(credentials) as files:
                data = files.readlines()
                username = data[0].rstrip()
            welcome_label = ttk.Label(self, text='Welcome {}!'.format(username))
            welcome_label.grid(row=0, sticky='n')
            search_buttonImage = Image.open('search.png')
            self.search_buttonPhoto = ImageTk.PhotoImage(search_buttonImage)
            new_movie = ttk.Button(self, text='Search a movie',image=self.search_buttonPhoto, compound=tk.LEFT, command=lambda: masterframe.show_frame(SearchBox))
            new_movie.grid(row=1, sticky='n')
            list_buttonImage = Image.open('list.png')
            self.list_buttonPhoto = ImageTk.PhotoImage(list_buttonImage)
            watched_movies_list_button = ttk.Button(self, text='Show watched list',image=self.list_buttonPhoto, compound=tk.LEFT, command=lambda: masterframe.show_frame(WatchedList))
            watched_movies_list_button.grid(row=2, sticky='n')

            to_watchlist_button = ttk.Button(self, text='Show watchlist',image=self.list_buttonPhoto, compound=tk.LEFT, command=lambda: masterframe.show_frame(ToWatchList))
            to_watchlist_button.grid(row=3, sticky='n')
            exit_buttonImage = Image.open('x.png')
            self.buttonPhoto = ImageTk.PhotoImage(exit_buttonImage)
            exit_button = ttk.Button(self, text='Exit', image=self.buttonPhoto, compound=tk.LEFT, command=self.on_closing)
            exit_button.grid(row=4, sticky='n')

        def on_closing(self):
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.destroy()
                exit(0)

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
            search_buttonImage = Image.open('search.png')
            self.search_buttonPhoto = ImageTk.PhotoImage(search_buttonImage)
            button = ttk.Button(self, text='Search',image=self.search_buttonPhoto, compound=tk.LEFT,
                                command=lambda: ShowInfo(parent, entry.get(), masterframe) and entry.delete(0, 'end'))
            button.grid(row=1, sticky='n')
            back_buttonImage = Image.open('back.png')
            self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
            back_to_main = ttk.Button(self,  text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT, command=lambda: masterframe.show_frame(MainMenu))
            back_to_main.grid(row=2, sticky='n')

    class WatchedList(ttk.LabelFrame):
        def __init__(self, parent, masterframe):
            ttk.LabelFrame.__init__(self, parent, text="Watched movies")
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            remove_buttonImage = Image.open('remove.png')
            self.remove_buttonPhoto = ImageTk.PhotoImage(remove_buttonImage)
            if len(watched_list) != 0:
                self.grid_columnconfigure(10, minsize=900)
                self.grid_rowconfigure(len(watched_list) + 1, minsize=880)
                for x in range(len(watched_list)):
                    self.grid_rowconfigure(x, weight=1)
                for x in range(len(watched_list)):
                    watched_movie_buttons.append(ttk.Button(self, text='{}'.format(watched_list[x]),
                                                            command=lambda b=x: ShowInfo(parent, watched_list[b],masterframe)))
                    watched_movie_buttons[x].grid(row=x, column=0, sticky='w', columnspan=10)
                    remove_watched_movie_buttons.append(
                        ttk.Button(self, text='Remove', image=self.remove_buttonPhoto, compound=tk.LEFT, command=lambda b=x: self.remove_movie(b)))
                    remove_watched_movie_buttons[x].grid(row=x, column=10, sticky='w')
                back_buttonImage = Image.open('back.png')
                self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
                back_to_main = ttk.Button(self, text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT,
                                          command=self.reset)
                back_to_main.grid(columnspan=2, sticky='n')
            else:
                self.grid_columnconfigure(0, minsize=900)
                self.grid_rowconfigure(1, minsize=880)
                no_movies = ttk.Label(self, text='No movies in watched list', font='Arial 30', anchor=tk.W)
                no_movies.grid(row=0, column=0)
                back_buttonImage = Image.open('back.png')
                self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
                back_to_main = ttk.Button(self, text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT,
                                          command=self.reset)
                back_to_main.grid(columnspan=2, sticky='n')

        def remove_movie(self, x):
            watched_list[x] = '-'
            with open('watched', 'wb') as w:
                pickle.dump(watched_list, w)
            watched_movie_buttons[x].grid_forget()
            remove_watched_movie_buttons[x].grid_forget()
        def reset(self):
            app.destroy()
            main()
    class ToWatchList(ttk.LabelFrame):
        def __init__(self, parent, masterframe):
            ttk.LabelFrame.__init__(self, parent, text="Watchlist")
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            list_buttonImage = Image.open('add.png')
            self.list_buttonPhoto = ImageTk.PhotoImage(list_buttonImage)
            remove_buttonImage = Image.open('remove.png')
            self.remove_buttonPhoto = ImageTk.PhotoImage(remove_buttonImage)
            if len(to_watch_list) != 0:
                self.grid_columnconfigure(11, minsize=900)
                self.grid_rowconfigure(len(to_watch_list) + 1, minsize=880)
                self.grid_columnconfigure(0, weight=1)
                for x in range(len(to_watch_list)):
                    self.grid_rowconfigure(x, weight=1)
                for x in range(len(to_watch_list)):
                    to_watch_movie_buttons.append(ttk.Button(self, text='{}'.format(to_watch_list[x]),
                                                             command=lambda b=x: ShowInfo(parent, to_watch_list[b],
                                                                                          masterframe)))
                    to_watch_movie_buttons[x].grid(row=x, column=0, sticky='w', columnspan=10)
                    add_to_watched_list_buttons.append(
                        ttk.Button(self, text='Add to watched list', image=self.list_buttonPhoto, compound=tk.LEFT, command=lambda b=x: self.add_to_watched(b)))
                    add_to_watched_list_buttons[x].grid(row=x, column=10, sticky='w')
                    remove_to_watch_movie_buttons.append(
                        ttk.Button(self, text='Remove', image=self.remove_buttonPhoto, compound=tk.LEFT, command=lambda b=x: self.remove_movie_from_watchlist(b)))
                    remove_to_watch_movie_buttons[x].grid(row=x, column=11, sticky='w')
                back_buttonImage = Image.open('back.png')
                self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
                back_to_main = ttk.Button(self, text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT,
                                          command=self.reset)
                back_to_main.grid(columnspan=2, sticky='n')
            else:
                self.grid_columnconfigure(0, minsize=900)
                self.grid_rowconfigure(1, minsize=880)
                no_movies = ttk.Label(self, text='No movies in watchlist', font='Arial 30', anchor=tk.W)
                no_movies.grid(row=0, column=0)
                back_buttonImage = Image.open('back.png')
                self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
                back_to_main = ttk.Button(self, text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT,
                                          command=self.reset)
                back_to_main.grid(columnspan=2, sticky='n')

        def add_to_watched(self, x):
            if to_watch_list[x] not in watched_list:
                watched_list.append(to_watch_list[x])
                with open('watched', 'wb') as w:
                    pickle.dump(watched_list, w)
            self.remove_movie_from_watchlist(x)

        def remove_movie_from_watchlist(self, x):
            to_watch_list[x] = '-'
            with open('watchlist', 'wb') as w:
                pickle.dump(to_watch_list, w)
            to_watch_movie_buttons[x].grid_forget()
            add_to_watched_list_buttons[x].grid_forget()
            remove_to_watch_movie_buttons[x].grid_forget()

        def reset(self):
            app.destroy()
            main()

    class ShowInfo(ttk.LabelFrame):
        def __init__(self, parent, name, masterframe):
            ttk.LabelFrame.__init__(self, parent, text="Movie info", labelanchor='n')
            self.grid(row=0, column=0, sticky="nsew")
            for x in range(30):
                self.grid_rowconfigure(x, weight=1)
            self.tkraise()

            title = name
            try:
                res = requests.get('http://www.omdbapi.com/?t=' + title + '&apikey=6a32ca26')
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
                rate = self.all_ratings(details['Ratings'])
                pstr = details['Poster']
                comm = ''
                self.m1 = Movie(t, y, rt, gen, direct, write, act, pl, rate, pstr)
                movie_name = self.m1.title
                year = self.m1.year
                runtime = self.m1.runtime
                genre = self.m1.genre
                director = self.m1.director
                writers = self.m1.writers
                actors = self.m1.actors
                plot = self.m1.plot
                rating = self.m1.ratings
                poster = self.m1.poster
                label1 = ttk.Label(self, text='Title:', font='Times 30 bold')
                label1.grid(row=1, column=1, sticky='w')
                title = ttk.Label(self, text='{}'.format(movie_name))
                title.grid(row=1, column=2, sticky='w')
                label2 = ttk.Label(self, text='Year:', font='Times 30 bold')
                label2.grid(row=2, column=1, sticky='w')
                year = ttk.Label(self, text='{}'.format(year))
                year.grid(row=2, column=2, sticky='w')
                label3 = ttk.Label(self, text='Runtime:', font='Times 30 bold')
                label3.grid(row=3, column=1, sticky='w')
                runtime = ttk.Label(self, text='{}'.format(runtime))
                runtime.grid(row=3, column=2, sticky='w')
                label4 = ttk.Label(self, text='Genre:', font='Times 30 bold')
                label4.grid(row=4, column=1, sticky='w')
                genre = ttk.Label(self, text='{}'.format(genre))
                genre.grid(row=4, column=2, sticky='w')
                label5 = ttk.Label(self, text='Director:', font='Times 30 bold')
                label5.grid(row=5, column=1, sticky='w')
                direct = ttk.Label(self, text='{}'.format(director))
                direct.grid(row=5, column=2, sticky='w')
                label6 = ttk.Label(self, text='Writers:', font='Times 30 bold')
                label6.grid(row=6, column=1, sticky='w')
                if len(writers) < 88:
                    ar = 7
                    write = ttk.Label(self, text='{}'.format(writers))
                    write.grid(row=6, column=2, sticky='w')
                elif 88 < len(writers) < 172:
                    ar = 8
                    write1 = ttk.Label(self, text='{}'.format(writers[:88] + '-'))
                    write1.grid(row=6, column=2, sticky='w')
                    write2 = ttk.Label(self, text='{}'.format(writers[88:]))
                    write2.grid(row=7, column=2, sticky='w')
                else:
                    ar = 9
                    write1 = ttk.Label(self, text='{}'.format(writers[:88] + '-'))
                    write1.grid(row=6, column=2, sticky='w')
                    write2 = ttk.Label(self, text='{}'.format(writers[88:172] + '-'))
                    write2.grid(row=7, column=2, sticky='w')
                    write3 = ttk.Label(self, text='{}'.format(writers[172:]))
                    write3.grid(row=8, column=2, sticky='w')
                label7 = ttk.Label(self, text='Actors:', font='Times 30 bold')
                label7.grid(row=ar, column=1, sticky='w')
                act = ttk.Label(self, text='{}'.format(actors))
                act.grid(row=ar, column=2, sticky='w')
                label8 = ttk.Label(self, text='Plot:', font='Times 30 bold')
                label8.grid(row=ar + 1, column=1, sticky='w')
                if len(plot) < 93:
                    rr = ar + 2
                    pl = ttk.Label(self, text='{}'.format(plot))
                    pl.grid(row=ar + 1, column=2, sticky='w')
                elif 93 < len(plot) < 186:
                    rr = ar + 3
                    pl1 = ttk.Label(self, text='{}'.format(plot[:93]) + '-')
                    pl1.grid(row=ar + 1, column=2, sticky='w')
                    pl2 = ttk.Label(self, text='{}'.format(plot[93:]))
                    pl2.grid(row=ar + 2, column=2, sticky='w')
                else:
                    rr = ar + 4
                    pl1 = ttk.Label(self, text='{}'.format(plot[:93]) + '-')
                    pl1.grid(row=ar + 1, column=2, sticky='w')
                    pl2 = ttk.Label(self, text='{}'.format(plot[93:186] + '-'))
                    pl2.grid(row=ar + 2, column=2, sticky='w')
                    pl3 = ttk.Label(self, text='{}'.format(plot[186:]))
                    pl3.grid(row=ar + 3, column=2, sticky='w')
                label9 = ttk.Label(self, text='Ratings:', font='Times 30 bold')
                label9.grid(row=rr, column=1, sticky='w')
                ratinglabel = ttk.Label(self, text='{}'.format(rating))
                ratinglabel.grid(row=rr, column=2, sticky='w')
                add_buttonImage = Image.open('add.png')
                self.add_buttonPhoto = ImageTk.PhotoImage(add_buttonImage)
                add_to_watched_list = ttk.Button(self, text='Add to watched list', image=self.add_buttonPhoto, compound=tk.LEFT,
                                                 command=lambda: self.add_in_watched_list(movie_name))
                add_to_watched_list.grid(row=rr + 2, column=0, sticky='n')
                add_to_watchlist = ttk.Button(self, text='  Add to watchlist   ', image=self.add_buttonPhoto, compound=tk.LEFT,
                                              command=lambda: self.add_in_to_watch_list(movie_name))
                add_to_watchlist.grid(row=rr+3, column=0, sticky='n')
                back_buttonImage = Image.open('back.png')
                self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
                back_to_main = ttk.Button(self, text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT,
                                          command=self.reset)
                back_to_main.grid(row=rr+3, column=1, sticky='n')
                search_buttonImage = Image.open('search.png')
                self.search_buttonPhoto = ImageTk.PhotoImage(search_buttonImage)
                search_new = ttk.Button(self, text='Search a movie', image=self.search_buttonPhoto, compound=tk.LEFT,
                                       command=lambda: masterframe.show_frame(SearchBox))
                search_new.grid(row=rr+2, column=1, sticky='n')
                self.image(poster)
                imagelabel = tk.Label(self, image=tk_image)
                imagelabel.grid(column=0, row=0, rowspan=10)
            except:
                self.grid_columnconfigure(0, weight=1)
                error_label = ttk.Label(self, text='Movie not found!', font='Times 30 bold')
                error_label.grid(column=0, row=0, sticky='n')
                back_buttonImage = Image.open('back.png')
                self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
                back_to_main_error = ttk.Button(self, text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT,
                                          command=lambda: masterframe.show_frame(MainMenu))
                back_to_main_error.grid(column=0, row=1, sticky='n')
                search_buttonImage = Image.open('search.png')
                self.search_buttonPhoto = ImageTk.PhotoImage(search_buttonImage)
                new_search_error= ttk.Button(self, text='Search a movie', image=self.search_buttonPhoto, compound=tk.LEFT,
                                       command=lambda: masterframe.show_frame(SearchBox))
                new_search_error.grid(column=0, row=2, sticky='n')

        def add_in_watched_list(self, new_movie_watched=''):
            if new_movie_watched not in watched_list:
                watched_list.append(new_movie_watched)
                with open('watched', 'wb') as w:
                    pickle.dump(watched_list, w)

        def add_in_to_watch_list(self, new_movie_to_watchlist=''):
            if new_movie_to_watchlist not in to_watch_list:
                to_watch_list.append(new_movie_to_watchlist)
                with open('watchlist', 'wb') as w:
                    pickle.dump(to_watch_list, w)

        def comment_submit(self):
            pass

        def all_ratings(self, rate):
            global ratings
            ratings = ''
            for i in range(len(rate)):
                ratings += rate[i]['Source'] + " :" + " " + rate[i]['Value'] + "    "
            return ratings

        def image(self,link):
            global tk_image
            try:
                url = link
                response = requests.get(url)
                tk_image = ImageTk.PhotoImage(Image.open(BytesIO(response.content)))
            except:
                url = 'https://lezzet.blob.core.windows.net/images-test/no-image.png'
                response = requests.get(url)
                tk_image = ImageTk.PhotoImage(Image.open(BytesIO(response.content)))

        def reset(self):
            app.destroy()
            main()

    class Movie(object):
        def __init__(self, title, year, runtime, genre, director, writers, actors, plot, rating, poster):
            self.title = title
            self.year = year
            self.runtime = runtime
            self.genre = genre
            self.director = director
            self.writers = writers
            self.actors = actors
            self.plot = plot
            self.ratings = rating
            self.poster = poster

    class ScrolledWindow(tk.Frame, object):
        def __init__(self, parent, *args, **kwargs):

            super().__init__(parent, *args, **kwargs)
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.parent = parent

            self.yscrlbr = ttk.Scrollbar(self.parent)
            self.yscrlbr.grid(column=1, row=0, sticky='ns')

            self.canv = tk.Canvas(self.parent)
            self.canv.config(relief='flat', width=10, heigh=10, bd=2)

            self.canv.grid(column=0, row=0, sticky='nsew')
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)

            self.yscrlbr.config(command=self.canv.yview)

            self.scrollwindow = ttk.Frame(self.parent)

            self.canv.create_window(0, 0, window=self.scrollwindow, anchor='nw')

            self.canv.config(yscrollcommand=self.yscrlbr.set, scrollregion=(0, 0, 100, 100))

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
            self.canv.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _configure_window(self, event):
            size = (self.scrollwindow.winfo_reqwidth(), self.scrollwindow.winfo_reqheight())
            self.canv.config(scrollregion='0 0 %s %s' % size)
            if self.scrollwindow.winfo_reqwidth() != self.canv.winfo_width():
                self.canv.config(width=self.scrollwindow.winfo_reqwidth())
            if self.scrollwindow.winfo_reqheight() != self.canv.winfo_height():
                self.canv.config(height=self.scrollwindow.winfo_reqheight())

    app = Master()
    app.mainloop()
    try:
        app.destroy()
    except tk.TclError:
        pass


# Login
credentials = 'signup.txt'


def signup():
    global password_entry
    global name_entry
    global root_signup

    root_signup = tk.Tk()
    root_signup.title('Signup')
    root_signup.geometry('350x150+600+350')
    root_signup.protocol("WM_DELETE_WINDOW", lambda: login_exit(root_signup))
    instruction = tk.Label(root_signup, text='Create a new account\n')
    instruction.grid(row=0, sticky='E')

    name_label = tk.Label(root_signup, text='New Username: ')
    password_label = tk.Label(root_signup, text='New Password: ')
    name_label.grid(row=1, column=0, sticky='W')
    password_label.grid(row=2, column=0, sticky='W')

    name_entry = tk.Entry(root_signup)
    password_entry = tk.Entry(root_signup, show='*')
    name_entry.grid(row=1, column=1)
    password_entry.grid(row=2, column=1)

    signup_button = ttk.Button(root_signup, text='Signup', command=finalize_signup)
    signup_button.grid(row=3, column=1, sticky='N')
    root_signup.mainloop()


def finalize_signup():
    with open(credentials, 'w') as file:
        file.write(name_entry.get())
        file.write('\n')
        file.write(password_entry.get())
        file.close()
    root_signup.destroy()
    main()


def login():
    global name_entry_label
    global password_entry_label
    global root_login

    root_login = tk.Tk()
    root_login.title('Login')
    root_login.geometry('350x150+600+350')
    root_login.protocol("WM_DELETE_WINDOW", lambda: login_exit(root_login))
    instruction = tk.Label(root_login, text='Please Login\n')
    instruction.grid(sticky='E')

    name_label = tk.Label(root_login, text='Username: ')
    password_label = tk.Label(root_login, text='Password: ')
    name_label.grid(row=1, sticky='W')
    password_label.grid(row=2, sticky='W')

    name_entry_label = tk.Entry(root_login)
    password_entry_label = tk.Entry(root_login, show='*')
    name_entry_label.grid(row=1, column=1)
    password_entry_label.grid(row=2, column=1)

    login_button = ttk.Button(root_login, text='Login', command=check_login)
    login_button.grid(row=3, column=1, sticky='N')

    delete_user_button = ttk.Button(root_login, text='Delete User', command=delete_user)
    delete_user_button.grid(row=4, column=1, sticky='N')
    root_login.mainloop()


def check_login():
    with open(credentials) as file:
        data = file.readlines()
        username = data[0].rstrip()
        password = data[1].rstrip()

    if name_entry_label.get() == username and password_entry_label.get() == password:
        root_login.destroy()
        main()
    else:
        r = tk.Tk()
        r.title('Error')
        r.geometry('100x50+600+350')
        error_label = tk.Label(r, text='\n[!] Invalid Login')
        name_entry_label.delete(0, 'end')
        password_entry_label.delete(0, 'end')
        error_label.pack()
        r.mainloop()


def delete_user():
    os.remove(credentials)
    if os.path.isfile('watched'):
        os.remove('watched')
    if os.path.isfile('watchlist'):
        os.remove('watchlist')
    root_login.destroy()
    signup()

def login_exit(root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        exit(0)


if os.path.isfile(credentials):
    login()
else:
    signup()

if __name__ == '__main__':
    main()
