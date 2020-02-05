'''
File : entry.py
Name : Ethan Salcedo
Date : 12/25/2019
'''

import tkinter as tk
#without this line you would have to call tkinter in every instance that 'tk' is used
import sqlite3
import csv
from tkcalendar import Calendar, DateEntry

LARGE_FONT = ('Verdana', 12) # font's family is Verdana, font's size is 12
conn = sqlite3.connect('foodinfo.db')
cur = conn.cursor()

def number_check(entry):
    return entry.isdigit()

def delete_database():
    conn.execute('''DROP TABLE food''')

def create_food_database():
    conn.execute('''CREATE TABLE IF NOT EXISTS food(food_id integer primary key, name text NOT NULL, serving_size text NOT NULL, calories int, protein int, sugar int)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS food_log(entry_id integer primary key, food_date datetime, calories int, protein int, sugar int)''')


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Beginner Food Log') # set the title of the main window
        self.geometry('300x350') # set size of the main window to 300x300 pixels
        self.resizable(False, False)
        # this container contains all the pages
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)   # make the cell in grid cover the entire window
        container.grid_columnconfigure(0,weight=1) # make the cell in grid cover the entire window
        self.frames = {} # these are pages we want to navigate to

        for F in (HomePage, AddPage, DataPage, GoalPage, ViewPage, SettingsPage): # for each page
            frame = F(container, self) # create the page
            self.frames[F] = frame  # store into frames
            frame.grid(row=0, column=0, sticky='nsew') # grid it to container

        self.show_frame(HomePage) # let the first page is StartPage

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Welcome to your log! \n ...hopefully you have good news...', font=LARGE_FONT, pady=10)
        label.grid(row=1, column=1, sticky='NSEW') # center alignment

        button1 = tk.Button(self, text='Log Food',  # when click on this button, call the show_frame method to make PageOne appear
                            command=lambda : controller.show_frame(AddPage))
        button1.grid(row=2, column=1, padx=5, pady=5) # pack it in
        button2 = tk.Button(self, text='Add to Database',
                            command=lambda : controller.show_frame(DataPage))
        button2.grid(row=3, column=1, padx=5, pady=5)
        button3 = tk.Button(self, text='Adjust Goals',
                            command=lambda : controller.show_frame(GoalPage))
        button3.grid(row=4, column=1, padx=5, pady=5)
        button4 = tk.Button(self, text='View Database',
                            command=lambda : controller.show_frame(ViewPage))
        button4.grid(row=5, column=1, padx=5, pady=5)
        button5 = tk.Button(self, text='Settings',
                            command=lambda : controller.show_frame(SettingsPage))
        button5.grid(row=6, column=1, padx=5, pady=5)

class AddPage(tk.Frame):
    def __init__(self, parent, controller):
        #use tkcalendar to allow users to input a date-time for each logged food
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Log Page', font=LARGE_FONT, pady=10)
        label.grid(row=2, column=1, sticky='NSEW')
        label02 = tk.Label(self, text='Food/Drink Name:')
        label02.grid(row=2, column=1, sticky='NSEW', pady=5)
        entry01 = tk.Entry(self)
        entry01.grid(row=2, column=2, sticky='NSEW', pady=5)
        button1 = tk.Button(self, text='Back to Home', # likewise StartPage
                            command=lambda : controller.show_frame(HomePage))
        button1.grid(row=3, column=1, sticky='NSEW')

class GoalPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Nutritional Goals', font=LARGE_FONT, pady=10)
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text='Back to Home', # likewise StartPage
                            command=lambda : controller.show_frame(HomePage))
        button1.pack()

def validate(entry):
    return entry.isnumeric()

def print_db():
    cur.execute('SELECT * FROM food')
    print(cur.fetchall())
#page to view the database
class ViewPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='View Database Page', font=LARGE_FONT, padx=10, pady=10)
        label.pack(padx=10, pady=10)
        view_button = tk.Button(self, text='Print Database',
                                    command=lambda : print_db())
        view_button.pack(padx=10, pady=10)
        home_button = tk.Button(self, text='Back to Home', # likewise StartPage
                                    command=lambda : controller.show_frame(HomePage))
        home_button.pack(padx=10, pady=10)

'''
This class represents the page where you add foods to the database.
'''

class DataPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Add to Database', font=LARGE_FONT, padx=10, pady=10)
        label.grid(row=1, column=2, sticky='NSEW', pady=10)

        name_label = tk.Label(self, text='Name :')
        name_label.grid(row=2, column=1, sticky='NSEW')
        e1 = tk.Entry(self)
        e1.grid(row=2, column=2, sticky='NSEW', pady=5)

        serv_label = tk.Label(self, text='Serving Size :')
        serv_label.grid(row=3, column=1, sticky='NSEW')
        e2 = tk.Entry(self)
        e2.grid(row=3, column=2, sticky='NSEW', pady=5)

        cal_label = tk.Label(self, text='Calories :')
        cal_label.grid(row=4, column=1,sticky='NSEW')
        e3 = tk.Entry(self)
        e3.grid(row=4, column=2, sticky='NSEW', pady=5)

        pro_label = tk.Label(self, text='Protein(g) :')
        pro_label.grid(row=5, column=1, sticky='NSEW')
        e4 = tk.Entry(self)
        e4.grid(row=5, column=2, sticky='NSEW', pady=5)

        carb_label = tk.Label(self, text='Sugar(g) :')
        carb_label.grid(row=6, column=1, sticky='NSEW')
        e5 = tk.Entry(self)
        e5.grid(row=6, column=2, sticky='NSEW', pady=5)

        button2 = tk.Button(self, text='Submit to Database',
                            command=lambda : getFoodEntry())
        button2.grid(row=8, column=2, stick='NSEW', pady=5)

        button1 = tk.Button(self, text='Back to Home', # likewise StartPage
                            command=lambda : controller.show_frame(HomePage))
        button1.grid(row=9, column=2, sticky='NSEW', pady=5)

        def getFoodEntry():
            p1 = e1.get()
            p2 = e2.get()
            p3 = e3.get()
            p4 = e4.get()
            p5 = e5.get()
            try:
                conn.execute('''INSERT into food (name, serving_size, calories, protein, sugar) values (?, ?, ?, ?, ?)''',
                                (p1, p2, int(p3), int(p4), int(p5)))
            except:
                print('Sorry your entry did not meet the data guidelines ')

            conn.commit()
class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Settings', font=LARGE_FONT, pady=10)
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text='Back to Home',
                            command=lambda : controller.show_frame(HomePage))
        button1.pack()

if __name__ == '__main__':
    create_food_database()
    app = MainWindow()
    app.mainloop()
