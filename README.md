# Blog Template Creator

The blog template creator takesn your niche, such as "travel" or "tech", and turns it into a HTML blog template that the user can then edit and customize as per needed. This allows for beginner bloggers and journalists to get blogging rather spending hours creating the structure and understanding waht will best convey their message.

It is aimed toward bloggers, marketers, and anyone who needs to create a post quickly, and this tool allows for that by genereating a structure which then the user can replace with real images and content.

## How it works

1. You pick a niche and a color palette.
2. content_generator.py sends a prompt to OpenAI and gets back a JSON file which has a title, subtitle, author, intro, sections, heading/body, conclusion, and two image place holders and captions.
3. template_builder.py puts that JSON into aa HTML template, so the output is a downloadable file.
4. You get a finished HTML file, ready to open in a browser, to drop images into, and publish.

## Modules

content_generator.py - Calls the OpenAI API to generate a structured JSON blog
template_builder.py - Changes the JSON into a HTML file
main.py - Desktop GUI using customtkinter — form, color picker, and generation history |
index.py - Flask app — form UI, live preview, and endpoint, deployable to Vercel |

**Dependencies:** OpenAI, python-dotenv, customtkinter, flask

For AI use, I have used it to assist me in my journey of learning how to use HTML, the module CustomTkinter, and even used it to push my code into github.
