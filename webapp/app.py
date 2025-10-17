from flask import Flask, jsonify, send_from_directory, request
import json
import random

app = Flask(__name__, static_folder='.')

# Загружаем вопросы
with open('../questions.json', 'r', encoding='utf-8') as f:
    QUESTIONS = json.load(f)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/get-question')
def get_question():
    category = request.args.get('category')
    if category not in QUESTIONS:
        return jsonify({"error": "Категория не найдена"}), 400
    
    question = random.choice(QUESTIONS[category])
    return jsonify({"question": question})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)