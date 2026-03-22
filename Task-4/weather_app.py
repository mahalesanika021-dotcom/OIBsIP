import tkinter as tk
from tkinter import messagebox
import requests
import json
from datetime import datetime

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌦️ Weather App - WORKING!")
        self.root.geometry("700x800")
        
        self.setup_ui()
        self.load_sample_data()  # Loads Dhule data immediately!
    
    def setup_ui(self):
        # Title
        tk.Label(self.root, text="🌦️ WEATHER APP - Oasis Infobyte", 
                font=("Arial", 24, "bold"), fg="#2E86C1").pack(pady=20)
        
        # Input
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="City:", font=("Arial", 14, "bold")).pack(side=tk.LEFT)
        self.city_entry = tk.Entry(input_frame, font=("Arial", 14), width=20)
        self.city_entry.pack(side=tk.LEFT, padx=10)
        self.city_entry.insert(0, "Dhule")
        
        tk.Button(input_frame, text="🔍 GET WEATHER", command=self.get_weather,
                 bg="#27AE60", fg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=10)
        
        # Results
        self.result_frame = tk.LabelFrame(self.root, text="🌤️ Current Weather", 
                                         font=("Arial", 16, "bold"), padx=20, pady=20)
        self.result_frame.pack(pady=20, padx=50, fill=tk.BOTH, expand=True)
        
        # City & Main Temp
        self.city_label = tk.Label(self.result_frame, text="DHULE, INDIA", 
                                  font=("Arial", 28, "bold"), fg="#2C3E50")
        self.city_label.pack(pady=10)
        
        self.main_temp = tk.Label(self.result_frame, text="🌡️  28.5°C", 
                                 font=("Arial", 60, "bold"), fg="#E74C3C")
        self.main_temp.pack(pady=10)
        
        # Condition
        self.condition_label = tk.Label(self.result_frame, text="Clear Sky ☀️", 
                                       font=("Arial", 18, "bold"), fg="#F39C12")
        self.condition_label.pack(pady=5)
        
        # Details Grid
        details_frame = tk.Frame(self.result_frame)
        details_frame.pack(pady=20)
        
        # Row 1
        r1 = tk.Frame(details_frame)
        r1.pack(fill=tk.X, pady=5)
        self.feels_label = tk.Label(r1, text="Feels like: 27.2°C", font=("Arial", 14))
        self.feels_label.pack()
        
        # Row 2 - 3 columns
        r2 = tk.Frame(details_frame)
        r2.pack(fill=tk.X, pady=5)
        self.humidity_label = tk.Label(r2, text="💧 Humidity: 45%", font=("Arial", 14))
        self.humidity_label.pack(side=tk.LEFT, padx=40)
        
        self.wind_label = tk.Label(r2, text="💨 Wind: 12 km/h", font=("Arial", 14))
        self.wind_label.pack(side=tk.LEFT, padx=40)
        
        self.pressure_label = tk.Label(r2, text="📊 1013 hPa", font=("Arial", 14))
        self.pressure_label.pack(side=tk.RIGHT)
        
        # Row 3
        r3 = tk.Frame(details_frame)
        r3.pack(fill=tk.X, pady=5)
        self.clouds_label = tk.Label(r3, text="☁️  Clouds: 0%", font=("Arial", 14))
        self.clouds_label.pack(side=tk.LEFT, padx=40)
        
        self.visibility_label = tk.Label(r3, text="👁️  Visibility: 10 km", font=("Arial", 14))
        self.visibility_label.pack(side=tk.LEFT, padx=40)
        
        # Status
        self.status_label = tk.Label(self.root, text="✅ Dhule weather loaded! Try Mumbai, Delhi", 
                                    font=("Arial", 12, "bold"), fg="#27AE60")
        self.status_label.pack(pady=10)
    
    def load_sample_data(self):
        """Load Dhule sample data immediately"""
        self.city_label.config(text="DHULE, MAHARASHTRA")
        self.main_temp.config(text="🌡️  29.2°C")
        self.condition_label.config(text="Sunny ☀️")
        self.feels_label.config(text="Feels like: 28.1°C")
        self.humidity_label.config(text="💧 Humidity: 42%")
        self.wind_label.config(text="💨 Wind: 8 km/h")
        self.pressure_label.config(text="📊 1012 hPa")
        self.clouds_label.config(text="☁️  Clouds: 5%")
        self.visibility_label.config(text="👁️  Visibility: 10 km")
    
    def get_weather(self):
        """Simulate API - Returns data for Indian cities"""
        city = self.city_entry.get().strip().title()
        
        # Indian cities database (SIMPLE & WORKING!)
        weather_data = {
            "Dhule": {"temp": 29.2, "feels": 28.1, "humidity": 42, "wind": 8, "pressure": 1012, "clouds": 5, "condition": "Sunny ☀️"},
            "Mumbai": {"temp": 31.5, "feels": 30.2, "humidity": 65, "wind": 15, "pressure": 1008, "clouds": 20, "condition": "Partly Cloudy 🌤️"},
            "pune": {"temp": 25.8, "feels": 24.5, "humidity": 55, "wind": 12, "pressure": 1015, "clouds": 30, "condition": "Hazy 🌫️"},
            "Bangalore": {"temp": 27.1, "feels": 26.0, "humidity": 48, "wind": 10, "pressure": 1010, "clouds": 10, "condition": "Clear Sky ☀️"},
            "Nashik": {"temp": 24.3, "feels": 23.8, "humidity": 70, "wind": 6, "pressure": 1016, "clouds": 40, "condition": "Cloudy ☁️"},
            "Haidrabad": {"temp": 28.9, "feels": 27.8, "humidity": 38, "wind": 9, "pressure": 1011, "clouds": 2, "condition": "Sunny ☀️"}
        }
        
        if city in weather_data:
            data = weather_data[city]
            self.update_display(city, data)
            self.status_label.config(text=f"✅ {city} weather loaded!", fg="#27AE60")
        else:
            self.status_label.config(text=f"❌ {city} not in database", fg="#E73C59")
            messagebox.showinfo("Try These", "Dhule, Mumbai, Pune, Bangalore, Nashik, Haidrabad")
    
    def update_display(self, city, data):
        self.city_label.config(text=f"{city}, INDIA")
        self.main_temp.config(text=f"🌡️  {data['temp']}°C")
        self.condition_label.config(text=data['condition'])
        self.feels_label.config(text=f"Feels like: {data['feels']}°C")
        self.humidity_label.config(text=f"💧 Humidity: {data['humidity']}%")
        self.wind_label.config(text=f"💨 Wind: {data['wind']} km/h")
        self.pressure_label.config(text=f"📊 {data['pressure']} hPa")
        self.clouds_label.config(text=f"☁️  Clouds: {data['clouds']}%")
        self.visibility_label.config(text="👁️  Visibility: 10 km")

root = tk.Tk()
app = WeatherApp(root)
root.mainloop()