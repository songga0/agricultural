from flask import Flask, request, jsonify
import cv2
import numpy as np
from sklearn.preprocessing import LabelEncoder
import json
import tensorflow as tf
import jwt
import datetime
from functools import wraps

def load_model_and_labels():
    # 모델 불러오기
    model = tf.keras.models.load_model("model.h5")

    # JSON 파일에서 레이블 정보 로드
    with open("dataset.json", 'r') as f:
        data = json.load(f)
        labels = [entry["class_label"] for entry in data]

    # LabelEncoder 생성 및 학습 데이터에 적용
    label_encoder = LabelEncoder()
    label_encoder.fit(labels)

    return model, label_encoder

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'

    # API 키를 저장할 딕셔너리
    api_keys = {
        "your_api_key": "client_id_1",
        # 다른 API 키들 추가
    }

    model, label_encoder = load_model_and_labels()

    def validate_api_key(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            api_key = request.headers.get('Authorization')
            if api_key not in api_keys:
                return jsonify({"error": "Invalid API key"}), 401
            return func(*args, **kwargs)
        return wrapper

    def validate_token(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization').split(' ')[-1] if 'Authorization' in request.headers else None
            if not is_valid_token(token):
                return jsonify({"error": "Invalid token"}), 401
            return func(*args, **kwargs)
        return wrapper

    def is_valid_token(token):
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    def check_roles(token, roles=[]):
        try:
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_roles = decoded_token.get('roles', [])
            return any(role in user_roles for role in roles)
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    @app.route('/predict', methods=['POST'])
    @validate_api_key
    @validate_token
    def predict():
        try:
            uploaded_file = request.files['file']
            max_file_size = 2 * 1024 * 1024  # 2 MB
            if uploaded_file and len(uploaded_file.read()) <= max_file_size:
                image = preprocess_image(uploaded_file)
                predictions = model.predict(image)
                predicted_label = label_encoder.inverse_transform(np.argmax(predictions, axis=1))[0]
                return jsonify({"predicted_label": predicted_label}), 200
            else:
                return jsonify({"error": "Invalid file or file size exceeded"}), 400
        except Exception as e:
            app.logger.error(f"Unexpected error: {e}")
            return jsonify({"error": "Internal Server Error"}), 500

    @app.route('/protected', methods=['GET'])
    @validate_token
    def protected():
        token = request.headers.get('Authorization').split(' ')[-1] if 'Authorization' in request.headers else None
        try:
            if not check_roles(token, roles=['admin']):
                return jsonify({"error": "Insufficient privileges"}), 403
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            username = decoded_token['username']
            return jsonify({'message': f'Hello, {username}! This is a protected resource.'}), 200
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

    @app.route('/login', methods=['POST'])
    def login():
        user = {'username': 'example_user', 'password': 'example_password', 'roles': ['admin']}
        if request.json and request.json.get('username') == user['username'] and request.json.get('password') == user['password']:
            expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            token = jwt.encode({'username': user['username'], 'roles': user['roles'], 'exp': expiration},
                               app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token': token.decode('utf-8')}), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401

    @app.route('/')
    def index():
        return "Welcome to the API endpoint!"

    @app.route('/favicon.ico')
    def favicon():
        return "Favicon endpoint"

    @app.errorhandler(404)
    def page_not_found(e):
        return "404 Not Found", 404

    return app

def preprocess_image(uploaded_file):
    image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (64, 64))
    image = image / 255.0
    return np.expand_dims(image, axis=0)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
