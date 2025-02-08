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

        # Create Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(fill="x", padx=10, pady=10)
        save_button = tk.Button(root, text="Save Note", command=self.save_note)
        save_button.pack(side="left", padx=10, pady=10)

        load_button = tk.Button(root, text="Load Note", command=self.load_note)
        load_button.pack(side="right", padx=10, pady=10)

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

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()
