import time
import tkinter as tk
import tkinter.ttk as ttk
import threading
import queue
import traceback
import json
import bcrypt
import tkinter.messagebox as tkmb

appdata = json.load(open("appdata.json", "r"))

root = tk.Tk()
root.title("Navratil Creator Manager "+appdata["version"])

def adminPanel():
    pass

def adminPwd():
    pwdwind = tk.Toplevel(root)
    def check(pwdentry: ttk.Entry, root):
        if bcrypt.checkpw(pwdentry.get().encode("utf-8"), appdata["adminpwd"].encode("utf-8")):
            root.destroy()
            adminPanel()
        else:
            tkmb.showerror("Incorrect Password", "The password you've entered is incorrect", detail="Please try again", parent=pwdwind)
            pwdentry.selection_range(0, "end")
            pwdentry.focus_force()
    pwdwind.title("Navratil Creator Manager - Elevation required")
    
    pdtext = ttk.Label(pwdwind, text="Elevation required")
    pdentry = ttk.Entry(pwdwind, width=100)
    cancbutton = ttk.Button(pwdwind, text="Cancel", command=pwdwind.destroy)
    okbutton = ttk.Button(pwdwind, text="Ok", command=lambda: check(pdentry, root))
    
    pdtext.pack(padx=5, pady=5, anchor="w")
    pdentry.pack(padx=5, pady=(0, 5), anchor="w", fill="x")
    okbutton.pack(side="right", anchor="s", padx=5, pady=(0, 5))
    cancbutton.pack(side="right", anchor="s", padx=5, pady=(0, 5))
    pwdwind.mainloop()

def main():
    
    selbtnmanm = tk.Button(root, text="Administrator Mode", font=("", 30), command=adminPwd)
    selbtnkiok = tk.Button(root, text="Kiosk Mode", font=("", 30))
    
    selbtnmanm.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
    selbtnkiok.grid(row=1, column=0, padx=5, pady=(0, 5), sticky=tk.NSEW)
    
    root.grid_columnconfigure(0, weight=1)
    
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    
    root.mainloop()

main()