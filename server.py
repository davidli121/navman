import http.server
import socketserver
import threading
import tkinter as tk
from tkinter import messagebox
import webbrowser
import os

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            if os.path.exists("pg/index.html"):
                self.path = "pg/index.html"
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def run_server(port):
    """Starts the local HTTP server."""
    Handler = MyHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        httpd.serve_forever()

def main():
    """Main function to start the server, display the address, and handle shutdown."""
    port = 8000  # You can change this port number
    server_thread = threading.Thread(target=run_server, args=(port,))
    server_thread.daemon = True  # Allows the thread to be killed when the main program exits
    server_thread.start()

    root = tk.Tk()
    root.title("Localhost Running")
    root.iconify()
    label = tk.Label(root, text=f"Localhost running on http://localhost:{port}")
    label.pack(padx=20, pady=20)

    url = f"http://localhost:{port}"
    messagebox.showinfo("Running", f"The Navratil Creator Maanger Localhost is currently running on http://localhost:{port}", detail="The program will open automatically once you press [OK], please do not close the program window while the browser window is active.")
    webbrowser.open(url)

    def on_closing():
        """Stops the server and closes the window."""
        root.destroy()
        os._exit(0) #closes the server.

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()