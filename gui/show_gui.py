import tkinter as tk
from tkinter import ttk, messagebox
from database import database
from utils import validation

# Home window dimensions
WINDOW_WIDTH, WINDOW_HEIGHT, PADDING = 1000, 600, 30

FORM_FIELDS = [
    ("Show Title", "title"), 
    ("Season (Optional, ONLY enter this if the title doesn't reflect the seasons.)", "season"),
    [("Year", "year"), ("Month", "month")],
    ("Type", "type"),
    ("Note", "note")
]
 
BG_COLOR, HEADER_COLOR = "#f0f2f5", "#2c3e50"
BUTTON_COLOR, BUTTON_HOVER_COLOR = "#16A085", "#1ABC9C"

FONTS = {
    "title": ("Brush Script MT", 35, "bold"),
    "body": ("Segoe UI", 10),
    "header": ("Segoe UI", 16, "bold"),
    "entry": ("Segoe UI", 11),
    "button": ("Segoe UI", 10, "bold"),
}

TYPES = [
    'Anime',
    'Cartoon', 
    'Comedy',          # Covers sitcoms, stand-up, comedy series
    'Drama',
    'Documentary',
    'Others'
]

class ShowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MyShow")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=BG_COLOR)
        self._setup_styles()

        main_frame = ttk.Frame(self.root, padding=PADDING)
        main_frame.pack(expand=True, fill="both")

        ttk.Label(main_frame, text="MyShow", style="Header.TLabel", font=FONTS["title"]).pack(pady=(0, 10))

        # Create two-column layout
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(expand=True, fill="both")

        # Left column - Form fields
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))

        # Right column - Buttons
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side="right", fill="both", expand = True, padx=(15, 0))

        self.entries, self.entry_list = {}, []
        self._create_form_fields(left_frame)
        self._create_action_buttons(right_frame)

    def submit_show(self):
        # Data collection with 10 items
        data = tuple(
            self.entries[key].get().strip() 
            for item in FORM_FIELDS 
            for _, key in (item if isinstance(item, list) else [item])
        )

        # Input validation
        # Check all required fields
        for i in [0,4]:
            if validation.is_empty(data[i]):
                messagebox.showwarning("Incomplete Input", "Please fill in all required fields.")
                return
            
        # Check year
        if not validation.check_season(data[1], accept_empty=True): # Check season
            messagebox.showwarning("Invalid Season", "Season should be a positive integer.")
            return
        if not validation.check_year(data[2], accept_empty=True): # Empty year will be set to current year in database.py
            messagebox.showwarning("Invalid Year", "Year should be an integer value.")
            return
        # Check month
        if not validation.check_month(data[3], accept_empty=True): # Empty month will be set to current month in database.py
            messagebox.showwarning("Invalid Month", "Month should be between 1 and 12.")
            return

        
        try:
            database.save_show(data)
            messagebox.showinfo("Success", f"'{data[0]}' saved successfully!")
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not save data: {e}")

    def view_database(self):
        try:
            self._display_shows_window(database.get_shows())
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not fetch data: {e}")

    def search_shows(self):
        data = tuple(
            self.entries[key].get().strip() 
            for item in FORM_FIELDS 
            for _, key in (item if isinstance(item, list) else [item])
        ) 

        # Check if at least one box is filled
        if all(validation.is_empty(data[i]) for i in range(6)):
            messagebox.showwarning("Empty Form", "Please fill in at least a box to search.")
            return
        if validation.is_empty(data[0]) and not validation.is_empty(data[1]):
            messagebox.showwarning("Incomplete Input", "Please enter a title when searching by season.")
            return
        
        try:
            self._display_shows_window(database.search_shows(data))
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not fetch data: {e}")

    def delete_last_entry(self):
        # Ask for confirmation
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the last entry?"):
            return  # User clicked "No", so exit the function
        
        try:
            database.delete_last_entry(table="shows")
            messagebox.showinfo("Success", "Last entry deleted successfully!")
        except Exception as e:
            messagebox.showerror("Database Error", f"Could not delete entry: {e}")

    def clear_entries(self):
        for entry in self.entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set("")
            else:
                entry.delete(0, tk.END)

    def _create_action_buttons(self, parent):
        ttk.Label(parent, text="", style="Header.TLabel").pack(pady=(0, 0))
        for text, cmd in [
            ("SAVE", self.submit_show), 
            ("SEARCH", self.search_shows),
            ("DELETE LAST ENTRY", self.delete_last_entry),
            ("VIEW ALL", self.view_database)
        ]:
            btn = ttk.Button(parent, text=text, command=cmd, style="Action.TButton", width=20)
            btn.pack(fill="x", ipady=10, pady=5)

    def _create_form_fields(self, parent):
        for item in FORM_FIELDS:
            if isinstance(item, list):
                row_frame = ttk.Frame(parent)
                row_frame.pack(fill="x", pady=(10, 5))
                for label_text, key in item:
                    col_frame = ttk.Frame(row_frame)
                    col_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
                    ttk.Label(col_frame, text=label_text).pack(anchor="w", pady=(0, 2))
                    
                    widget = ttk.Entry(col_frame, font=FONTS["entry"])
                    self._bind_arrows(widget)
                    widget.pack(fill="x", ipady=5)
                    self.entries[key] = widget
                    self.entry_list.append(widget)
            else:
                label_text, key = item
                ttk.Label(parent, text=label_text).pack(anchor="w", pady=(10, 2))
                widget = ttk.Combobox(parent, font=FONTS["entry"], state="readonly") if key in ["type"] else ttk.Entry(parent, font=FONTS["entry"])
                if key == "type":
                    widget["values"] = TYPES
                else:
                    self._bind_arrows(widget)
                widget.pack(fill="x", ipady=5)
                self.entries[key] = widget
                self.entry_list.append(widget)

    def _bind_arrows(self, entry):
        entry.bind("<Right>", lambda e: self._move_focus(1))
        entry.bind("<Left>", lambda e: self._move_focus(-1))

    def _move_focus(self, direction):
        current = self.root.focus_get()
        if current in self.entry_list:
            idx = self.entry_list.index(current)
            next_idx = idx + direction
            if 0 <= next_idx < len(self.entry_list):
                self.entry_list[next_idx].focus()
        return "break"

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabel", background=BG_COLOR, font=FONTS["body"])
        style.configure("Header.TLabel", font=FONTS["header"], foreground=HEADER_COLOR)
        style.configure("Action.TButton", font=FONTS["button"], foreground="white", background=BUTTON_COLOR)
        style.map("Action.TButton", background=[('active', BUTTON_HOVER_COLOR)])

    def _display_shows_window(self, shows):
        # View window dimensions
        VIEW_WINDOW_WIDTH, VIEW_WINDOW_HEIGHT = 1000, 600
        # View window fonts
        VIEW_WINDOW_FONTS = {
            "content": ("Segoe UI", 12),
            "header": ("Segoe UI", 11, "bold")
        }

        view_window = tk.Toplevel(self.root)
        view_window.title("Show Database")
        view_window.geometry(f"{VIEW_WINDOW_WIDTH}x{VIEW_WINDOW_HEIGHT}")
        view_window.configure(bg=BG_COLOR)

        ttk.Label(view_window, text=f"Total Shows/Movies: {len(shows)}", style="Header.TLabel").pack(pady=10)
        tree_frame = ttk.Frame(view_window)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Shows desired columns
        
        columns = ("title", "time", "type")
        headings = {"title": "Title", "time": "Time", "type": "Type"}
        tree = ttk.Treeview(tree_frame, columns=columns, height=20, show="headings")
        
        style = ttk.Style()
        style.configure("Treeview", font=VIEW_WINDOW_FONTS["content"])
        style.configure("Treeview.Heading", font=VIEW_WINDOW_FONTS["header"])

        for col, heading in headings.items():
            tree.heading(col, text=heading)
            tree.column(col, width=120)

        for show in shows:
            tree.insert("", "end", values=show)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        ttk.Button(view_window, text="Close", command=view_window.destroy).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = ShowApp(root)
    root.mainloop()