# app.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, User, TextData
from utils import analyze_sentiment  # Import analyze_sentiment function
import config

app = Flask(__name__)
app.config.from_object(config.Config)
db.init_app(app)

# Create all database tables before the first request
with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"msg": "User already exists"}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    if user is None or not user.check_password(password):
        return jsonify({"msg": "Bad credentials"}), 401

    return jsonify({"msg": "Login successful"}), 200

@app.route('/upload-text', methods=['POST'])
def upload_text():
    data = request.get_json()
    user_id = data.get('user_id')  # Assuming you have user authentication and obtain user_id from token or session
    content = data.get('content')

    # Validate user_id if needed
    if not user_id:
        return jsonify({"msg": "User not authenticated"}), 401

    # Perform sentiment analysis using TextBlob
    sentiment = analyze_sentiment(content)

    # Create a new TextData object with sentiment analysis result
    new_text_data = TextData(user_id=user_id, content=content, sentiment=sentiment)
    db.session.add(new_text_data)
    db.session.commit()

    return jsonify({"msg": "Text data uploaded successfully", "sentiment": sentiment}), 201

@app.route('/text-data', methods=['GET'])
def get_all_text_data():
    # Retrieve all text data with user information
    text_data = TextData.query.all()
    text_data_list = []
    for data in text_data:
        text_data_list.append({
            'id': data.id,
            'user_id': data.user_id,
            'username': User.query.get(data.user_id).username,
            'content': data.content,
            'sentiment': data.sentiment,
            'timestamp': data.timestamp
        })
    return jsonify({"text_data": text_data_list}), 200

@app.route('/text-data/<int:user_id>', methods=['GET'])
def get_user_text_data(user_id):
    # Retrieve all text data uploaded by a specific user
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    text_data = TextData.query.filter_by(user_id=user_id).all()
    text_data_list = []
    for data in text_data:
        text_data_list.append({
            'id': data.id,
            'user_id': data.user_id,
            'content': data.content,
            'sentiment': data.sentiment,
            'timestamp': data.timestamp
        })
    return jsonify({"user_text_data": text_data_list}), 200

@app.route('/protected', methods=['GET'])
def protected():
    # Example of a protected endpoint
    return jsonify({"msg": "Access granted"}), 200

if __name__ == '__main__':
    app.run()
