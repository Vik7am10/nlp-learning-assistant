import requests

# Test generate_questions endpoint
url_questions = "http://127.0.0.1:5000/generate_questions"
payload_questions = {"content": "The Eiffel Tower is located in Paris, France."}
response_questions = requests.post(url_questions, json=payload_questions)
print("Generate Questions Response:", response_questions.json())

# Test summarize endpoint
url_summarize = "http://127.0.0.1:5000/summarize"
payload_summarize = {
    "content": "The Eiffel Tower is located in Paris, France, and attracts millions of tourists every year due to its cultural significance."
}
response_summarize = requests.post(url_summarize, json=payload_summarize)
print("Summarize Response:", response_summarize.json())

# Test view_requests endpoint
url_view = "http://127.0.0.1:5000/view_requests"
response_view = requests.get(url_view)
print("View Requests Response:", response_view.json())
