import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser, Listbox
import ctypes
from datetime import datetime

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
        self.text_area.tag_configure("font_size", font=("Helvetica", 12))
        self.text_area.tag_configure("font_family", font=("Helvetica", 12))
        self.text_area.tag_configure("text_color", foreground="black")

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
        dates_events_menu.add_command(label="Delete Event", command=self.delete_event)  # Added Delete Event

        # Create Context Menu for Text Area
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Bold", command=self.make_bold)
        self.context_menu.add_command(label="Italic", command=self.make_italic)
        self.context_menu.add_command(label="Underline", command=self.make_underline)
        self.context_menu.add_command(label="Font Size", command=self.change_font_size)
        self.context_menu.add_command(label="Font Family", command=self.change_font_family)
        self.context_menu.add_command(label="Text Color", command=self.change_text_color)

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
        add_event_window = tk.Toplevel(self.root)
        add_event_window.title("Add Event")

        tk.Label(add_event_window, text="Event Name:").pack(pady=5)
        event_name_entry = tk.Entry(add_event_window)
        event_name_entry.pack(pady=5)

        tk.Label(add_event_window, text="Event Date (YYYY-MM-DD):").pack(pady=5)
        event_date_entry = tk.Entry(add_event_window)
        event_date_entry.pack(pady=5)

        tk.Label(add_event_window, text="Event Description:").pack(pady=5)
        event_description_entry = tk.Entry(add_event_window)
        event_description_entry.pack(pady=5)

        def save_event():
            event_name = event_name_entry.get()
            event_date = event_date_entry.get()
            event_description = event_description_entry.get()
            try:
                datetime.strptime(event_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
                return

            folder_name = os.path.join(os.path.expanduser("~"), "QueWid", "Events")
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            event_file = os.path.join(folder_name, "events.txt")
            with open(event_file, "a", encoding="utf-8") as file:
                file.write(f"{event_date} - {event_name} - {event_description}\n")

            messagebox.showinfo("Event Saved", "Event has been saved successfully!")
            add_event_window.destroy()

        save_button = tk.Button(add_event_window, text="Save", command=save_event)
        save_button.pack(pady=10)

    def view_events(self):
        folder_name = os.path.join(os.path.expanduser("~"), "QueWid", "Events")
        event_file = os.path.join(folder_name, "events.txt")

        if not os.path.exists(event_file):
            messagebox.showinfo("No Events", "No events found.")
            return

        with open(event_file, "r", encoding="utf-8") as file:
            events = file.readlines()

        events.sort(reverse=True, key=lambda x: x.split(" - ")[0])

        events_window = tk.Toplevel(self.root)
        events_window.title("View Events")

        for event in events:
            event_parts = event.strip().split(" - ")
            event_label = tk.Label(events_window, text=f"{event_parts[1]} - {event_parts[2]}", anchor="w", justify="left", padx=10, pady=5, relief="groove")
            event_label.pack(fill="x", padx=10, pady=5)
            date_label = tk.Label(events_window, text=event_parts[0], anchor="e", justify="right", padx=10, pady=5, relief="groove")
            date_label.pack(fill="x", padx=10, pady=5)

    def delete_event(self):
        folder_name = os.path.join(os.path.expanduser("~"), "QueWid", "Events")
        event_file = os.path.join(folder_name, "events.txt")

        if not os.path.exists(event_file):
            messagebox.showinfo("No Events", "No events found.")
            return

        with open(event_file, "r", encoding="utf-8") as file:
            events = file.readlines()

        delete_event_window = tk.Toplevel(self.root)
        delete_event_window.title("Delete Event")

        listbox = Listbox(delete_event_window, selectmode=tk.SINGLE)
        listbox.pack(fill="both", expand=True, padx=10, pady=10)

        for event in events:
            event_parts = event.strip().split(" - ")
            listbox.insert(tk.END, f"{event_parts[1]} - {event_parts[2]}")

        def delete_selected_event():
            selected_index = listbox.curselection()
            if not selected_index:
                messagebox.showwarning("Warning", "No event selected")
                return

            selected_event = listbox.get(selected_index)
            for event in events:
                if selected_event in event:
                    events.remove(event)
                    break

            with open(event_file, "w", encoding="utf-8") as file:
                file.writelines(events)

            messagebox.showinfo("Event Deleted", "Event has been deleted successfully!")
            delete_event_window.destroy()

        delete_button = tk.Button(delete_event_window, text="Delete", command=delete_selected_event)
        delete_button.pack(pady=10)

    def make_bold(self):
        self.apply_tag("bold")

    def make_italic(self):
        self.apply_tag("italic")

    def make_underline(self):
        self.apply_tag("underline")

    def change_font_size(self):
        size = simpledialog.askinteger("Font Size", "Enter font size:", initialvalue=12)
        if size:
            self.text_area.tag_configure("font_size", font=("Helvetica", size))
            self.apply_tag("font_size")

    def change_font_family(self):
        family = simpledialog.askstring("Font Family", "Enter font family:", initialvalue="Helvetica")
        if family:
            self.text_area.tag_configure("font_family", font=(family, 12))
            self.apply_tag("font_family")

    def change_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_area.tag_configure("text_color", foreground=color)
            self.apply_tag("text_color")

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
