import tkinter as tk
from tkinter import ttk

# Menu window dimensions
MENU_WIDTH, MENU_HEIGHT = 600, 500

BG_COLOR = "#f0f2f5"
HEADER_COLOR = "#2c3e50"
BUTTON_COLOR = "#16A085"
BUTTON_HOVER_COLOR = "#1ABC9C"

FONTS = {
    "title": ("Brush Script MT", 48, "bold"),
    "subtitle": ("Segoe UI", 14),
    "button": ("Segoe UI", 14, "bold"),
}

class MyMediaMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("MyMedia")
        self.root.geometry(f"{MENU_WIDTH}x{MENU_HEIGHT}")
        self.root.configure(bg=BG_COLOR)
        self._setup_styles()
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (MENU_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (MENU_HEIGHT // 2)
        self.root.geometry(f"{MENU_WIDTH}x{MENU_HEIGHT}+{x}+{y}")

        main_frame = ttk.Frame(self.root, padding=40)
        main_frame.pack(expand=True, fill="both")

        # Title
        ttk.Label(main_frame, text="MyMedia", style="Title.TLabel", 
                 font=FONTS["title"]).pack(pady=(20, 5))
        
        # Subtitle
        ttk.Label(main_frame, text="Select your media collection", 
                 style="Subtitle.TLabel", font=FONTS["subtitle"]).pack(pady=(0, 40))

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(expand=True)

        # Create menu buttons
        for text, cmd in [
            ("Books", self.open_books),
            ("Shows", self.open_shows)
        ]:
            btn = ttk.Button(buttons_frame, text=text, command=cmd, 
                           style="Menu.TButton", width=25)
            btn.pack(pady=10, ipady=15)

    def open_books(self):
        """Open the Books GUI"""
        self.root.withdraw()  # Hide menu window
        books_window = tk.Toplevel(self.root)
        
        # Import and initialize BookApp
        from gui import book_gui  
        book_gui.BookApp(books_window)
        
        # Show menu again when books window is closed
        books_window.protocol("WM_DELETE_WINDOW", lambda: self._on_close_child(books_window))

    def open_shows(self):
        """Open the Shows GUI"""
        self.root.withdraw()  # Hide menu window
        shows_window = tk.Toplevel(self.root)
        
        # Import and initialize ShowApp
        from gui import show_gui  
        show_gui.ShowApp(shows_window)
        
        # Show menu again when shows window is closed
        shows_window.protocol("WM_DELETE_WINDOW", lambda: self._on_close_child(shows_window))

    def _on_close_child(self, child_window):
        """Handle closing of child windows and return to menu"""
        child_window.destroy()
        self.root.deiconify()  # Show menu window again

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabel", background=BG_COLOR)
        style.configure("Title.TLabel", foreground=HEADER_COLOR)
        style.configure("Subtitle.TLabel", foreground="#7f8c8d")
        style.configure("Menu.TButton", font=FONTS["button"], 
                       foreground="white", background=BUTTON_COLOR)
        style.map("Menu.TButton", background=[('active', BUTTON_HOVER_COLOR)])


if __name__ == "__main__":
    root = tk.Tk()
    app = MyMediaMenu(root)
    root.mainloop()