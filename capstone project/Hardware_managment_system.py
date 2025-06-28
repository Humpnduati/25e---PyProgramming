# Hardware Store Billing System with Receipt Saving and Stock Management
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
from datetime import datetime
import os
import json

class HardwareStoreManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hardware Store Billing System")
        self.root.geometry("1200x900+0+0")
        self.root.configure(bg="#f5f5f5")
        
                                     # Define hardware-themed colors
        self.bg_color = "#2C3E50"  # Dark blue
        self.fg_color = "#ECF0F1"  # Light gray
        self.lbl_color = '#3498DB'  # Blue
        self.highlight_color = "#E74C3C"  # Red for important elements
        self.button_color = "#16A085"  # Green
        self.stock_warning_color = "#F39C12"  # Orange for low stock
        
                                    # Prices dictionary
        self.prices = {
            "nails": 10, "screws": 15, "hammers": 250, "screwdrivers": 150, "pliers": 200,
            "pipes": 180, "valves": 350, "faucets": 1200, "pvc_joints": 45, "taps": 800,
            "paint_buckets": 1800, "brushes": 120, "thinners": 250, "rollers": 300, "tapes": 80,
            "wires": 25, "switches": 120, "bulbs": 100, "sockets": 85, "circuit_breakers": 450
        }
        
                                     # Stock management
        self.stock_file = "stock.json"
        self.stock = self.load_stock()
        self.low_stock_threshold = 10  # Threshold for low stock warning
        
                                    # Initialize variables
        self.bill_no = random.randint(10, 999999)
        self.customer_name = tk.StringVar()
        self.customer_phone = tk.StringVar()
        self.customer_address = tk.StringVar()
        
                                     # Create widgets
        self.create_widgets()
        
                                     # Create receipts directory
        if not os.path.exists('receipts'):
            os.makedirs('receipts')
            
                                    # Create stock directory if it doesn't exist
        if not os.path.exists('stock_history'):
            os.makedirs('stock_history')
    
    def load_stock(self):
        """Load stock from file or initialize with default values"""
        try:
            if os.path.exists(self.stock_file):
                with open(self.stock_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            messagebox.showwarning("Stock Error", f"Could not load stock data: {str(e)}")
        
                                    # Initialize stock if file doesn't exist
        stock = {product: 100 for product in self.prices}
        self.save_stock(stock)
        return stock
    
    def save_stock(self, stock=None):
        """Save current stock to file"""
        if stock is None:
            stock = self.stock
            
        try:
            with open(self.stock_file, 'w') as f:
                json.dump(stock, f, indent=4)
                
            # Save stock history
            history_file = f"stock_history/stock_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(history_file, 'w') as f:
                json.dump(stock, f, indent=4)
                
        except Exception as e:
            messagebox.showerror("Stock Error", f"Could not save stock data: {str(e)}")
    
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
        
                                        # Stock summary button
        stock_button = tk.Button(header_frame, text="Stock Summary", command=self.show_stock_summary,
                                font=("Arial", 11), bg=self.stock_warning_color, fg=self.fg_color)
        stock_button.pack(side=tk.RIGHT, padx=10)
        
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
            stock = self.stock.get(product, 0)
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
            stock = self.stock.get(product, 0)
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
            stock = self.stock.get(product, 0)
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
            stock = self.stock.get(product, 0)
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
        
        tk.Button(button_frame, text="Save Receipt", command=self.save_bill,
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
            "5. Click 'Save Receipt' to save as a printable text file and update stock",
            "6. Use 'Clear All' to start a new transaction",
            "7. Use 'Restock Items' to add inventory",
            "8. Use 'Stock Summary' to view current inventory levels"
        ]
        
        for instruction in instructions:
            tk.Label(instructions_frame, text=instruction, font=("Arial", 10), 
                    bg="#f0f8ff", fg="#2C3E50", justify="left").pack(anchor="w", padx=20)
        
        tk.Label(instructions_frame, text="Note: Receipts are saved in the 'receipts' folder, stock history in 'stock_history'", 
                font=("Arial", 10), bg="#f0f8ff", fg=self.highlight_color).pack(anchor="w", padx=20, pady=(0, 5))
    
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
            current_stock = self.stock.get(product, 0)
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
        customer_name = self.customer_name.get()
        if not customer_name:
            messagebox.showwarning("Input Error", "Please enter customer name!")
            return
            
                                        # Calculate totals
        tools_total = sum(self.tools_inputs[item][0].get() * self.prices[item] for item in self.tools_inputs)
        plumbing_total = sum(self.plumbing_inputs[item][0].get() * self.prices[item] for item in self.plumbing_inputs)
        paint_total = sum(self.paint_inputs[item][0].get() * self.prices[item] for item in self.paint_inputs)
        electrical_total = sum(self.electrical_inputs[item][0].get() * self.prices[item] for item in self.electrical_inputs)
        
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
        self.output_text.insert(tk.END, "="*80 + "\n")
        self.output_text.insert(tk.END, f"{'HARDWARE STORE MANAGEMENT SYSTEM':^80}\n")
        self.output_text.insert(tk.END, "="*80 + "\n")
        self.output_text.insert(tk.END, f"Bill No: {self.bill_no} {'Date:':>50} {datetime.now().strftime('%d-%m-%Y')}\n")
        self.output_text.insert(tk.END, f"Customer: {customer_name}\n")
        self.output_text.insert(tk.END, f"Phone: {self.customer_phone.get()}\n")
        self.output_text.insert(tk.END, f"Address: {self.customer_address.get()}\n")
        self.output_text.insert(tk.END, "-"*80 + "\n")
        
                                        # Create a table for totals
        self.output_text.insert(tk.END, f"{'Category':<20}{'Subtotal':>20}{'Tax':>20}\n")
        self.output_text.insert(tk.END, "-"*80 + "\n")
        self.output_text.insert(tk.END, f"{'Tools':<20}{'Ksh.' + str(tools_total):>20}{'Ksh.' + str(tools_tax):>20}\n")
        self.output_text.insert(tk.END, f"{'Plumbing':<20}{'Ksh.' + str(plumbing_total):>20}{'Ksh.' + str(plumbing_tax):>20}\n")
        self.output_text.insert(tk.END, f"{'Paint':<20}{'Ksh.' + str(paint_total):>20}{'Ksh.' + str(paint_tax):>20}\n")
        self.output_text.insert(tk.END, f"{'Electrical':<20}{'Ksh.' + str(electrical_total):>20}{'Ksh.' + str(electrical_tax):>20}\n")
        self.output_text.insert(tk.END, "-"*80 + "\n")
        self.output_text.insert(tk.END, f"{'GRAND TOTAL:':<40}Ksh.{grand_total}\n")
        self.output_text.insert(tk.END, "="*80 + "\n")
    
    def generate_bill_text(self):
        customer_name = self.customer_name.get()
        if not customer_name:
            return " Please enter customer name!", None
        
                                        # Calculate totals
        tools_total = sum(self.tools_inputs[item][0].get() * self.prices[item] for item in self.tools_inputs)
        plumbing_total = sum(self.plumbing_inputs[item][0].get() * self.prices[item] for item in self.plumbing_inputs)
        paint_total = sum(self.paint_inputs[item][0].get() * self.prices[item] for item in self.paint_inputs)
        electrical_total = sum(self.electrical_inputs[item][0].get() * self.prices[item] for item in self.electrical_inputs)
        
                                        # Calculate ETR
        tools_tax = round(tools_total * 0.05)
        plumbing_tax = round(plumbing_total * 0.05)
        paint_tax = round(paint_total * 0.05)
        electrical_tax = round(electrical_total * 0.05)
        
                                        # Grand total
        grand_total = tools_total + plumbing_total + paint_total + electrical_total + \
                     tools_tax + plumbing_tax + paint_tax + electrical_tax
        
                                        # Generate bill header
        bill_text = "\n" + "="*80 + "\n"
        bill_text += f"{'HARDWARE EMPORIUM':^80}\n"
        bill_text += f"{'='*80}\n"
        bill_text += f"Bill No: {self.bill_no} {'Date:':>50} {datetime.now().strftime('%d-%m-%Y')}\n"
        bill_text += f"Customer: {customer_name}\n"
        bill_text += f"Phone: {self.customer_phone.get()}\n"
        bill_text += f"Address: {self.customer_address.get()}\n"
        bill_text += "-"*80 + "\n"
        bill_text += f"{'Product':<30}{'Qty':>10}{'Price':>15}{'Amount':>15}\n"
        bill_text += "-"*80 + "\n"
        
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
        
        bill_text += "-"*80 + "\n"
        bill_text += f"{'SUBTOTAL:':<50}Ksh.{grand_total - (tools_tax + plumbing_tax + paint_tax + electrical_tax)}\n"
        bill_text += f"{'TAX (5%):':<50}Ksh.{tools_tax + plumbing_tax + paint_tax + electrical_tax}\n"
        bill_text += f"{'GRAND TOTAL:':<50}Ksh.{grand_total}\n"
        bill_text += "="*80 + "\n"
        bill_text += f"{'THANK YOU FOR YOUR BUSINESS!':^80}\n"
        bill_text += f"{'Quality Hardware for All Your Project Needs':^80}\n"
        bill_text += "="*80
        
        return bill_text, customer_name
    
    def generate_bill(self):
        bill_text, customer_name = self.generate_bill_text()
        if customer_name is None:
            messagebox.showwarning("Input Error", bill_text)
            return
            
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, bill_text)
    
    def save_bill(self):
        bill_text, customer_name = self.generate_bill_text()
        
        if customer_name is None:
            messagebox.showwarning("Input Error", bill_text)
            return
            
                                                # Create filename
        filename = f"receipts/{customer_name.replace(' ', '_')}_{self.bill_no}_{datetime.now().strftime('%Y%m%d')}.txt"
        
                                                # Save to file
        try:
            with open(filename, 'w') as file:
                file.write(bill_text)
            
                                                # Update stock levels
            for category in [self.tools_inputs, self.plumbing_inputs, self.paint_inputs, self.electrical_inputs]:
                for product, (var, lbl) in category.items():
                    qty = var.get()
                    if qty > 0:
                        self.stock[product] -= qty
            
                                                # Save updated stock
            self.save_stock()
            
            messagebox.showinfo("Success", f" Receipt saved successfully as:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f" Error saving receipt: {str(e)}")
    
    def clear_all(self):
                                                # Clear inputs
        self.customer_name.set("")
        self.customer_phone.set("")
        self.customer_address.set("")
        
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
        for category in [self.tools_inputs, self.plumbing_inputs, 
                         self.paint_inputs, self.electrical_inputs]:
            for product, (var, lbl) in category.items():
                stock = self.stock.get(product, 0)
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
        for product, stock in self.stock.items():
            status = "Low" if stock <= self.low_stock_threshold else "OK"
            display_name = product.replace('_', ' ').title()
            if "Pvc" in display_name:
                display_name = display_name.replace("Pvc", "PVC")
            if display_name == "Tapes":
                display_name = "Painter's Tape"
            tree.insert("", tk.END, values=(display_name, stock, status), 
                        tags=("low" if status == "Low" else "ok"))
        
                                            # Configure tag colors
        tree.tag_configure("low", background="#FFF2CC")
        tree.tag_configure("ok", background="white")
        
                                            # Add summary
        low_stock_count = sum(1 for stock in self.stock.values() if stock <= self.low_stock_threshold)
        summary_frame = tk.Frame(stock_window)
        summary_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(summary_frame, text=f"Total Items: {len(self.stock)}", 
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
        restock_window.geometry("400x500")
        restock_window.transient(self.root)
        restock_window.grab_set()
        
                                            # Create a frame for the listbox and scrollbar
        list_frame = tk.Frame(restock_window)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
                                            # Create a listbox to select products
        tk.Label(list_frame, text="Select Product:", 
                font=("Arial", 11)).pack(anchor="w", pady=5)
        
        products_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE, height=10,
                                    font=("Arial", 11))
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=products_listbox.yview)
        products_listbox.config(yscrollcommand=scrollbar.set)
        
                                            # Add products to listbox
        sorted_products = sorted(self.stock.keys())
        for product in sorted_products:
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
            self.stock[product_key] += quantity
            self.save_stock()
            
                                            # Refresh displays
            self.refresh_stock_displays()
            messagebox.showinfo("Success", f"Restocked {display_name} with {quantity} units")
            restock_window.destroy()
        
        tk.Button(button_frame, text="Restock", command=apply_restock,
                 font=("Arial", 11), bg=self.button_color, fg=self.fg_color,
                 width=10).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Cancel", command=restock_window.destroy,
                 font=("Arial", 11), bg=self.highlight_color, fg=self.fg_color,
                 width=10).pack(side=tk.RIGHT, padx=5)
    
    def exit_app(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit the application?"):
            # Save stock before exiting
            self.save_stock()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HardwareStoreManagementSystem(root)
    root.mainloop()