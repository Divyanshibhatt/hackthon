import requests

res = requests.post("http://127.0.0.1:5000/optimize", json={
    "product_info": "Eco-friendly water bottle with BPA-free material",
    "generated_content": {
        "linkedin": "Eco bottle post",
        "blog": "Blog content",
        "twitter": "Tweet",
        "email": "Email content"
    }
})

print(res.json())