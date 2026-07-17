import os
import webbrowser
from datetime import datetime
from tkinter import colorchooser, messagebox

import customtkinter as ctk

from content_generator import generate_content
from template_builder import build_html, save_template

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Blog Template Creator")
root.geometry("520x700")
root.resizable(False, False)

header = ctk.CTkFrame(root, fg_color="#e9e9e9", corner_radius=0, height=88)
header.pack(fill="x")
header.pack_propagate(False)

header_text = ctk.CTkFrame(header, fg_color="transparent")
header_text.pack(side="left", padx=24, fill="y")

ctk.CTkLabel(
    header_text,
    text="Blog Template Creator",
    font=ctk.CTkFont(family="Georgia", size=22, weight="bold"),
).pack(anchor="w", pady=(20, 2))

ctk.CTkLabel(
    header_text,
    text="Generates a ready-to-edit blog post template",
    font=ctk.CTkFont(size=11),
    text_color="gray45",
).pack(anchor="w")

badge_frame = ctk.CTkFrame(header, fg_color="#d6d6d6", corner_radius=8)
badge_frame.pack(side="right", padx=20)
ctk.CTkLabel(
    badge_frame,
    text="GPT-4o mini",
    font=ctk.CTkFont(size=10, weight="bold"),
    text_color="gray30",
    padx=10,
    pady=5,
).pack()

card = ctk.CTkFrame(root, corner_radius=16, fg_color="white", border_width=1, border_color="#dcdcdc")
card.pack(fill="both", expand=True, padx=20, pady=(14, 18))


def section_header(parent, title):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", padx=20, pady=(16, 8))
    ctk.CTkLabel(row, text=title, font=ctk.CTkFont(size=10, weight="bold"), text_color="gray45").pack(side="left")
    ctk.CTkFrame(row, height=1, fg_color="#d4d4d4").pack(side="left", fill="x", expand=True, padx=(10, 0), pady=1)


def labeled_entry(parent, label, placeholder, default=""):
    ctk.CTkLabel(parent, text=label, font=ctk.CTkFont(size=12, weight="bold")).pack(fill="x", padx=20, pady=(0, 3))
    entry = ctk.CTkEntry(parent, height=38, placeholder_text=placeholder)
    if default:
        entry.insert(0, default)
    entry.pack(fill="x", padx=20, pady=(0, 2))
    return entry


def color_entry(parent, label, default, col):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.grid(row=0, column=col, sticky="ew", padx=(0, 6) if col == 0 else (6, 0))

    ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=12, weight="bold")).pack(fill="x", pady=(0, 3))

    row = ctk.CTkFrame(frame, fg_color="transparent")
    row.pack(fill="x")

    swatch = ctk.CTkFrame(row, width=38, height=38, corner_radius=10, fg_color=default,
                           border_width=1, border_color="#bbbbbb", cursor="pointinghand")
    swatch.pack(side="left", padx=(0, 6))
    swatch.pack_propagate(False)

    entry = ctk.CTkEntry(row, height=38)
    entry.insert(0, default)
    entry.pack(side="left", fill="x", expand=True)

    def update_swatch(*_):
        try:
            swatch.configure(fg_color=entry.get().strip())
        except Exception:
            pass

    def pick_color(*_):
        _, hex_color = colorchooser.askcolor(color=entry.get().strip() or default, title=f"Choose {label}")
        if hex_color:
            entry.delete(0, "end")
            entry.insert(0, hex_color)
            update_swatch()

    entry.bind("<KeyRelease>", update_swatch)
    swatch.bind("<Button-1>", pick_color)
    return entry


section_header(card, "CONTENT")
entry_type = labeled_entry(card, "Blog Type", "e.g. travel, food, tech, fashion")

section_header(card, "APPEARANCE")
colors_row = ctk.CTkFrame(card, fg_color="transparent")
colors_row.pack(fill="x", padx=20, pady=(0, 2))
colors_row.columnconfigure(0, weight=1)
colors_row.columnconfigure(1, weight=1)
entry_bg = color_entry(colors_row, "Background Color", "#ffffff", 0)
entry_text = color_entry(colors_row, "Text Color", "#000000", 1)

section_header(card, "OUTPUT")
entry_file = labeled_entry(card, "File Name", "template.html", "template.html")

history_header_row = ctk.CTkFrame(card, fg_color="transparent")
history_header_row.pack(fill="x", padx=20, pady=(16, 8))
ctk.CTkLabel(history_header_row, text="HISTORY", font=ctk.CTkFont(size=10, weight="bold"), text_color="gray45").pack(side="left")
ctk.CTkFrame(history_header_row, height=1, fg_color="#d4d4d4").pack(side="left", fill="x", expand=True, padx=(10, 6), pady=1)

history_frame = ctk.CTkScrollableFrame(card, height=110, fg_color="#f2f2f2", corner_radius=8)
history_frame.pack(fill="x", padx=20, pady=(0, 4))

history_empty_label = ctk.CTkLabel(
    history_frame,
    text="No templates generated yet.",
    font=ctk.CTkFont(size=11),
    text_color="gray50",
)
history_empty_label.pack(pady=10)

history_entries = []


def clear_history():
    for row in history_entries:
        row.destroy()
    history_entries.clear()
    history_empty_label.pack(pady=10)


def add_history_entry(file_name):
    history_empty_label.pack_forget()

    row = ctk.CTkFrame(history_frame, fg_color="white", corner_radius=6)
    row.pack(fill="x", pady=3, padx=2)

    info = ctk.CTkFrame(row, fg_color="transparent")
    info.pack(side="left", fill="x", expand=True, padx=(8, 4), pady=6)
    ctk.CTkLabel(info, text=file_name, font=ctk.CTkFont(size=12, weight="bold"), anchor="w").pack(fill="x")
    ctk.CTkLabel(
        info,
        text=f"Generated at {datetime.now().strftime('%H:%M:%S')}",
        font=ctk.CTkFont(size=10),
        text_color="gray50",
        anchor="w",
    ).pack(fill="x")

    actions = ctk.CTkFrame(row, fg_color="transparent")
    actions.pack(side="right", padx=(0, 8))

    def open_file(_=None, path=file_name):
        webbrowser.open(f"file://{os.path.abspath(path)}")

    def copy_path(_=None, path=file_name):
        root.clipboard_clear()
        root.clipboard_append(os.path.abspath(path))

    ctk.CTkButton(actions, text="Open", width=52, height=24, fg_color="#dcdcdc", text_color="gray20",
                  hover_color="#c8c8c8", command=open_file).pack(side="left", padx=(0, 4))
    ctk.CTkButton(actions, text="Copy Path", width=70, height=24, fg_color="#dcdcdc", text_color="gray20",
                  hover_color="#c8c8c8", command=copy_path).pack(side="left")

    history_entries.append(row)
    if len(history_entries) > 4:
        history_entries.pop(0).destroy()


clear_history_btn = ctk.CTkButton(
    history_header_row, text="Clear", width=44, height=18,
    font=ctk.CTkFont(size=9, weight="bold"), fg_color="transparent",
    text_color="gray50", hover_color="#e0e0e0", command=clear_history,
)
clear_history_btn.pack(side="right")

status_var = ctk.StringVar(value="")
status_label = ctk.CTkLabel(card, textvariable=status_var, font=ctk.CTkFont(size=11), text_color="gray50")
status_label.pack(pady=(10, 0))


def generate_code():
    user_need = entry_type.get().strip()
    background_color = entry_bg.get().strip()
    text_color = entry_text.get().strip()
    file_name = entry_file.get().strip()

    if not user_need:
        messagebox.showerror("Error", "Please enter a blog type.")
        return

    btn.configure(state="disabled", text="Generating...")
    status_var.set("Calling GPT-4o mini...")
    status_label.configure(text_color="gray50")
    root.update_idletasks()

    try:
        data = generate_content(user_need)
        html = build_html(data, background_color, text_color)
        save_template(html, file_name)
        messagebox.showinfo("Done", f"Template saved as {file_name}")
        add_history_entry(file_name)
        status_var.set(f"Saved to {file_name}")
        status_label.configure(text_color="#15803d")
    except Exception as e:
        messagebox.showerror("API Error", str(e))
        status_var.set("Error - see dialog")
        status_label.configure(text_color="#dc2626")
    finally:
        btn.configure(state="normal", text="Generate Template")


btn = ctk.CTkButton(
    card,
    text="Generate Template",
    command=generate_code,
    height=46,
    corner_radius=10,
    font=ctk.CTkFont(size=14, weight="bold"),
)
btn.pack(padx=20, pady=(10, 20), fill="x")

root.mainloop()
