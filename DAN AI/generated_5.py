import os
import subprocess
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Configuration file name
CONFIG_FILE = "game_launcher_config.json"

def load_config():
    """Loads the game configuration from a JSON file."""
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        # If the config file doesn't exist, return an empty dictionary
        return {"games": []}
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON in config file.  Creating a new one.")
        return {"games": []}


def save_config(config):
    """Saves the game configuration to a JSON file."""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save config: {e}")


def launch_game(game_path):
    """Launches the game using subprocess."""
    try:
        subprocess.Popen(game_path)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Game executable not found: {game_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch game: {e}")


def add_game():
    """Adds a new game to the launcher."""
    global config, game_list
    file_path = filedialog.askopenfilename(title="Select Game Executable")
    if file_path:
        game_name = os.path.basename(file_path)
        config["games"].append({"name": game_name, "path": file_path})
        save_config(config)
        update_game_list()


def remove_game():
    """Removes a selected game from the launcher."""
    global config, game_list
    selected_index = game_list.curselection()
    if selected_index:
        selected_index = selected_index[0]  # Get the actual index
        game_name = game_list.get(selected_index)
        # Find the game in the config and remove it
        for i, game in enumerate(config["games"]):
            if game["name"] == game_name:
                del config["games"][i]
                break
        save_config(config)
        update_game_list()
    else:
        messagebox.showinfo("Info", "Please select a game to remove.")


def update_game_list():
    """Updates the game list in the GUI."""
    global config, game_list
    game_list.delete(0, tk.END)  # Clear the current list
    for game in config["games"]:
        game_list.insert(tk.END, game["name"])


def on_game_selected(event):
    """Handles the event when a game is selected in the list."""
    global config, game_list
    selected_index = game_list.curselection()
    if selected_index:
        selected_index = selected_index[0]
        game_name = game_list.get(selected_index)
        for game in config["games"]:
            if game["name"] == game_name:
                launch_game(game["path"])
                break


if __name__ == "__main__":
    # Load the configuration
    config = load_config()

    # Create the main window
    root = tk.Tk()
    root.title("Game Launcher")

    # Create and configure the game list
    game_list = tk.Listbox(root, width=50, height=15)
    game_list.pack(pady=10)
    game_list.bind("<Double-Button-1>", on_game_selected)  # Launch on double click

    # Create buttons
    add_button = ttk.Button(root, text="Add Game", command=add_game)
    add_button.pack(pady=5)

    remove_button = ttk.Button(root, text="Remove Game", command=remove_game)
    remove_button.pack(pady=5)

    # Initial population of the game list
    update_game_list()

    # Start the main event loop
    root.mainloop()