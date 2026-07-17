from datetime import datetime


def build_html(data, background_color, text_color):
    title = data.get("title", "Blog Post Title")
    subtitle = data.get("subtitle", "A compelling subtitle for this post")
    author = data.get("author", "Author Name")
    tags = data.get("tags", [])
    intro = data.get("intro", "")
    section_heading = data.get("section_heading", "")
    section_body = data.get("section_body", "")
    quote = data.get("quote", "")
    conclusion = data.get("conclusion", "")
    img1_caption = data.get("image1_caption", "Add a caption for this image")
    img2_caption = data.get("image2_caption", "Add a caption for this image")

    tags_html = " ".join(f'<span class="tag">{t}</span>' for t in tags)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: Arial, Helvetica, sans-serif; background: {background_color}; color: {text_color}; line-height: 1.6; }}

        .hero {{ max-width: 860px; margin: 40px auto 0; padding: 0 24px; text-align: center; }}
        .hero-img {{ width: 100%; height: 400px; background: #e5e7eb; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 0.9rem; color: #9ca3af; border: 2px dashed #d1d5db; margin-bottom: 30px; }}
        .hero h1 {{ font-family: Georgia, serif; font-size: 2.4rem; line-height: 1.2; margin-bottom: 12px; }}
        .subtitle {{ font-size: 1.1rem; opacity: 0.7; margin-bottom: 18px; }}
        .post-meta {{ display: flex; align-items: center; justify-content: center; gap: 14px; font-size: 0.85rem; opacity: 0.6; margin-bottom: 36px; }}
        .tag {{ display: inline-block; background: #f3f4f6; color: #374151; border-radius: 20px; padding: 3px 12px; font-size: 0.78rem; margin: 0 2px; }}

        .content-grid {{ max-width: 1100px; margin: 0 auto; padding: 0 24px 60px; display: grid; grid-template-columns: 1fr 300px; gap: 50px; }}

        article p {{ margin-bottom: 1.3rem; font-size: 1.05rem; }}
        article h2 {{ font-family: Georgia, serif; font-size: 1.5rem; margin: 32px 0 12px; }}
        .img-block {{ margin: 30px 0; }}
        .img-placeholder {{ width: 100%; height: 300px; background: #e5e7eb; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 0.88rem; color: #9ca3af; border: 2px dashed #d1d5db; }}
        .img-caption {{ text-align: center; font-size: 0.82rem; opacity: 0.6; margin-top: 8px; }}
        blockquote {{ border-left: 4px solid {text_color}; padding: 12px 20px; margin: 30px 0; font-style: italic; font-size: 1.1rem; opacity: 0.85; }}

        .widget {{ border: 1px solid #e5e7eb; border-radius: 10px; padding: 18px; margin-bottom: 22px; }}
        .widget h3 {{ font-size: 0.85rem; opacity: 0.6; margin-bottom: 12px; }}
        .author-avatar {{ width: 60px; height: 60px; border-radius: 50%; background: #e5e7eb; border: 2px dashed #d1d5db; display: flex; align-items: center; justify-content: center; font-size: 0.65rem; color: #9ca3af; margin-bottom: 10px; }}
        .author-name {{ font-weight: bold; margin-bottom: 6px; }}
        .author-bio {{ font-size: 0.85rem; opacity: 0.65; }}
        .tags-widget {{ display: flex; flex-wrap: wrap; gap: 6px; }}
        .related-item {{ display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }}
        .related-thumb {{ width: 54px; height: 54px; border-radius: 6px; background: #e5e7eb; border: 2px dashed #d1d5db; flex-shrink: 0; display: flex; align-items: center; justify-content: center; font-size: 0.6rem; color: #9ca3af; }}
        .related-title {{ font-size: 0.88rem; font-weight: bold; line-height: 1.3; }}

        footer {{ text-align: center; padding: 28px 24px; border-top: 1px solid #e5e7eb; font-size: 0.85rem; opacity: 0.5; }}
    </style>
</head>
<body>

<section class="hero">
    <div class="hero-img">[ Hero Image - replace with &lt;img src="hero.jpg" alt="..."&gt; ]</div>
    <h1>{title}</h1>
    <p class="subtitle">{subtitle}</p>
    <div class="post-meta">
        <span>By {author}</span>
        <span>-</span>
        <span>{datetime.now().strftime('%B %Y')}</span>
        <span>-</span>
        <div>{tags_html}</div>
    </div>
</section>

<div class="content-grid">
    <article>
        <p>{intro}</p>

        <div class="img-block">
            <div class="img-placeholder">[ Image - replace with &lt;img src="image1.jpg" alt="..."&gt; ]</div>
            <p class="img-caption">{img1_caption}</p>
        </div>

        <h2>{section_heading}</h2>
        <p>{section_body}</p>

        <blockquote>"{quote}"</blockquote>

        <div class="img-block">
            <div class="img-placeholder">[ Image - replace with &lt;img src="image2.jpg" alt="..."&gt; ]</div>
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
    <p>&copy; {datetime.now().year} My Blog - All rights reserved.</p>
</footer>

</body>
</html>"""


def save_template(html, file_name):
    with open(file_name, "w") as f:
        f.write(html)
