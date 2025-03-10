import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from tkinter import simpledialog

def create_progress_dialog(root, message="Processing...", max_value=100):
    """Creates a modal dialog with a progress bar and message."""

    dialog = tk.Toplevel(root)
    dialog.title("Processing")
    dialog.resizable(False, False)
    dialog.overrideredirect(True) # Keep this if you want no decorations

    def prevent_close():
        pass
    dialog.protocol("WM_DELETE_WINDOW", prevent_close)

    message_label = tk.Label(dialog, text=message)
    message_label.pack(padx=10, pady=(10, 0))

    progress_bar = ttk.Progressbar(dialog, orient=tk.HORIZONTAL, length=200, mode='determinate', maximum=max_value)
    progress_bar.pack(pady=10, fill='x', padx=10)

    dialog.update_idletasks()  # Force layout to update and get correct size

    # Center the dialog
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    dialog_width = dialog.winfo_reqwidth() # Now get the correct width
    dialog_height = dialog.winfo_reqheight() # Now get the correct height
    x = (screen_width - dialog_width) // 2  # Use // for integer division for pixel positions
    y = (screen_height - dialog_height) // 2  # Use // for integer division for pixel positions
    dialog.geometry(f"+{x}+{y}")

    dialog.progress_bar = progress_bar
    dialog.message_label = message_label

    dialog.update() #force initial dialog display.
    return dialog

def progress_set(dialog, value):
    """Sets the progress bar value."""
    dialog.progress_bar['value'] = value
    dialog.update() #force update

def message_set(dialog, message):
    """Sets the message label text."""
    dialog.message_label['text'] = message
    dialog.update() #force update


def show_detailed_error_dialog(title, message, more_info=None):
    """
    Displays a modal error dialog with an error symbol, message, and optional "More Info" button.

    Args:
        title (str): The title of the dialog.
        message (str): The error message to display.
        more_info (str, optional): Additional information to display when "More Info" is clicked.
    """
    root = tk.Tk()
    root.withdraw()

    def show_more_info():
        if more_info:
            info_window = tk.Toplevel(root)
            info_window.title("More Information")
            text_area = tk.Text(info_window, wrap=tk.WORD, padx=10, pady=10)
            text_area.insert(tk.END, more_info)
            text_area.config(state=tk.DISABLED)  # Make it read-only
            text_area.pack(fill=tk.BOTH, expand=True)

    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.resizable(False, False) #Prevent resizing

    # Error Icon (using standard messagebox icon)
    messagebox.showerror(title, message, parent=dialog) #This creates the standard error icon and message.

    if more_info:
        more_info_button = ttk.Button(dialog, text="More Info", command=show_more_info)
        more_info_button.pack(pady=(0, 10))

    # Center the dialog on the screen
    dialog.update_idletasks()
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    dialog.geometry(f"+{x}+{y}")

    dialog.transient(root) #Makes the dialog modal
    dialog.wait_window(dialog) #Wait for dialog to be closed.
    root.destroy()