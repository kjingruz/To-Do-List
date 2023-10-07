import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
from datetime import datetime


def load_tasks():
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not filepath:
        return

    df = pd.read_csv(filepath)

    for tree in [tree_all, tree_today]:
        for row in tree.get_children():
            tree.delete(row)

    for _, row in df.iterrows():
        date, time_slot, task = row["Date"], row["Time Slot"], row["Task"]
        tree_all.insert("", tk.END, values=(date, time_slot, task))
        if date == today_date:
            tree_today.insert("", tk.END, values=(date, time_slot, task))


def mark_done(tree):
    selected = tree.selection()[0]
    tree.item(selected, tags=("done",))


def remove_task(tree):
    selected = tree.selection()[0]
    tree.delete(selected)


# Initialize the Tkinter window
root = tk.Tk()
root.title("Reading Week To-Do List")

# Create Notebook for tabs
notebook = ttk.Notebook(root)
notebook.pack(pady=20)

frame_all = ttk.Frame(notebook, width=480, height=460)
frame_today = ttk.Frame(notebook, width=480, height=460)

frame_all.pack(fill="both", expand=1)
frame_today.pack(fill="both", expand=1)

notebook.add(frame_all, text="All Tasks")
notebook.add(frame_today, text="Today's Tasks")

# Add a label
label_all = ttk.Label(frame_all, text="All Tasks", font=("Arial", 20))
label_all.pack(pady=20)

label_today = ttk.Label(frame_today, text="Today's Tasks", font=("Arial", 20))
label_today.pack(pady=20)

# Create Treeview
columns = ("Date", "Time Slot", "Task")
tree_all = ttk.Treeview(frame_all, columns=columns, show="headings")
tree_today = ttk.Treeview(frame_today, columns=columns, show="headings")

for tree in [tree_all, tree_today]:
    tree.heading("#1", text="Date")
    tree.heading("#2", text="Time Slot")
    tree.heading("#3", text="Task")
    tree.pack(pady=20)

# Create button frame for each tab
button_frame_all = ttk.Frame(frame_all)
button_frame_all.pack(side=tk.BOTTOM, fill=tk.X)

button_frame_today = ttk.Frame(frame_today)
button_frame_today.pack(side=tk.BOTTOM, fill=tk.X)

# Add buttons to mark tasks as done and remove tasks
for frame in [button_frame_all, button_frame_today]:
    btn_done = ttk.Button(frame, text="Mark as Done", command=lambda t=tree: mark_done(t))
    btn_done.pack(side=tk.LEFT, padx=10, pady=10)

    btn_remove = ttk.Button(frame, text="Remove Task", command=lambda t=tree: remove_task(t))
    btn_remove.pack(side=tk.LEFT, padx=10, pady=10)

# Add a tag to style completed tasks
tree_all.tag_configure("done", background="light green")
tree_today.tag_configure("done", background="light green")

# Add Load Button
btn_load = ttk.Button(root, text="Load Tasks", command=load_tasks)
btn_load.pack(pady=20)

# Get today's date to filter tasks for the "Today's Tasks" tab
today_date = datetime.now().strftime('%Y-%m-%d')

# Run the Tkinter event loop
root.mainloop()
# Function to save tasks from the Treeview widget to a CSV file
def save_tasks(tree):
    tasks = []
    for row in tree.get_children():
        tasks.append(tree.item(row, "values"))
    if tasks:  # Check if the list is not empty
        df = pd.DataFrame(tasks, columns=["Date", "Time Slot", "Task"])
        df.to_csv("saved_tasks.csv", index=False)
    else:
        if os.path.exists("saved_tasks.csv"):  # Remove the saved file if no tasks are left
            os.remove("saved_tasks.csv")

