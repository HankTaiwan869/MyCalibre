import tkinter as tk
from gui import BookApp
import database

def main():
    # 1. Initialize the database (create table if not exists)
    database.init_db()

    # 2. Start the UI
    root = tk.Tk()
    app = BookApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()