import os
import sys
import time
import tkinter as tk
import tkinter.ttk as ttk
import json
import bcrypt
import tkinter.messagebox as tkmb
import random
import gc
from PIL import Image, ImageTk
import dialogue

appdata = json.load(open("appdata.json", "r"))
fontconfig = json.load(open(os.path.join("resources", "font.json"), "r"))

root = tk.Tk()
root.title("Navratil Creator Manager " + appdata["version"])

import tkinter as tk
import tkinter.ttk as ttk


def clearFrame(frame):
    for item in frame.winfo_children():
        item.destroy()
        frame.update()


def onExit():
    adminPwd(2)

def makePurchasePanel():
    pass

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
    dialog_width = processWindow.winfo_reqwidth()  # Now get the correct width
    dialog_height = processWindow.winfo_reqheight()  # Now get the correct height
    x = (
        screen_width - dialog_width
    ) // 2  # Use // for integer division for pixel positions
    y = (
        screen_height - dialog_height
    ) // 2  # Use // for integer division for pixel positions
    processWindow.geometry(f"+{x}+{y}")

    processWindow.update()

    clearFrame(root)
    root.attributes("-fullscreen", True)

    gc.collect()

    root.update()

    thenavbankimg = Image.open(os.path.join("resources", "thenavbank.png")).resize(
        (root.winfo_width() - 10, root.winfo_height() //2 - 10),
        Image.Resampling.LANCZOS,
    )
    root.thenavbankimgtk = ImageTk.PhotoImage(thenavbankimg)
    thenavbankimgtklbl = tk.Label(root, image=root.thenavbankimgtk)
    thenavbankimgtklbl.pack(padx=10, pady=10, fill="x", expand=True, side=tk.TOP)
    
    cbalancebtn = tk.Button(root, text="Check Balance", font=fontconfig["kioskbuttonfont"])
    pbutton = tk.Button(root, text="Make Purchase", font=fontconfig["kioskbuttonfont"])
    mbutton = tk.Button(root, text="Manage Account", font=fontconfig["kioskbuttonfont"])
    minbutton = ttk.Button(root, text="Hide", command=lambda: root.iconify())

    minbutton.pack(anchor="e", side="bottom")
    mbutton.pack(side="bottom", fill="both", padx=10, pady=10)
    pbutton.pack(side="bottom", fill="both", padx=10, pady=(0, 10))
    cbalancebtn.pack(side="bottom", fill="both", padx=10, pady=(0, 10))

    root.wm_protocol("WM_DELETE_WINDOW", onExit)
    
    root.bind("<Control-F4>", lambda e: onExit())
    
    processWindow.destroy()


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
    if act == 2:
        pwdwind.overrideredirect(True)

    def check(pwdentry: ttk.Entry):
        if act == 1:
            diag = dialogue.create_progress_dialog(
                pwdwind, "The system is now processing the chkpwd task (0/4)", 4
            )
        elif act == 2:
            sample = tk.Tk()
            sample.update()
            diag = dialogue.create_progress_dialog(
                sample, "The system is now processing the onExit task (0/1)...", 1
            )
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
            elif act == 2:
                time.sleep(1)
                root.destroy()
                dialogue.message_set(
                    diag, "The system is now processing the onExit task (1/1) ... done"
                )
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
            if act == 2:
                sample.destroy()

    pwdwind.title("Navratil Creator Manager - Administrator Req'd")

    pdtext = ttk.Label(pwdwind, text="Administrator Password")
    pdentry = ttk.Entry(pwdwind, width=75, show="*")
    cancbutton = ttk.Button(pwdwind, text="Cancel", command=pwdwind.destroy)
    okbutton = ttk.Button(pwdwind, text="Ok", command=lambda: check(pdentry))

    pdtext.pack(padx=5, pady=5, anchor="w")
    root.update()
    pdentry.pack(padx=5, pady=(0, 5), anchor="w", fill="x")
    root.update()
    okbutton.pack(side="right", anchor="s", padx=5, pady=(0, 5))
    root.update()
    cancbutton.pack(side="right", anchor="s", padx=5, pady=(0, 5))
    root.update()

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
