from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
import os
import psycopg2

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'change_me_in_production')
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

jwt = JWTManager(app)

_cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, supports_credentials=True, origins=_cors_origins)

_db_params = {
    'dbname': os.environ.get('DB_NAME', 'tepro'),
    'user': os.environ.get('DB_USER', 'postgres'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'host': os.environ.get('DB_HOST', 'localhost'),
    'port': os.environ.get('DB_PORT', '5432'),
}

@app.route('/', methods=['GET'])
def index():
    return ""

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    admin_user = os.environ.get('ADMIN_USERNAME', '')
    admin_pass = os.environ.get('ADMIN_PASSWORD', '')
    if username == admin_user and password == admin_pass:
        access_token = create_access_token(identity=username)
        # Return format expected by frontend: message[0]=userId, message[1]=token
        return jsonify(message=[1, access_token]), 200
    return jsonify({"msg": "Credenciales incorrectas"}), 401

@app.route('/users/<int:user_id>/parcels', methods=['GET'])
def get_user_parcels(user_id):
    try:
        conn = psycopg2.connect(**_db_params)
        cur = conn.cursor()
        cur.execute(
            "SELECT catastral_ref, geojson_data FROM parcelas WHERE user_id = %s",
            (user_id,)
        )
        rows = cur.fetchall()
        parcels = [{'catastral_ref': r[0], 'geojson_data': r[1]} for r in rows]
        return jsonify(parcels), 200
    except Exception:
        return jsonify([]), 200
    finally:
        try:
            cur.close()
            conn.close()
        except Exception:
            pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
