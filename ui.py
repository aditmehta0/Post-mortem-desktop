import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

def build_ui(root, db):
    root.title("Post-Mortem Dashboard")
    root.geometry("1000x720")

    # Logo image
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        img = Image.open(logo_path).resize((120, 120))
        logo = ImageTk.PhotoImage(img)
        logo_label = ttk.Label(root, image=logo)
        logo_label.image = logo
        logo_label.pack(pady=5)

    ### Project Creation Frame ###
    proj_frame = ttk.LabelFrame(root, text="Create New Project")
    proj_frame.pack(fill="x", padx=10, pady=5)

    fields = {}
    labels = ["Name", "Description", "Owner", "Status", "Start Date", "End Date"]
    for i, lbl in enumerate(labels):
        ttk.Label(proj_frame, text=f"{lbl}:").grid(row=i, column=0, sticky="w")
        ent = ttk.Entry(proj_frame, width=50) if lbl != "Description" else tk.Text(proj_frame, height=3, width=38)
        ent.grid(row=i, column=1, padx=5, pady=2)
        fields[lbl.lower().replace(" ", "_")] = ent

    def create_project():
        vals = []
        for key in ["name", "description", "owner", "status", "start_date", "end_date"]:
            if isinstance(fields[key], tk.Text):
                vals.append(fields[key].get("1.0", tk.END).strip())
            else:
                vals.append(fields[key].get())
        if not vals[0]:
            messagebox.showwarning("Required", "Project name required.")
            return
        db.insert_project(*vals)
        messagebox.showinfo("Saved", "Project added.")
        refresh_projects()
        for f in fields.values():
            if isinstance(f, tk.Text): f.delete("1.0", tk.END)
            else: f.delete(0, tk.END)

    ttk.Button(proj_frame, text="Create", command=create_project).grid(row=6, column=1, sticky="e")

    ### Project List Frame ###
    view_frame = ttk.LabelFrame(root, text="Projects and Stories")
    view_frame.pack(fill="both", expand=True, padx=10, pady=5)

    search_var = tk.StringVar()
    search_entry = ttk.Entry(view_frame, textvariable=search_var, width=40)
    search_entry.pack(side="left", padx=10, pady=5)
    ttk.Button(view_frame, text="Search", command=lambda: refresh_projects(search_var.get())).pack(side="left")

    tree = ttk.Treeview(view_frame, columns=("desc",), show="tree")
    tree.heading("#0", text="Projects / Stories")
    tree.pack(fill="both", expand=True)

    def refresh_projects(query=""):
        tree.delete(*tree.get_children())
        for proj in db.get_projects():
            pid, name, *extra = proj
            if query.lower() not in name.lower():
                continue
            node = tree.insert("", "end", text=f"📁 {name} ({extra[1]})", open=False)
            for s in db.get_stories_by_project(pid):
                title, desc, risk, fail, root, learn, sev, mit, created = s
                summary = f"📝 {title} ({created})\n- Desc: {desc}\n- Risk: {risk}\n- Failure: {fail}\n- Root: {root}\n- Learn: {learn}\n- Severity: {sev}\n- Mitigation: {mit}"
                tree.insert(node, "end", text=summary)

    ### Add Story Frame ###
    story_frame = ttk.LabelFrame(root, text="Add Story to Project")
    story_frame.pack(fill="x", padx=10, pady=5)

    story_fields = {}
    story_labels = ["Project", "Title", "Description", "Risk", "Failure", "Root Cause", "Lessons Learned", "Severity", "Mitigation"]

    proj_var = tk.StringVar()
    proj_combo = ttk.Combobox(story_frame, textvariable=proj_var, state="readonly", width=47)
    proj_combo.grid(row=0, column=1, sticky="w")
    story_fields["project"] = proj_combo
    ttk.Label(story_frame, text="Project:").grid(row=0, column=0, sticky="w")

    for i, lbl in enumerate(story_labels[1:], start=1):
        ttk.Label(story_frame, text=f"{lbl}:").grid(row=i, column=0, sticky="nw")
        ent = tk.Text(story_frame, width=50, height=2)
        ent.grid(row=i, column=1, pady=2)
        story_fields[lbl.lower().replace(" ", "_")] = ent

    def load_project_choices():
        choices = db.get_projects()
        proj_combo["values"] = [f"{p[0]}: {p[1]}" for p in choices]

    def add_story():
        try:
            pid = int(proj_var.get().split(":")[0])
        except:
            messagebox.showerror("Error", "Select valid project")
            return
        vals = [story_fields[key].get("1.0", tk.END).strip() for key in list(story_fields.keys())[1:]]
        if not vals[0]:
            messagebox.showwarning("Missing", "Title is required")
            return
        db.insert_story(pid, *vals)
        messagebox.showinfo("Success", "Story added")
        for f in story_fields.values():
            if isinstance(f, tk.Text): f.delete("1.0", tk.END)
        refresh_projects()

    ttk.Button(story_frame, text="Add Story", command=add_story).grid(row=9, column=1, sticky="e", pady=5)
    root.bind("<FocusIn>", lambda e: load_project_choices())
    refresh_projects()