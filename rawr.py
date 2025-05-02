import tkinter as tk
from tkinter import filedialog, messagebox
import json
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import webbrowser
import os
import time

# Create root window (GUI setup)
root = ttk.Window(themename="flatly")
root.title("rawr - Discohook Embed Generator")
root.geometry("500x400")

# Add Tomie image to the top (use an appropriate path here)
image_path = 'assets/tomie.jpg'  # Make sure you place this image in the assets folder
try:
    img = Image.open(image_path)
    img = img.resize((100, 100), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    label_img = ttk.Label(root, image=img)
    label_img.pack(pady=10)
except FileNotFoundError:
    print("Tomie image not found. Please add an image named 'tomie.jpg' to the 'assets' folder.")

# Function to process raw JSON
def process_json():
    try:
        # Get raw JSON input from the text area
        raw_json = text_input.get("1.0", tk.END)
        parsed_json = json.loads(raw_json)
        
        # Get the embed data (this is a basic example; you may need to expand based on your needs)
        embed = parsed_json.get('embeds', [])[0]
        title = embed.get('title', 'No Title')
        description = embed.get('description', 'No Description')

        # Create output JSON for Discohook
        discohook_json = {
            "embeds": [{
                "title": title,
                "description": description,
                "color": embed.get('color', 16711680)  # Default color red if none is provided
            }]
        }

        # Display the output
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, json.dumps(discohook_json, indent=4))

    except json.JSONDecodeError:
        messagebox.showerror("Invalid JSON", "The JSON input is invalid. Please check your input.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to save the embed JSON to a file
def save_json():
    try:
        embed_data = output_text.get("1.0", tk.END)
        if not embed_data.strip():
            messagebox.showwarning("No Data", "There's no data to save. Please generate the embed first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as json_file:
                json_file.write(embed_data)
            messagebox.showinfo("Success", f"Embed saved to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Function to open Discohook in browser with the generated embed
def open_in_discord():
    embed_data = output_text.get("1.0", tk.END)
    if not embed_data.strip():
        messagebox.showwarning("No Data", "There's no data to open. Please generate the embed first.")
        return
    url = f"https://discohook.org/?data={json.dumps(json.loads(embed_data))}"
    webbrowser.open(url)

# Text input area for raw JSON
text_input = tk.Text(root, height=10, wrap=tk.WORD)
text_input.pack(padx=10, pady=10)

# Buttons for options
button_process = ttk.Button(root, text="Generate Discohook Embed", command=process_json)
button_process.pack(pady=5)

button_save = ttk.Button(root, text="Save Embed to File", command=save_json)
button_save.pack(pady=5)

button_open_discord = ttk.Button(root, text="Open in Discohook", command=open_in_discord)
button_open_discord.pack(pady=5)

# Output area for generated embed
output_text = tk.Text(root, height=10, wrap=tk.WORD)
output_text.pack(padx=10, pady=10)

# Start the GUI loop
root.mainloop()
