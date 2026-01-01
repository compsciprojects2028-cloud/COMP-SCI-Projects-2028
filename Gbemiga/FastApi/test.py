import requests
payload = {"title":"Deep Work","author":"Cal Newport","year":"2008"}
site= "http://127.0.0.1:8000/books"
#htp:// must be specifieds
response = requests.post(url=site, json=payload)
print(response.status_code, "code", response.text, "text")
# response2 = requests.get(url = "https://google-mrwa.onrender.com/hello") 
# print(response2.text, response2.status_code)