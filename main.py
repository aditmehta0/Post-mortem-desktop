import tkinter as tk
import database
import ui

class DB:
    def __init__(self, db_path):
        self.conn = database.init_db(db_path)
        self.cursor = self.conn.cursor()

    def get_projects(self):
        return database.get_projects(self.cursor)

    def get_stories_by_project(self, pid):
        return database.get_stories(self.cursor, pid)

    def insert_project(self, name, desc, owner, status, start_date, end_date):
        database.add_project(self.cursor, name, desc, owner, status, start_date, end_date)
        self.conn.commit()

    def insert_story(self, pid, title, desc, risk, failure, root_cause, lessons_learned, severity, mitigation):
        database.add_story(self.cursor, pid, title, desc, risk, failure, root_cause, lessons_learned, severity, mitigation)
        self.conn.commit()

if __name__ == "__main__":
    import tkinter.filedialog as fd
    import os

    root = tk.Tk()
    root.withdraw()

    if tk.messagebox.askyesno("Select Database", "Do you want to create a new database?\nPress NO to open an existing database."):
        db_path = fd.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite DB", "*.db")], title="Create New Database")
    else:
        db_path = fd.askopenfilename(defaultextension=".db", filetypes=[("SQLite DB", "*.db")], title="Open Existing Database")

    if not db_path:
        tk.messagebox.showinfo("Exit", "No database selected. Exiting.")
        root.destroy()
        exit()

    root.deiconify()
    db = DB(db_path)
    ui.build_ui(root, db)
    root.mainloop()
