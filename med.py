@app.route('/image/<path:random_characters>', methods=['GET'])
def show_image_nometadata_pixle(random_characters):
    try:
        cip = checkifproxy(get_real_ip())
        if cip:
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
            file_name = f"tracking_data_open/1px_{unix_time}.json"
            save_to_gcs(tracking_data_json_open, file_name)
            # Path to the image file
            file_path = f'static/1px.png'

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