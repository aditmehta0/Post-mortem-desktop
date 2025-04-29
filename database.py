import sqlite3
from pathlib import Path

# Initialize database with full schema
def init_db(db_path):
    first_time = not Path(db_path).exists()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if first_time:
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            owner TEXT,
            status TEXT,
            start_date TEXT,
            end_date TEXT
        );

        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            risk TEXT,
            failure TEXT,
            root_cause TEXT,
            lessons_learned TEXT,
            severity TEXT,
            mitigation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE
        );
        """)
        conn.commit()

    return conn

# Project operations
def get_projects(cursor):
    return cursor.execute("SELECT id, name, description, owner, status, start_date, end_date FROM projects ORDER BY id DESC").fetchall()

def add_project(cursor, name, description, owner, status, start_date, end_date):
    cursor.execute(
        "INSERT INTO projects (name, description, owner, status, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)",
        (name, description, owner, status, start_date, end_date)
    )

# Story operations
def get_stories(cursor, project_id):
    return cursor.execute(
        "SELECT title, description, risk, failure, root_cause, lessons_learned, severity, mitigation, created_at FROM stories WHERE project_id = ? ORDER BY created_at DESC",
        (project_id,)
    ).fetchall()

def add_story(cursor, project_id, title, description, risk, failure, root_cause, lessons_learned, severity, mitigation):
    cursor.execute(
        "INSERT INTO stories (project_id, title, description, risk, failure, root_cause, lessons_learned, severity, mitigation) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (project_id, title, description, risk, failure, root_cause, lessons_learned, severity, mitigation)
    )
