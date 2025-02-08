import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import ctypes

class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QueWid")
        self.root.geometry("1000x800")

        # Create a Text Area
        self.text_area = tk.Text(root, wrap="word")
        self.text_area.pack(expand=True, fill="both")

        # Configure text tags for formatting
        self.text_area.tag_configure("bold", font=("Helvetica", 12, "bold"))
        self.text_area.tag_configure("italic", font=("Helvetica", 12, "italic"))
        self.text_area.tag_configure("underline", font=("Helvetica", 12, "underline"))

        # Create Menu Bar
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        # Add Notes Menu
        notes_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Notes", menu=notes_menu)
        notes_menu.add_command(label="New Note", command=self.new_note)
        notes_menu.add_command(label="Save Note", command=self.save_note)
        notes_menu.add_command(label="Load Note", command=self.load_note)

        # Add Dates & Events Menu
        dates_events_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Dates & Events", menu=dates_events_menu)
        dates_events_menu.add_command(label="Add Event", command=self.add_event)
        dates_events_menu.add_command(label="View Events", command=self.view_events)

        # Add Format Menu (initially hidden)
        self.format_menu = tk.Menu(menu_bar, tearoff=0)
        self.format_menu.add_command(label="Bold", command=self.make_bold)
        self.format_menu.add_command(label="Italic", command=self.make_italic)
        self.format_menu.add_command(label="Underline", command=self.make_underline)

        # Create Context Menu for Text Area
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Bold", command=self.make_bold)
        self.context_menu.add_command(label="Italic", command=self.make_italic)
        self.context_menu.add_command(label="Underline", command=self.make_underline)

        # Bind right-click to show context menu
        self.text_area.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def new_note(self):
        self.text_area.delete("1.0", tk.END)

    def save_note(self):
        folder_name = os.path.join(os.path.expanduser("~"), "QueWid")
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            if not ctypes.windll.kernel32.SetFileAttributesW(folder_name, 0x02):
                error_code = ctypes.GetLastError()
                if error_code == 5:  # ERROR_ACCESS_DENIED
                    messagebox.showwarning("Permission Error", "Failed to set folder as hidden. Please run the application with administrative privileges.")

        file_name = simpledialog.askstring("Save Note", "Enter file name:", initialvalue="note.txt")
        if file_name:
            if not file_name.endswith(".txt"):
                file_name += ".txt"
            file_path = os.path.join(folder_name, file_name)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.text_area.get("1.0", tk.END))

            messagebox.showinfo("Saved", f"Note saved in {file_path}!")

    def load_note(self):
        folder_name = os.path.join(os.path.expanduser("~"), "QueWid")
        file_path = filedialog.askopenfilename(initialdir=folder_name, title="Select Note",
                                               filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, content)

    def add_event(self):
        # Placeholder for adding an event
        messagebox.showinfo("Add Event", "This feature is not implemented yet.")

    def view_events(self):
        # Placeholder for viewing events
        messagebox.showinfo("View Events", "This feature is not implemented yet.")

    def make_bold(self):
        self.apply_tag("bold")

    def make_italic(self):
        self.apply_tag("italic")

    def make_underline(self):
        self.apply_tag("underline")

    def apply_tag(self, tag_name):
        try:
            current_tags = self.text_area.tag_names("sel.first")
            if tag_name in current_tags:
                self.text_area.tag_remove(tag_name, "sel.first", "sel.last")
            else:
                self.text_area.tag_add(tag_name, "sel.first", "sel.last")
        except tk.TclError:
            messagebox.showwarning("Warning", "No text selected")

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()
