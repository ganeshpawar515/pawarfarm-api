import requests

staff_access_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMTcxNTQxLCJpYXQiOjE3NTEwODUxMDIsImp0aSI6ImRhOTQ3Y2RjOWZiODQyM2ZiOTU1MmYzYmIyODg0MzgyIiwidXNlcl9pZCI6OX0.jFvHD0rRQmakAn9R0P4XAnkfCznMajC0eL5JaACQpIg'
user_access_token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUxMTcxNzMxLCJpYXQiOjE3NTEwODUzMDUsImp0aSI6IjdiOGU0MjE1N2YyZDQ4ODBiMGZkMGJlNWQ0YzUyZjQ1IiwidXNlcl9pZCI6Nn0.RN5LPGIfjPYtNoCPhKhzlMf6tH4ODZsLVS7ZIaecmEo'

# url="http://127.0.0.1:8000/products/create/"

headers={
    "Authorization":f"Bearer {staff_access_token}"
}


# data = {
#     'name':'1 liter cow milk',
#     'price':60,
#     'category':'milk',
#     'delivery_time':1
# }
# files = {
#     'image': open("C:/Users/GANESH/Desktop/G.Pawar/Django/temp/Images/milk1L.jpeg", 'rb')
# }

# response = requests.post(url,headers=headers,data=data,files=files)
# print(response.json())

url="http://127.0.0.1:8000/products/get/"

response=requests.get(url)

print(response.json())

# p_id=2

# url=f"http://127.0.0.1:8000/products/detail/{p_id}/"

# response=requests.get(url)

# print(response.json())

# p_id=1

# url=f"http://127.0.0.1:8000/products/update/{p_id}/"

# data={
#     'name':'Eggs Pack of 12',
#     'price':120,
# }
# response=requests.patch(url,data=data,headers=headers)

# print(response.json())

# p_category="milk"

# url=f"http://127.0.0.1:8000/products/get_by_category/{p_category}/"

# response=requests.get(url)

# print(response.json())


# p_id=2

# url=f"http://127.0.0.1:8000/products/delete/{p_id}/"

# response=requests.delete(url,headers=headers)

# print(response.json())