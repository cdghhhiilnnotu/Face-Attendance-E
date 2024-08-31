# From Python
from customtkinter import CTk as ctk
import tkinter as tk
from customtkinter import CTkLabel
from PIL import Image, ImageTk, ImageDraw

class TechSupports:

    def transparent_color(root: ctk, color: str):
        root.attributes("-transparentcolor", color)
        root.config(bg=color)

    def center_app(window: tk):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def blank_label(label: CTkLabel):
        label_width, label_height = label.winfo_width(), label.winfo_height()
        img = Image.new("RGBA", (label_width, label_height), (0, 0, 0, 255))
        
        TechSupports.display_to_label(label, img)

    def display_to_label(label: CTkLabel, img):
        # Resize the image to match the label's size
        label_width, label_height = label.winfo_width(), label.winfo_height()
        img = img.resize((label_width, label_height), Image.Resampling.LANCZOS)

        # Add rounded corners
        corner_radius = 10
        mask = Image.new("L", (label_width, label_height), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), (label_width, label_height)], corner_radius, fill=255)
        img.putalpha(mask)

        photo_image = ImageTk.PhotoImage(image=img)
        label.photo_image = photo_image
        label.configure(image=photo_image)



