import tkinter as tk
from PIL import ImageTk
from numpy import random
import sqlite3

#define the bg colour
bg_colour="#FF8C00"

def clear_widgets(frame):
	# select all frame widgets and delete them
	for widget in frame.winfo_children():
		widget.destroy()
def fetch_db():
      connection  = sqlite3.connect("data/recipes.sqlite")
      cursor = connection.cursor()
      cursor.execute("SELECT * FROM sqlite_schema WHERE type ='table';")
      all_tables = cursor.fetchall()
      idx = random.randint(0, len(all_tables)-1)
      #fetch ingredients
      table_name = all_tables[idx][1]
      cursor.execute("SELECT * FROM " + table_name + ';')
      table_records = cursor.fetchall()
      connection.close()
      return table_name, table_records
def pre_process(table_name, table_records):
      title = table_name[:-6]
      title = "".join([char if char.islower() else "" + char for char in title])
      #ingredients
      ingredients = []
      for i in table_records:
            name = i[1]
            qty =  i[2]
            unit = i[3]
            ingredients.append(qty + "" + unit + "of" + name)
      return title, ingredients

def load_frame1():
    clear_widgets(frame2)
    frame2.tkraise()
    frame1.pack_propagate(False)
    #frame widgets
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo.png")
    logo_widget = tk.Label(frame1, image=logo_img, bg=bg_colour)
    logo_widget.image = logo_img
    logo_widget.pack()

    tk.Label(
            frame1,
            text="Are you ready for your random recipe?",
            bg=bg_colour,
            fg="black",
            font=("TKMenuFont", 14)
            ).pack()
    #button widget
    tk.Button(
        frame1,
        text="Click here to get it",
        font=("TKHeadingFONT", 20), 
        bg="#28393a",
        fg="white",
        cursor="hand2", 
        activebackground="#badee2", 
        activeforeground="black",
        command=lambda:load_frame2()
        ).pack(pady=20)
    



def load_frame2():
      clear_widgets(frame1)
      frame2.tkraise()
      table_name, table_records = fetch_db()
      title, ingredients = pre_process(table_name, table_records)
      #frame widgets
      logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo_bottom.png")
      logo_widget = tk.Label(frame2, image=logo_img, bg=bg_colour)
      logo_widget.image = logo_img
      logo_widget.pack(pady=20) 
      tk.Label(
            frame2,
            text=title,
            bg=bg_colour,
            fg="black",
            font=("TKHeadingFont", 14)
            ).pack(pady=25) 
      for i in ingredients:
            tk.Label(
            frame2,
            text=i,
            bg=bg_colour,
            fg="white",
            font=("TKMenuFont", 12)
            ).pack() 
            
      tk.Button(
        frame2,
        text="BACK",
        font=("TKHeadingFONT", 18), 
        bg="#28393a",
        fg="white",
        cursor="hand2", 
        activebackground="#badee2", 
        activeforeground="black",
        command=lambda:load_frame1()
        ).pack(pady=20)                         
# initiallize app
root = tk.Tk()
root.title("Random Recipe Picker")
root.eval("tk::PlaceWindow . center")
frame1 = tk.Frame(root, width=500, height=600, bg=bg_colour)
frame2 = tk.Frame(root, bg=bg_colour)
for frame in (frame1, frame2):
    frame.grid(row=0, column=0)
    #sticky="nesw")

load_frame1()

# run app
root.mainloop()