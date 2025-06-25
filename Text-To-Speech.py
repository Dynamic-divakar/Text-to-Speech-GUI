import tkinter as tk
from tkinter import messagebox, filedialog
import pyttsx3
import os
from pydub import AudioSegment
import logging

logging.basicConfig(level=logging.ERROR)

# Initialize pyttsx3 engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Extract short voice names
def extract_short_name(voice):
    for word in voice.name.split():
        if word.lower() in ["david", "zira", "hazel"]:
            return word
    return voice.name.split()[0]

voice_names_clean = [extract_short_name(voice) for voice in voices]
voice_map = {extract_short_name(voice): voice.id for voice in voices}

# Text-to-Speech function
def speak_text():
    text = entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("⚠️ Warning", "Please enter some text!")
        return
    engine.setProperty('voice', voice_map[voice_var.get()])
    engine.say(text)
    engine.runAndWait()

# Save audio as MP3
def download_audio():
    text = entry.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("⚠️ Warning", "Please enter some text!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                             filetypes=[("MP3 files", "*.mp3")],
                                             title="Save Audio As")
    if file_path:
        temp_wav = "temp_audio.wav"
        try:
            engine.setProperty('voice', voice_map[voice_var.get()])
            engine.save_to_file(text, temp_wav)
            engine.runAndWait()
            sound = AudioSegment.from_wav(temp_wav)
            sound.export(file_path, format="mp3")
            os.remove(temp_wav)
            messagebox.showinfo("✅ Success", f"Audio saved as:\n{file_path}")
        except Exception as e:
            messagebox.showerror("❌ Error", f"Something went wrong:\n{str(e)}")

# Toggle between dark/light mode
def on_click(event=None):
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        apply_dark_theme()
        canvas.itemconfig(circle, fill="#444444", outline="#666666")
        canvas.itemconfig(icon, text=".     ☀️", fill="white")
    else:
        apply_light_theme()
        canvas.itemconfig(circle, fill="#dddddd", outline="#aaaaaa")
        canvas.itemconfig(icon, text="🌙", fill="#333333")

def apply_dark_theme():
    root.config(bg="#1e1e1e")
    title_label.config(bg="#1e1e1e", fg="white")
    entry.config(bg="#2a2a2a", fg="white", insertbackground="white")
    voice_frame.config(bg="#1e1e1e")
    voice_label.config(bg="#1e1e1e", fg="white")
    button_frame.config(bg="#1e1e1e")
    speak_button.config(bg="#3c3c3c", fg="white")
    download_button.config(bg="#3c3c3c", fg="white")
    footer.config(bg="#1e1e1e", fg="#888")
    canvas.config(bg="#1e1e1e")

def apply_light_theme():
    root.config(bg="#fdf6f0")
    title_label.config(bg="#fdf6f0", fg="#333")
    entry.config(bg="white", fg="black", insertbackground="black")
    voice_frame.config(bg="#fdf6f0")
    voice_label.config(bg="#fdf6f0", fg="#333")
    button_frame.config(bg="#fdf6f0")
    speak_button.config(bg="#4a90e2", fg="white")
    download_button.config(bg="#4a90e2", fg="white")
    footer.config(bg="#fdf6f0", fg="#888")
    canvas.config(bg="#fdf6f0")

# GUI Setup
root = tk.Tk()
root.title("🎤 Text to Speech Converter")
# root.geometry("520x540")
root.resizable(False, False)
dark_mode = False

FONT_TITLE = ("Helvetica", 18, "bold")
FONT_TEXT = ("Helvetica", 12)

# Title
title_label = tk.Label(root, text="🗣️ Text to Speech", font=FONT_TITLE)
title_label.pack(pady=20)

# Text Entry
entry = tk.Text(root, height=8, width=55, font=FONT_TEXT, wrap="word", bd=2, relief="groove")
entry.pack(pady=10)

# Voice Selection
voice_var = tk.StringVar(value=voice_names_clean[0])
voice_frame = tk.Frame(root)
voice_frame.pack(pady=5)

voice_label = tk.Label(voice_frame, text="Select Voice: ", font=FONT_TEXT)
voice_label.grid(row=0, column=0, padx=5)

voice_dropdown = tk.OptionMenu(voice_frame, voice_var, *voice_names_clean)
voice_dropdown.config(font=("Helvetica", 11), bg="white", width=20 )
voice_dropdown.grid(row=0, column=1)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

speak_button = tk.Button(button_frame, text="🔊 Speak", font=FONT_TEXT, command=speak_text)
speak_button.grid(row=0, column=0, padx=10)

download_button = tk.Button(button_frame, text="💾 Download MP3", font=FONT_TEXT, command=download_audio)
download_button.grid(row=0, column=1, padx=10)

# Footer
footer = tk.Label(root, text="Made with ❤️ using Python", font=("Helvetica", 10))
footer.pack(side="bottom", pady=10)

# Circular Canvas Dark Mode Toggle Button
canvas = tk.Canvas(root, width=40, height=40, bg=root['bg'], highlightthickness=0)
canvas.place(relx=1.0, x=-10, y=10, anchor="ne")

circle = canvas.create_oval(5, 5, 35, 35, fill="#dddddd", outline="#aaaaaa")
icon = canvas.create_text(20, 20, text="🌙", font=("Helvetica", 12, "bold"), fill="#333333", anchor="center")


canvas.tag_bind(circle, "<Button-1>", on_click)
canvas.tag_bind(icon, "<Button-1>", on_click)

# Start with light theme
apply_light_theme()

root.mainloop()
