import sqlite3
import os
import sys
import csv
from datetime import datetime
from utils import validation


def get_base_dir():
    # Running as a bundled executable
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    # Running as a script
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = get_base_dir()
DB_PATH = os.path.join(BASE_DIR, "MEDIA.db")

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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                time TEXT NOT NULL,
                type TEXT NOT NULL,
                note TEXT
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

def save_show(show_data):
    """Expects a tuple of 6 strings: (title, season, year, month, type, note)"""
    title, season, year, month, type, note = show_data

    # Convert year and month to YYYY-MM format
    if year and month:
        date_str = f"{year}-{month.zfill(2)}"  # zfill(2) pads single digits with 0
    elif year:
        date_str = f"{year}-00"
    else:
        year = str(datetime.now().year)
        month = str(datetime.now().month)
        date_str = f"{year}-{month.zfill(2)}"

    # Handle season if provided
    if not validation.is_empty(season):
        title = f"{title} - Season {season.strip()}"

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO shows (title, time, type, note)
            VALUES (?, ?, ?, ?)
        ''', (title, date_str, type, note))
                
def search_books(book_data):
    """Expects a tuple of 10 strings: (title, author, year, month, lang, orig_lang, trans, genre, note, rating)"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Translator input is not suppported
        title, author, year, month, lang, orig_lang, trans, genre, note, rating = book_data

        # Convert year and month to wild card search friendly format
        if year and month:
            date_str = f"{year}-{month.zfill(2)}"  # zfill(2) pads single digits with 0
        elif year and not month:
            date_str = str(year)
        elif not year and month:
            date_str = str(month)
        else:
            date_str = ""

        if validation.is_empty(trans):
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
                ORDER BY time ASC, title ASC
            ''', (f"%{title}%", f"%{author}%", f"%{date_str}%", f"%{lang}%", f"%{orig_lang}%", f"%{genre}%", f"%{note}%", f"%{rating}%"))
        else:
            cursor.execute('''
                SELECT b.title, b.author, t.translator, b.time, b.language, b.genre, b.rating
                FROM books b
                JOIN translated t ON b.id = t.title_id
                WHERE b.title LIKE ?
                AND b.author LIKE ?
                AND b.time LIKE ?
                AND b.language LIKE ?
                AND b.original_language LIKE ?
                AND t.translator LIKE ?
                AND b.genre LIKE ?           
                AND b.note LIKE ?
                AND b.rating LIKE ?
                ORDER BY b.time ASC, b.title ASC
            ''',  (f"%{title}%", f"%{author}%", f"%{date_str}%", f"%{lang}%", f"%{orig_lang}%", f"%{trans}%", f"%{genre}%", f"%{note}%", f"%{rating}%"))

        books = cursor.fetchall() 
    return books

def search_shows(show_data):
    """Expects a tuple of 6 strings: (title, season, year, month, type, note)"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        title, season, year, month, type, note = show_data

        # Convert year and month to wild card search friendly format
        if year and month:
            date_str = f"{year}-{month.zfill(2)}"  # zfill(2) pads single digits with 0
        elif year and not month:
            date_str = str(year)
        elif not year and month:
            date_str = str(month)
        else:
            date_str = ""
 
        if not validation.is_empty(season):
            title = f"{title} - Season {season.strip()}"
            cursor.execute('''
                SELECT title, time, type FROM shows
                WHERE title LIKE ?
                AND time LIKE ?
                AND type LIKE ?           
                AND note LIKE ?
                ORDER BY time ASC, title ASC
            ''', (f"%{title}%", f"%{date_str}%", f"%{type}%", f"%{note}%"))
        else:
            cursor.execute('''
                SELECT title, time, type FROM shows
                WHERE title LIKE ?
                AND time LIKE ?
                AND type LIKE ?           
                AND note LIKE ?
                ORDER BY time ASC, title ASC
            ''', (f"%{title}%", f"%{date_str}%", f"%{type}%", f"%{note}%"))

        shows = cursor.fetchall() 
    return shows

def delete_last_entry(table):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        if table == "books":
            cursor.execute("""
                DELETE FROM books
                WHERE id = (
                    SELECT id FROM books ORDER BY id DESC LIMIT 1)
            """)
        elif table == "shows":
            cursor.execute("""
                DELETE FROM shows
                WHERE id = (
                    SELECT id FROM shows ORDER BY id DESC LIMIT 1)
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

        books = cursor.fetchall() 
    return books

def get_shows():
    """Retrieve all shows from the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT title, time, type 
            FROM shows 
            ORDER BY time, title
        """)
        shows = cursor.fetchall() 
    return shows