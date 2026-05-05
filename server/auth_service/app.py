from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'change_me_in_production')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # CSRF protection

jwt = JWTManager(app)

_cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, supports_credentials=True, origins=_cors_origins)

@app.route('/', methods=['GET'])
def index():
    return ""

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # Compare against environment-configured credentials
    admin_user = os.environ.get('ADMIN_USERNAME', '')
    admin_pass = os.environ.get('ADMIN_PASSWORD', '')
    if username == admin_user and password == admin_pass:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Credenciales incorrectas"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)