# ============================================
# Advanced Password Generator GUI - FIXED VERSION
# Oasis Infobyte Internship - Project 2
# Author: Sanika Mahale
# ============================================

import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import pyperclip
import json
import os
from datetime import datetime

class AdvancedPasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Advanced Password Generator Pro")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")
        
        self.generated_count = 0
        self.history = self.load_history()
        self.current_password = ""  # Store current password
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#2196F3", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title = tk.Label(header_frame, text="🔐 ADVANCED PASSWORD GENERATOR", 
                        font=("Arial", 18, "bold"), fg="white", bg="#2196F3")
        title.pack(expand=True)
        
        # Main Content Frame
        content_frame = tk.Frame(self.root, bg="#f5f5f5")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Length Control
        tk.Label(content_frame, text="Password Length:", font=("Arial", 12, "bold"), 
                bg="#f5f5f5").pack(pady=(0,5))
        
        length_frame = tk.Frame(content_frame, bg="#f5f5f5")
        length_frame.pack(pady=5)
        
        self.length_var = tk.IntVar(value=16)
        length_scale = tk.Scale(length_frame, from_=8, to=50, orient=tk.HORIZONTAL,
                               variable=self.length_var, bg="#e3f2fd", highlightthickness=0,
                               font=("Arial", 10), length=300)
        length_scale.pack()
        
        self.length_display = tk.Label(length_frame, text="16", font=("Arial", 14, "bold"),
                                      bg="#f5f5f5")
        self.length_display.pack()
        self.length_var.trace('w', self.update_length_display)
        
        # Character Options
        options_frame = tk.LabelFrame(content_frame, text="Character Types", 
                                     font=("Arial", 11, "bold"), padx=10, pady=10)
        options_frame.pack(pady=20, fill=tk.X)
        
        self.letters_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.avoid_similar_var = tk.BooleanVar(value=False)
        
        tk.Checkbutton(options_frame, text="🔤 Letters (a-z)", variable=self.letters_var,
                      bg="#f5f5f5").pack(anchor="w")
        tk.Checkbutton(options_frame, text="🔢 Numbers (0-9)", variable=self.numbers_var,
                      bg="#f5f5f5").pack(anchor="w")
        tk.Checkbutton(options_frame, text="🔣 Symbols (!@#$%)", variable=self.symbols_var,
                      bg="#f5f5f5").pack(anchor="w")
        tk.Checkbutton(options_frame, text="🔠 Uppercase (A-Z)", variable=self.uppercase_var,
                      bg="#f5f5f5").pack(anchor="w")
        tk.Checkbutton(options_frame, text="🚫 Avoid similar chars (0,O,l,1)", 
                      variable=self.avoid_similar_var, bg="#f5f5f5").pack(anchor="w")
        
        # Action Buttons
        button_frame = tk.Frame(content_frame, bg="#f5f5f5")
        button_frame.pack(pady=20)
        
        self.generate_btn = tk.Button(button_frame, text="🎲 GENERATE PASSWORD", 
                                     command=self.generate_password, bg="#4CAF50", 
                                     fg="white", font=("Arial", 12, "bold"), 
                                     width=18, height=2, relief="raised")
        self.generate_btn.pack(side=tk.LEFT, padx=10)
        
        self.copy_btn = tk.Button(button_frame, text="📋 COPY TO CLIPBOARD", 
                                 command=self.copy_password, bg="#2196F3", 
                                 fg="white", font=("Arial", 12, "bold"), 
                                 width=18, height=2, relief="raised", state="disabled")
        self.copy_btn.pack(side=tk.LEFT, padx=10)
        
        self.save_btn = tk.Button(button_frame, text="💾 SAVE TO HISTORY", 
                                 command=self.save_to_history, bg="#FF9800", 
                                 fg="white", font=("Arial", 12, "bold"), 
                                 width=18, height=2, relief="raised", state="disabled")
        self.save_btn.pack(side=tk.LEFT, padx=10)
        
        # Password Display - FIXED
        password_frame = tk.LabelFrame(content_frame, text="Generated Password", 
                                      font=("Arial", 11, "bold"), padx=15, pady=15)
        password_frame.pack(pady=20, fill=tk.X)
        
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(password_frame, textvariable=self.password_var,
                                      font=("Arial", 16, "bold"), width=35, 
                                      state="normal", justify="center",  # Changed to 'normal'
                                      relief="solid", bd=2, bg="white")
        self.password_entry.pack(pady=10)
        self.password_entry.config(state="readonly")  # Set readonly after creation
        
        # Strength Meter
        strength_frame = tk.Frame(content_frame, bg="#f5f5f5")
        strength_frame.pack(pady=15)
        
        tk.Label(strength_frame, text="Security Level:", font=("Arial", 12, "bold"),
                bg="#f5f5f5").pack()
        
        self.strength_label = tk.Label(strength_frame, text="📊 Not Generated", 
                                      font=("Arial", 14, "bold"), bg="#f5f5f5")
        self.strength_label.pack(pady=5)
        
        # Progress Bar
        self.progress_frame = tk.Frame(strength_frame, height=25, bg="#e0e0e0", relief="sunken", bd=2)
        self.progress_frame.pack(fill=tk.X, padx=20)
        self.progress_bar = tk.Frame(self.progress_frame, height=20, bg="#666", width=0)
        self.progress_bar.pack(fill=tk.X, pady=2)
        
        # Stats
        stats_frame = tk.Frame(content_frame, bg="#f5f5f5")
        stats_frame.pack(pady=10)
        
        self.stats_label = tk.Label(stats_frame, text="Generated: 0 | Saved: 0", 
                                   font=("Arial", 10), fg="#666", bg="#f5f5f5")
        self.stats_label.pack()
        
        # History Button
        history_btn = tk.Button(content_frame, text="📜 VIEW HISTORY", 
                               command=self.show_history, bg="#9C27B0", fg="white",
                               font=("Arial", 11, "bold"), width=20)
        history_btn.pack(pady=10)
        
        # Footer
        footer = tk.Label(self.root, text="Oasis Infobyte Python Internship | Project 2/4", 
                         font=("Arial", 9), fg="#999", bg="#f5f5f5")
        footer.pack(side=tk.BOTTOM, pady=10)
    
    def update_length_display(self, *args):
        self.length_display.config(text=str(self.length_var.get()))
    
    def generate_password(self):
        length = self.length_var.get()
        characters = ""
        
        if self.letters_var.get():
            characters += string.ascii_lowercase
        if self.uppercase_var.get():
            characters += string.ascii_uppercase
        if self.numbers_var.get():
            characters += string.digits
        if self.symbols_var.get():
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?/"
        
        # Avoid similar characters
        if self.avoid_similar_var.get():
            characters = ''.join(c for c in characters if c not in '0OIl1')
        
        if len(characters) < 3:
            messagebox.showerror("Error", "Select at least 3 character types!")
            return
        
        password = ''.join(random.choice(characters) for _ in range(length))
        
        # FIXED: Update both variable and current_password
        self.password_var.set(password)
        self.current_password = password
        self.password_entry.config(state="normal")  # Temporarily enable to update
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)
        self.password_entry.config(state="readonly")
        
        self.update_strength(password)
        self.generated_count += 1
        self.stats_label.config(text=f"Generated: {self.generated_count} | Saved: {len(self.history)}")
        
        self.copy_btn.config(state="normal")
        self.save_btn.config(state="normal")
    
    def update_strength(self, password):
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_numbers = any(c.isdigit() for c in password)
        has_symbols = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        score = sum([length >= 12, has_upper, has_lower, has_numbers, has_symbols, length >= 16])
        
        if score >= 5:
            strength, color, width = "🟢 ULTRA STRONG", "#4CAF50", 100
        elif score >= 4:
            strength, color, width = "🟢 STRONG", "#8BC34A", 85
        elif score >= 3:
            strength, color, width = "🟡 MODERATE", "#FF9800", 60
        else:
            strength, color, width = "🔴 WEAK", "#F44336", 30
        
        self.strength_label.config(text=f"📊 {strength}", fg=color)
        self.progress_bar.config(bg=color, width=width)
        self.progress_bar.pack_propagate(False)
    
    def copy_password(self):
        if self.current_password:
            pyperclip.copy(self.current_password)
            messagebox.showinfo("✅ Success", f"Copied:\n{self.current_password[:20]}...")
    
    def save_to_history(self):
        if self.current_password:
            entry = {
                "password": self.current_password,
                "length": self.length_var.get(),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "strength": self.strength_label.cget("text")
            }
            self.history.append(entry)
            self.save_history()
            self.stats_label.config(text=f"Generated: {self.generated_count} | Saved: {len(self.history)}")
            messagebox.showinfo("✅ Saved", "Added to history!")
    
    def load_history(self):
        if os.path.exists("password_history.json"):
            with open("password_history.json", "r") as f:
                return json.load(f)
        return []
    
    def save_history(self):
        with open("password_history.json", "w") as f:
            json.dump(self.history, f, indent=2)
    
    def show_history(self):
        if not self.history:
            messagebox.showinfo("History", "No passwords saved yet!")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("Password History")
        history_window.geometry("700x400")
        
        tree = ttk.Treeview(history_window, columns=("Date", "Password", "Length", "Strength"), show='headings')
        tree.heading("Date", text="Generated")
        tree.heading("Password", text="Password")
        tree.heading("Length", text="Length")
        tree.heading("Strength", text="Strength")
        
        tree.column("Date", width=140)
        tree.column("Password", width=300)
        tree.column("Length", width=80)
        tree.column("Strength", width=140)
        
        for entry in self.history[-20:]:
            pass_preview = entry["password"][:25] + "..." if len(entry["password"]) > 25 else entry["password"]
            tree.insert("", "end", values=(entry["timestamp"], pass_preview, 
                                         entry["length"], entry["strength"]))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedPasswordGenerator(root)
    root.mainloop()

    