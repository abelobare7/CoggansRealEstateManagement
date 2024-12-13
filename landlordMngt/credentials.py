# from datetime import datetime
# import requests
# import base64
# import json


# # authorisation to access allowed APIs
# class c2bCredentials:
#     consumer_key = 'BNVogZJHhMQ4S3XHPveZGAqNwxDdVeoG'
#     consumer_secret = '1WOPKIVCkTcXS2j6'
#     api_endpoint_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'


# # acquire access token for use in all API calls.
# class AccessToken:
#     requestToken = requests.get(c2bCredentials.api_endpoint_url,
#                                 auth=(c2bCredentials.consumer_key, c2bCredentials.consumer_secret))
#     token = json.loads(requestToken.text)
#     validToken = token['access_token']



# # Generate password Used to encrypt requests sent while using  MPESA Express.
# class Password:
#     timeStamp = datetime.now().strftime('%Y%m%d%H%M%S')
#     shortCode = '174379'
#     passKey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

#     dataToEncode = shortCode + passKey + timeStamp
#     onlinePassword = base64.b64encode(dataToEncode.encode())
#     decodedPassword = onlinePassword.decode('utf-8')
