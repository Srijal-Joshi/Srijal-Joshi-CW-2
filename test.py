import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import requests
import threading
import json

class APITool:
    def __init__(self, root):
        self.root = root
        self.root.title("API Tracking Tool with Advanced Features")

        self.create_widgets()

    def create_widgets(self):
        # Label for API Endpoint
        self.label = tk.Label(self.root, text="API Endpoint:")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        # Entry for API Endpoint
        self.endpoint_entry = tk.Entry(self.root, width=50)
        self.endpoint_entry.grid(row=0, column=1, padx=10, pady=10)

        # Track Button
        self.track_button = tk.Button(self.root, text="Track API", command=self.track_api)
        self.track_button.grid(row=0, column=2, padx=10, pady=10)

        # Label for Request Method
        self.method_label = tk.Label(self.root, text="HTTP Method:")
        self.method_label.grid(row=1, column=0, padx=10, pady=10)

        # Dropdown for HTTP Method
        self.method_var = tk.StringVar(value="GET")
        self.method_menu = tk.OptionMenu(self.root, self.method_var, "GET", "POST", "PUT", "DELETE")
        self.method_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Label for Headers
        self.headers_label = tk.Label(self.root, text="Headers (JSON format):")
        self.headers_label.grid(row=2, column=0, padx=10, pady=10)

        # Entry for Headers
        self.headers_entry = tk.Entry(self.root, width=50)
        self.headers_entry.grid(row=2, column=1, padx=10, pady=10)

        # Label for Request Body (for POST/PUT)
        self.body_label = tk.Label(self.root, text="Request Body (JSON format):")
        self.body_label.grid(row=3, column=0, padx=10, pady=10)

        # Scrolled Text for Request Body
        self.body_text = scrolledtext.ScrolledText(self.root, width=50, height=5)
        self.body_text.grid(row=3, column=1, padx=10, pady=10)

        # Label for Authentication
        self.auth_label = tk.Label(self.root, text="Authentication (API Key):")
        self.auth_label.grid(row=4, column=0, padx=10, pady=10)

        # Entry for API Key
        self.api_key_entry = tk.Entry(self.root, width=50)
        self.api_key_entry.grid(row=4, column=1, padx=10, pady=10)

        # Scrolled Text for Output
        self.output_text = scrolledtext.ScrolledText(self.root, width=80, height=20)
        self.output_text.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

    def track_api(self):
        endpoint = self.endpoint_entry.get()
        method = self.method_var.get()
        headers = self.headers_entry.get()
        body = self.body_text.get(1.0, tk.END).strip()
        api_key = self.api_key_entry.get()

        if not endpoint:
            messagebox.showerror("Error", "API Endpoint cannot be empty.")
            return

        # Clear the output area
        self.output_text.delete(1.0, tk.END)

        # Convert headers from JSON string to dictionary
        try:
            headers_dict = json.loads(headers) if headers else {}
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format for headers.")
            return

        # Add API Key to headers if provided
        if api_key:
            headers_dict["Authorization"] = f"Bearer {api_key}"

        # Convert request body from JSON string to dictionary (if applicable)
        if body:
            try:
                body_dict = json.loads(body)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Invalid JSON format for request body.")
                return
        else:
            body_dict = {}

        # Use threading to avoid blocking the GUI
        threading.Thread(target=self.make_request, args=(endpoint, method, headers_dict, body_dict)).start()

    def make_request(self, endpoint, method, headers, body):
        try:
            if method == "GET":
                response = requests.get(endpoint, headers=headers)
            elif method == "POST":
                response = requests.post(endpoint, headers=headers, json=body)
            elif method == "PUT":
                response = requests.put(endpoint, headers=headers, json=body)
            elif method == "DELETE":
                response = requests.delete(endpoint, headers=headers)
            else:
                raise ValueError("Unsupported HTTP Method")

            self.handle_response(response)
        except requests.RequestException as e:
            self.root.after(0, self.display_output, f"Request failed: {e}")
        except Exception as e:
            self.root.after(0, self.display_output, f"An unexpected error occurred: {e}")

    def handle_response(self, response):
        status_code = response.status_code
        headers = response.headers
        content = response.text

        output = f"Status Code: {status_code}\n\n"
        output += "Headers:\n"
        for header, value in headers.items():
            output += f"{header}: {value}\n"
        output += "\nContent:\n"
        output += content

        # Update the GUI with the response
        self.root.after(0, self.display_output, output)

    def display_output(self, output):
        self.output_text.insert(tk.END, output)

# Create the main window
root = tk.Tk()
api_tool = APITool(root)
root.mainloop()
