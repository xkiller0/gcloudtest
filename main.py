from flask import Flask, send_file, jsonify, redirect, make_response, request
import os
import random
import string
from faker import Faker
from io import BytesIO

app = Flask(__name__)
faker = Faker()


@app.route('/api/<random_characters>', methods=['GET'])
def show_image_nometadata(random_characters):
    # Path to the image file
    file_path = 'static/trump-w-gold.png'

    # Check if the file exists
    if not os.path.exists(file_path):
        return jsonify({'error': 'Image not found'}), 404

    # Generate random metadata
    random_title = faker.sentence()
    random_description = faker.paragraph()
    random_keywords = ", ".join(faker.words(5))  # 5 random keywords

    # Read the image file
    with open(file_path, 'rb') as img_file:
        img_data = img_file.read()

    # Generate random cookies
    random_cookie1 = faker.word()
    random_cookie2 = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # Create the response
    response = make_response(img_data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['X-Image-Title'] = random_title
    response.headers['X-Image-Description'] = random_description
    response.headers['X-Image-Keywords'] = random_keywords

    # Set cookies with random values
    response.set_cookie('__cf_bm_' + ''.join(random.choices(string.ascii_letters, k=3)), random_cookie1,
                        max_age=60 * 60)
    response.set_cookie('_umsid_' + ''.join(random.choices(string.ascii_letters, k=4)), random_cookie2, max_age=60 * 60)

    return response


@app.route('/apiv2/<random_characters>', methods=['GET'])
def redirect_url(random_characters):
    # Define the target URL
    target_url = 'https://www.google.com'

    # Generate a large block of Lorem Ipsum text
    lorem_ipsum = faker.paragraphs(30)
    lorem_ipsum_small = faker.name_male()

    # HTML content with hidden Lorem Ipsum in the body, and also in the title
    html_content = f"""
    <html>
    <head>
        <meta http-equiv="refresh" content="0;url={target_url}">
        <title>{lorem_ipsum_small} - {random_characters}</title>
        <style>
            .hidden-text {{
                visibility: hidden;
                height: 0;
                width: 0;
                overflow: hidden;
            }}
        </style>
    </head>
    <body>
        <div class="hidden-text">{''.join(lorem_ipsum)}</div>
    </body>
    </html>
    """

    response = make_response(html_content)
    response.headers['Content-Type'] = 'text/html'

    return response


@app.route('/hello/<name>')
def hello_name(name):
    return f"Hello, {name}!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=True)
