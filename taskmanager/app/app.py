#!/usr/bin/python3

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Task Manager API is running"})

@app.route('/tasks')
def tasks():
    return jsonify({"tasks": ["Buy groceries", "Write Dockerfile", "Learn Docker"]})

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
