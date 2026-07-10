#Create a program which generates a blog template in HTML format. The template should include a title, a heading, an image, and a paragraph of text. The image should be displayed on the left side of the paragraph, and the paragraph should wrap around the image. The template should also have a background color and text color that can be customized.
#Use an api-key which will generate specific template based on what you need and it will talk you through how to use it

def questions():
    print("Welcome to the Blog Template Creator!")
    user_need = input("What type of blog template do you need? (e.g., travel, food, tech): ")
    background_color = input("Enter the background color (e.g., #ffffff for white): ")
    text_color = input("Enter the text color (e.g., #000000 for black): ")
    return user_need, background_color, text_color

def generate_template(user_need, background_color, text_color):
    if user_need.lower() == "travel":
        # Travel blog needs more images and a more detailed description of the destinations. It should also include a section for travel tips and recommendations.
        title = "Travel Blog"
        heading = "Exploring the World"
        paragraph = "Join me as I explore the most beautiful destinations around the globe. From bustling cities to serene landscapes, I'll share my experiences and tips for fellow travelers."
    elif user_need.lower() == "food":
        # Food blog needs more images and a more detailed description of the food and recipes. It should also include a section for restaurant reviews and cooking tips.
        title = "Food Blog"
        heading = "Delicious Recipes and Culinary Adventures"
        paragraph = "Discover mouth-watering recipes and culinary adventures from around the world. I'll share my favorite dishes, cooking tips, and restaurant reviews."
    elif user_need.lower() == "tech":
        # More updated with text and images but also needs a section to include news articles.
        title = "Tech Blog"
        heading = "Latest Tech Trends and Innovations"
        paragraph = "Stay updated with the latest tech trends and innovations. I'll cover everything from gadgets and software to industry news and insights."
    else:
        title = "My Blog"
        heading = "Welcome to My Blog"
        paragraph = "This is a place where I share my thoughts, experiences, and insights on various topics. Stay tuned for interesting content!"

file_name = "template.html"
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
