# Hardware Store Billing System with Database, PDF Receipts, User Auth, and More
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
from datetime import datetime
import os
import sqlite3
import re
import threading
from fpdf import FPDF

# Database setup and connection
def setup_database():
    conn = sqlite3.connect('hardware_store.db')
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          username TEXT UNIQUE NOT NULL,
                          password TEXT NOT NULL,
                          role TEXT NOT NULL
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS products
                      (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT UNIQUE NOT NULL,
                          price REAL NOT NULL,
                          stock INTEGER NOT NULL,
                          barcode TEXT UNIQUE
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
                      (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          bill_no INTEGER NOT NULL,
                          customer_name TEXT NOT NULL,
                          customer_phone TEXT,
                          customer_address TEXT,
                          total REAL NOT NULL,
                          tax REAL NOT NULL,
                          datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
                          user_id INTEGER,
                          FOREIGN KEY(user_id) REFERENCES users(id)
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS transaction_details
                      (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          transaction_id INTEGER,
                          product_id INTEGER,
                          quantity INTEGER NOT NULL,
                          price REAL NOT NULL,
                          FOREIGN KEY(transaction_id) REFERENCES transactions(id),
                          FOREIGN KEY(product_id) REFERENCES products(id)
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS stock_history
                      (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          product_id INTEGER,
                          change INTEGER NOT NULL,
                          new_stock INTEGER NOT NULL,
                          note TEXT,
                          datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
                          user_id INTEGER,
                          FOREIGN KEY(product_id) REFERENCES products(id),
                          FOREIGN KEY(user_id) REFERENCES users(id)
                      )''')

    # Create admin user if none exists
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       ('admin', 'admin123', 'admin'))

    # Add default products if none exist
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        default_products = [
            ("nails", 10, 100, "123456"),
            ("screws", 15, 100, "123457"),
            ("hammers", 250, 50, "123458"),
            ("screwdrivers", 150, 75, "123459"),
            ("pliers", 200, 60, "123460"),
            ("pipes", 180, 80, "123461"),
            ("valves", 350, 40, "123462"),
            ("faucets", 1200, 30, "123463"),
            ("pvc_joints", 45, 120, "123464"),
            ("taps", 800, 25, "123465"),
            ("paint_buckets", 1800, 20, "123466"),
            ("brushes", 120, 70, "123467"),
            ("thinners", 250, 50, "123468"),
            ("rollers", 300, 60, "123469"),
            ("tapes", 80, 90, "123470"),
            ("wires", 25, 200, "123471"),
            ("switches", 120, 65, "123472"),
            ("bulbs", 100, 85, "123473"),
            ("sockets", 85, 75, "123474"),
            ("circuit_breakers", 450, 35, "123475")
        ]
        cursor.executemany("INSERT INTO products (name, price, stock, barcode) VALUES (?, ?, ?, ?)", default_products)

    conn.commit()
    conn.close()

# Run database setup
setup_database()

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Hardware Store - Login")
        self.root.geometry("400x300")
        self.root.configure(bg="#f5f5f5")

        # Center window
        self.root.eval('tk::PlaceWindow . center')

        # Theme colors
        self.bg_color = "#2C3E50"
        self.fg_color = "#ECF0F1"
        self.button_color = "#16A085"

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color, bd=2, relief=tk.GROOVE)
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        title_label = tk.Label(header_frame, text="HARDWARE STORE LOGIN",
                               font=("Arial", 16, "bold"), bg=self.bg_color, fg=self.fg_color)
        title_label.pack(padx=10, pady=10)

        # Login form
        form_frame = tk.Frame(self.root, bg=self.fg_color)
        form_frame.pack(fill=tk.BOTH, padx=20, pady=20, expand=True)

        # Username
        tk.Label(form_frame, text="Username:", font=("Arial", 11),
                 bg=self.fg_color).grid(row=0, column=0, padx=5, pady=10, sticky="e")
        self.username = tk.StringVar()
        username_entry = tk.Entry(form_frame, textvariable=self.username,
                                  font=("Arial", 11), width=25)
        username_entry.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        username_entry.focus()

        # Password
        tk.Label(form_frame, text="Password:", font=("Arial", 11),
                 bg=self.fg_color).grid(row=1, column=0, padx=5, pady=10, sticky="e")
        self.password = tk.StringVar()
        password_entry = tk.Entry(form_frame, textvariable=self.password,
                                  font=("Arial", 11), width=25, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        # Buttons
        button_frame = tk.Frame(form_frame, bg=self.fg_color)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        tk.Button(button_frame, text="Login", command=self.authenticate,
                  font=("Arial", 11, "bold"), bg=self.button_color, fg=self.fg_color,
                  width=10).pack(side=tk.LEFT, padx=10)

        tk.Button(button_frame, text="Exit", command=self.root.destroy,
                  font=("Arial", 11, "bold"), bg="#E74C3C", fg=self.fg_color,
                  width=10).pack(side=tk.RIGHT, padx=10)

        # Status label
        self.status_label = tk.Label(form_frame, text="", font=("Arial", 10),
                                     bg=self.fg_color, fg="#E74C3C")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=5)

    def authenticate(self):
        username = self.username.get().strip()
        password = self.password.get().strip()

        if not username or not password:
            self.status_label.config(text="Please enter both username and password")
            return

        conn = sqlite3.connect('hardware_store.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, password, role FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and user[1] == password:
            self.root.destroy()
            main_root = tk.Tk()
            app = HardwareManagementSystem(main_root, user[0], user[2])
            main_root.mainloop()
        else:
            self.status_label.config(text="Invalid username or password")

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'HARDWARE EMPORIUM', 0, 1, 'C')
        self.set_font('Arial', '', 12)
        self.cell(0, 10, 'Quality Hardware for All Your Project Needs', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

class HardwareManagementSystem:
    def __init__(self, root, user_id, user_role):
        self.root = root
        self.user_id = user_id
        self.user_role = user_role
        self.root.title(f"Hardware Management System - User: {user_id}")
        self.root.geometry("1200x900+0+0")
        self.root.configure(bg="#f5f5f5")

        # Define hardware-themed colors
        self.bg_color = "#2C3E50"  # Dark blue
        self.fg_color = "#ECF0F1"  # Light gray
        self.lbl_color = '#3498DB'  # Blue
        self.highlight_color = "#E74C3C"  # Red for important elements
        self.button_color = "#16A085"  # Green
        self.stock_warning_color = "#F39C12"  # Orange for low stock

        # Database connection
        self.conn = sqlite3.connect('hardware_store.db')
        self.cursor = self.conn.cursor()

        # Load products and prices
        self.cursor.execute("SELECT name, price, stock, barcode FROM products")
        self.products = {row[0]: {'price': row[1], 'stock': row[2], 'barcode': row[3]} for row in
                         self.cursor.fetchall()}
        self.prices = {product: data['price'] for product, data in self.products.items()}
        self.barcode_map = {data['barcode']: product for product, data in self.products.items() if data['barcode']}

        # Initialize variables
        self.bill_no = random.randint(10, 999999)
        self.customer_name = tk.StringVar()
        self.customer_phone = tk.StringVar()
        self.customer_address = tk.StringVar()
        self.low_stock_threshold = 10

        # Create widgets
        self.create_widgets()

        # Create receipts directory
        if not os.path.exists('receipts'):
            os.makedirs('receipts')

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg=self.bg_color, bd=2, relief=tk.GROOVE)
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        title_label = tk.Label(header_frame, text="HARDWARE STORE MANAGEMENT SYSTEM",
                               font=("Arial", 20, "bold"), bg=self.bg_color, fg=self.fg_color)
        title_label.pack(side=tk.LEFT, padx=10, pady=10)

        date_label = tk.Label(header_frame, text=datetime.now().strftime("%d-%m-%Y"),
                              font=("Arial", 12), bg=self.bg_color, fg=self.fg_color)
        date_label.pack(side=tk.RIGHT, padx=10, pady=10)

        # User info
        user_label = tk.Label(header_frame, text=f"User: {self.user_id} ({self.user_role})",
                              font=("Arial", 12), bg=self.bg_color, fg=self.fg_color)
        user_label.pack(side=tk.RIGHT, padx=10)

        # Stock summary button
        stock_button = tk.Button(header_frame, text="Stock Summary", command=self.show_stock_summary,
                                 font=("Arial", 11), bg=self.stock_warning_color, fg=self.fg_color)
        stock_button.pack(side=tk.RIGHT, padx=10)

        # Reports button
        reports_button = tk.Button(header_frame, text="Reports", command=self.show_reports,
                                   font=("Arial", 11), bg="#8E44AD", fg=self.fg_color)
        reports_button.pack(side=tk.RIGHT, padx=10)

        # Customer details
        customer_frame = tk.LabelFrame(self.root, text="Customer Details", font=("Arial", 12, "bold"),
                                       bg=self.fg_color, bd=2, relief=tk.GROOVE)
        customer_frame.pack(fill=tk.X, padx=10, pady=5)

        # Customer name
        tk.Label(customer_frame, text="Customer Name:", font=("Arial", 11),
                 bg=self.fg_color).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        name_entry = tk.Entry(customer_frame, textvariable=self.customer_name,
                              font=("Arial", 11), width=30)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Customer phone
        tk.Label(customer_frame, text="Phone:", font=("Arial", 11),
                 bg=self.fg_color).grid(row=0, column=2, padx=5, pady=5, sticky="e")
        phone_entry = tk.Entry(customer_frame, textvariable=self.customer_phone,
                               font=("Arial", 11), width=20)
        phone_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Bill number
        tk.Label(customer_frame, text=f"Bill No: {self.bill_no}", font=("Arial", 11, "bold"),
                 bg=self.fg_color).grid(row=0, column=4, padx=5, pady=5)

        # Customer address
        tk.Label(customer_frame, text="Address:", font=("Arial", 11),
                 bg=self.fg_color).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        address_entry = tk.Entry(customer_frame, textvariable=self.customer_address,
                                 font=("Arial", 11), width=70)
        address_entry.grid(row=1, column=1, columnspan=4, padx=5, pady=5, sticky="we")

        # Barcode entry
        tk.Label(customer_frame, text="Barcode:", font=("Arial", 11),
                 bg=self.fg_color).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.barcode_var = tk.StringVar()
        barcode_entry = tk.Entry(customer_frame, textvariable=self.barcode_var,
                                 font=("Arial", 11), width=20)
        barcode_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        barcode_entry.bind("<Return>", self.process_barcode)

        # Product categories
        categories_frame = tk.Frame(self.root, bg=self.fg_color)
        categories_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

        # Tools & Fasteners
        tools_frame = tk.LabelFrame(categories_frame, text="Tools & Fasteners",
                                    font=("Arial", 12, "bold"), bg=self.fg_color, bd=2, relief=tk.GROOVE)
        tools_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=True)

        self.tools_inputs = {}
        row = 0
        for product in ["nails", "screws", "hammers", "screwdrivers", "pliers"]:
            # Create label with stock information
            stock = self.products.get(product, {}).get('stock', 0)
            stock_color = "black" if stock > self.low_stock_threshold else self.stock_warning_color
            stock_text = f"{product.title()}: (Stock: {stock})"
            lbl = tk.Label(tools_frame, text=stock_text, font=("Arial", 11),
                           bg=self.fg_color, fg=stock_color)
            lbl.grid(row=row, column=0, padx=5, pady=5, sticky="e")

            # Create spinbox for quantity input
            var = tk.IntVar(value=0)
            self.tools_inputs[product] = (var, lbl)
            spinbox = tk.Spinbox(tools_frame, textvariable=var, from_=0, to=stock if stock > 0 else 0,
                                 font=("Arial", 11), width=8, command=lambda p=product: self.update_stock_display(p))
            spinbox.grid(row=row, column=1, padx=5, pady=5)
            row += 1

        # Plumbing Supplies
        plumbing_frame = tk.LabelFrame(categories_frame, text="Plumbing Supplies",
                                       font=("Arial", 12, "bold"), bg=self.fg_color, bd=2, relief=tk.GROOVE)
        plumbing_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=True)

        self.plumbing_inputs = {}
        row = 0
        for product in ["pipes", "valves", "faucets", "pvc_joints", "taps"]:
            stock = self.products.get(product, {}).get('stock', 0)
            stock_color = "black" if stock > self.low_stock_threshold else self.stock_warning_color
            display_name = product.title().replace('Pvc', 'PVC')
            stock_text = f"{display_name}: (Stock: {stock})"
            lbl = tk.Label(plumbing_frame, text=stock_text, font=("Arial", 11),
                           bg=self.fg_color, fg=stock_color)
            lbl.grid(row=row, column=0, padx=5, pady=5, sticky="e")

            var = tk.IntVar(value=0)
            self.plumbing_inputs[product] = (var, lbl)
            spinbox = tk.Spinbox(plumbing_frame, textvariable=var, from_=0, to=stock if stock > 0 else 0,
                                 font=("Arial", 11), width=8, command=lambda p=product: self.update_stock_display(p))
            spinbox.grid(row=row, column=1, padx=5, pady=5)
            row += 1

        # Paint & Supplies
        paint_frame = tk.LabelFrame(categories_frame, text="Paint & Supplies",
                                    font=("Arial", 12, "bold"), bg=self.fg_color, bd=2, relief=tk.GROOVE)
        paint_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=True)

        self.paint_inputs = {}
        row = 0
        for product in ["paint_buckets", "brushes", "thinners", "rollers", "tapes"]:
            stock = self.products.get(product, {}).get('stock', 0)
            stock_color = "black" if stock > self.low_stock_threshold else self.stock_warning_color
            display_name = product.title().replace("_", " ")
            if display_name == "Tapes":
                display_name = "Painter's Tape"
            stock_text = f"{display_name}: (Stock: {stock})"
            lbl = tk.Label(paint_frame, text=stock_text, font=("Arial", 11),
                           bg=self.fg_color, fg=stock_color)
            lbl.grid(row=row, column=0, padx=5, pady=5, sticky="e")

            var = tk.IntVar(value=0)
            self.paint_inputs[product] = (var, lbl)
            spinbox = tk.Spinbox(paint_frame, textvariable=var, from_=0, to=stock if stock > 0 else 0,
                                 font=("Arial", 11), width=8, command=lambda p=product: self.update_stock_display(p))
            spinbox.grid(row=row, column=1, padx=5, pady=5)
            row += 1

        # Electrical Supplies
        electrical_frame = tk.LabelFrame(categories_frame, text="Electrical Supplies",
                                         font=("Arial", 12, "bold"), bg=self.fg_color, bd=2, relief=tk.GROOVE)
        electrical_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=True)

        self.electrical_inputs = {}
        row = 0
        for product in ["wires", "switches", "bulbs", "sockets", "circuit_breakers"]:
            stock = self.products.get(product, {}).get('stock', 0)
            stock_color = "black" if stock > self.low_stock_threshold else self.stock_warning_color
            stock_text = f"{product.title()}: (Stock: {stock})"
            lbl = tk.Label(electrical_frame, text=stock_text, font=("Arial", 11),
                           bg=self.fg_color, fg=stock_color)
            lbl.grid(row=row, column=0, padx=5, pady=5, sticky="e")

            var = tk.IntVar(value=0)
            self.electrical_inputs[product] = (var, lbl)
            spinbox = tk.Spinbox(electrical_frame, textvariable=var, from_=0, to=stock if stock > 0 else 0,
                                 font=("Arial", 11), width=8, command=lambda p=product: self.update_stock_display(p))
            spinbox.grid(row=row, column=1, padx=5, pady=5)
            row += 1

        # Buttons
        button_frame = tk.Frame(self.root, bg=self.fg_color)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(button_frame, text="Calculate Total", command=self.calculate_total,
                  font=("Arial", 11, "bold"), bg=self.button_color, fg=self.fg_color,
                  width=15, height=2).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Generate Bill", command=self.generate_bill,
                  font=("Arial", 11, "bold"), bg=self.button_color, fg=self.fg_color,
                  width=15, height=2).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Save Receipt", command=lambda: threading.Thread(target=self.save_bill, daemon=True).start(),
                  font=("Arial", 11, "bold"), bg=self.button_color, fg=self.fg_color,
                  width=15, height=2).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Clear All", command=self.clear_all,
                  font=("Arial", 11, "bold"), bg=self.button_color, fg=self.fg_color,
                  width=15, height=2).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Restock Items", command=self.show_restock_dialog,
                  font=("Arial", 11, "bold"), bg=self.stock_warning_color, fg=self.fg_color,
                  width=15, height=2).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Exit", command=self.exit_app,
                  font=("Arial", 11, "bold"), bg=self.highlight_color, fg=self.fg_color,
                  width=15, height=2).pack(side=tk.LEFT, padx=5)

        # Output area
        output_frame = tk.LabelFrame(self.root, text="Bill Summary",
                                     font=("Arial", 12, "bold"), bg=self.fg_color, bd=2, relief=tk.GROOVE)
        output_frame.pack(fill=tk.BOTH, padx=10, pady=5, expand=True)

        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD,
                                                     font=("Courier New", 10), height=15)
        self.output_text.pack(fill=tk.BOTH, padx=5, pady=5, expand=True)

        # Instructions
        instructions_frame = tk.Frame(self.root, bg="#f0f8ff", bd=1, relief=tk.GROOVE)
        instructions_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(instructions_frame, text="Instructions:", font=("Arial", 11, "bold"),
                 bg="#f0f8ff", fg="#2C3E50").pack(anchor="w", padx=5, pady=5)

        instructions = [
            "1. Enter customer details (name is required)",
            "2. Select product quantities (stock levels shown in orange if low)",
            "3. Click 'Calculate Total' to see category totals",
            "4. Click 'Generate Bill' to create a receipt preview",
            "5. Click 'Save Receipt' to save as a PDF and update stock",
            "6. Use 'Clear All' to start a new transaction",
            "7. Use 'Restock Items' to add inventory",
            "8. Use 'Stock Summary' to view current inventory levels",
            "9. Use 'Reports' for sales and stock analysis",
            "10. Scan barcode and press Enter to add items"
        ]

        for instruction in instructions:
            tk.Label(instructions_frame, text=instruction, font=("Arial", 10),
                     bg="#f0f8ff", fg="#2C3E50", justify="left").pack(anchor="w", padx=20)

        tk.Label(instructions_frame, text="Note: Receipts are saved in the 'receipts' folder",
                 font=("Arial", 10), bg="#f0f8ff", fg=self.highlight_color).pack(anchor="w", padx=20, pady=(0, 5))

    def process_barcode(self, event=None):
        barcode = self.barcode_var.get().strip()
        if not barcode:
            return

        product = self.barcode_map.get(barcode)
        if not product:
            messagebox.showwarning("Barcode Error", "Invalid barcode. Product not found!")
            self.barcode_var.set("")
            return

        # Find which category the product belongs to
        category = None
        if product in self.tools_inputs:
            category = self.tools_inputs
        elif product in self.plumbing_inputs:
            category = self.plumbing_inputs
        elif product in self.paint_inputs:
            category = self.paint_inputs
        elif product in self.electrical_inputs:
            category = self.electrical_inputs

        if category:
            var, lbl = category[product]
            var.set(var.get() + 1)
            self.update_stock_display(product)
            self.barcode_var.set("")
        else:
            messagebox.showwarning("Product Error", "Product not found in categories")

    def validate_phone(self, phone):
        if not phone:
            return True  # Phone is optional
        # Simple phone validation (at least 10 digits)
        return re.match(r'^[0-9+-\s]{10,}$', phone) is not None

    def update_stock_display(self, product):
        """Update stock display after quantity change"""
        # Find which category the product belongs to
        inputs_dict = None
        if product in self.tools_inputs:
            inputs_dict = self.tools_inputs
        elif product in self.plumbing_inputs:
            inputs_dict = self.plumbing_inputs
        elif product in self.paint_inputs:
            inputs_dict = self.paint_inputs
        elif product in self.electrical_inputs:
            inputs_dict = self.electrical_inputs

        if inputs_dict:
            var, lbl = inputs_dict[product]
            current_stock = self.products.get(product, {}).get('stock', 0)
            ordered = var.get()
            available = max(0, current_stock - ordered)

            # Update label color based on available stock
            stock_color = "black" if available > self.low_stock_threshold else self.stock_warning_color
            display_name = product.replace('_', ' ').title()
            if "Pvc" in display_name:
                display_name = display_name.replace("Pvc", "PVC")
            if display_name == "Tapes":
                display_name = "Painter's Tape"

            lbl.config(text=f"{display_name}: (Stock: {available})", fg=stock_color)

            # Update spinbox max value
            for frame in [self.tools_inputs, self.plumbing_inputs, self.paint_inputs, self.electrical_inputs]:
                if product in frame:
                    var, lbl = frame[product]
                    spinbox = lbl.master.grid_slaves(row=lbl.grid_info()["row"], column=1)[0]
                    spinbox.config(to=available if available > 0 else 0)

    def calculate_total(self):
        customer_name = self.customer_name.get().strip()
        if not customer_name:
            messagebox.showwarning("Input Error", "Please enter customer name!")
            return

        # Validate phone number
        if not self.validate_phone(self.customer_phone.get()):
            messagebox.showwarning("Input Error", "Invalid phone number format!")
            return

        # Calculate totals
        tools_total = sum(self.tools_inputs[item][0].get() * self.prices[item] for item in self.tools_inputs)
        plumbing_total = sum(self.plumbing_inputs[item][0].get() * self.prices[item] for item in self.plumbing_inputs)
        paint_total = sum(self.paint_inputs[item][0].get() * self.prices[item] for item in self.paint_inputs)
        electrical_total = sum(
            self.electrical_inputs[item][0].get() * self.prices[item] for item in self.electrical_inputs)

        # Calculate ETR
        tools_tax = round(tools_total * 0.05)
        plumbing_tax = round(plumbing_total * 0.05)
        paint_tax = round(paint_total * 0.05)
        electrical_tax = round(electrical_total * 0.05)

        # Grand total
        grand_total = tools_total + plumbing_total + paint_total + electrical_total + \
                      tools_tax + plumbing_tax + paint_tax + electrical_tax

        # Display results
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "=" * 80 + "\n")
        self.output_text.insert(tk.END, f"{'HARDWARE STORE MANAGEMENT SYSTEM':^80}\n")
        self.output_text.insert(tk.END, "=" * 80 + "\n")
        self.output_text.insert(tk.END,
                                f"Bill No: {self.bill_no} {'Date:':>50} {datetime.now().strftime('%d-%m-%Y')}\n")
        self.output_text.insert(tk.END, f"Customer: {customer_name}\n")
        self.output_text.insert(tk.END, f"Phone: {self.customer_phone.get()}\n")
        self.output_text.insert(tk.END, f"Address: {self.customer_address.get()}\n")
        self.output_text.insert(tk.END, "-" * 80 + "\n")

        # Create a table for totals
        self.output_text.insert(tk.END, f"{'Category':<20}{'Subtotal':>20}{'Tax':>20}\n")
        self.output_text.insert(tk.END, "-" * 80 + "\n")
        self.output_text.insert(tk.END, f"{'Tools':<20}{'Ksh.' + str(tools_total):>20}{'Ksh.' + str(tools_tax):>20}\n")
        self.output_text.insert(tk.END,
                                f"{'Plumbing':<20}{'Ksh.' + str(plumbing_total):>20}{'Ksh.' + str(plumbing_tax):>20}\n")
        self.output_text.insert(tk.END, f"{'Paint':<20}{'Ksh.' + str(paint_total):>20}{'Ksh.' + str(paint_tax):>20}\n")
        self.output_text.insert(tk.END,
                                f"{'Electrical':<20}{'Ksh.' + str(electrical_total):>20}{'Ksh.' + str(electrical_tax):>20}\n")
        self.output_text.insert(tk.END, "-" * 80 + "\n")
        self.output_text.insert(tk.END, f"{'GRAND TOTAL:':<40}Ksh.{grand_total}\n")
        self.output_text.insert(tk.END, "=" * 80 + "\n")

    def generate_bill_text(self):
        customer_name = self.customer_name.get().strip()
        if not customer_name:
            return " Please enter customer name!", None, None

        # Calculate totals
        tools_total = sum(self.tools_inputs[item][0].get() * self.prices[item] for item in self.tools_inputs)
        plumbing_total = sum(self.plumbing_inputs[item][0].get() * self.prices[item] for item in self.plumbing_inputs)
        paint_total = sum(self.paint_inputs[item][0].get() * self.prices[item] for item in self.paint_inputs)
        electrical_total = sum(
            self.electrical_inputs[item][0].get() * self.prices[item] for item in self.electrical_inputs)

        # Calculate ETR
        tools_tax = round(tools_total * 0.05)
        plumbing_tax = round(plumbing_total * 0.05)
        paint_tax = round(paint_total * 0.05)
        electrical_tax = round(electrical_total * 0.05)

        # Grand total
        grand_total = tools_total + plumbing_total + paint_total + electrical_total + \
                      tools_tax + plumbing_tax + paint_tax + electrical_tax

        # Generate bill header
        bill_text = "\n" + "=" * 80 + "\n"
        bill_text += f"{'HARDWARE EMPORIUM':^80}\n"
        bill_text += f"{'=' * 80}\n"
        bill_text += f"Bill No: {self.bill_no} {'Date:':>50} {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
        bill_text += f"Customer: {customer_name}\n"
        bill_text += f"Phone: {self.customer_phone.get()}\n"
        bill_text += f"Address: {self.customer_address.get()}\n"
        bill_text += f"Attendant: User {self.user_id} ({self.user_role})\n"
        bill_text += "-" * 80 + "\n"
        bill_text += f"{'Product':<30}{'Qty':>10}{'Price':>15}{'Amount':>15}\n"
        bill_text += "-" * 80 + "\n"

        # Add products to bill
        all_inputs = {
            "Tools": self.tools_inputs,
            "Plumbing": self.plumbing_inputs,
            "Paint": self.paint_inputs,
            "Electrical": self.electrical_inputs
        }

        for category, products in all_inputs.items():
            for item, (var, lbl) in products.items():
                qty = var.get()
                if qty > 0:
                    price = self.prices[item]
                    amount = qty * price
                    product_name = item.replace('_', ' ').title()
                    if "Pvc" in product_name:
                        product_name = product_name.replace("Pvc", "PVC")
                    if product_name == "Tapes":
                        product_name = "Painter's Tape"
                    bill_text += f"{product_name:<30}{qty:>10}Ksh.{price:>14}Ksh.{amount:>14}\n"

        bill_text += "-" * 80 + "\n"
        bill_text += f"{'SUBTOTAL:':<50}Ksh.{grand_total - (tools_tax + plumbing_tax + paint_tax + electrical_tax)}\n"
        bill_text += f"{'TAX (5%):':<50}Ksh.{tools_tax + plumbing_tax + paint_tax + electrical_tax}\n"
        bill_text += f"{'GRAND TOTAL:':<50}Ksh.{grand_total}\n"
        bill_text += "=" * 80 + "\n"
        bill_text += f"{'THANK YOU FOR YOUR BUSINESS!':^80}\n"
        bill_text += f"{'Quality Hardware for All Your Project Needs':^80}\n"
        bill_text += "=" * 80

        return bill_text, customer_name, grand_total

    def generate_bill(self):
        bill_text, customer_name, _ = self.generate_bill_text()
        if customer_name is None:
            messagebox.showwarning("Input Error", bill_text)
            return

        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, bill_text)

    def save_bill(self):
        bill_text, customer_name, grand_total = self.generate_bill_text()
        
        if customer_name is None:
            messagebox.showwarning("Input Error", bill_text)
            return
            
        # Create a new database connection for this thread
        def save_in_thread():
            try:
                conn = sqlite3.connect('hardware_store.db')
                cursor = conn.cursor()
                
                # Insert transaction
                cursor.execute('''INSERT INTO transactions
                                (bill_no, customer_name, customer_phone, customer_address, total, tax, user_id)
                                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                                (self.bill_no, customer_name, self.customer_phone.get(),
                                self.customer_address.get(), grand_total,
                                grand_total - (grand_total / 1.05), self.user_id))
                transaction_id = cursor.lastrowid

                # Insert transaction details
                for category in [self.tools_inputs, self.plumbing_inputs, self.paint_inputs, self.electrical_inputs]:
                    for product, (var, lbl) in category.items():
                        qty = var.get()
                        if qty > 0:
                            price = self.prices[product]
                            cursor.execute('''INSERT INTO transaction_details
                                            (transaction_id, product_id, quantity, price)
                                        VALUES (?, (SELECT id FROM products WHERE name = ?), ?, ?)''',
                                        (transaction_id, product, qty, price))

                # Update stock levels
                for category in [self.tools_inputs, self.plumbing_inputs, self.paint_inputs, self.electrical_inputs]:
                    for product, (var, lbl) in category.items():
                        qty = var.get()
                        if qty > 0:
                            cursor.execute("UPDATE products SET stock = stock - ? WHERE name = ?", (qty, product))
                            cursor.execute('''INSERT INTO stock_history
                                            (product_id, change, new_stock, note, user_id)
                                        VALUES ((SELECT id FROM products WHERE name = ?), ?,
                                                (SELECT stock FROM products WHERE name = ?), ?, ?)''',
                                        (product, -qty, product,
                                        f"Sold {qty} units in transaction {transaction_id}",
                                        self.user_id))

                conn.commit()
                
                # Generate PDF receipt
                pdf = PDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                # Add receipt content
                lines = bill_text.split('\n')
                for line in lines:
                    if '=' in line:  # Draw line
                        pdf.set_font("Arial", 'B', 12)
                        pdf.cell(0, 10, line.replace('=', '').strip(), 0, 1, 'C')
                    else:
                        pdf.set_font("Arial", size=10)
                        pdf.cell(0, 7, line, 0, 1)

                # Create filename
                filename = f"capstone project/{customer_name.replace(' ', '_')}_{self.bill_no}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                pdf.output(filename)

                # Schedule UI updates on main thread
                self.root.after(0, lambda: self.on_save_complete(filename))
            except sqlite3.Error as e:
                self.root.after(0, lambda: messagebox.showerror("Database Error", f"Error saving transaction: {str(e)}"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("PDF Error", f"Error generating PDF: {str(e)}"))
            finally:
                try:
                    conn.close()
                except:
                    pass

        # Start the save operation in a new thread
        threading.Thread(target=save_in_thread, daemon=True).start()

    def on_save_complete(self, filename):
        """Called after save operation completes successfully"""
        messagebox.showinfo("Success", f" Receipt saved successfully as:\n{filename}")
        self.clear_all()

    def clear_all(self):
        # Clear inputs
        self.customer_name.set("")
        self.customer_phone.set("")
        self.customer_address.set("")
        self.barcode_var.set("")

        # Generate new bill number
        self.bill_no = random.randint(100, 9999999)

        # Reset all quantities
        for category in [self.tools_inputs, self.plumbing_inputs,
                         self.paint_inputs, self.electrical_inputs]:
            for (var, lbl) in category.values():
                var.set(0)

        # Clear output
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, " Form cleared. Ready for new customer.")

        # Refresh stock displays
        self.refresh_stock_displays()

    def refresh_stock_displays(self):
        """Refresh all stock displays with current stock levels"""
        # Update product data from database
        self.cursor.execute("SELECT name, stock FROM products")
        self.products = {row[0]: {'stock': row[1]} for row in self.cursor.fetchall()}

        for category in [self.tools_inputs, self.plumbing_inputs,
                         self.paint_inputs, self.electrical_inputs]:
            for product, (var, lbl) in category.items():
                stock = self.products.get(product, {}).get('stock', 0)
                stock_color = "black" if stock > self.low_stock_threshold else self.stock_warning_color
                display_name = product.replace('_', ' ').title()
                if "Pvc" in display_name:
                    display_name = display_name.replace("Pvc", "PVC")
                if display_name == "Tapes":
                    display_name = "Painter's Tape"
                lbl.config(text=f"{display_name}: (Stock: {stock})", fg=stock_color)

                # Update spinbox max value
                spinbox = lbl.master.grid_slaves(row=lbl.grid_info()["row"], column=1)[0]
                spinbox.config(to=stock if stock > 0 else 0)

    def show_stock_summary(self):
        """Show a window with current stock summary"""
        stock_window = tk.Toplevel(self.root)
        stock_window.title("Current Stock Levels")
        stock_window.geometry("600x500")
        stock_window.transient(self.root)
        stock_window.grab_set()

        # Create a frame for the treeview and scrollbar
        tree_frame = tk.Frame(stock_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a treeview with columns
        columns = ("Product", "Current Stock", "Status")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        # Define headings
        tree.heading("Product", text="Product")
        tree.heading("Current Stock", text="Current Stock")
        tree.heading("Status", text="Status")

        # Define column widths
        tree.column("Product", width=300, anchor="w")
        tree.column("Current Stock", width=100, anchor="center")
        tree.column("Status", width=100, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)

        # Pack the tree and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Add stock data to the treeview
        self.cursor.execute("SELECT name, stock FROM products")
        for row in self.cursor.fetchall():
            status = "Low" if row[1] <= self.low_stock_threshold else "OK"
            display_name = row[0].replace('_', ' ').title()
            if "Pvc" in display_name:
                display_name = display_name.replace("Pvc", "PVC")
            if display_name == "Tapes":
                display_name = "Painter's Tape"
            tree.insert("", tk.END, values=(display_name, row[1], status),
                        tags=("low" if status == "Low" else "ok"))

        # Configure tag colors
        tree.tag_configure("low", background="#FFF2CC")
        tree.tag_configure("ok", background="white")

        # Add summary
        self.cursor.execute("SELECT COUNT(*), SUM(CASE WHEN stock <= ? THEN 1 ELSE 0 END) FROM products",
                            (self.low_stock_threshold,))
        total_items, low_stock_count = self.cursor.fetchone()

        summary_frame = tk.Frame(stock_window)
        summary_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(summary_frame, text=f"Total Items: {total_items}",
                 font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        tk.Label(summary_frame, text=f"Low Stock Items: {low_stock_count}",
                 font=("Arial", 10), fg=self.stock_warning_color).pack(side=tk.LEFT, padx=10)

        # Add button to close
        button_frame = tk.Frame(stock_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(button_frame, text="Close", command=stock_window.destroy,
                  font=("Arial", 11), bg=self.button_color, fg=self.fg_color,
                  width=15).pack(pady=5)

    def show_restock_dialog(self):
        """Show dialog to restock items"""
        restock_window = tk.Toplevel(self.root)
        restock_window.title("Restock Items")
        restock_window.geometry("500x500")
        restock_window.transient(self.root)
        restock_window.grab_set()

        # Create a frame for the search and list
        search_frame = tk.Frame(restock_window)
        search_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        tk.Label(search_frame, text="Search Product:",
                 font=("Arial", 11)).pack(side=tk.LEFT, padx=(0, 5))

        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var,
                                font=("Arial", 11), width=25)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.focus()

        # Create a frame for the listbox and scrollbar
        list_frame = tk.Frame(restock_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create a listbox to select products
        products_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE, height=15,
                                      font=("Arial", 11))
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=products_listbox.yview)
        products_listbox.config(yscrollcommand=scrollbar.set)

        # Add products to listbox
        self.cursor.execute("SELECT name FROM products ORDER BY name")
        self.all_products = [row[0] for row in self.cursor.fetchall()]
        self.filtered_products = self.all_products.copy()

        for product in self.filtered_products:
            display_name = product.replace('_', ' ').title()
            if "Pvc" in display_name:
                display_name = display_name.replace("Pvc", "PVC")
            if display_name == "Tapes":
                display_name = "Painter's Tape"
            products_listbox.insert(tk.END, display_name)

        products_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Default to first item
        products_listbox.selection_set(0)
        products_listbox.activate(0)

        # Search functionality
        def update_list(event=None):
            search_term = search_var.get().lower()
            self.filtered_products = [p for p in self.all_products if search_term in p.lower()]

            products_listbox.delete(0, tk.END)
            for product in self.filtered_products:
                display_name = product.replace('_', ' ').title()
                if "Pvc" in display_name:
                    display_name = display_name.replace("Pvc", "PVC")
                if display_name == "Tapes":
                    display_name = "Painter's Tape"
                products_listbox.insert(tk.END, display_name)

            if self.filtered_products:
                products_listbox.selection_set(0)
                products_listbox.activate(0)

        search_var.trace("w", lambda *args: update_list())

        # Quantity entry
        quantity_frame = tk.Frame(restock_window)
        quantity_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(quantity_frame, text="Restock Quantity:",
                 font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        quantity_var = tk.IntVar(value=10)
        quantity_entry = tk.Spinbox(quantity_frame, textvariable=quantity_var, from_=1, to=1000,
                                    font=("Arial", 11), width=10)
        quantity_entry.grid(row=0, column=1, padx=5, pady=5)

        # Button frame
        button_frame = tk.Frame(restock_window)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        def apply_restock():
            # Get selected product
            selected_idx = products_listbox.curselection()
            if not selected_idx:
                messagebox.showwarning("Selection Error", "Please select a product!")
                return

            # Get product key from display name
            display_name = products_listbox.get(selected_idx[0])
            product_key = display_name.lower().replace(' ', '_').replace("painter's_tape", "tapes")
            product_key = product_key.replace('pvc', 'pvc').replace('joints', 'joints')

            # Restock
            quantity = quantity_var.get()
            try:
                # Update stock in database
                self.cursor.execute("UPDATE products SET stock = stock + ? WHERE name = ?", (quantity, product_key))
                self.cursor.execute('''INSERT INTO stock_history
                                           (product_id, change, new_stock, note, user_id)
                                       VALUES ((SELECT id FROM products WHERE name = ?), ?,
                                               (SELECT stock FROM products WHERE name = ?), ?, ?)''',
                                    (product_key, quantity, product_key,
                                     f"Restocked {quantity} units", self.user_id))
                self.conn.commit()

                # Update local data
                if product_key in self.products:
                    self.products[product_key]['stock'] += quantity

                # Refresh displays
                self.refresh_stock_displays()
                messagebox.showinfo("Success", f"Restocked {display_name} with {quantity} units")
                restock_window.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error restocking: {str(e)}")

        tk.Button(button_frame, text="Restock", command=apply_restock,
                  font=("Arial", 11), bg=self.button_color, fg=self.fg_color,
                  width=10).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Cancel", command=restock_window.destroy,
                  font=("Arial", 11), bg=self.highlight_color, fg=self.fg_color,
                  width=10).pack(side=tk.RIGHT, padx=5)

    def show_reports(self):
        """Show reports window"""
        reports_window = tk.Toplevel(self.root)
        reports_window.title("Reports")
        reports_window.geometry("800x600")
        reports_window.transient(self.root)
        reports_window.grab_set()

        # Create notebook for different reports
        notebook = ttk.Notebook(reports_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Daily Sales Report
        daily_frame = tk.Frame(notebook)
        notebook.add(daily_frame, text="Daily Sales")

        # Date selection
        date_frame = tk.Frame(daily_frame)
        date_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(date_frame, text="Date:", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        self.report_date = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        date_entry = tk.Entry(date_frame, textvariable=self.report_date, font=("Arial", 11), width=15)
        date_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(date_frame, text="Generate Report", command=lambda: self.generate_daily_sales(daily_frame),
                  font=("Arial", 11), bg=self.button_color, fg=self.fg_color).pack(side=tk.LEFT, padx=10)

        # Stock Alerts Report
        stock_frame = tk.Frame(notebook)
        notebook.add(stock_frame, text="Stock Alerts")

        tk.Label(stock_frame, text="Low Stock Items", font=("Arial", 12, "bold")).pack(pady=10)

        # Generate stock alerts by default
        self.generate_stock_alerts(stock_frame)

    def generate_daily_sales(self, parent_frame):
        """Generate daily sales report"""
        # Clear previous results
        for widget in parent_frame.winfo_children():
            if widget.winfo_class() != 'Frame':  # Keep the date frame
                widget.destroy()

        try:
            # Get sales data
            self.cursor.execute('''SELECT strftime('%Y-%m-%d', datetime) AS sale_date,
                                          COUNT(*)                       AS transactions,
                                          SUM(total)                     AS total_sales
                                   FROM transactions
                                   WHERE sale_date = ?
                                   GROUP BY sale_date''', (self.report_date.get(),))
            summary = self.cursor.fetchone()

            if not summary:
                tk.Label(parent_frame, text=f"No sales data for {self.report_date.get()}",
                         font=("Arial", 12)).pack(pady=20)
                return

            # Create summary frame
            summary_frame = tk.LabelFrame(parent_frame, text="Daily Summary", font=("Arial", 11))
            summary_frame.pack(fill=tk.X, padx=10, pady=10)

            tk.Label(summary_frame, text=f"Date: {summary[0]}", font=("Arial", 11)).grid(row=0, column=0, sticky="w",
                                                                                         padx=10, pady=5)
            tk.Label(summary_frame, text=f"Transactions: {summary[1]}", font=("Arial", 11)).grid(row=1, column=0,
                                                                                                 sticky="w", padx=10,
                                                                                                 pady=5)
            tk.Label(summary_frame, text=f"Total Sales: Ksh.{summary[2]:,.2f}", font=("Arial", 11)).grid(row=2,
                                                                                                         column=0,
                                                                                                         sticky="w",
                                                                                                         padx=10,
                                                                                                         pady=5)

            # Create details frame
            details_frame = tk.LabelFrame(parent_frame, text="Transaction Details", font=("Arial", 11))
            details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Create treeview
            columns = ("ID", "Bill No", "Customer", "Total", "Time")
            tree = ttk.Treeview(details_frame, columns=columns, show="headings")

            # Define headings
            tree.heading("ID", text="ID")
            tree.heading("Bill No", text="Bill No")
            tree.heading("Customer", text="Customer")
            tree.heading("Total", text="Total")
            tree.heading("Time", text="Time")

            # Define column widths
            tree.column("ID", width=50, anchor="center")
            tree.column("Bill No", width=80, anchor="center")
            tree.column("Customer", width=150, anchor="w")
            tree.column("Total", width=100, anchor="e")
            tree.column("Time", width=100, anchor="center")

            # Add scrollbar
            scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)

            # Pack the tree and scrollbar
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Get transaction details
            self.cursor.execute('''SELECT id, bill_no, customer_name, total, strftime('%H:%M:%S', datetime)
                                   FROM transactions
                                   WHERE date(datetime) = ?''', (self.report_date.get(),))

            for row in self.cursor.fetchall():
                tree.insert("", tk.END, values=row)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error generating report: {str(e)}")

    def generate_stock_alerts(self, parent_frame):
        """Generate stock alerts report"""
        try:
            # Get low stock items
            self.cursor.execute('''SELECT name, stock
                                   FROM products
                                   WHERE stock <= ?
                                   ORDER BY stock ASC''', (self.low_stock_threshold,))
            low_stock_items = self.cursor.fetchall()

            if not low_stock_items:
                tk.Label(parent_frame, text="No low stock items",
                         font=("Arial", 12)).pack(pady=20)
                return

            # Create treeview
            tree_frame = tk.Frame(parent_frame)
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            columns = ("Product", "Current Stock")
            tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

            # Define headings
            tree.heading("Product", text="Product")
            tree.heading("Current Stock", text="Current Stock")

            # Define column widths
            tree.column("Product", width=400, anchor="w")
            tree.column("Current Stock", width=150, anchor="center")

            # Add scrollbar
            scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)

            # Pack the tree and scrollbar
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Add data
            for row in low_stock_items:
                display_name = row[0].replace('_', ' ').title()
                if "Pvc" in display_name:
                    display_name = display_name.replace("Pvc", "PVC")
                if display_name == "Tapes":
                    display_name = "Painter's Tape"
                tree.insert("", tk.END, values=(display_name, row[1]),
                            tags=("low",))

            tree.tag_configure("low", background="#FFF2CC")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error generating report: {str(e)}")

    def exit_app(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit the application?"):
            self.conn.close()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    login = LoginWindow(root)
    root.mainloop()