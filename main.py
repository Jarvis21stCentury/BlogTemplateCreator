import customtkinter as ctk
from tkinter import messagebox, colorchooser
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Blog Template Creator")
root.geometry("520x600")
root.resizable(False, False)

header = ctk.CTkFrame(root, fg_color=("gray90", "gray15"), corner_radius=0, height=88)
header.pack(fill="x")
header.pack_propagate(False)

header_text = ctk.CTkFrame(header, fg_color="transparent")
header_text.pack(side="left", padx=24, fill="y")

ctk.CTkLabel(
    header_text,
    text="Blog Template Creator",
    font=ctk.CTkFont(family="Georgia", size=22, weight="bold"),
    anchor="w",
).pack(anchor="w", pady=(20, 2))

ctk.CTkLabel(
    header_text,
    text="AI-powered HTML templates in seconds",
    font=ctk.CTkFont(family="Arial", size=11),
    text_color=("gray50", "gray60"),
    anchor="w",
).pack(anchor="w")

badge_frame = ctk.CTkFrame(header, fg_color=("gray80", "gray22"), corner_radius=8)
badge_frame.pack(side="right", padx=20)
ctk.CTkLabel(
    badge_frame,
    text="GPT-4o mini",
    font=ctk.CTkFont(family="Arial", size=10, weight="bold"),
    text_color=("gray40", "gray65"),
    padx=10,
    pady=5,
).pack()

card = ctk.CTkFrame(
    root,
    corner_radius=14,
    fg_color=("white", "gray17"),
    border_width=1,
    border_color=("gray85", "gray25"),
)
card.pack(fill="both", expand=True, padx=20, pady=(14, 18))

def section_header(parent, title):
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", padx=20, pady=(16, 8))
    ctk.CTkLabel(
        row,
        text=title,
        font=ctk.CTkFont(family="Arial", size=10, weight="bold"),
        text_color=("gray45", "gray55"),
        anchor="w",
    ).pack(side="left")
    ctk.CTkFrame(row, height=1, fg_color=("gray82", "gray30"), corner_radius=0).pack(
        side="left", fill="x", expand=True, padx=(10, 0), pady=1
    )

def labeled_entry(parent, label, placeholder, default=""):
    ctk.CTkLabel(
        parent,
        text=label,
        font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
        anchor="w",
    ).pack(fill="x", padx=20, pady=(0, 3))
    entry = ctk.CTkEntry(
        parent,
        height=38,
        font=ctk.CTkFont(family="Arial", size=13),
        corner_radius=8,
        border_width=1,
        placeholder_text=placeholder,
    )
    if default:
        entry.insert(0, default)
    entry.pack(fill="x", padx=20, pady=(0, 2))
    return entry

def color_entry(parent, label, default, col):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.grid(row=0, column=col, sticky="ew", padx=(0, 6) if col == 0 else (6, 0))

    ctk.CTkLabel(
        frame,
        text=label,
        font=ctk.CTkFont(family="Arial", size=12, weight="bold"),
        anchor="w",
    ).pack(fill="x", pady=(0, 3))

    row = ctk.CTkFrame(frame, fg_color="transparent")
    row.pack(fill="x")

    swatch = ctk.CTkFrame(
        row,
        width=38,
        height=38,
        corner_radius=8,
        fg_color=default,
        border_width=1,
        border_color=("gray75", "gray35"),
        cursor="pointinghand",
    )
    swatch.pack(side="left", padx=(0, 6))
    swatch.pack_propagate(False)

    entry = ctk.CTkEntry(
        row,
        height=38,
        font=ctk.CTkFont(family="Arial", size=13),
        corner_radius=8,
        border_width=1,
    )
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
entry_type = labeled_entry(card, "Blog Type", "e.g. travel, food, tech, fashion…")

section_header(card, "APPEARANCE")
colors_row = ctk.CTkFrame(card, fg_color="transparent")
colors_row.pack(fill="x", padx=20, pady=(0, 2))
colors_row.columnconfigure(0, weight=1)
colors_row.columnconfigure(1, weight=1)
entry_bg   = color_entry(colors_row, "Background Color", "#ffffff", 0)
entry_text = color_entry(colors_row, "Text Color",       "#000000", 1)

section_header(card, "OUTPUT")
entry_file = labeled_entry(card, "File Name", "template.html", "template.html")

status_var = ctk.StringVar(value="")
status_label = ctk.CTkLabel(
    card,
    textvariable=status_var,
    font=ctk.CTkFont(family="Arial", size=11),
    text_color=("gray50", "gray60"),
)
status_label.pack(pady=(10, 0))

def generate_template(data, background_color, text_color, file_name):
    title            = data.get("title", "Blog Post Title")
    subtitle         = data.get("subtitle", "A compelling subtitle for this post")
    author           = data.get("author", "Author Name")
    tags             = data.get("tags", [])
    intro            = data.get("intro", "")
    section_heading  = data.get("section_heading", "")
    section_body     = data.get("section_body", "")
    quote            = data.get("quote", "")
    conclusion       = data.get("conclusion", "")
    img1_caption     = data.get("image1_caption", "Add a caption for this image")
    img2_caption     = data.get("image2_caption", "Add a caption for this image")

    tags_html = " ".join(f'<span class="tag">{t}</span>' for t in tags)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Inter', sans-serif; background: {background_color}; color: {text_color}; line-height: 1.7; }}

        nav {{ display: flex; justify-content: space-between; align-items: center; padding: 18px 48px; border-bottom: 1px solid #e5e7eb; background: {background_color}; position: sticky; top: 0; z-index: 100; }}
        .nav-brand {{ font-family: 'Playfair Display', serif; font-size: 1.4rem; font-weight: 700; color: {text_color}; text-decoration: none; }}
        .nav-links a {{ margin-left: 24px; text-decoration: none; color: {text_color}; opacity: 0.7; font-size: 0.9rem; }}
        .nav-links a:hover {{ opacity: 1; }}

        .hero {{ max-width: 860px; margin: 48px auto 0; padding: 0 24px; text-align: center; }}
        .hero-img {{ width: 100%; height: 420px; background: #e5e7eb; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; color: #9ca3af; border: 2px dashed #d1d5db; margin-bottom: 32px; }}
        .hero h1 {{ font-family: 'Playfair Display', serif; font-size: 2.6rem; line-height: 1.2; margin-bottom: 14px; }}
        .subtitle {{ font-size: 1.1rem; opacity: 0.7; margin-bottom: 20px; }}
        .post-meta {{ display: flex; align-items: center; justify-content: center; gap: 16px; font-size: 0.85rem; opacity: 0.6; margin-bottom: 40px; }}
        .tag {{ display: inline-block; background: #f3f4f6; color: #374151; border-radius: 20px; padding: 3px 12px; font-size: 0.78rem; margin: 0 2px; }}

        .content-grid {{ max-width: 1100px; margin: 0 auto; padding: 0 24px 64px; display: grid; grid-template-columns: 1fr 300px; gap: 56px; align-items: start; }}

        article p {{ margin-bottom: 1.4rem; font-size: 1.05rem; }}
        article h2 {{ font-family: 'Playfair Display', serif; font-size: 1.6rem; margin: 36px 0 14px; }}
        .img-block {{ margin: 32px 0; }}
        .img-placeholder {{ width: 100%; height: 320px; background: #e5e7eb; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 0.88rem; color: #9ca3af; border: 2px dashed #d1d5db; }}
        .img-caption {{ text-align: center; font-size: 0.82rem; opacity: 0.55; margin-top: 8px; font-style: italic; }}
        blockquote {{ border-left: 4px solid {text_color}; padding: 14px 24px; margin: 32px 0; font-style: italic; font-size: 1.15rem; opacity: 0.8; background: rgba(0,0,0,0.03); border-radius: 0 8px 8px 0; }}

        aside {{ position: sticky; top: 80px; }}
        .widget {{ border: 1px solid #e5e7eb; border-radius: 10px; padding: 20px; margin-bottom: 24px; }}
        .widget h3 {{ font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.08em; opacity: 0.5; margin-bottom: 14px; }}
        .author-avatar {{ width: 64px; height: 64px; border-radius: 50%; background: #e5e7eb; border: 2px dashed #d1d5db; display: flex; align-items: center; justify-content: center; font-size: 0.65rem; color: #9ca3af; margin-bottom: 10px; }}
        .author-name {{ font-weight: 600; margin-bottom: 6px; }}
        .author-bio {{ font-size: 0.85rem; opacity: 0.65; }}
        .tags-widget {{ display: flex; flex-wrap: wrap; gap: 6px; }}
        .related-item {{ display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }}
        .related-thumb {{ width: 56px; height: 56px; border-radius: 6px; background: #e5e7eb; border: 2px dashed #d1d5db; flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-size: 0.6rem; color: #9ca3af; }}
        .related-title {{ font-size: 0.88rem; font-weight: 600; line-height: 1.3; }}

        footer {{ text-align: center; padding: 32px 24px; border-top: 1px solid #e5e7eb; font-size: 0.85rem; opacity: 0.5; }}
    </style>
</head>
<body>

<section class="hero">
    <div class="hero-img">[ Hero Image ]</div>
    <h1>{title}</h1>
    <p class="subtitle">{subtitle}</p>
    <div class="post-meta">
        <span>By {author}</span>
        <span>&middot;</span>
        <span>July 2025</span>
        <span>&middot;</span>
        <div>{tags_html}</div>
    </div>
</section>

<div class="content-grid">
    <article>
        <p>{intro}</p>

        <div class="img-block">
            <div class="img-placeholder">[ Image &mdash; replace with &lt;img src="image1.jpg" alt="..."&gt; ]</div>
            <p class="img-caption">{img1_caption}</p>
        </div>

        <h2>{section_heading}</h2>
        <p>{section_body}</p>

        <blockquote>&ldquo;{quote}&rdquo;</blockquote>

        <div class="img-block">
            <div class="img-placeholder">[ Image &mdash; replace with &lt;img src="image2.jpg" alt="..."&gt; ]</div>
            <p class="img-caption">{img2_caption}</p>
        </div>

        <p>{conclusion}</p>
    </article>

    <aside>
        <div class="widget">
            <h3>About the Author</h3>
            <div class="author-avatar">Photo</div>
            <div class="author-name">{author}</div>
            <p class="author-bio">Replace this with a short bio about the author. A sentence or two works great here.</p>
        </div>

        <div class="widget">
            <h3>Tags</h3>
            <div class="tags-widget">{tags_html}</div>
        </div>

        <div class="widget">
            <h3>Related Posts</h3>
            <div class="related-item">
                <div class="related-thumb">img</div>
                <span class="related-title">Related Post Title One</span>
            </div>
            <div class="related-item">
                <div class="related-thumb">img</div>
                <span class="related-title">Related Post Title Two</span>
            </div>
            <div class="related-item">
                <div class="related-thumb">img</div>
                <span class="related-title">Related Post Title Three</span>
            </div>
        </div>
    </aside>
</div>

<footer>
    <p>&copy; 2025 My Blog &mdash; All rights reserved.</p>
</footer>

</body>
</html>"""

    with open(file_name, "w") as f:
        f.write(html)
    messagebox.showinfo("Done", f"Template saved as {file_name}")


def generate_code():
    user_need        = entry_type.get().strip()
    background_color = entry_bg.get().strip()
    text_color       = entry_text.get().strip()
    file_name        = entry_file.get().strip()

    if not user_need:
        messagebox.showerror("Error", "Please enter a blog type.")
        return

    btn.configure(state="disabled", text="Generating…")
    status_var.set("Calling GPT-4o mini…")
    status_label.configure(text_color=("gray50", "gray60"))
    root.update_idletasks()

    prompt = (
        f"Generate content for a {user_need} blog post template. "
        "Return a JSON object with exactly these keys: "
        "'title' (post title), "
        "'subtitle' (one sentence hook), "
        "'author' (a realistic author name), "
        "'tags' (collection of 3 to 4 relevant short tags), "
        "'intro' (2-3 sentence opening paragraph), "
        "'section_heading' (subheading for the main section), "
        "'section_body' (2-3 sentence body paragraph for section), "
        "'quote' (one memorable pull-quote sentence, no quotation marks), "
        "'conclusion' (2 sentence closing paragraph), "
        "'image1_caption' (short descriptive caption for the first inline image), "
        "'image2_caption' (short descriptive caption for the second inline image). "
        "Keep all text relevant to the blog type. No markdown, valid JSON only."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a blog content generator. Always respond with valid JSON only, no markdown."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
        )
        data = json.loads(response.choices[0].message.content)
        generate_template(data, background_color, text_color, file_name)
        status_var.set(f"✓ Saved to {file_name}")
        status_label.configure(text_color=("#15803d", "#4ade80"))
    except Exception as e:
        messagebox.showerror("API Error", str(e))
        status_var.set("✗ Error — see dialog")
        status_label.configure(text_color=("#dc2626", "#f87171"))
    finally:
        btn.configure(state="normal", text="Generate Template")


btn = ctk.CTkButton(
    card,
    text="Generate Template",
    command=generate_code,
    height=44,
    corner_radius=10,
    font=ctk.CTkFont(family="Arial", size=14, weight="bold"),
    hover_color=("#1f4fd1", "#4c7bf0"),
)
btn.pack(padx=20, pady=(10, 20), fill="x")

root.mainloop()
