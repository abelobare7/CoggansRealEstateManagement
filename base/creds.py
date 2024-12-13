import base64
import requests
import json


consumer_key = "v3kNfWPVjnMuDBL8IOP4AtfuRWQMnHHy"
consumer_secret = "CmJ1gvkv2BWaojvr"

# Encode the consumer key and secret in base64
encoded = base64.b64encode((consumer_key + ":" + consumer_secret).encode())

# Set the API endpoint URL and headers
url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
headers = {
    "Authorization": "Basic " + encoded.decode(),
    "Content-Type": "application/json"
}

# Send a GET request to obtain the access token
response = requests.get(url, headers=headers)

# Extract the access token from the response
if response.status_code == 200:
    token = json.loads(response.text)["access_token"]
    print("Access token:", token)
else:
    print("Failed to obtain access token")
