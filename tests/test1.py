import requests

# Define the URL and payload
url = "http://127.0.0.1:5000/generate_questions"
payload = {"content": "The Eiffel Tower is located in Paris, France."}

# Make a POST request
response = requests.post(url, json=payload)

# Print the response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
