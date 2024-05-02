import requests

# Specify the URL of the Flask API endpoint
url = 'http://127.0.0.1:5001/upload_manual'

# Path to the file you want to upload
# file_path = 'fan manual.pdf'
file_path = 'Treadclimber manual.pdf'

# Create a dictionary containing the file to be uploaded
files = {'file': open(file_path, 'rb')}

# Send a POST request to the API endpoint with the file attached
response = requests.post(url, files=files)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    try:
        # Try to parse the response as JSON
        json_response = response.json()
        print(json_response)
    except ValueError:
        # If parsing fails, print the raw response content
        print("Response is not in JSON format:")
        print(response.content)
else:
    # Print an error message if the request was not successful
    print("Request failed with status code:", response.status_code)
