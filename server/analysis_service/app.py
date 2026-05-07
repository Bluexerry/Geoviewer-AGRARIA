from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
_cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, supports_credentials=True, origins=_cors_origins)

@app.route('/', methods=['GET'])
def index():
    return ""

@app.route('/analyze', methods=['POST'])
def analyze_data():
    data = request.json
    df = pd.DataFrame(data)
    result = df.describe()
    return jsonify(result.to_dict()), 200

if __name__ == '__main__':
    app.run(port=5003)
