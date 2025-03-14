function doAction(action) {
    def do_GET(self):
        if self.path.startswith("/python_action"):
            self.handle_python_action()
            return
        # ... other code ...

    def handle_python_action(self):
        """Handles actions based on query parameters."""
        from urllib.parse import urlparse, parse_qs

        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        action = query_params.get("action", [None])[0]

        if action == "action1":
            message = "Action 1 performed!"
            # Perform action 1
        elif action == "action2":
            message = "Action 2 performed!"
            # Perform action 2
        else:
            message = "Invalid action."

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(message.encode())
}