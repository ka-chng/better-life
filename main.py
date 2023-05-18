import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

conn = sqlite3.connect('todo_list.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS tasks
            (id INTEGER PRIMARY KEY, task TEXT, date_added TEXT, due_date TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS groceries
            (id INTEGER PRIMARY KEY, item TEXT, date_added TEXT)''')
conn.commit()

def add_task():
    task = task_entry.get()
    due_date = due_date_entry.get()

    if task and due_date:
        c.execute("INSERT INTO tasks (task, date_added, due_date) VALUES (?, ?, ?)", (task, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), due_date))
        conn.commit()
        task_entry.delete(0, tk.END)
        due_date_entry.delete(0, tk.END)
        load_tasks()
    else:
        messagebox.showerror("Error", "Please enter a task and due date.")

def load_tasks():
    tasks_list.delete(0, tk.END)
    for row in c.execute("SELECT * FROM tasks"):
        tasks_list.insert(tk.END, f"{row[0]} - {row[1]} (Added: {row[2]}, Due: {row[3]})")

def remove_task():
    selected_task = tasks_list.curselection()
    if selected_task:
        task_id = tasks_list.get(selected_task)[0]
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        load_tasks()
    else:
        messagebox.showerror("Error", "Please select a task to remove.")

def add_grocery():
    item = grocery_entry.get()

    if item:
        c.execute("INSERT INTO groceries (item, date_added) VALUES (?, ?)", (item, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        grocery_entry.delete(0, tk.END)
        load_groceries()
    else:
        messagebox.showerror("Error", "Please enter a grocery item.")

def load_groceries():
    groceries_list.delete(0, tk.END)
    for row in c.execute("SELECT * FROM groceries"):
        groceries_list.insert(tk.END, f"{row[0]} - {row[1]} (Added: {row[2]})")

def remove_grocery():
    selected_grocery = groceries_list.curselection()
    if selected_grocery:
        grocery_id = groceries_list.get(selected_grocery)[0]
        c.execute("DELETE FROM groceries WHERE id=?", (grocery_id,))
        conn.commit()
        load_groceries()
    else:
        messagebox.showerror("Error", "Please select a grocery item to remove.")

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    update_theme()

def update_theme():
    if dark_mode:
        bg_color = "#2c2c2c"
        fg_color = "#ffffff"
        select_bg_color = "#3c3c3c"
    else:
        bg_color = "#ffffff"
        fg_color = "#000000"
        select_bg_color = "#c0c0c0"

    root.configure(bg=bg_color)

    task_label.config(bg=bg_color, fg=fg_color)
    task_entry.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)

    due_date_label.config(bg=bg_color, fg=fg_color)
    due_date_entry.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)

    add_button.config(bg=bg_color, fg=fg_color, activebackground=select_bg_color, activeforeground=fg_color)
    remove_button.config(bg=bg_color, fg=fg_color, activebackground=select_bg_color, activeforeground=fg_color)
    toggle_theme_button.config(bg=bg_color, fg=fg_color, activebackground=select_bg_color, activeforeground=fg_color)

    tasks_list.config(bg=bg_color, fg=fg_color, selectbackground=select_bg_color, selectforeground=fg_color)

    grocery_label.config(bg=bg_color, fg=fg_color)
    grocery_entry.config(bg=bg_color, fg=fg_color, insertbackground=fg_color)

    add_grocery_button.config(bg=bg_color, fg=fg_color, activebackground=select_bg_color, activeforeground=fg_color)
    remove_grocery_button.config(bg=bg_color, fg=fg_color, activebackground=select_bg_color, activeforeground=fg_color)

    groceries_list.config(bg=bg_color, fg=fg_color, selectbackground=select_bg_color, selectforeground=fg_color)

root = tk.Tk()
root.title("To-Do List and Groceries")

task_label = tk.Label(root, text="Task:")
task_label.grid(row=0, column=0, padx=5, pady=5)
task_entry = tk.Entry(root)
task_entry.grid(row=0, column=1, padx=5, pady=5)

due_date_label = tk.Label(root, text="Due Date (YYYY-MM-DD):")
due_date_label.grid(row=1, column=0, padx=5, pady=5)
due_date_entry = tk.Entry(root)
due_date_entry.grid(row=1, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.grid(row=2, column=1, padx=5, pady=5)

remove_button = tk.Button(root, text="Remove Task", command=remove_task)
remove_button.grid(row=2, column=0, padx=5, pady=5)

toggle_theme_button = tk.Button(root, text="Toggle Theme", command=toggle_theme)
toggle_theme_button.grid(row=2, column=2, padx=5, pady=5)

tasks_list = tk.Listbox(root, width=80)
tasks_list.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

grocery_label = tk.Label(root, text="Grocery Item:")
grocery_label.grid(row=4, column=0, padx=5, pady=5)
grocery_entry = tk.Entry(root)
grocery_entry.grid(row=4, column=1, padx=5, pady=5)

add_grocery_button = tk.Button(root, text="Add Grocery", command=add_grocery)
add_grocery_button.grid(row=5, column=1, padx=5, pady=5)

remove_grocery_button = tk.Button(root, text="Remove Grocery", command=remove_grocery)
remove_grocery_button.grid(row=5, column=0, padx=5, pady=5)

groceries_list = tk.Listbox(root, width=80)
groceries_list.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

dark_mode = True
update_theme()
load_tasks()
load_groceries()

root.mainloop()

conn.close()
