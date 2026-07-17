import os
import sys

from flask import Flask, Response, jsonify, request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from content_generator import generate_content
from template_builder import build_html

app = Flask(__name__)

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blog Template Creator</title>
<style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: Arial, Helvetica, sans-serif; background: #f2f2f2; color: #1a1a1a; }

    header { background: #e9e9e9; padding: 18px 32px; display: flex; align-items: center; justify-content: space-between; }
    header h1 { font-family: Georgia, serif; font-size: 1.4rem; }
    header p { font-size: 0.8rem; color: #555; margin-top: 2px; }
    .badge { background: #d6d6d6; color: #333; font-size: 0.7rem; font-weight: bold; padding: 5px 10px; border-radius: 8px; }

    main { max-width: 960px; margin: 24px auto; padding: 0 20px; display: grid; grid-template-columns: 340px 1fr; gap: 24px; align-items: start; }

    .card { background: white; border: 1px solid #dcdcdc; border-radius: 14px; padding: 20px; }

    label { display: block; font-size: 0.8rem; font-weight: bold; margin: 14px 0 4px; }
    label:first-child { margin-top: 0; }
    input[type=text] { width: 100%; height: 36px; padding: 0 10px; border: 1px solid #ccc; border-radius: 8px; font-size: 0.9rem; }

    .color-row { display: flex; gap: 10px; }
    .color-field { flex: 1; }
    .color-field .inputs { display: flex; gap: 6px; align-items: center; }
    .color-field input[type=color] { width: 36px; height: 36px; border: 1px solid #ccc; border-radius: 8px; padding: 0; }
    .color-field input[type=text] { flex: 1; }

    button { width: 100%; height: 42px; margin-top: 18px; border: none; border-radius: 10px; background: #2f6fed; color: white; font-size: 0.95rem; font-weight: bold; cursor: pointer; }
    button:disabled { background: #9db8f0; cursor: default; }

    #status { font-size: 0.8rem; color: #666; margin-top: 10px; min-height: 1em; }
    #status.error { color: #dc2626; }
    #status.ok { color: #15803d; }

    #download { display: none; text-align: center; margin-top: 10px; font-size: 0.85rem; color: #2f6fed; text-decoration: none; }

    .preview { background: white; border: 1px solid #dcdcdc; border-radius: 14px; overflow: hidden; height: 640px; }
    .preview iframe { width: 100%; height: 100%; border: none; }
    .preview .empty { display: flex; align-items: center; justify-content: center; height: 100%; color: #999; font-size: 0.9rem; }
</style>
</head>
<body>

<header>
    <div>
        <h1>Blog Template Creator</h1>
        <p>Generates a ready-to-edit blog post template</p>
    </div>
    <div class="badge">GPT-4o mini</div>
</header>

<main>
    <div class="card">
        <label>Blog Type</label>
        <input type="text" id="blogType" placeholder="e.g. travel, food, tech, fashion">

        <div class="color-row">
            <div class="color-field">
                <label>Background Color</label>
                <div class="inputs">
                    <input type="color" id="bgSwatch" value="#ffffff">
                    <input type="text" id="bgHex" value="#ffffff">
                </div>
            </div>
            <div class="color-field">
                <label>Text Color</label>
                <div class="inputs">
                    <input type="color" id="textSwatch" value="#000000">
                    <input type="text" id="textHex" value="#000000">
                </div>
            </div>
        </div>

        <label>File Name</label>
        <input type="text" id="fileName" value="template.html">

        <button id="generateBtn">Generate Template</button>
        <div id="status"></div>
        <a id="download">Download template.html</a>
    </div>

    <div class="preview">
        <div class="empty" id="previewEmpty">Your generated template will show up here</div>
        <iframe id="previewFrame" style="display:none"></iframe>
    </div>
</main>

<script>
function syncSwatch(swatchId, hexId) {
    const swatch = document.getElementById(swatchId);
    const hex = document.getElementById(hexId);
    swatch.addEventListener("input", () => { hex.value = swatch.value; });
    hex.addEventListener("input", () => {
        if (/^#[0-9a-fA-F]{6}$/.test(hex.value)) swatch.value = hex.value;
    });
}
syncSwatch("bgSwatch", "bgHex");
syncSwatch("textSwatch", "textHex");

const btn = document.getElementById("generateBtn");
const status = document.getElementById("status");
const download = document.getElementById("download");
const previewFrame = document.getElementById("previewFrame");
const previewEmpty = document.getElementById("previewEmpty");

btn.addEventListener("click", async () => {
    const blogType = document.getElementById("blogType").value.trim();
    if (!blogType) {
        status.textContent = "Please enter a blog type.";
        status.className = "error";
        return;
    }

    const fileName = document.getElementById("fileName").value.trim() || "template.html";

    btn.disabled = true;
    btn.textContent = "Generating...";
    status.textContent = "Calling GPT-4o mini...";
    status.className = "";
    download.style.display = "none";

    try {
        const res = await fetch("/api/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                blog_type: blogType,
                background_color: document.getElementById("bgHex").value.trim(),
                text_color: document.getElementById("textHex").value.trim(),
            }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Request failed");

        previewEmpty.style.display = "none";
        previewFrame.style.display = "block";
        previewFrame.srcdoc = data.html;

        const blob = new Blob([data.html], { type: "text/html" });
        download.href = URL.createObjectURL(blob);
        download.download = fileName;
        download.textContent = "Download " + fileName;
        download.style.display = "block";

        status.textContent = "Generated successfully";
        status.className = "ok";
    } catch (err) {
        status.textContent = "Error: " + err.message;
        status.className = "error";
    } finally {
        btn.disabled = false;
        btn.textContent = "Generate Template";
    }
});
</script>

</body>
</html>"""


@app.route("/")
def index():
    return Response(PAGE, mimetype="text/html")


@app.route("/api/generate", methods=["POST"])
def generate():
    payload = request.get_json(silent=True) or {}
    blog_type = (payload.get("blog_type") or "").strip()
    background_color = (payload.get("background_color") or "#ffffff").strip()
    text_color = (payload.get("text_color") or "#000000").strip()

    if not blog_type:
        return jsonify({"error": "Please enter a blog type."}), 400

    try:
        data = generate_content(blog_type)
    except Exception as e:
        return jsonify({"error": str(e)}), 502

    html = build_html(data, background_color, text_color)
    return jsonify({"html": html})
