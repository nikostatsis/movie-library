# Import necessary libraries
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import requests
import ast
import pickle

# Define empty lists for storing movie lists and buttons
watched_list = []
to_watch_list = []
watched_movie_buttons = []
remove_watched_movie_buttons = []
to_watch_movie_buttons = []
add_to_watched_list_buttons = []
remove_to_watch_movie_buttons = []

# Check if there are saved movie lists and load them
# Check if the 'watchlist' file exists and is not empty
if os.path.isfile('watchlist') and os.path.getsize('watchlist') > 0:
    # Open the 'watchlist' file in binary read mode using the 'rb' flag
    with open('watchlist', 'rb') as r:
        # Load the saved movie list from the file using pickle.load()
        to_watch_list = pickle.load(r)
    # Remove any hyphen characters '-' from the list if they exist
    while '-' in to_watch_list:
        for i in to_watch_list:
            if i == '-':
                to_watch_list.remove(i)

# Check if the 'watched' file exists and is not empty
if os.path.isfile('watched') and os.path.getsize('watched'):
    # Open the 'watched' file in binary read mode using the 'rb' flag
    with open('watched', 'rb') as r:
        # Load the saved movie list from the file using pickle.load()
        watched_list = pickle.load(r)
    # Remove any hyphen characters '-' from the list if they exist
    while '-' in watched_list:
        for i in watched_list:
            if i == '-':
                watched_list.remove(i)


 # Define the 'Master' class, which extends the 'tk.Tk' class
class Master(tk.Tk):
    # Define the '__init__' method, which initializes the application window
    def __init__(self, *args, **kwargs):
        # Call the constructor of the parent class 'tk.Tk'
        tk.Tk.__init__(self, *args, **kwargs)
        # Set the title of the window
        self.title('Personal movie library')
        # Set the size and position of the window to fill the screen
        self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(),self.winfo_screenheight()))
        # Configure the row and column of the window to have weight 1
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # Set the protocol for closing the window to call the 'on_closing' method
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # Create a frame for the window
        masterframe = ttk.Frame(self)
        masterframe.grid(column=0, row=0, sticky="n")
        masterframe.grid_rowconfigure(0, weight=1)
        masterframe.grid_columnconfigure(0, weight=1)
        # Create a scrolled window for the frame
        sw = ScrolledWindow(masterframe)
        # Create frames for each section of the application
        self.frames = {}
        for frame_module in (MainMenu, SearchBox, WatchedList, ToWatchList):
            # Configure the style of the buttons, labels, and frames
            ttk.Style(master=self).configure("TButton", font="Times 20", relief='raised', foreground="black",
                                                 background="white")
            ttk.Style(master=self).configure("TLabelframe.Label", font="Times 30 bold")
            ttk.Style(master=self).configure("TLabel", font="Times 20")
            # Create a frame object for each frame module and store it in a dictionary
            frame = frame_module(sw.scrollwindow, self)
            self.frames[frame_module] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        # Show the main menu frame
        self.show_frame(MainMenu)

    # Define the 'show_frame' method, which raises a given frame to the front
    def show_frame(self, content):
        frame = self.frames[content]
        frame.tkraise()

    # Define the 'on_closing' method, which handles the event of closing the window
    def on_closing(self):
        # Show a messagebox to ask the user if they want to quit
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # Destroy the window and exit the application
            self.destroy()
            exit(0)

            
# Define the search box frame class
class SearchBox(ttk.LabelFrame):
    # Initialize the search box
    def __init__(self, parent, masterframe):
        # Call the constructor of the parent class (LabelFrame)
        ttk.LabelFrame.__init__(self, parent, text="Find new movie", labelanchor='n')
        
        # Configure the grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        # Create an entry box to enter the movie name
        entry = tk.Entry(self, font='Arial 20', width=20)
        entry.grid(row=0, sticky='n')
        entry.config(relief='solid')
        
        # Load the search button image and create a button with the image
        search_buttonImage = Image.open('search.png')
        self.search_buttonPhoto = ImageTk.PhotoImage(search_buttonImage)
        button = ttk.Button(self, text='Search',image=self.search_buttonPhoto, compound=tk.LEFT,
                            command=lambda: ShowInfo(parent, entry.get(), masterframe) and entry.delete(0, 'end'))
        button.grid(row=1, sticky='n')
        
        # Load the back button image and create a button with the image to go back to the main menu
        back_buttonImage = Image.open('back.png')
        self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
        back_to_main = ttk.Button(self,  text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT, command=lambda: masterframe.show_frame(MainMenu))
        back_to_main.grid(row=2, sticky='n')
        
        
# Define a class to create a label frame widget for the list of watched movies
class WatchedList(ttk.LabelFrame):
    
    # Constructor method to initialize the widget
    def __init__(self, parent, masterframe):
        # Call the __init__ method of the parent class to create the label frame
        ttk.LabelFrame.__init__(self, parent, text="Watched movies")
        
        # Configure the grid layout to have one column and one row, and set weight of row 0 and column 0 to 1
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create an image object from a PNG file to use as the icon for the "Remove" button
        remove_buttonImage = Image.open('remove.png')
        self.remove_buttonPhoto = ImageTk.PhotoImage(remove_buttonImage)
        
        # Check if there are movies in the watched list
        if len(watched_list) != 0:
            # If there are movies, configure the grid layout to have 10 columns and len(watched_list) + 1 rows
            self.grid_columnconfigure(10, minsize=900)
            self.grid_rowconfigure(len(watched_list) + 1, minsize=880)
            
            # Set the weight of each row to 1 so that the buttons expand to fill any extra space
            for x in range(len(watched_list)):
                self.grid_rowconfigure(x, weight=1)
                
            # Create a button for each movie in the watched list and add it to the grid
            for x in range(len(watched_list)):
                # Create a button with the movie name as the label, and bind it to a ShowInfo function with the parent and masterframe arguments
                watched_movie_buttons.append(ttk.Button(self, text='{}'.format(watched_list[x]), command=lambda b=x: ShowInfo(parent, watched_list[b],masterframe)))
                watched_movie_buttons[x].grid(row=x, column=0, sticky='w', columnspan=10)
                
                # Create a "Remove" button with the remove_movie method bound to it, and add it to the grid
                remove_watched_movie_buttons.append(ttk.Button(self, text='Remove', image=self.remove_buttonPhoto, compound=tk.LEFT, command=lambda b=x: self.remove_movie(b)))
                remove_watched_movie_buttons[x].grid(row=x, column=10, sticky='w')
            
            # Create a button to go back to the main menu and add it to the grid
            back_buttonImage = Image.open('back.png')
            self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
            back_to_main = ttk.Button(self, text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT, command=self.reset)
            back_to_main.grid(columnspan=2, sticky='n')
        else:
            # If there are no movies, configure the grid layout to have one column and one row
            self.grid_columnconfigure(0, minsize=900)
            self.grid_rowconfigure(1, minsize=880)
            
            # Create a label to indicate that there are no movies in the list, and add it to the grid
            no_movies = ttk.Label(self, text='No movies in watched list', font='Arial 30', anchor=tk.W)
            no_movies.grid(row=0, column=0)
            # Create a back button image and open it using the PIL library
            back_buttonImage = Image.open('back.png')
            # Create a PhotoImage object from the back button image using the tkinter library
            self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
            # Create a ttk button with the text "Back to main menu", image of the back button, and a command to call the reset method
            back_to_main = ttk.Button(self, text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT, command=self.reset)
            # Position the back_to_main button at the top of the grid, spanning two columns and sticking to the north
            back_to_main.grid(columnspan=2, sticky='n')

            # Define a method to remove a movie from the watched list
            def remove_movie(self, x):
                # Replace the movie at index x with a dash (-) in the watched list
                watched_list[x] = '-'
                # Open the "watched" file for writing in binary mode
                with open('watched', 'wb') as w:
                    # Write the updated watched list to the "watched" file using the pickle module
                    pickle.dump(watched_list, w)
                # Remove the button for the watched movie at index x from the GUI
                watched_movie_buttons[x].grid_forget()
                # Remove the button for removing the watched movie at index x from the GUI
                remove_watched_movie_buttons[x].grid_forget()

            # Define a method to reset the GUI and return to the main menu
            def reset(self):
                # Destroy the current GUI window
                app.destroy()
                # Call the main function to create a new GUI window and display the main menu
                main()

class ToWatchList(ttk.LabelFrame):
    # Initialize the class with the parent and masterframe arguments
    def __init__(self, parent, masterframe):
        # Initialize the ttk LabelFrame with the parent and "Watchlist" as the label text
        ttk.LabelFrame.__init__(self, parent, text="Watchlist")
        # Configure the first column to have weight of 1 (i.e. take up available space)
        self.grid_columnconfigure(0, weight=1)
        # Configure the first row to have weight of 1 (i.e. take up available space)
        self.grid_rowconfigure(0, weight=1)
        # Load the add.png image and create a PhotoImage object from it
        list_buttonImage = Image.open('add.png')
        self.list_buttonPhoto = ImageTk.PhotoImage(list_buttonImage)
        # Load the remove.png image and create a PhotoImage object from it
        remove_buttonImage = Image.open('remove.png')
        self.remove_buttonPhoto = ImageTk.PhotoImage(remove_buttonImage)
        # Check if there are movies in the to watch list
        if len(to_watch_list) != 0:
            # Configure the 11th column to have a minimum size of 900 pixels
            self.grid_columnconfigure(11, minsize=900)
            # Configure the last row to have a minimum size of 880 pixels
            self.grid_rowconfigure(len(to_watch_list) + 1, minsize=880)
            # Configure the first column to have a weight of 1 (i.e. take up available space)
            self.grid_columnconfigure(0, weight=1)
            # Configure each row to have a weight of 1 (i.e. take up available space)
            for x in range(len(to_watch_list)):
                self.grid_rowconfigure(x, weight=1)
            # Create buttons for each movie in the to watch list
            for x in range(len(to_watch_list)):
                # Create a button for the movie that shows the movie info when clicked
                to_watch_movie_buttons.append(ttk.Button(self, text='{}'.format(to_watch_list[x]),
                                                         command=lambda b=x: ShowInfo(parent, to_watch_list[b],
                                                                                      masterframe)))
                # Place the button in the first 10 columns of the xth row
                to_watch_movie_buttons[x].grid(row=x, column=0, sticky='w', columnspan=10)
                # Create a button for adding the movie to the watched list
                add_to_watched_list_buttons.append(
                    ttk.Button(self, text='Add to watched list', image=self.list_buttonPhoto, compound=tk.LEFT, command=lambda b=x: self.add_to_watched(b)))
                # Place the button in the 11th column of the xth row
                add_to_watched_list_buttons[x].grid(row=x, column=10, sticky='w')
                # Create a button for removing the movie from the to watch list
                remove_to_watch_movie_buttons.append(
                    ttk.Button(self, text='Remove', image=self.remove_buttonPhoto, compound=tk.LEFT, command=lambda b=x: self.remove_movie_from_watchlist(b)))
                # Place the button in the 12th column of the xth row
                remove_to_watch_movie_buttons[x].grid(row=x, column=11, sticky='w')
            # Load the back.png image and create a PhotoImage object from it
            back_buttonImage = Image.open('back.png')
            self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
            # Create a button for going back to the main menu
            back_to_main = ttk.Button(self, text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT,
                                      command=self.reset)
            back_to_main.grid(columnspan=2, sticky='n')
        else:
            # If there are no movies in the watchlist, configure the first column and second row to have minimum sizes
            self.grid_columnconfigure(0, minsize=900)
            self.grid_rowconfigure(1, minsize=880)
            # Create a label that says "No movies in watchlist"
            no_movies = ttk.Label(self, text='No movies in watchlist', font='Arial 30', anchor=tk.W)
            no_movies.grid(row=0, column=0)
            # Load the back.png image and create a PhotoImage object from it
            back_buttonImage = Image.open('back.png')
            self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
            # Create a button for going back to the main menu
            back_to_main = ttk.Button(self, text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT,
                                      command=self.reset)
            back_to_main.grid(columnspan=2, sticky='n')

    # This function handles adding a movie to the watched list
    def add_to_watched(self, x):
        # Check if the movie is not already in the watched list
        if to_watch_list[x] not in watched_list:
            # If not, add it to the watched list
            watched_list.append(to_watch_list[x])
            # Save the watched list to file using pickle
            with open('watched', 'wb') as w:
                pickle.dump(watched_list, w)
        # Call remove_movie_from_watchlist function to remove the movie from the watchlist
        self.remove_movie_from_watchlist(x)

    # This function removes a movie from the watchlist
    def remove_movie_from_watchlist(self, x):
        # Set the element at index x of to_watch_list to '-'
        to_watch_list[x] = '-'
        # Save the updated watchlist to file using pickle
        with open('watchlist', 'wb') as w:
            pickle.dump(to_watch_list, w)
        # Remove the buttons associated with the movie from the GUI
        to_watch_movie_buttons[x].grid_forget()
        add_to_watched_list_buttons[x].grid_forget()
        remove_to_watch_movie_buttons[x].grid_forget()

    # This function resets the GUI and goes back to the main menu
    def reset(self):
        # Destroy the current GUI window
        app.destroy()
        # Call the main function to go back to the main menu
        main()


# Define a class for a label frame to display movie information
class ShowInfo(ttk.LabelFrame):
    def __init__(self, parent, name, masterframe):
        ttk.LabelFrame.__init__(self, parent, text="Movie info", labelanchor='n')
        self.grid(row=0, column=0, sticky="nsew")
        for x in range(30):
            self.grid_rowconfigure(x, weight=1)
        self.tkraise()

        # Get movie information from the OMDb API
        title = name
        try:
            # Send request to the API and retrieve the data as a string
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
            # Create a new Movie object with the retrieved information
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
            # Create labels to display the movie information
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
                ar = 7 # set row number for actors label
                write = ttk.Label(self, text='{}'.format(writers))
                write.grid(row=6, column=2, sticky='w')
            elif 88 < len(writers) < 172:
                ar = 8 # set row number for actors label
                write1 = ttk.Label(self, text='{}'.format(writers[:88] + '-')) # slice first 88 characters of writers and add '-' at the end
                write1.grid(row=6, column=2, sticky='w')
                write2 = ttk.Label(self, text='{}'.format(writers[88:])) # slice characters after the 88th character of writers
                write2.grid(row=7, column=2, sticky='w')
            else:
                ar = 9 # set row number for actors label
                write1 = ttk.Label(self, text='{}'.format(writers[:88] + '-')) # slice first 88 characters of writers and add '-' at the end
                write1.grid(row=6, column=2, sticky='w')
                write2 = ttk.Label(self, text='{}'.format(writers[88:172] + '-')) # slice characters between 88th and 172nd character of writers and add '-' at the end
                write2.grid(row=7, column=2, sticky='w')
                write3 = ttk.Label(self, text='{}'.format(writers[172:])) # slice characters after the 172nd character of writers
                write3.grid(row=8, column=2, sticky='w')

            label7 = ttk.Label(self, text='Actors:', font='Times 30 bold')
            label7.grid(row=ar, column=1, sticky='w') # add actors label at the row number based on length of writers

            act = ttk.Label(self, text='{}'.format(actors))
            act.grid(row=ar, column=2, sticky='w') # add actors text at the row number based on length of writers

            label8 = ttk.Label(self, text='Plot:', font='Times 30 bold')
            label8.grid(row=ar + 1, column=1, sticky='w') # add plot label one row below the actors label

            if len(plot) < 93:
                rr = ar + 2 # set row number for plot label
                pl = ttk.Label(self, text='{}'.format(plot))
                pl.grid(row=ar + 1, column=2, sticky='w') # add plot text at the row number based on length of writers
            elif 93 < len(plot) < 186:
                rr = ar + 3 # set row number for plot label
                pl1 = ttk.Label(self, text='{}'.format(plot[:93]) + '-') # slice first 93 characters of plot and add '-' at the end
                pl1.grid(row=ar + 1, column=2, sticky='w')
                pl2 = ttk.Label(self, text='{}'.format(plot[93:])) # slice characters after the 93rd character of plot
                pl2.grid(row=ar + 2, column=2, sticky='w')
            else:
                rr = ar + 4 # set row number for plot label
                pl1 = ttk.Label(self, text='{}'.format(plot[:93]) + '-') # slice first 93 characters of plot and add '-' at the end
                pl1.grid(row=ar + 1, column=2, sticky='w')
                pl2 = ttk.Label(self, text='{}'.format(plot[93:186] + '-'))# slice characters between 93rd and 186th character of writers and add '-' at the end
                pl2.grid(row=ar + 2, column=2, sticky='w')
                pl3 = ttk.Label(self, text='{}'.format(plot[186:]))# slice characters after the 186th character of plot
                pl3.grid(row=ar + 3, column=2, sticky='w')
                
            label9 = ttk.Label(self, text='Ratings:', font='Times 30 bold')
            label9.grid(row=rr, column=1, sticky='w')# add Ratings label at the row number based on length of writers
            
            ratinglabel = ttk.Label(self, text='{}'.format(rating))
            ratinglabel.grid(row=rr, column=2, sticky='w')# add Ratings text at the row number based on length of writers
            
            #Open the add.png image file and create a PhotoImage object
            add_buttonImage = Image.open('add.png')
            self.add_buttonPhoto = ImageTk.PhotoImage(add_buttonImage)
            #Create a button to add the movie to the watched list with the add_buttonPhoto as its image
            #The command parameter calls the add_in_watched_list function with the movie name as its argument
            add_to_watched_list = ttk.Button(self, text='Add to watched list', image=self.add_buttonPhoto, compound=tk.LEFT,
                                             command=lambda: self.add_in_watched_list(movie_name))
            #Place the "Add to watched list" button on the grid at a specific row and column
            add_to_watched_list.grid(row=rr + 2, column=0, sticky='n')
            #Create a button to add the movie to the watchlist with the add_buttonPhoto as its image
            #The command parameter calls the add_in_to_watch_list function with the movie name as its argument
            add_to_watchlist = ttk.Button(self, text='  Add to watchlist   ', image=self.add_buttonPhoto, compound=tk.LEFT,
                                          command=lambda: self.add_in_to_watch_list(movie_name))
            #Place the "Add to watchlist" button on the grid at a specific row and column
            add_to_watchlist.grid(row=rr+3, column=0, sticky='n')
            #Open the back.png image file and create a PhotoImage object
            back_buttonImage = Image.open('back.png')
            self.buttonPhoto = ImageTk.PhotoImage(back_buttonImage)
            
            #Create a button to go back to the main menu with the buttonPhoto as its image
            #The command parameter calls the reset function
            back_to_main = ttk.Button(self, text='Back to main menu', image=self.buttonPhoto, compound=tk.LEFT,
                                      command=self.reset)
            #Place the "Back to main menu" button on the grid at a specific row and column
            back_to_main.grid(row=rr+3, column=1, sticky='n')
            
            #Open the search.png image file and create a PhotoImage object
            search_buttonImage = Image.open('search.png')
            self.search_buttonPhoto = ImageTk.PhotoImage(search_buttonImage)
            #Create a button to search for a new movie with the search_buttonPhoto as its image
            #The command parameter calls the show_frame function to switch to the SearchBox frame
            search_new = ttk.Button(self, text='Search a movie', image=self.search_buttonPhoto, compound=tk.LEFT,
                                   command=lambda: masterframe.show_frame(SearchBox))
            #Place the "Search a movie" button on the grid at a specific row and column
            search_new.grid(row=rr+2, column=1, sticky='n')
            
            #Set the poster as the background image of the frame
            self.image(poster)
            #Create a label to display the poster image
            imagelabel = tk.Label(self, image=tk_image)
            #Place the image label on the grid at a specific row and column
            imagelabel.grid(column=0, row=0, rowspan=10)
        #If the movie is not found, handle the exception by displaying an error message and buttons to go back to the main menu or search for a new movie
        except:
             # Configure the first column of the grid to expand and take up all the available space
            self.grid_columnconfigure(0, weight=1)
            # Create a label to display the "Movie not found!" error message in bold Times font with a font size of 30
            error_label = ttk.Label(self, text='Movie not found!', font='Times 30 bold')
            # Place the error label on the grid at a specific row and column
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
        # function to add a movie to the watched list
        if new_movie_watched not in watched_list:
            watched_list.append(new_movie_watched)
            # saving the watched list to file using pickle
            with open('watched', 'wb') as w:
                pickle.dump(watched_list, w)

    def add_in_to_watch_list(self, new_movie_to_watchlist=''):
        # function to add a movie to the watchlist
        if new_movie_to_watchlist not in to_watch_list:
            to_watch_list.append(new_movie_to_watchlist)
            # saving the watchlist to file using pickle
            with open('watchlist', 'wb') as w:
                pickle.dump(to_watch_list, w)

    def comment_submit(self):
        # function to submit a comment
        pass

    def all_ratings(self, rate):
        # function to get all ratings for a movie and format them
        global ratings
        ratings = ''
        for i in range(len(rate)):
            ratings += rate[i]['Source'] + " :" + " " + rate[i]['Value'] + "    "
        return ratings

    def image(self,link):
        # function to retrieve and display a movie's poster image
        global tk_image
        try:
            url = link
            response = requests.get(url)
            tk_image = ImageTk.PhotoImage(Image.open(BytesIO(response.content)))
        except:
            # if an image can't be retrieved, use a default image
            url = 'https://lezzet.blob.core.windows.net/images-test/no-image.png'
            response = requests.get(url)
            tk_image = ImageTk.PhotoImage(Image.open(BytesIO(response.content)))

    def reset(self):
        # function to reset the application and return to the main menu
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
    
        # Initialize the parent class with the arguments
        super().__init__(parent, *args, **kwargs)
        
        # Set up grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Set parent instance variable
        self.parent = parent
        
        # Create vertical scrollbar and add it to the grid
        self.yscrlbr = ttk.Scrollbar(self.parent)
        self.yscrlbr.grid(column=1, row=0, sticky='ns')
        
        # Create a canvas and add it to the grid
        self.canv = tk.Canvas(self.parent)
        self.canv.config(relief='flat', width=10, heigh=10, bd=2)
        self.canv.grid(column=0, row=0, sticky='nsew')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Configure the scrollbar to move the canvas vertically
        self.yscrlbr.config(command=self.canv.yview)
        
        # Create a frame to hold the contents of the scrolled window
        self.scrollwindow = ttk.Frame(self.parent)
        
        # Add the scroll window frame to the canvas
        self.canv.create_window(0, 0, window=self.scrollwindow, anchor='nw')
        
        # Configure the canvas to use the scrollbar and set the scroll region
        self.canv.config(yscrollcommand=self.yscrlbr.set, scrollregion=(0, 0, 100, 100))
        
        # Bring the scrollbar to the front of the frame
        self.yscrlbr.lift(self.scrollwindow)
        
        # Bind events to the scroll window frame
        self.scrollwindow.bind('<Configure>', self._configure_window)
        self.scrollwindow.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollwindow.bind('<Leave>', self._unbound_to_mousewheel)
        
        return 
      
        # Method to bind the mousewheel to the scrollbar
        def _bound_to_mousewheel(self, event):
            self.canv.bind_all("<MouseWheel>", self._on_mousewheel)
            
        # Method to unbind the mousewheel from the scrollbar
        def _unbound_to_mousewheel(self, event):
            self.canv.unbind_all("<MouseWheel>")
        # Method to move the scrollbar when the mousewheel is used
        def _on_mousewheel(self, event):
            self.canv.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _configure_window(self, event):
          # Get the requested size of the scroll window
            size = (self.scrollwindow.winfo_reqwidth(), self.scrollwindow.winfo_reqheight())
            # Set the scroll region of the canvas to match the requested size of the scroll window
            self.canv.config(scrollregion='0 0 %s %s' % size)
            # If the requested width of the scroll window is different from the width of the canvas, adjust the canvas width
            if self.scrollwindow.winfo_reqwidth() != self.canv.winfo_width():
                self.canv.config(width=self.scrollwindow.winfo_reqwidth())
            # If the requested height of the scroll window is different from the height of the canvas, adjust the canvas height
            if self.scrollwindow.winfo_reqheight() != self.canv.winfo_height():
                self.canv.config(height=self.scrollwindow.winfo_reqheight())

 # Create a new instance of the Master class and start the main event loop of the application
 app = Master()
 app.mainloop()

# Try to destroy the application window and catch any errors that occur
try:
    app.destroy()
except tk.TclError:
    pass

# Set the file path of the login credentials
credentials = 'signup.txt'

# Define a function to create a signup window
def signup():
    # Declare global variables for the username and password entry fields, and the signup window
    global password_entry
    global name_entry
    global root_signup

    # Create a new Tkinter window for the signup process
    root_signup = tk.Tk()
    root_signup.title('Signup')
    root_signup.geometry('350x150+600+350')
    
    # Set the protocol for closing the window to call the login_exit function
    root_signup.protocol("WM_DELETE_WINDOW", lambda: login_exit(root_signup))
    
    # Create a label to display instructions for the user
    instruction = tk.Label(root_signup, text='Create a new account\n')
    instruction.grid(row=0, sticky='E')

    # Create labels and entry fields for the username and password
    name_label = tk.Label(root_signup, text='New Username: ')
    password_label = tk.Label(root_signup, text='New Password: ')
    name_label.grid(row=1, column=0, sticky='W')
    password_label.grid(row=2, column=0, sticky='W')

    name_entry = tk.Entry(root_signup)
    password_entry = tk.Entry(root_signup, show='*')
    name_entry.grid(row=1, column=1)
    password_entry.grid(row=2, column=1)

    # Create a button to finalize the signup process and call the finalize_signup function
    signup_button = ttk.Button(root_signup, text='Signup', command=finalize_signup)
    signup_button.grid(row=3, column=1, sticky='N')

    # Start the main event loop for the signup window
    root_signup.mainloop()

#This function is used to finalize the signup process and store the user's credentials
#in a file.
def finalize_signup():
    # Open the file for writing and write the user's name and password to it.
    with open(credentials, 'w') as file:
      file.write(name_entry.get())
      file.write('\n')
      file.write(password_entry.get())
      file.close()
    # Close the signup window and call the main function to display the main window.
    root_signup.destroy()
    main()

#This function is used to display the login window and allow the user to login or delete
#their account.
def login():
    # Declare global variables for the name and password entry fields, as well as the login window.
    global name_entry_label
    global password_entry_label
    global root_login

    # Create the login window with a title, size, and delete window protocol.
    root_login = tk.Tk()
    root_login.title('Login')
    root_login.geometry('350x150+600+350')
    root_login.protocol("WM_DELETE_WINDOW", lambda: login_exit(root_login))

    # Add a label to the login window to display instructions.
    instruction = tk.Label(root_login, text='Please Login\n')
    instruction.grid(sticky='E')

    # Add labels and entry fields for the user's name and password.
    name_label = tk.Label(root_login, text='Username: ')
    password_label = tk.Label(root_login, text='Password: ')
    name_label.grid(row=1, sticky='W')
    password_label.grid(row=2, sticky='W')
    name_entry_label = tk.Entry(root_login)
    password_entry_label = tk.Entry(root_login, show='*')
    name_entry_label.grid(row=1, column=1)
    password_entry_label.grid(row=2, column=1)

    # Add a button to allow the user to login with their credentials.
    login_button = ttk.Button(root_login, text='Login', command=check_login)
    login_button.grid(row=3, column=1, sticky='N')

    # Add a button to allow the user to delete their account.
    delete_user_button = ttk.Button(root_login, text='Delete User', command=delete_user)
    delete_user_button.grid(row=4, column=1, sticky='N')

    # Start the login window's event loop to display it to the user.
    root_login.mainloop()


# Function to check login credentials
def check_login():
    # Open the credentials file in read mode
    with open(credentials) as file:
        # Read the contents of the file
        data = file.readlines()
        # Extract the username and password from the data
        username = data[0].rstrip()
        password = data[1].rstrip()

    # If the entered username and password match the saved credentials
    if name_entry_label.get() == username and password_entry_label.get() == password:
        # Close the login window
        root_login.destroy()
        # Open the main window
        main()
    else:
        # If the credentials do not match, open a new window to display an error message
        r = tk.Tk()
        r.title('Error')
        r.geometry('100x50+600+350')
        # Create a label to display the error message
        error_label = tk.Label(r, text='\n[!] Invalid Login')
        # Clear the input fields
        name_entry_label.delete(0, 'end')
        password_entry_label.delete(0, 'end')
        # Add the error label to the window and display it
        error_label.pack()
        r.mainloop()

# Function to delete user account and associated files
def delete_user():
    # Remove the credentials file
    os.remove(credentials)
    # Check if the watched file exists, and remove it if it does
    if os.path.isfile('watched'):
        os.remove('watched')
    # Check if the watchlist file exists, and remove it if it does
    if os.path.isfile('watchlist'):
        os.remove('watchlist')
    # Close the login window
    root_login.destroy()
    # Open the signup window
    signup()

# Function to handle the exit of the login window
def login_exit(root):
    # Ask the user if they want to quit
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        # Close the login window and exit the program
        root.destroy()
        exit(0)

# Check if the credentials file exists
if os.path.isfile(credentials):
    # If it does, open the login window
    login()
else:
    # If it doesn't, open the signup window
    signup()

# Call the main function
if __name__ == '__main__':
    main()
