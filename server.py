import http.server
import socketserver
import threading
import tkinter as tk
from tkinter import messagebox
import webbrowser
import os
import requests
import json
from urllib.parse import urlparse, parse_qs


def load_firebase_config():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "resources", "dedede.json")
        with open(file_path, "r") as f:
            config = json.load(f)
            return config.get("databaseURL"), config.get("databaseSecret")
    except FileNotFoundError:
        print("Error: dedede.json not found.")
        return None, None
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in dedede.json.")
        return None, None
    except Exception as e:
        print(f"An unexpected error occured: {e}")
        return None, None


DATABASE_URL, DATABASE_SECRET = load_firebase_config()


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            if os.path.exists("pg/index.html"):
                self.path = "pg/index.html"
        elif self.path.startswith("/firebase"):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            action = query_params.get("action", [None])[0]
            if action == "fget":
                pass
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def firebaseHandler(self):
        def get_data(path):
            url = f"{DATABASE_URL}{path}.json"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code}")
                return None

def run_server(port):
    Handler = MyHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        httpd.serve_forever()


def main():
    port = 42688
    server_thread = threading.Thread(target=run_server, args=(port,))
    server_thread.daemon = True
    server_thread.start()

    root = tk.Tk()
    root.title("Localhost Running")
    root.iconify()
    label = tk.Label(root, text=f"Localhost running on http://localhost:{port}")
    label.pack(padx=20, pady=20)

    url = f"http://localhost:{port}"
    messagebox.showinfo(
        "Running",
        f"The Navratil Creator Maanger Localhost is currently running on http://localhost:{port}",
        detail="The program will open automatically once you press [OK], please do not close the program window while the browser window is active.",
    )
    webbrowser.open(url)

    def on_closing():
        root.destroy()
        os._exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
