import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re


class DatabaseManager:
    def __init__(self, db_name="profiles.db"):
        self.db_name = db_name
        self.conn = None
        self.create_table()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS person_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            city TEXT NOT NULL,
            age INTEGER NOT NULL,
            occupation TEXT NOT NULL
        )
        """
        conn = self.connect()
        conn.execute(query)
        conn.commit()
        self.close()

    def insert_profile(self, full_name, email, phone, city, age, occupation):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO person_profiles VALUES (NULL, ?, ?, ?, ?, ?, ?)",
                (full_name, email, phone, city, age, occupation)
            )
            conn.commit()
            return True, "Profile added successfully!"
        except Exception as e:
            return False, f"Error adding profile: {str(e)}"
        finally:
            self.close()

    def fetch_all_profiles(self):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM person_profiles")
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return []
        finally:
            self.close()

    def update_profile(self, profile_id, full_name, email, phone, city, age, occupation):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE person_profiles
                SET full_name=?, email=?, phone=?, city=?, age=?, occupation=?
                WHERE id=?
            """, (full_name, email, phone, city, age, occupation, profile_id))
            conn.commit()
            return True, "Profile updated successfully!"
        except Exception as e:
            return False, f"Error updating profile: {str(e)}"
        finally:
            self.close()

    def delete_profile(self, profile_id):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM person_profiles WHERE id=?", (profile_id,))
            conn.commit()
            return True, "Profile deleted successfully!"
        except Exception as e:
            return False, f"Error deleting profile: {str(e)}"
        finally:
            self.close()

    def search_profiles(self, keyword):

        all_profiles = self.fetch_all_profiles()
        keyword = keyword.lower()
        return [
            p for p in all_profiles
            if keyword in p[1].lower()  # full_name
            or keyword in p[4].lower()  # city
            or keyword in p[6].lower()  # occupation
        ]

class ProfileApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Person Profile Management System")
        self.root.geometry("1000x600")
        self.db = DatabaseManager()
        self.selected_id = None

        
        self.email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

        
        self.build_ui()
        self.load_profiles()

    def build_ui(self):
        
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    
        left_frame = ttk.Frame(paned, width=350)
        left_frame.pack(fill=tk.BOTH, expand=True)
        paned.add(left_frame, weight=1)

        ttk.Label(left_frame, text="Profile Entry Form", font=("Arial", 12, "bold")).pack(pady=10)

      
        self.entries = {}
        fields = [
            ("Full Name", "full_name"),
            ("Email Address", "email"),
            ("Phone Number", "phone"),
            ("City", "city"),
            ("Age", "age"),
            ("Occupation", "occupation")
        ]

        
