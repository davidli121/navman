import tkinter as tk
import tkinter.ttk as ttk

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
