import requests
staff_access_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMjg4NzU2LCJpYXQiOjE3NTEwODUxMDIsImp0aSI6IjJmMDIzOWNkYjRmNDQwMDA4NTRmNTc5ZDNhNjA4MDEyIiwidXNlcl9pZCI6OX0.4Z_Ux63kGZNn_41knzYJ4wpQU95GVMB14DSarL6JX1Q'
user_access_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxNDQyMDEyLCJpYXQiOjE3NTEzNTU2MTIsImp0aSI6IjA0ZjQ2MTE0ODM0MzQwMjBiYjZhZmJkNzg3YTVjOTk1IiwidXNlcl9pZCI6N30.fV7BTo5EHYJ4jEdA76tqJdl8qplPKFN3cbnZWd6uCYA'
url="http://127.0.0.1:8000/orders/get_cart/"


headers={
    "Authorization":f"Bearer {user_access_token}"
}
response = requests.get(url,headers=headers)
print(response.json())
# # data={
# #     'user':1,
# #     'payment_mode':"online",
# #     'items':[
# #         {"product":1,"quantity":1},
# #         # {"product":2,"quantity":1}
# #     ]
# # }
# data={
#     'quantity':3
# }
# response=requests.post(url,json=data,headers=headers)
# print(response.json())

# response=requests.delete(url,headers=headers)
# print(response.json())