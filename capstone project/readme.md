# Hardware Store Billing System with Stock Management

![System Screenshot](screenshot.png)

## Overview
This Python application is a comprehensive hardware store management system that combines billing, receipt generation, and inventory management. Built with Tkinter for the GUI interface, it allows store owners to process customer orders, generate printable receipts, and maintain real-time inventory tracking.

## Key Features

### 1. Billing System
- Customer information management (name, phone, address)
- Product categorization (Tools, Plumbing, Paint, Electrical)
- Tax calculation (5% on all items)
- Receipt generation with itemized billing
- Printable receipt saving in TXT format

### 2. Stock Management
- Real-time inventory tracking
- Low stock warnings (orange highlight)
- Stock history with timestamped snapshots
- Restocking functionality
- Stock summary reports
- Inventory-aware ordering (prevents overselling)

### 3. User Interface
- Hardware-themed color scheme
- Responsive layout with clear sections
- Interactive spinboxes for quantity selection
- Scrolled text area for bill previews
- Comprehensive instructions panel
- Visual indicators for low stock items

## System Components

### 1. Data Management
- **stock.json**: Current inventory levels (persistent storage)
- **receipts/**: Folder for saved customer receipts
- **stock_history/**: Historical inventory snapshots

### 2. Core Classes
- `HardwareStoreBillingSystem`: Main application class
- `load_stock()`: Loads inventory from JSON file
- `save_stock()`: Saves current inventory with timestamped history
- `refresh_stock_displays()`: Updates UI with current stock levels

### 3. UI Components
- **Customer Details Section**: Collects customer information
- **Product Categories**: Organized in labeled frames
- **Action Buttons**:
  - Calculate Total
  - Generate Bill
  - Save Receipt
  - Clear All
  - Restock Items
  - Stock Summary
  - Exit
- **Bill Summary**: Preview area for generated receipts
- **Instructions Panel**: Step-by-step usage guide

## How It Works

### Order Processing Workflow
1. Enter customer details (name required)
2. Select products using spinboxes (quantity limited by current stock)
3. Click "Calculate Total" to see category totals with taxes
4. Click "Generate Bill" to preview the itemized receipt
5. Click "Save Receipt" to:
   - Save printable TXT receipt
   - Deduct sold items from inventory
   - Create stock history snapshot

### Stock Management
- **Real-time Updates**: Stock levels decrease as items are sold
- **Low Stock Warnings**: Items with ≤10 units highlighted in orange
- **Restocking**:
  1. Click "Restock Items"
  2. Select product from list
  3. Enter quantity to add
  4. Inventory updates immediately
- **Stock Summary**:
  - Table view of all products
  - Current stock levels
  - Low stock indicators
  - Summary statistics

## Code Structure

```python
# Hardware Store Billing System with Stock Management
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
from datetime import datetime
import os
import json

class HardwareStoreBillingSystem:
    def __init__(self, root):
        # Initialization code (UI setup, variables, stock loading)
    
    # Stock management methods
    def load_stock(self):
    def save_stock(self, stock=None):
    
    # UI creation
    def create_widgets(self):
    
    # Stock display updates
    def update_stock_display(self, product):
    def refresh_stock_displays(self):
    
    # Billing functions
    def calculate_total(self):
    def generate_bill_text(self):
    def generate_bill(self):
    def save_bill(self):
    
    # Stock management UI
    def show_stock_summary(self):
    def show_restock_dialog(self):
    
    # Utility functions
    def clear_all(self):
    def exit_app(self):

if __name__ == "__main__":
    root = tk.Tk()
    app = HardwareStoreBillingSystem(root)
    root.mainloop()
	
	
	
	
Installation and Usage
Requirements
Python 3.x

Tkinter (usually included with Python)

Running the Application
Save the code as hardware_store.py

Run from command line:

bash
python hardware_store.py
First Run Setup
The system will automatically:

Create receipts/ directory for saving bills

Create stock_history/ directory for inventory snapshots

Generate stock.json with initial inventory (100 units per product)

File Structure
text
project-root/
├── hardware_store.py        # Main application
├── stock.json               # Current inventory data
├── receipts/                # Customer receipts
│   └── customer_1001_20240520.txt
├── stock_history/           # Inventory history
│   └── stock_20240520_143022.json
Key Algorithms
Stock Deduction Logic
python
def save_bill(self):
    # After saving receipt:
    for category in [self.tools_inputs, self.plumbing_inputs, ...]:
        for product, (var, lbl) in category.items():
            qty = var.get()
            if qty > 0:
                self.stock[product] -= qty  # Deduct from inventory
    self.save_stock()  # Persist changes
Real-time Stock Display Update
python
def update_stock_display(self, product):
    # Get current stock minus ordered quantity
    current_stock = self.stock.get(product, 0)
    ordered = var.get()
    available = max(0, current_stock - ordered)
    
    # Update label color based on availability
    stock_color = "black" if available > self.low_stock_threshold else "orange"
    lbl.config(text=f"{display_name}: (Stock: {available})", fg=stock_color)
    
    # Update spinbox maximum value
    spinbox.config(to=available if available > 0 else 0)
Benefits
Integrated Solution: Combines billing and inventory management

Error Prevention: Prevents overselling with stock-aware ordering

Business Insights: Identifies low-stock items needing reorder

Audit Trail: Maintains historical inventory records

Professional Receipts: Generates printable customer receipts

User-Friendly: Intuitive interface with visual cues

Sample Receipt
text
===============================================================
                            HARDWARE EMPORIUM                           
================================================================
Bill No: 4827                                     Date: 20-05-2025
Customer: John Smith
Phone: 555-1234
Address: 123 Main Street, Anytown
----------------------------------------------------------------
Product                          Qty         Price         Amount
----------------------------------------------------------------
Nails                              5           ₹10           ₹50
Hammers                            2          ₹250          ₹500
Paint Buckets                      1         ₹1800         ₹1800
Brushes                            3          ₹120          ₹360
Wires                             10           ₹25          ₹250
----------------------------------------------------------------
SUBTOTAL:                                              ₹2960
TAX (5%):                                              ₹148
GRAND TOTAL:                                          ₹3108
================================================================
               THANK YOU FOR YOUR BUSINESS!               
      Quality Hardware for All Your Project Needs      
================================================================
License
This project is open-source and available for modification and distribution under the MIT License.

text

To use this README:
1. Copy the entire content above
2. Create a new file named `README.md` in your project directory
3. Paste the content into the file
4. Save the file
