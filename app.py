from flask import Flask, jsonify
from flask_cors import CORS

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/page', methods=['GET'])
def page():
    return jsonify('Hello axios request!')

if __name__ == '__main__':
    app.run()