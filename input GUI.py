import os
import tkinter as tk
from tkinter import *
from tkinter import messagebox

class App(object):
    def __init__(self, window):

        window.wm_title("Travel Assistant")
        self.current_row=0

        # Hotel address
        self.home_label=tk.Label(window,text="Your hotel address:")
        self.home_label.grid(row=self.current_row, column=0)
        self.home_text=tk.StringVar()
        self.home_entry=tk.Entry(window, textvariable=self.home_text)
        self.home_entry.grid(row=self.current_row, column=1)
        self.current_row+=1

        #place have been 
        self.phb_label=tk.Label(window,text="Places that you have been to:")
        self.phb_label.grid(row=self.current_row, column=0)
        self.phb_entry=  Menubutton (window, text="Please select", relief=RAISED )
        self.phb_entry.grid(row=self.current_row, column=1)
        self.phb_entry.menu  =  Menu ( self.phb_entry, tearoff = 0 )
        self.phb_entry["menu"]  =  self.phb_entry.menu
#       Item0 = IntVar()
        #####----------change this-----------####
        self.phb_entry.menu.add_checkbutton ( label="Item0", variable=Item0)
        self.phb_entry.menu.add_checkbutton ( label="Item1", variable=Item1)
        self.phb_entry.menu.add_checkbutton ( label="Item2", variable=Item2)
        self.current_row+=1
        
        #place_to_go
        self.ptg_label=tk.Label(window,text="Places that you want to go:")
        self.ptg_label.grid(row=self.current_row, column=0)
        self.ptg_entry=  Menubutton (window, text="Please select", relief=RAISED )
        self.ptg_entry.grid(row=self.current_row, column=1)
        self.ptg_entry.menu  =  Menu ( self.ptg_entry, tearoff = 0 )
        self.ptg_entry["menu"]  =  self.ptg_entry.menu
        #####----------change this-----------####
        self.ptg_entry.menu.add_checkbutton ( label="Item0", variable=Item0)
        self.ptg_entry.menu.add_checkbutton ( label="Item1", variable=Item1)
        self.ptg_entry.menu.add_checkbutton ( label="Item2", variable=Item2)
        self.current_row+=1

        #duration
        self.duration_label=tk.Label(window,text="Your everyday travel duration is:")
        self.duration_label.grid(row=self.current_row, column=0)
        self.duration_text=tk.IntVar()
        self.duration_entry=tk.Entry(window, textvariable=self.duration_text)
        self.duration_entry.grid(row=self.current_row, column=1)
        self.current_row+=1
        
        #citypass
        self.cp_label=tk.Label(window,text="Did you buy citypass:")
        self.cp_label.grid(row=self.current_row, column=0)
        #####----------change this-----------####
        list_=["Yes", "No"]
        self.cp_text=StringVar()
        self.cp_entry=OptionMenu(window, self.cp_text, *list_)
        self.cp_entry.grid(row=self.current_row, column=1)
        self.current_row+=1
        
        #sort
        self.sort_label=tk.Label(window,text="Sort by:")
        self.sort_label.grid(row=self.current_row, column=0)
        #####----------change this-----------####
        list_=["Distance", "Duration","Museum", "Park"]
        self.sort_text=StringVar()
        self.sort_entry=OptionMenu(window, self.sort_text, *list_)
        self.sort_entry.grid(row=self.current_row, column=1)
        self.current_row+=1
        

        #OK button
        self.query_button=tk.Button(window, text="OK")
        self.query_button.configure(command=self.fetch)
        self.query_button.grid(row=self.current_row, column=0, columnspan=1)
        #self.current_row+=1

        #quit button
        self.quit_button=tk.Button(window, text="Quit")
        self.quit_button.configure(command=quit)
        self.quit_button.grid(row=self.current_row, column=1, columnspan=1)
        self.current_row+=1
    
    def fetch(self):
        
        #create local variable
        fname=self.fname_text.get()
        lname=self.lname_text.get()
        age=self.age_text.get()
        sex=self.sex_text.get()
        income=self.income_text.get()


            
#define main class implement execution loop
def main():
    window=tk.Tk()
    start=App(window)
    window.mainloop()

#run the main function
if __name__=="__main__":
    main()

