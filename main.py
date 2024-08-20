from flask import Flask, send_file, jsonify, redirect, make_response, request, render_template_string
import os
import random
import string
from faker import Faker
from flask import request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from io import BytesIO

app = Flask(__name__)
faker = Faker()

# Replace with your actual service account JSON credentials
service_account_info = {
  "type": "service_account",
  "project_id": "quickstart-1576936051869",
  "private_key_id": "3179ab060389bc7f57dcbe62508c08f1c6c2e30e",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDLcPU8PLYHj8BM\nU8KJ9/vdUVZjfuOYYyijnnL+v0bVInykuABzqNdHuiQfJc4kx5xT4YJ2bqRlFCGv\ncMQA/bVJ7y0X1njGKPH5XoYpB2ohfEmi5t9YiSof7NmqZyuefHyj3oe4mJlLuADu\npwBZ/SbCM72A1sZsve7aoJW+TTWfT+QR0gWOsAY8Kab9ESygNLLMOP6YzyBs2ege\nmUgq6srDElrnjGEyeKA3xMEdej19nT7jD8BMaQki9PBuddNgkARFfJaFfohqNFz4\nVODOeRJQxljV+rZ2kq0HPohzaivI7dLZhbVfSDkYx9BhcvCcfloHOpGjVlvblzzt\nqRWEIs/HAgMBAAECggEAJtfVav/ofX8b5zbi4PbhNvuNtAeJKxJbswnQyQT6YD1q\ncQTUyUCGgiJvPSc5udoG5hkbkMNFTitO1zF/qvTGBWzOPkvr2WH9+W/ry6+nuucB\nJEJSiJP/4AKX+KokMOlx3tPhNASm2Ec0nlxye7wTB2dbmlrnneGR1lps3N3fDCCc\ntAU6+qVCmsklEVDImF1ZxgdpDDE57aqaboMr3c0pH1ybLJfV8CH378o9GkXLGnOV\nMJbvl5EDYQrYYdjcGvH0sBoX8b02PqWF8sEKfGgWowAbBZD39FR4of0dolJ8QUgi\nFBo7Np8eVI4dNFsYGR1HAamLarFWqyGPFzBuqixn+QKBgQDl5Y1MnIdyzTlHWOB8\neOTG6LoRQFe6Cb1fYa1YbNjWWb7+gbSqnmFcLTvR9To3XIeThash1oWg2WvYrqco\niGkUqdGC4Qbb0q1xtlCAsr1GddA4q+motopuZkZUO/DtsJZMukOf8hEB1mzREi4d\naII1cuz6a+/9pHpz/k27DHoncwKBgQDiimu8u7vAN3CHsKxNMRJ16nftvg8O2LKD\n2JHJoN/+/5R9k+pcVfBvB6WJpqqq5haOc/9S+l3anAU/gcBD8OKsN0LmZCRd2WNu\nbvxPTXT832LC0WDVAxEVZSIHgWN2cXO/5IkHMLugLZ8mdUEskAAme7NPUdEs9ia+\nZ2XfRebZXQKBgFfXUxsPwA1UbutdAUFuK/P4nofS7vItoIceWk6sIFoepoS2aKK8\nq3S979p0ec8HcuIiM9ZVEm/4Q2XirgolvQjhLiV099rsb8tAHxhds0aF446T2U7W\nmKRAPeUXliIr0/HzRb2Kj4cFOETWTnp8ISxtAjFZJrTisMs7QtYSmWYTAoGBANna\no6DsKLHAnsbeb9QLzOT4hjxq+bAdVA7WxdxQiRiAUBwzkr0ZKA6eG+M0FAwlGKwF\ngRQbEQaZ47Ie5PZxQIq82ekVhKN72tLoiFr68fX8HM2c7LHsMRGSIBd3pl7Q2689\n50iy5Lw1I0eomvRvxrU7YER3OeEzFi8k4CLG5ilBAoGBAIQ/LUVZF+VlNU2hSjwh\nehZQ1B50HLAtrepe5KAUpk+SYh54D5eooeJq1aSvA0kNW7r1TR7vbI4ReTVvI11p\n4Jb67ySIhUb/Xp9b/OhW2HEOrZeMyxo4u9w69QYQkTN1qSoByCCVfxAb5eax08cP\nbHd8zXzNKEiBf18bDgap8nSi\n-----END PRIVATE KEY-----\n",
  "client_email": "smtpsfiilin@quickstart-1576936051869.iam.gserviceaccount.com",
  "client_id": "106456735674703070079",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/smtpsfiilin%40quickstart-1576936051869.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


# Authenticate and create a Google Sheets API service instance
credentials = service_account.Credentials.from_service_account_info(service_account_info)
service = build('sheets', 'v4', credentials=credentials)

# Replace with your actual Google Spreadsheet ID
spreadsheet_id = "1X-COXRF4-Us_5lqIVFn2OzbM41fkEBJmAU_BcB9hIfg"
spreadsheet_id_2 = "1Iu5q5p3hqwWoNJvhGUICsIc2Y_UEjZxMwpYCjQpkRNc"
sheet_range = "Sheet1!A1:E1"  # Adjust range if needed



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



def save_to_spreadsheet(data):
    # Prepare the data to be appended
    body = {
        'values': [data]
    }
    # Append the data to the spreadsheet
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=sheet_range,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()


def save_to_spreadsheet_2(data):
    # Prepare the data to be appended
    body = {
        'values': [data]
    }
    # Append the data to the spreadsheet
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id_2,
        range=sheet_range,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()

@app.route('/apiv3/<randomwords>/unsubscribe', methods=['GET', 'POST'])
def unsubscribe(randomwords):
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            user_agent = request.headers.get('User-Agent')
            ip_address = get_real_ip()
            device_type = detect_device(user_agent)

            data = [
                email,
                ip_address,
                user_agent,
                device_type,
                randomwords
            ]
            save_to_spreadsheet(data)

            return {"message": "You have been unsubscribed."}, 200
        else:
            return {"message": "No email provided."}, 400

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

@app.route('/apiv3/<randomwords>', methods=['GET'])
def track_user(randomwords):
    # Get the request details
    user_agent = request.headers.get('User-Agent')
    ip_address = get_real_ip()
    url = request.url
    device_type = detect_device(user_agent)

    # Log the details to the Google Spreadsheet
    data = [
        url,
        ip_address,
        user_agent,
        device_type,
        randomwords
    ]
    save_to_spreadsheet_2(data)

    return {"message": "Success."}, 200
@app.route('/hello/<name>')
def hello_name(name):
    return f"Hello, {name}!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=True)
