from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from transformers import T5Tokenizer, T5ForConditionalGeneration, pipeline

# Initialize Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nlp_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the UserRequest model
class UserRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_text = db.Column(db.Text, nullable=False)
    result = db.Column(db.Text, nullable=False)
    task = db.Column(db.String(50), nullable=False)  # Task: 'generate_questions' or 'summarize'
    timestamp = db.Column(db.DateTime, default=db.func.now())

# Create database tables
with app.app_context():
    db.create_all()

# Initialize models and pipelines
model_name = "mrm8488/t5-base-finetuned-question-generation-ap"  # Fine-tuned for question generation
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate_questions", methods=["POST"])
def generate_questions():
    content = request.json.get("content")
    if not content:
        return jsonify({"error": "No content provided"}), 400

    # Generate question
    inputs = tokenizer.encode("context: " + content + " question:", return_tensors="pt")
    outputs = model.generate(inputs, max_length=64, do_sample=True, top_k=50, top_p=0.95, temperature=0.7)
    question = tokenizer.decode(outputs[0], skip_special_tokens=True).replace("question: ", "").strip()

    # Save to database
    user_request = UserRequest(input_text=content, result=question, task="generate_questions")
    db.session.add(user_request)
    db.session.commit()

    return jsonify({"question": question})


@app.route("/summarize", methods=["POST"])
def summarize():
    content = request.json.get("content")
    if not content:
        return jsonify({"error": "No content provided"}), 400

    # Generate summary
    summary = summarizer(content, max_length=150, min_length=40, do_sample=False)[0]['summary_text']

    # Save to database
    user_request = UserRequest(input_text=content, result=summary, task="summarize")
    db.session.add(user_request)
    db.session.commit()

    return jsonify({"summary": summary})

@app.route("/answer_question", methods=["POST"])
def answer_question():
    data = request.json
    question = data.get("question")
    context = data.get("context")
    
    if not question or not context:
        return jsonify({"error": "Both 'question' and 'context' are required."}), 400

    # Use the QA pipeline to get an answer
    result = qa_pipeline(question=question, context=context)
    return jsonify({"answer": result['answer'], "confidence": result['score']})


@app.route("/view_requests", methods=["GET"])
def view_requests():
    all_requests = UserRequest.query.all()
    results = [
        {
            "id": req.id,
            "input_text": req.input_text,
            "result": req.result,
            "task": req.task,
            "timestamp": req.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for req in all_requests
    ]
    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
