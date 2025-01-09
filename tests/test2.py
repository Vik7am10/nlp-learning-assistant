import requests
# Summarization Test
url = "http://127.0.0.1:5000/summarize"
payload = {"content": "The Eiffel Tower is one of the most famous landmarks in the world. It is located in Paris, France, and attracts millions of tourists every year."}

response = requests.post(url, json=payload)

print("Summarization Status Code:", response.status_code)
print("Response JSON:", response.json())
