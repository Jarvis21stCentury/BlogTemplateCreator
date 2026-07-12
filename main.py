import customtkinter as ctk
from tkinter import messagebox
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Blog Template Creator")
root.geometry("400x500")

ctk.CTkLabel(root, text="Blog type (travel, food, tech):").pack(pady=(20, 2))
entry_type = ctk.CTkEntry(root, width=240, font=("Arial", 12), corner_radius=6, border_width=1, border_color="#cccccc", placeholder_text="Enter blog type")
entry_type.pack()

ctk.CTkLabel(root, text="Background color (e.g. #ffffff):").pack(pady=(10, 2))
entry_bg = ctk.CTkEntry(root, width=240, font=("Arial", 12), corner_radius=6, border_width=1, border_color="#cccccc", placeholder_text="Enter background color")
entry_bg.insert(0, "#ffffff")
entry_bg.pack()

ctk.CTkLabel(root, text="Text color (e.g. #000000):").pack(pady=(10, 2))
entry_text = ctk.CTkEntry(root, width=240, font=("Arial", 12), corner_radius=6, border_width=1, border_color="#cccccc", placeholder_text="Enter text color")
entry_text.insert(0, "#000000")
entry_text.pack()

ctk.CTkLabel(root, text="File Name:").pack(pady=(10, 2))
entry_file_name = ctk.CTkEntry(root, width=240, font=("Arial", 12), corner_radius=6, border_width=1, border_color="#cccccc", placeholder_text="Enter file name")
entry_file_name.insert(0, "template.html")
entry_file_name.pack()

def generate_template(title, heading, paragraph, background_color, text_color, file_name):
    with open(file_name, "w") as f:
        f.write(f"""<html>
    <head>
        <title>{title}</title>
    </head>
    <body style="background-color: {background_color}; color: {text_color};">
        <h1>{heading}</h1>
        <p>{paragraph}</p>
    </body>
</html>""")
    messagebox.showinfo("Done", f"Template saved as {file_name}")

def generate_code():
    user_need = entry_type.get().strip()
    background_color = entry_bg.get().strip()
    text_color = entry_text.get().strip()
    file_name = entry_file_name.get().strip()

    if user_need.lower() not in ("travel", "food", "tech"):
        messagebox.showerror("Error", "Invalid blog type. Please enter 'travel', 'food', or 'tech'.")
        return

    prompt = (
        f"Generate content for a {user_need} blog HTML template. "
        "Return a JSON object with exactly these keys: 'title', 'heading', 'paragraph'. "
        "The paragraph should be 2-3 sentences relevant to the blog type."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a blog content generator. Always respond with valid JSON only, no markdown."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        generate_template(data["title"], data["heading"], data["paragraph"], background_color, text_color, file_name)
    except Exception as e:
        messagebox.showerror("API Error", str(e))

ctk.CTkButton(root, text="Generate Template", command=generate_code, corner_radius=8).pack(pady=20)
root.mainloop()
