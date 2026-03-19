import requests

res = requests.post(
    "http://127.0.0.1:5000/generate",
    json={"product_info": "Eco-friendly water bottle with BPA-free material"}
)
print(res.json())