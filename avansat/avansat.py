import requests

url = "http://localhost:8069/avansat_api/avansat/create"
headers = {
    "accept": "*/*",
    "Cookie": "session_id=apikey",  # Include the session_id with your API key
}

# Since the data in your cURL command is empty, we pass an empty dictionary
data = {}

try:
    response = requests.post(url, headers=headers, json=data)
    # Check if the request was successful
    if response.status_code == 200:
        print("Request succeeded:", response.json())
    else:
        print("Request failed with status code:", response.status_code)
        print("Response:", response.text)
except requests.exceptions.RequestException as e:
    print("An error occurred:", e)
