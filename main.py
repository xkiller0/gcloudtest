import base64
import json

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

service_account_info = 'eyJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsICJwcm9qZWN0X2lkIjogInF1aWNrc3RhcnQtMTU3NjkzNjA1MTg2OSIsICJwcml2YXRlX2tleV9pZCI6ICIzMTc5YWIwNjAzODliYzdmNTdkY2JlNjI1MDhjMDhmMWM2YzJlMzBlIiwgInByaXZhdGVfa2V5IjogIi0tLS0tQkVHSU4gUFJJVkFURSBLRVktLS0tLVxuTUlJRXZnSUJBREFOQmdrcWhraUc5dzBCQVFFRkFBU0NCS2d3Z2dTa0FnRUFBb0lCQVFETGNQVThQTFlIajhCTVxuVThLSjkvdmRVVlpqZnVPWVl5aWpubkwrdjBiVklueWt1QUJ6cU5kSHVpUWZKYzRreDV4VDRZSjJicVJsRkNHdlxuY01RQS9iVko3eTBYMW5qR0tQSDVYb1lwQjJvaGZFbWk1dDlZaVNvZjdObXFaeXVlZkh5ajNvZTRtSmxMdUFEdVxucHdCWi9TYkNNNzJBMXNac3ZlN2FvSlcrVFRXZlQrUVIwZ1dPc0FZOEthYjlFU3lnTkxMTU9QNll6eUJzMmVnZVxubVVncTZzckRFbHJuakdFeWVLQTN4TUVkZWoxOW5UN2pEOEJNYVFraTlQQnVkZE5na0FSRmZKYUZmb2hxTkZ6NFxuVk9ET2VSSlF4bGpWK3JaMmtxMEhQb2h6YWl2STdkTFpoYlZmU0RrWXg5QmhjdkNjZmxvSE9wR2pWbHZibHp6dFxucVJXRUlzL0hBZ01CQUFFQ2dnRUFKdGZWYXYvb2ZYOGI1emJpNFBiaE52dU50QWVKS3hKYnN3blF5UVQ2WUQxcVxuY1FUVXlVQ0dnaUp2UFNjNXVkb0c1aGtia01ORlRpdE8xekYvcXZUR0JXek9Qa3ZyMldIOStXL3J5NitudXVjQlxuSkVKU2lKUC80QUtYK0tva01PbHgzdFBoTkFTbTJFYzBubHh5ZTd3VEIyZGJtbHJubmVHUjFscHMzTjNmRENDY1xudEFVNitxVkNtc2tsRVZESW1GMVp4Z2RwRERFNTdhcWFib01yM2MwcEgxeWJMSmZWOENIMzc4bzlHa1hMR25PVlxuTUpidmw1RURZUXJZWWRqY0d2SDBzQm9YOGIwMlBxV0Y4c0VLZkdnV293QWJCWkQzOUZSNG9mMGRvbEo4UVVnaVxuRkJvN05wOGVWSTRkTkZzWUdSMUhBYW1MYXJGV3F5R1BGekJ1cWl4bitRS0JnUURsNVkxTW5JZHl6VGxIV09COFxuZU9URzZMb1JRRmU2Q2IxZllhMVliTmpXV2I3K2diU3FubUZjTFR2UjlUbzNYSWVUaGFzaDFvV2cyV3ZZcnFjb1xuaUdrVXFkR0M0UWJiMHExeHRsQ0FzcjFHZGRBNHErbW90b3B1WmtaVU8vRHRzSlpNdWtPZjhoRUIxbXpSRWk0ZFxuYUlJMWN1ejZhKy85cEhwei9rMjdESG9uY3dLQmdRRGlpbXU4dTd2QU4zQ0hzS3hOTVJKMTZuZnR2ZzhPMkxLRFxuMkpISm9OLysvNVI5aytwY1ZmQnZCNldKcHFxcTVoYU9jLzlTK2wzYW5BVS9nY0JEOE9Lc04wTG1aQ1JkMldOdVxuYnZ4UFRYVDgzMkxDMFdEVkF4RVZaU0lIZ1dOMmNYTy81SWtITUx1Z0xaOG1kVUVza0FBbWU3TlBVZEVzOWlhK1xuWjJYZlJlYlpYUUtCZ0ZmWFV4c1B3QTFVYnV0ZEFVRnVLL1A0bm9mUzd2SXRvSWNlV2s2c0lGb2Vwb1MyYUtLOFxucTNTOTc5cDBlYzhIY3VJaU05WlZFbS80UTJYaXJnb2x2UWpoTGlWMDk5cnNiOHRBSHhoZHMwYUY0NDZUMlU3V1xubUtSQVBlVVhsaUlyMC9IelJiMktqNGNGT0VUV1RucDhJU3h0QWpGWkpyVGlzTXM3UXRZU21XWVRBb0dCQU5uYVxubzZEc0tMSEFuc2JlYjlRTHpPVDRoanhxK2JBZFZBN1d4ZHhRaVJpQVVCd3prcjBaS0E2ZUcrTTBGQXdsR0t3RlxuZ1JRYkVRYVo0N0llNVBaeFFJcTgyZWtWaEtONzJ0TG9pRnI2OGZYOEhNMmM3TEhzTVJHU0lCZDNwbDdRMjY4OVxuNTBpeTVMdzFJMGVvbXZSdnhyVTdZRVIzT2VFekZpOGs0Q0xHNWlsQkFvR0JBSVEvTFVWWkYrVmxOVTJoU2p3aFxuZWhaUTFCNTBITEF0cmVwZTVLQVVwaytTWWg1NEQ1ZW9vZUpxMWFTdkEwa05XN3IxVFI3dmJJNFJlVFZ2STExcFxuNEpiNjd5U0loVWIvWHA5Yi9PaFcySEVPclplTXl4bzR1OXc2OVFZUWtUTjFxU29CeUNDVmZ4QWI1ZWF4MDhjUFxuYkhkOHpYek5LRWlCZjE4YkRnYXA4blNpXG4tLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tXG4iLCAiY2xpZW50X2VtYWlsIjogInNtdHBzZmlpbGluQHF1aWNrc3RhcnQtMTU3NjkzNjA1MTg2OS5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsICJjbGllbnRfaWQiOiAiMTA2NDU2NzM1Njc0NzAzMDcwMDc5IiwgImF1dGhfdXJpIjogImh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi9hdXRoIiwgInRva2VuX3VyaSI6ICJodHRwczovL29hdXRoMi5nb29nbGVhcGlzLmNvbS90b2tlbiIsICJhdXRoX3Byb3ZpZGVyX3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vb2F1dGgyL3YxL2NlcnRzIiwgImNsaWVudF94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL3JvYm90L3YxL21ldGFkYXRhL3g1MDkvc210cHNmaWlsaW4lNDBxdWlja3N0YXJ0LTE1NzY5MzYwNTE4NjkuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCAidW5pdmVyc2VfZG9tYWluIjogImdvb2dsZWFwaXMuY29tIn0='


decoded_json_str = base64.b64decode(service_account_info).decode('utf-8')

# Convert the JSON string back to a dictionary
decoded_service_account_info = json.loads(decoded_json_str)

# Authenticate and create a Google Sheets API service instance
credentials = service_account.Credentials.from_service_account_info(decoded_service_account_info)
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
