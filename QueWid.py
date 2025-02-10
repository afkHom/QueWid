import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser, Listbox, Scrollbar
import ctypes
from datetime import datetime

class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QueWid")
        self.root.geometry("1000x800")

        self.setup_paned_window()
        self.setup_text_area()
        self.setup_menu_bar()
        self.setup_context_menu()
        self.setup_events_listbox()
        self.setup_notes_listbox()
        self.setup_status_bar()
        self.bind_shortcuts()
        self.view_events()  # Refresh the events list when the application starts
        self.view_notes()  # Refresh the notes list when the application starts

    def setup_paned_window(self):
        self.paned_window = tk.PanedWindow(self.root, orient=tk.VERTICAL)
        self.paned_window.pack(fill=tk.BOTH, expand=1)

        self.notes_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.notes_frame, stretch="always")

        self.dates_events_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.dates_events_frame, stretch="always")

        self.paned_window.paneconfig(self.notes_frame, minsize=500)
        self.paned_window.paneconfig(self.dates_events_frame, minsize=500)
        self.paned_window.sash_place(0, 0, 400)

    def setup_text_area(self):
        self.text_area = tk.Text(self.notes_frame, wrap="word")
        self.text_area.pack(expand=True, fill="both", side=tk.LEFT)
        text_scrollbar = Scrollbar(self.notes_frame, command=self.text_area.yview)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=text_scrollbar.set)

        self.text_area.tag_configure("bold", font=("Helvetica", 12, "bold"))
        self.text_area.tag_configure("italic", font=("Helvetica", 12, "italic"))
        self.text_area.tag_configure("underline", font=("Helvetica", 12, "underline"))
        self.text_area.tag_configure("font_size", font=("Helvetica", 12))
        self.text_area.tag_configure("font_family", font=("Helvetica", 12))
        self.text_area.tag_configure("text_color", foreground="black")

    def setup_menu_bar(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        notes_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Notes", menu=notes_menu)
        notes_menu.add_command(label="New Note", command=self.new_note, accelerator="Ctrl+N")
        notes_menu.add_command(label="Save Note", command=self.save_note, accelerator="Ctrl+S")
        notes_menu.add_command(label="Load Note", command=self.load_note, accelerator="Ctrl+O")
        notes_menu.add_command(label="Search", command=self.search_note, accelerator="Ctrl+F")
        notes_menu.add_command(label="Categorize Note", command=self.categorize_note)

        dates_events_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Dates & Events", menu=dates_events_menu)
        dates_events_menu.add_command(label="Add Event", command=self.add_event)
        dates_events_menu.add_command(label="View Events", command=self.view_events)
        dates_events_menu.add_command(label="Delete Event", command=self.delete_event)

    def setup_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Bold", command=self.make_bold, accelerator="Ctrl+B")
        self.context_menu.add_command(label="Italic", command=self.make_italic, accelerator="Ctrl+I")
        self.context_menu.add_command(label="Underline", command=self.make_underline, accelerator="Ctrl+U")
        self.context_menu.add_command(label="Font Size", command=self.change_font_size)
        self.context_menu.add_command(label="Font Family", command=self.change_font_family)
        self.context_menu.add_command(label="Text Color", command=self.change_text_color)

        self.text_area.bind("<Button-3>", self.show_context_menu)

    def setup_events_listbox(self):
        self.events_listbox = Listbox(self.dates_events_frame)
        self.events_listbox.pack(expand=True, fill="both", side=tk.LEFT)
        listbox_scrollbar = Scrollbar(self.dates_events_frame, command=self.events_listbox.yview)
        listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.events_listbox.config(yscrollcommand=listbox_scrollbar.set)

    def setup_notes_listbox(self):
        self.notes_listbox = Listbox(self.dates_events_frame)
        self.notes_listbox.pack(expand=True, fill="both", side=tk.RIGHT)
        listbox_scrollbar = Scrollbar(self.dates_events_frame, command=self.notes_listbox.yview)
        listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.notes_listbox.config(yscrollcommand=listbox_scrollbar.set)
        self.notes_listbox.bind("<<ListboxSelect>>", self.load_selected_note)

    def setup_status_bar(self):
        self.status_bar = tk.Label(self.root, text="Welcome to QueWid", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def bind_shortcuts(self):
        self.root.bind("<Control-n>", lambda event: self.new_note())
        self.root.bind("<Control-s>", lambda event: self.save_note())
        self.root.bind("<Control-o>", lambda event: self.load_note())
        self.root.bind("<Control-b>", lambda event: self.make_bold())
        self.root.bind("<Control-i>", lambda event: self.make_italic())
        self.root.bind("<Control-u>", lambda event: self.make_underline())
        self.root.bind("<Control-f>", lambda event: self.search_note())

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def new_note(self):
        self.text_area.delete("1.0", tk.END)
        self.status_bar.config(text="New note created")

    def save_note(self):
        folder_name = self.get_folder_path("QueWid")
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            self.set_folder_hidden(folder_name)

        file_name = simpledialog.askstring("Save Note", "Enter file name:", initialvalue="note.txt")
        if file_name:
            if not file_name.endswith(".txt"):
                file_name += ".txt"
            file_path = os.path.join(folder_name, file_name)
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.text_area.get("1.0", tk.END))
                messagebox.showinfo("Saved", f"Note saved in {file_path}!")
                self.status_bar.config(text=f"Note saved in {file_path}")
                self.view_notes()  # Refresh the notes list
            except IOError as e:
                messagebox.showerror("Error", f"Failed to save note: {e}")

    def load_note(self):
        folder_name = self.get_folder_path("QueWid")
        file_path = filedialog.askopenfilename(initialdir=folder_name, title="Select Note",
                                               filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert(tk.END, content)
                    self.status_bar.config(text=f"Loaded note from {file_path}")
            except IOError as e:
                messagebox.showerror("Error", f"Failed to load note: {e}")

    def load_selected_note(self, event):
        selected_index = self.notes_listbox.curselection()
        if selected_index:
            file_name = self.notes_listbox.get(selected_index)
            folder_name = self.get_folder_path("QueWid")
            file_path = os.path.join(folder_name, file_name)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert(tk.END, content)
                    self.status_bar.config(text=f"Loaded note from {file_path}")
            except IOError as e:
                messagebox.showerror("Error", f"Failed to load note: {e}")

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
        event_description_entry = tk.Text(add_event_window, wrap="word", height=5)
        event_description_entry.pack(pady=5)

        def save_event():
            event_name = event_name_entry.get()
            event_date = event_date_entry.get()
            event_description = event_description_entry.get("1.0", tk.END).strip()
            if not self.validate_date(event_date):
                messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
                return

            folder_name = self.get_folder_path("QueWid/Events")
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            event_file = os.path.join(folder_name, "events.txt")
            try:
                with open(event_file, "a", encoding="utf-8") as file:
                    file.write(f"{event_date} - {event_name} - {event_description}\n")
                messagebox.showinfo("Event Saved", "Event has been saved successfully!")
                add_event_window.destroy()
                self.view_events()  # Refresh the events list
                self.status_bar.config(text="Event added")
            except IOError as e:
                messagebox.showerror("Error", f"Failed to save event: {e}")

        save_button = tk.Button(add_event_window, text="Save", command=save_event)
        save_button.pack(pady=10)

    def view_events(self):
        folder_name = self.get_folder_path("QueWid/Events")
        event_file = os.path.join(folder_name, "events.txt")

        if not os.path.exists(event_file):
            messagebox.showinfo("No Events", "No events found.")
            return

        try:
            with open(event_file, "r", encoding="utf-8") as file:
                events = file.readlines()
            events.sort(reverse=True, key=lambda x: x.split(" - ")[0])
            self.events_listbox.delete(0, tk.END)
            for event in events:
                event_parts = event.strip().split(" - ")
                self.events_listbox.insert(tk.END, f"{event_parts[0]} - {event_parts[1]} - {event_parts[2]}")
            self.status_bar.config(text="Events loaded")
        except IOError as e:
            messagebox.showerror("Error", f"Failed to load events: {e}")

    def view_notes(self):
        folder_name = self.get_folder_path("QueWid")
        if not os.path.exists(folder_name):
            return

        try:
            notes = [f for f in os.listdir(folder_name) if f.endswith(".txt")]
            self.notes_listbox.delete(0, tk.END)
            for note in notes:
                self.notes_listbox.insert(tk.END, note)
            self.status_bar.config(text="Notes loaded")
        except IOError as e:
            messagebox.showerror("Error", f"Failed to load notes: {e}")

    def delete_event(self):
        folder_name = self.get_folder_path("QueWid/Events")
        event_file = os.path.join(folder_name, "events.txt")

        if not os.path.exists(event_file):
            messagebox.showinfo("No Events", "No events found.")
            return

        try:
            with open(event_file, "r", encoding="utf-8") as file:
                events = file.readlines()
        except IOError as e:
            messagebox.showerror("Error", f"Failed to load events: {e}")
            return

        delete_event_window = tk.Toplevel(self.root)
        delete_event_window.title("Delete Event")

        listbox = Listbox(delete_event_window, selectmode=tk.SINGLE)
        listbox.pack(fill="both", expand=True, padx=10, pady=10)

        for event in events:
            event_parts = event.strip().split(" - ")
            listbox.insert(tk.END, f"{event_parts[0]} - {event_parts[1]} - {event_parts[2]}")

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

            try:
                with open(event_file, "w", encoding="utf-8") as file:
                    file.writelines(events)
                messagebox.showinfo("Event Deleted", "Event has been deleted successfully!")
                delete_event_window.destroy()
                self.view_events()  # Refresh the events list
                self.status_bar.config(text="Event deleted")
            except IOError as e:
                messagebox.showerror("Error", "Failed to delete event: {e}")

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

    def search_note(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Note")

        tk.Label(search_window, text="Search for:").pack(pady=5)
        search_entry = tk.Entry(search_window)
        search_entry.pack(pady=5)

        def perform_search():
            search_text = search_entry.get()
            self.text_area.tag_remove("search", "1.0", tk.END)
            if search_text:
                start_pos = "1.0"
                while True:
                    start_pos = self.text_area.search(search_text, start_pos, stopindex=tk.END)
                    if not start_pos:
                        break
                    end_pos = f"{start_pos}+{len(search_text)}c"
                    self.text_area.tag_add("search", start_pos, end_pos)
                    start_pos = end_pos
                self.text_area.tag_config("search", background="yellow")

        search_button = tk.Button(search_window, text="Search", command=perform_search)
        search_button.pack(pady=10)

    def categorize_note(self):
        category_window = tk.Toplevel(self.root)
        category_window.title("Categorize Note")

        tk.Label(category_window, text="Category:").pack(pady=5)
        category_entry = tk.Entry(category_window)
        category_entry.pack(pady=5)

        def save_category():
            category = category_entry.get()
            if category:
                folder_name = self.get_folder_path(f"QueWid/Categories/{category}")
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                file_name = simpledialog.askstring("Save Note", "Enter file name:", initialvalue="note.txt")
                if file_name:
                    if not file_name.endswith(".txt"):
                        file_name += ".txt"
                    file_path = os.path.join(folder_name, file_name)
                    try:
                        with open(file_path, "w", encoding="utf-8") as file:
                            file.write(self.text_area.get("1.0", tk.END))
                        messagebox.showinfo("Saved", f"Note saved in {file_path}!")
                        self.status_bar.config(text=f"Note saved in {file_path}")
                        self.view_notes()  # Refresh the notes list
                    except IOError as e:
                        messagebox.showerror("Error", f"Failed to save note: {e}")
            category_window.destroy()

        save_button = tk.Button(category_window, text="Save", command=save_category)
        save_button.pack(pady=10)

    def get_folder_path(self, folder_name):
        return os.path.join(os.path.expanduser("~"), folder_name)

    def set_folder_hidden(self, folder_name):
        try:
            if not ctypes.windll.kernel32.SetFileAttributesW(folder_name, 0x02):
                error_code = ctypes.GetLastError()
                if error_code == 5:  # ERROR_ACCESS_DENIED
                    messagebox.showwarning("Permission Error", "Failed to set folder as hidden. Please run the application with administrative privileges.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set folder as hidden: {e}")

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()
