# Advanced BMI Calculator - Professional Version
# Oasis Infobyte Internship Project
# Author: Sanika Mahale


import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
from datetime import datetime

# File to store BMI history
HISTORY_FILE = "bmi_history.csv"

def calculate_bmi():
    """Calculate BMI and display results"""
    try:
        # Get input values
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        
        # Validate inputs
        if weight <= 0 or height <= 0:
            messagebox.showerror("Invalid Input", "Values must be greater than 0")
            return
        
        # Calculate BMI
        bmi = weight / (height ** 2)
        
        # Determine category and health tips
        if bmi < 18.5:
            category = "Underweight"
            tip = "Eat nutritious food, increase calorie intake"
            color = "#FFA500"  # Orange
        elif 18.5 <= bmi < 24.9:
            category = "Normal Weight"
            tip = "Maintain balanced diet and regular exercise"
            color = "#00C853"  # Green
        elif 25 <= bmi < 29.9:
            category = "Overweight"
            tip = "Reduce calorie intake, exercise more"
            color = "#FF6D00"  # Dark Orange
        else:
            category = "Obese"
            tip = "Consult healthcare provider, diet plan needed"
            color = "#D50000"  # Red
        
        # Display result
        result_label.config(
            text=f"Your BMI: {bmi:.2f}\nCategory: {category}",
            fg=color
        )
        tip_label.config(text=f"💡 Health Tip: {tip}")
        
        # Save to history
        save_to_history(weight, height, bmi, category)
        
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers")

def save_to_history(weight, height, bmi, category):
    """Save BMI calculation to CSV file"""
    file_exists = os.path.exists(HISTORY_FILE)
    
    with open(HISTORY_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Weight (kg)", "Height (m)", "BMI", "Category"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), 
                         weight, height, f"{bmi:.2f}", category])

def view_history():
    """Show BMI history in a new window"""
    if not os.path.exists(HISTORY_FILE):
        messagebox.showinfo("History", "No BMI records found yet!")
        return
    
    history_window = tk.Toplevel(root)
    history_window.title("BMI History")
    history_window.geometry("500x400")
    
    # Create treeview
    tree = ttk.Treeview(history_window, columns=("Date", "Weight", "Height", "BMI", "Category"), show='headings')
    tree.heading("Date", text="Date")
    tree.heading("Weight", text="Weight (kg)")
    tree.heading("Height", text="Height (m)")
    tree.heading("BMI", text="BMI")
    tree.heading("Category", text="Category")
    
    # Read and display data
    with open(HISTORY_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            tree.insert("", "end", values=row)
    
    tree.pack(fill="both", expand=True, padx=10, pady=10)

def clear_fields():
    """Clear all input fields"""
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)
    result_label.config(text="", fg="black")
    tip_label.config(text="")

# ============================================
# GUI Setup
# ============================================

root = tk.Tk()
root.title("Advanced BMI Calculator")
root.geometry("400x450")
root.resizable(False, False)

# Style configuration
style = ttk.Style()
style.configure("TButton", font=("Arial", 10, "bold"))
style.configure("TLabel", font=("Arial", 10))

# Title
title_label = tk.Label(root, text="🏥 Advanced BMI Calculator", 
                       font=("Arial", 18, "bold"), fg="#1976D2")
title_label.pack(pady=15)

# Weight Input
weight_frame = tk.Frame(root)
weight_frame.pack(pady=5)

weight_label = tk.Label(weight_frame, text="Weight (kg):", font=("Arial", 11))
weight_label.pack(side=tk.LEFT, padx=5)

weight_entry = tk.Entry(weight_frame, font=("Arial", 11), width=15)
weight_entry.pack(side=tk.LEFT, padx=5)

# Height Input
height_frame = tk.Frame(root)
height_frame.pack(pady=5)

height_label = tk.Label(height_frame, text="Height (m):", font=("Arial", 11))
height_label.pack(side=tk.LEFT, padx=5)

height_entry = tk.Entry(height_frame, font=("Arial", 11), width=15)
height_entry.pack(side=tk.LEFT, padx=5)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=15)

calc_button = ttk.Button(button_frame, text="Calculate BMI", command=calculate_bmi)
calc_button.pack(side=tk.LEFT, padx=5)

clear_button = ttk.Button(button_frame, text="Clear", command=clear_fields)
clear_button.pack(side=tk.LEFT, padx=5)

history_button = ttk.Button(button_frame, text="View History", command=view_history)
history_button.pack(side=tk.LEFT, padx=5)

# Result Display
result_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
result_label.pack(pady=10)

# Health Tip
tip_label = tk.Label(root, text="", font=("Arial", 10), fg="#666", wraplength=350)
tip_label.pack(pady=5)

# BMI Scale Visual
scale_label = tk.Label(root, text="BMI Scale:", font=("Arial", 10, "bold"))
scale_label.pack(pady=5)

scale_frame = tk.Frame(root)
scale_frame.pack(pady=5)

# BMI Scale colors
scales = [("Underweight\n<18.5", "#FFA500"), 
          ("Normal\n18.5-24.9", "#00C853"), 
          ("Overweight\n25-29.9", "#FF6D00"), 
          ("Obese\n≥30", "#D50000")]

for text, color in scales:
    lbl = tk.Label(scale_frame, text=text, bg=color, fg="white", 
                   font=("Arial", 8), width=12, height=3, relief="raised")
    lbl.pack(side=tk.LEFT, padx=2)

# Footer
footer_label = tk.Label(root, text="Oasis Infobyte - Python Internship", 
                        font=("Arial", 8), fg="#999")
footer_label.pack(side=tk.BOTTOM, pady=10)

# Run application
root.mainloop()