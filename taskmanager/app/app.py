#!/usr/bin/python3
import os
import redis
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# postgresql connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URI',
        'postgresql://taskuser:taskpass@db:5432/taskdb'
)

db = SQLAlchemy(app)

# Redis connection
cache = redis.Redis(
        host=os.getenv('REDIS_HOST', 'redis'),
        port=6379,
        decode_responses=True
)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

@app.route('/')
def home():
    return jsonify({"message": "Task Manager API is running"})

@app.route('/tasks')
def get_tasks():
    cached = cache.get('tasks')
    if cached:
        return jsonify({"source": "cache", "tasks": cached})
    tasks = Task.query.all()
    result = [{"id": t.id, "title": t.title, "done": t.done} for t in tasks]

    cache.setex('tasks', 30, str(result))
    return jsonify({"source": "database", "tasks": result})

@app.route('/tasks/seed')
def seed():
    with app.app_context():
        db.create_all() 
        if Task.query.count() == 0:
            sample = [Task(title="Buy groceries"), Task(title="Write Dockerfile"), Task(title="Learn Docker")]
            db.session.add_all(sample)
            db.session.commit()
    return jsonify({"message": "Database seeded!"})

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)


