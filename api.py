import requests
access_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMDA2ODQyLCJpYXQiOjE3NTA5MTg4NTMsImp0aSI6IjYwN2NhOGYyNGJjNzQ5MGM4YzQxYjUyNWU1ZWE3NWY3IiwidXNlcl9pZCI6N30.G4SWluNlLoK96AWhibo0u8WnV4JsDRTuR8D1F0_6RB8'
# url="http://127.0.0.1:8000/api/token"
# data={
#     "username":"win",
#     "password":"window"
# }
# response = requests.post(url,data)
# tokens = response.json()
# print(tokens)

headers={
    'Authorization':f'Bearer {access_token}'
}

#@Create User
# data={
#     "username":"ganesh",
#     "password":"@Ganesh123",
#     "phone_number":"",
#     "email":"ganeshp.py07@gmail.com",
#     "address":"new pune"

# }

# url="http://127.0.0.1:8000/user/create/"
# response=requests.post(url,json=data)
# print(response.json())

#@Get Otp For Email verification
# url="http://127.0.0.1:8000/user/verify_email/"
# response=requests.post(url,headers=headers)
# print(response.json())

#@Submit Otp for email verification
data={
    "otp":8987
}
url="http://127.0.0.1:8000/user/verify_email_otp/"
response=requests.post(url,headers=headers,data=data)
print(response.json())