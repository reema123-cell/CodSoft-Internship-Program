import tkinter as tk
from tkinter import messagebox
import pickle
from datetime import datetime

class Task:
    def __init__(self, title, description="", priority="Low", due_date=None, completed=False):
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = completed

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.tasks = self.load_tasks()
        self.render_tasks()

        self.title_entry = tk.Entry(root, width=40)
        self.title_entry.grid(row=0, column=0, padx=5, pady=5)

        add_button = tk.Button(root, text="Add Task", command=self.add_task)
        add_button.grid(row=0, column=1, padx=5, pady=5)

    def load_tasks(self):
        try:
            with open("tasks.pkl", "rb") as file:
                tasks = pickle.load(file)
        except FileNotFoundError:
            tasks = []
        return tasks

    def save_tasks(self):
        with open("tasks.pkl", "wb") as file:
            pickle.dump(self.tasks, file)

    def render_tasks(self):
        for i, task in enumerate(self.tasks):
            task_frame = tk.Frame(self.root)
            task_frame.grid(row=i+1, column=0, padx=5, pady=5, sticky="w")

            title_label = tk.Label(task_frame, text=task.title)
            title_label.grid(row=0, column=0, sticky="w")

            complete_button = tk.Button(task_frame, text="Complete" if not task.completed else "Active",
                                         command=lambda t=task: self.toggle_completion(t))
            complete_button.grid(row=0, column=1, padx=5, sticky="w")

            edit_button = tk.Button(task_frame, text="Edit", command=lambda t=task: self.edit_task(t))
            edit_button.grid(row=0, column=2, padx=5, sticky="w")

            delete_button = tk.Button(task_frame, text="Delete", command=lambda t=task: self.delete_task(t))
            delete_button.grid(row=0, column=3, padx=5, sticky="w")

    def add_task(self):
        title = self.title_entry.get().strip()
        if title:
            new_task = Task(title)
            self.tasks.append(new_task)
            self.save_tasks()
            self.render_tasks()
            self.title_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task title.")

    def edit_task(self, task):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Task")

        tk.Label(edit_window, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        title_entry = tk.Entry(edit_window, width=40)
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        title_entry.insert(tk.END, task.title)

        tk.Label(edit_window, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        description_entry = tk.Entry(edit_window, width=40)
        description_entry.grid(row=1, column=1, padx=5, pady=5)
        description_entry.insert(tk.END, task.description)

        save_button = tk.Button(edit_window, text="Save",
                            command=lambda: self.save_edited_task(task, title_entry.get(), description_entry.get(), edit_window))
        save_button.grid(row=2, columnspan=2, padx=5, pady=5)

    def save_edited_task(self, task, new_title, new_description, edit_window):
        task.title = new_title
        task.description = new_description
        self.save_tasks()
        self.render_tasks()
        edit_window.destroy()

    def delete_task(self, task):
        confirmation = messagebox.askokcancel("Delete Task", f"Are you sure you want to delete task '{task.title}'?")
        if confirmation:
            self.tasks.remove(task)
            self.save_tasks()
            for widget in self.root.winfo_children():
                widget.destroy()
            self.render_tasks()

    def toggle_completion(self, task):
        task.completed = not task.completed
        self.save_tasks()
        self.render_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
