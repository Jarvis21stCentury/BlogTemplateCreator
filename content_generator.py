import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

PROMPT_TEMPLATE = (
    "Generate content for a {blog_type} blog post template. "
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


def generate_content(blog_type):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a blog content generator. Always respond with valid JSON only, no markdown."},
            {"role": "user", "content": PROMPT_TEMPLATE.format(blog_type=blog_type)},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)
