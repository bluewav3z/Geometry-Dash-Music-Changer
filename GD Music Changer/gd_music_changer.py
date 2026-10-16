
import os
import shutil
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

# ==========================================
# GEOMETRY DASH MUSIC CHANGER
# ==========================================

DOWNLOADS_FOLDER = Path.home() / "Downloads"

GD_RESOURCES_FOLDER = Path(
    r"C:\Program Files (x86)\Steam\steamapps\common"
    r"\Geometry Dash\Resources"
)

TARGET_FILE = GD_RESOURCES_FOLDER / "menuLoop.mp3"
BACKUP_FILE = GD_RESOURCES_FOLDER / "menuLoop_original_backup.mp3"


def turn_into_background_music():
    # Get the filename entered by the user.
    filename = filename_entry.get().strip()

    if not filename:
        messagebox.showerror(
            "Missing Filename",
            "Please type the name of an MP3 file first!"
        )
        return

    # Only allow a filename, not a path to another folder.
    if Path(filename).name != filename:
        messagebox.showerror(
            "Invalid Filename",
            "Please enter just the filename, such as song.mp3."
        )
        return

    # Only allow MP3 files.
    if Path(filename).suffix.lower() != ".mp3":
        messagebox.showerror(
            "Invalid File Type",
            "Only .mp3 files are allowed!"
        )
        return

    source_file = DOWNLOADS_FOLDER / filename

    # Make sure the file exists in Downloads.
    if not source_file.is_file():
        messagebox.showerror(
            "File Not Found",
            f"Could not find:\n\n{source_file}\n\n"
            "Check the filename and try again."
        )
        return

    # Make sure the Geometry Dash folder exists.
    if not GD_RESOURCES_FOLDER.is_dir():
        messagebox.showerror(
            "Geometry Dash Not Found",
            "The Geometry Dash Resources folder could not be found.\n\n"
            "If you installed GD in another Steam library, "
            "change GD_RESOURCES_FOLDER in the script."
        )
        return

    # Warn the user before changing their game files.
    confirmed = messagebox.askyesno(
        "Confirm Music Change",
        "Make sure Geometry Dash is CLOSED!\n\n"
        f"New music: {filename}\n\n"
        "Your original menu music will be backed up "
        "if a backup does not already exist.\n\n"
        "Continue?"
    )

    if not confirmed:
        return

    try:
        # Back up the original menu music only once.
        if TARGET_FILE.exists() and not BACKUP_FILE.exists():
            shutil.copy2(TARGET_FILE, BACKUP_FILE)

        # Copy the selected song to a temporary file first.
        # This keeps the original Downloads file untouched.
        temporary_file = GD_RESOURCES_FOLDER / "menuLoop_temp.mp3"

        try:
            shutil.copy2(source_file, temporary_file)

            # Replace menuLoop.mp3 with the new music.
            os.replace(temporary_file, TARGET_FILE)

        finally:
            # Clean up any leftover temporary file.
            if temporary_file.exists():
                temporary_file.unlink()

        messagebox.showinfo(
            "Success!",
            f"Your background music has been changed!\n\n"
            f"Selected song: {filename}\n\n"
            "Open Geometry Dash to enjoy your new music!"
        )

    except PermissionError:
        messagebox.showerror(
            "Permission Denied",
            "Windows could not modify the Geometry Dash files.\n\n"
            "Close Geometry Dash and check whether Windows "
            "allows you to write to its Resources folder."
        )

    except OSError as error:
        messagebox.showerror(
            "Error",
            f"Something went wrong:\n\n{error}"
        )


# ==========================================
# APP WINDOW
# ==========================================

root = tk.Tk()
root.title("Geometry Dash Music Changer")
root.geometry("500x330")
root.resizable(False, False)
root.configure(bg="#20232b")

# Main title
title_label = tk.Label(
    root,
    text="Geometry Dash Music Changer",
    font=("Arial", 17, "bold"),
    fg="#ffffff",
    bg="#20232b"
)
title_label.pack(pady=(20, 12))

# Filename label
filename_label = tk.Label(
    root,
    text="Enter the MP3 filename from your Downloads folder:",
    font=("Arial", 10),
    fg="#ffffff",
    bg="#20232b"
)
filename_label.pack(pady=(0, 8))

# Filename input
filename_entry = tk.Entry(
    root,
    font=("Arial", 12),
    width=38,
    justify="center"
)
filename_entry.pack(pady=(0, 8))

# MP3 warning below the input box
mp3_warning = tk.Label(
    root,
    text=(
        'MP3 Files allowed only. Make sure the file you put in is '
        'an MP3 File before pressing the "Turn into Background Music" button.'
    ),
    font=("Arial", 9),
    fg="red",
    bg="#20232b",
    wraplength=455,
    justify="center"
)
mp3_warning.pack(padx=15, pady=(0, 15))

# Main action button
change_button = tk.Button(
    root,
    text="Turn into Background Music",
    font=("Arial", 11, "bold"),
    bg="#5865f2",
    fg="white",
    activebackground="#4752c4",
    activeforeground="white",
    relief="flat",
    padx=12,
    pady=9,
    cursor="hand2",
    command=turn_into_background_music
)
change_button.pack(pady=(0, 15))

# Bottom warning
bottom_warning = tk.Label(
    root,
    text=(
        'Warning: You HAVE to have your Geometry Dash closed '
        'before pressing the "Turn into Background Music" button.'
    ),
    font=("Arial", 9, "bold"),
    fg="red",
    bg="#20232b",
    wraplength=455,
    justify="center"
)
bottom_warning.pack(side="bottom", padx=15, pady=12)

# Start the application
root.mainloop()
