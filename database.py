import sqlite3
import os
import sys
import csv
from datetime import datetime


def get_base_dir():
    """Get the directory where the app is running from"""
    if getattr(sys, 'frozen', False):
        # Running as compiled exe
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()
DB_PATH = os.path.join(BASE_DIR, "READ.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                time TEXT NOT NULL,
                language TEXT NOT NULL,
                original_language TEXT NOT NULL,
                genre TEXT NOT NULL,
                rating TEXT NOT NULL,
                note TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS translated (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title_id INT,
                translator TEXT NOT NULL,
                FOREIGN KEY (title_id) REFERENCES books(id) ON DELETE CASCADE
            )
        ''')

def save_book(book_data):
    """Expects a tuple of 10 strings: (title, author, year, month, lang, orig_lang, trans, genre, note, rating)"""
    title, author, year, month, lang, orig_lang, trans, genre, note, rating = book_data

    # Convert year and month to YYYY-MM format
    if year and month:
        date_str = f"{year}-{month.zfill(2)}"  # zfill(2) pads single digits with 0
    elif year:
        date_str = f"{year}-00"
    else:
        year = str(datetime.now().year)
        month = str(datetime.now().month)
        date_str = f"{year}-{month.zfill(2)}"

    # Handle multiple translator of a book
    trans_split = trans.split('/') if trans else []
    trans_split = [s.strip() for s in trans_split]

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO books (title, author, time, language, original_language, genre, rating, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, author, date_str, lang, orig_lang, genre, rating, note))

        # Insert translators if any
        book_id = cursor.lastrowid
        if trans:
            for tran in trans_split:
                cursor.execute('''
                    INSERT INTO translated (title_id, translator)
                    VALUES (?, ?)
                ''', (book_id, tran))
                
def search_books(book_data):
    """Expects a tuple of 10 strings: (title, author, year, month, lang, orig_lang, trans, genre, note, rating)"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Translator input is not suppported
        title, author, year, month, lang, orig_lang, _, genre, note, rating = book_data

        # Convert year and month to wild card search friendly format
        if year and month:
            date_str = f"{year}-{month.zfill(2)}"  # zfill(2) pads single digits with 0
        elif year and not month:
            date_str = str(year)
        elif not year and month:
            date_str = str(month)
        else:
            date_str = ""

        cursor.execute('''
            SELECT title, author, time, language, genre, rating FROM books
            WHERE title LIKE ?
            AND author LIKE ?
            AND time LIKE ?
            AND language LIKE ?
            AND original_language LIKE ?
            AND genre LIKE ?           
            AND note LIKE ?
            AND rating LIKE ?
            ORDER BY time DESC, title ASC
        ''', (f"%{title}%", f"%{author}%", f"%{date_str}%", f"%{lang}%", f"%{orig_lang}%", f"%{genre}%", f"%{note}%", f"%{rating}%"))

        books = cursor.fetchall() 
    return books

def delete_last_entry():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM books
            WHERE id = (
                SELECT id FROM books ORDER BY id DESC LIMIT 1)
        """)
    return

def export_as_csv(output_file = "READ.csv"):
    output_file = os.path.join(BASE_DIR, output_file)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        # Get column names
        column_names = [description[0] for description in cursor.description]
        
        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(column_names)  # Write headers
            writer.writerows(cursor.fetchall())  # Write data
    return

def get_books(type = "all"):
    """Retrieve all books from the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        if type == "all":
            cursor.execute("""
                SELECT * 
                FROM books 
                ORDER BY time, title
            """)
        elif type == "view":
            cursor.execute("""
                SELECT title, author, time, language, genre, rating
                FROM books
                ORDER BY time DESC, title ASC
            """)
        elif type == "random":
            cursor.execute("""
                SELECT title, author, time, language, genre, rating
                FROM books
                ORDER BY RANDOM() 
                LIMIT 5
            """)        
        
        books = cursor.fetchall() 
    return books


