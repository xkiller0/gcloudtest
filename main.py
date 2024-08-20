from flask import Flask, send_file, jsonify, redirect, make_response, request, render_template_string
import os
import random
import string
from faker import Faker
from flask import request
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


def detect_device(user_agent):
    # Simple check to identify if the device is a phone or laptop based on user agent string
    if any(device in user_agent.lower() for device in ['iphone', 'android', 'blackberry', 'windows phone']):
        return "Phone"
    else:
        return "Laptop"


def get_real_ip():
    # Get the real IP address from the headers or remote address
    if 'X-Forwarded-For' in request.headers:
        ip = request.headers['X-Forwarded-For'].split(',')[0].strip()
    elif 'X-Real-IP' in request.headers:
        ip = request.headers['X-Real-IP']
    else:
        ip = request.remote_addr
    return ip


@app.route('/apiv3/<randomwords>', methods=['GET'])
def track_user(randomwords):
    # Get the request details
    user_agent = request.headers.get('User-Agent')
    ip_address = get_real_ip()
    url = request.url
    device_type = detect_device(user_agent)

    # Log the details to the file
    with open('all-tracking.txt', 'a') as file:
        file.write(f"URL: {url}\n")
        file.write(f"IP Address: {ip_address}\n")
        file.write(f"User Agent: {user_agent}\n")
        file.write(f"Device Type: {device_type}\n")
        file.write("-" * 50 + "\n")

    return {"message": "Tracking information logged."}, 200


@app.route('/apiv3/<randomwords>/unsubscribe', methods=['GET', 'POST'])
def unsubscribe(randomwords):
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            user_agent = request.headers.get('User-Agent')
            ip_address = get_real_ip()
            device_type = detect_device(user_agent)

            with open('unsubscribe.txt', 'a') as file:
                file.write(f"Email: {email}\n")
                file.write(f"IP Address: {ip_address}\n")
                file.write(f"User Agent: {user_agent}\n")
                file.write(f"Device Type: {device_type}\n")
                file.write(f"Random Words: {randomwords}\n")
                file.write("-" * 50 + "\n")

            return {"message": "You have been unsubscribed."}, 200
        else:
            return {"message": "No email provided."}, 400

    # HTML form to get email address
    unsubscribe_form = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Unsubscribe</title>
    </head>
    <body>
        <h1>Unsubscribe</h1>
        <form action="/apiv3/{{ randomwords }}/unsubscribe" method="post">
            <label for="email">Enter your email to unsubscribe:</label><br><br>
            <input type="email" id="email" name="email" required><br><br>
            <input type="submit" value="Unsubscribe">
        </form>
    </body>
    </html>
    '''
    return render_template_string(unsubscribe_form, randomwords=randomwords)
@app.route('/hello/<name>')
def hello_name(name):
    return f"Hello, {name}!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=True)
