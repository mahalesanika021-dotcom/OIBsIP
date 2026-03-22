# ============================================
# Voice Assistant - Speech Recognition
# Oasis Infobyte Internship - FINAL PROJECT
# Author: Sanika mahale 
# ============================================

import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import random


class VoiceAssistant:
    def __init__(self, root):
        self.root = root
        self.root.title("🎤 Voice Assistant - Jarvis")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        # Initialize recognizer
        self.recognizer = sr.Recognizer()

        # Try microphone safely
        try:
            self.microphone = sr.Microphone()
        except:
            messagebox.showerror(
                "Microphone Error",
                "PyAudio not installed.\nInstall using:\n\npip install pipwin\npipwin install pyaudio"
            )
            self.microphone = None

        # Text to speech
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 170)

        self.setup_ui()
        self.greet_user()

    def setup_ui(self):

        header_frame = tk.Frame(self.root, bg="#2C3E50", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        title = tk.Label(
            header_frame,
            text="🎤 VOICE ASSISTANT - JARVIS",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#2C3E50"
        )
        title.pack(expand=True)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=30)

        tk.Button(
            btn_frame,
            text="🎤 LISTEN",
            command=self.listen_command,
            bg="#E74C3C",
            fg="white",
            font=("Arial", 16, "bold"),
            width=12,
            height=2
        ).pack(side=tk.LEFT, padx=20)

        tk.Button(
            btn_frame,
            text="🗣 SPEAK TEST",
            command=self.test_speak,
            bg="#3498DB",
            fg="white",
            font=("Arial", 16, "bold"),
            width=12,
            height=2
        ).pack(side=tk.LEFT, padx=20)

        tk.Button(
            btn_frame,
            text="📝 MANUAL INPUT",
            command=self.manual_input,
            bg="#F39C12",
            fg="white",
            font=("Arial", 16, "bold"),
            width=12,
            height=2
        ).pack(side=tk.LEFT, padx=20)

        chat_frame = tk.LabelFrame(
            self.root,
            text="💬 Conversation",
            font=("Arial", 14, "bold"),
            padx=20,
            pady=20
        )
        chat_frame.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            height=15,
            font=("Arial", 12),
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        self.status_label = tk.Label(
            self.root,
            text="✅ Ready to listen! Say 'hello jarvis'",
            font=("Arial", 12, "bold"),
            fg="#27AE60"
        )
        self.status_label.pack(pady=10)

    def speak(self, text):

        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"Jarvis: {text}\n\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

        self.engine.say(text)
        self.engine.runAndWait()

    def add_user_text(self, text):

        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"You: {text}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def greet_user(self):

        greeting = random.choice([
            "Hello! I am Jarvis. Click LISTEN and say hello jarvis.",
            "Hi there! Try saying time, date or search.",
            "Welcome! Say hello jarvis to start talking."
        ])
        self.speak(greeting)

    def test_speak(self):
        self.speak("Voice test successful! Now try the microphone.")

    def manual_input(self):

        text = simpledialog.askstring("Manual Input", "Type your command:")

        if text:
            self.add_user_text(text)
            self.process_command(text.lower())

    def listen_command(self):

        if self.microphone is None:
            self.speak("Microphone not available.")
            return

        self.status_label.config(text="🎤 Listening...", fg="#F39C12")
        self.root.update()

        try:

            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source, timeout=5)

            self.status_label.config(text="Processing...", fg="#3498DB")

            command = self.recognizer.recognize_google(audio).lower()

            self.add_user_text(command)
            self.process_command(command)

            self.status_label.config(text="Ready for next command!", fg="#27AE60")

        except sr.UnknownValueError:
            self.speak("Sorry, I didn't understand that.")

        except sr.RequestError:
            self.speak("Speech service error.")

        except sr.WaitTimeoutError:
            self.speak("No speech detected.")

    def process_command(self, command):

        if "hello jarvis" in command or "hey jarvis" in command:
            self.speak("Hello! How can I help you?")

        elif "time" in command:
            now = datetime.datetime.now().strftime("%H:%M")
            self.speak(f"The time is {now}")

        elif "date" in command:
            today = datetime.date.today().strftime("%B %d, %Y")
            self.speak(f"Today is {today}")

        elif "search" in command or "google" in command:
            query = command.replace("search", "").replace("google", "").strip()

            if query:
                webbrowser.open(f"https://google.com/search?q={query}")
                self.speak("Searching Google")

        elif "open youtube" in command:
            webbrowser.open("https://youtube.com")
            self.speak("Opening YouTube")

        elif "open github" in command:
            webbrowser.open("https://github.com")
            self.speak("Opening GitHub")

        elif "joke" in command:

            jokes = [
                "Why don't scientists trust atoms? Because they make up everything.",
                "Why did the scarecrow win an award? Because he was outstanding in his field.",
                "Why don't eggs tell jokes? They would crack each other up."
            ]

            self.speak(random.choice(jokes))

        elif "thanks" in command:
            self.speak("You're welcome!")

        elif "bye" in command:
            self.speak("Goodbye! Have a great day!")

        else:
            self.speak("Sorry, I didn't understand that command.")


if __name__ == "__main__":

    root = tk.Tk()
    app = VoiceAssistant(root)
    root.mainloop()