import sys
import time
import tkinter as tk
import tkinter.ttk as ttk
import threading
import queue
import traceback
import json
import bcrypt
import tkinter.messagebox as tkmb
import random
import gc

import dialogue

appdata = json.load(open("appdata.json", "r"))

root = tk.Tk()
root.title("Navratil Creator Manager " + appdata["version"])

import tkinter as tk
import tkinter.ttk as ttk


def clearFrame(frame):
    for item in frame.winfo_children():
        item.destroy()

def onExit():
    adminPwd(2)

def kioskPanel():
    processWindow = tk.Toplevel(root)
    processWindow.overrideredirect(True)
    
    label = tk.Label(processWindow, text="Launching, please wait...")
    label.pack(side=tk.LEFT)
    
    processWindow.attributes("-topmost", True)
    processWindow.geometry("250x100")
    processWindow.update()
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    dialog_width = processWindow.winfo_reqwidth() # Now get the correct width
    dialog_height = processWindow.winfo_reqheight() # Now get the correct height
    x = (screen_width - dialog_width) // 2  # Use // for integer division for pixel positions
    y = (screen_height - dialog_height) // 2  # Use // for integer division for pixel positions
    processWindow.geometry(f"+{x}+{y}")
    
    processWindow.update()
    
    time.sleep(2.5)
    
    clearFrame(root)
    root.attributes("-fullscreen", True)
    
    time.sleep(1)
    
    processWindow.destroy()
    
    gc.collect()
    
    exitbutton = ttk.Button(root, text="Exit", command=onExit)
    
    exitbutton.pack(side=tk.RIGHT, anchor=tk.S)
    
    root.wm_protocol("WM_DELETE_WINDOW", onExit)
    
    


def adminPanel():
    clearFrame(root)
    root.title(
        "Navratil Creator Manager " + appdata["version"] + " - Administrator Mode"
    )
    root.state("zoomed")

    menubar = tk.Menu(root)

    filemenu = tk.Menu(root, tearoff=0)
    viewmenu = tk.Menu(root, tearoff=0)
    selectionmenu = tk.Menu(root, tearoff=0)
    helpmenu = tk.Menu(root, tearoff=0)

    filemenu.add_command(label="New Entry")
    filemenu.add_command(label="Edit Entry")
    filemenu.add_command(label="Delete Entry")
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.destroy)

    root.config(menu=menubar)

    root.mainloop()


def adminPwd(act):
    pwdwind = tk.Toplevel(root)
    pwdwind.attributes("-topmost", True)
    if act==2:
        pwdwind.overrideredirect(True)
    def check(pwdentry: ttk.Entry):
        if act == 1:
            diag = dialogue.create_progress_dialog(
                pwdwind, "The system is now processing the chkpwd task (0/4)", 4
            )
        elif act==2:
            sample = tk.Tk()
            sample.update()
            diag = dialogue.create_progress_dialog(sample, "The system is now processing the onExit task (0/1)...", 1)
        if bcrypt.checkpw(
            pwdentry.get().encode("utf-8"), appdata["adminpwd"].encode("utf-8")
        ):
            if act == 1:
                time.sleep(0.1)
                dialogue.message_set(
                    diag, "The system is now processing the chkusr task (1/4)"
                )
                dialogue.progress_set(diag, 1)
                time.sleep(random.random())
                dialogue.message_set(
                    diag, "The system is now processing the chkent task (2/4)"
                )
                dialogue.progress_set(diag, 2)
                time.sleep(random.random())
                dialogue.message_set(
                    diag, "The system is now processing the cleanup task (3/4)"
                )
                dialogue.progress_set(diag, 3)
                time.sleep(random.random())
                dialogue.message_set(
                    diag, "The system is now processing the cleanup task (4/4) ... done"
                )
                dialogue.progress_set(diag, 4)
                gc.collect()
                time.sleep(random.random())
                diag.destroy()
                pwdwind.destroy()
                adminPanel()
            elif act==2:
                time.sleep(1)
                root.destroy()
                dialogue.message_set(diag, "The system is now processing the onExit task (1/1) ... done")
                dialogue.progress_set(diag, 1)
                time.sleep(1)
                sys.exit()
        else:
            diag.destroy()
            tkmb.showerror(
                "Incorrect Password",
                "The password you've entered is incorrect",
                detail="Please try again",
                parent=pwdwind,
            )
            pwdentry.selection_range(0, "end")
            pwdentry.focus_force()
            if act==2:
                sample.destroy()

    pwdwind.title("Navratil Creator Manager - Administrator Req'd")

    pdtext = ttk.Label(pwdwind, text="Administrator Password")
    pdentry = ttk.Entry(pwdwind, width=75, show="*")
    cancbutton = ttk.Button(pwdwind, text="Cancel", command=pwdwind.destroy)
    okbutton = ttk.Button(pwdwind, text="Ok", command=lambda: check(pdentry))

    pdtext.pack(padx=5, pady=5, anchor="w")
    pdentry.pack(padx=5, pady=(0, 5), anchor="w", fill="x")
    okbutton.pack(side="right", anchor="s", padx=5, pady=(0, 5))
    cancbutton.pack(side="right", anchor="s", padx=5, pady=(0, 5))

    pdentry.bind("<Return>", lambda e: check(pdentry))
    pdentry.focus_force()

    pwdwind.mainloop()


def main():

    selbtnmanm = tk.Button(
        root, text="Administrator Mode", font=("", 30), command=lambda: adminPwd(1)
    )
    selbtnkiok = tk.Button(root, text="Kiok Mode", font=("", 30), command=kioskPanel)

    selbtnmanm.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    selbtnkiok.grid(row=1, column=0, padx=5, pady=(0, 5), sticky=tk.NSEW)

    root.grid_columnconfigure(0, weight=1)

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)

    root.mainloop()


main()
