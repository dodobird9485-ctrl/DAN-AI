```python
import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox

def detect_language(file_path):
    """Detects the language of the script based on file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.py':
        return 'Python'
    elif ext == '.js':
        return 'JavaScript'
    elif ext == '.java':
        return 'Java'
    elif ext == '.exe':
        return 'Executable'
    elif ext == '.sh':
        return 'Shell Script'
    elif ext == '.bat':
        return 'Batch Script'
    else:
        return 'Unknown'

def launch_game(file_path):
    """Launches the game based on detected language."""
    language = detect_language(file_path)
    try:
        if language == 'Python':
            subprocess.Popen(['python', file_path])
        elif language == 'JavaScript':
            subprocess.Popen(['node', file_path])  # Requires Node.js
        elif language == 'Java':
            subprocess.Popen(['java', '-jar', file_path]) # Assumes JAR
        elif language == 'Executable':
            subprocess.Popen([file_path])
        elif language == 'Shell Script':
            subprocess.Popen(['bash', file_path])
        elif language == 'Batch Script':
            subprocess.Popen([file_path])
        else:
            messagebox.showerror("Error", f"Unsupported language for {file_path}")
            return

        messagebox.showinfo("Success", f"Launched {os.path.basename(file_path)} using {language}!")
    except FileNotFoundError as e:
        messagebox.showerror("Error", f"File not found or interpreter missing: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def add_game():
    """Adds a new game entry."""
    file_path = file_path_entry.get()
    if not os.path.exists(file_path):
        messagebox.showerror("Error", "File does not exist.")
        return

    game_name = os.path.basename(file_path)
    game_list.insert(tk.END, game_name)
    game_paths[game_name] = file_path
    file_path_entry.delete(0, tk.END)

def launch_selected_game():
    """Launches the game selected in the listbox."""
    selected_game = game_list.get(tk.ACTIVE)
    if selected_game:
        launch_game(game_paths[selected_game])
    else:
        messagebox.showinfo("Info", "Please select a game to launch.")

# Initialize main window
root = tk.Tk()
root.title("Simple Game Launcher")

# Game list
game_list = tk.Listbox(root, width=50)
game_list.pack(pady=10)

# Game paths dictionary
game_paths = {}

# File path entry
file_path_label = ttk.Label(root, text="Game File Path:")
file_path_label.pack()
file_path_entry = ttk.Entry(root, width=50)
file_path_entry.pack()

# Add game button
add_game_button = ttk.Button(root, text="Add Game", command=add_game)
add_game_button.pack(pady=5)

# Launch game button
launch_button = ttk.Button(root, text="Launch Game", command=launch_selected_game)
launch_button.pack(pady=10)

root.mainloop()
```