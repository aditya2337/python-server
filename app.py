import json
from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'androiditya'
app.config['MONGO_URI'] = 'mongodb://admin1:admin1@ds053206.mlab.com:53206/androiditya'

mongo = PyMongo(app)

@app.route('/')
def index():
    return 'Hello, World'

@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    task = mongo.db.tasks
    output = []
    for t in task.find():
        output.append({'_id': str(t['_id']),'title' : t['title'], 'done' : t['done']})
    return jsonify({'result' : output})


@app.route('/todo/api/v1.0/tasks/<string:task_id>', methods=['GET'])
def get_task(task_id):
    task = mongo.db.tasks
    output = []
    t = task.find_one({"_id" : ObjectId(task_id)})
    if t:
        output = {'title' : t['title'], 'description' : t['description'], 'done' : t['done']}
    else:
        output = 'No such task'
    return jsonify({'task': output})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    data = json.loads(request.data)
    print(data['title'])
    task = mongo.db.tasks
    title = data['title']
    done = data['done']
    task_id = task.insert({
        'title': title,
        'done': done
    })
    new_task = task.find_one({"_id": ObjectId(task_id)})
    output = {'title' : new_task['title'], 'done' : new_task['done']}
    return jsonify({'task': output}), 201

@app.route('/todo/api/v1.0/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    data = json.loads(request.data)
    task = mongo.db.tasks
    output = []
    done = data['done']
    t = task.update_one({"_id" : ObjectId(task_id)}, {
    "$set": {
        "done": done
        }
    })
    for t in task.find():
        output.append({'_id': str(t['_id']),'title' : t['title'], 'done' : t['done']})
    return jsonify({'result' : output})

@app.route('/todo/api/v1.0/tasks/delete/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = mongo.db.tasks
    output = []
    t = task.remove({"_id" : ObjectId(task_id)})
    output = {'status': 'done'}
    return jsonify({'task': output}), 201

if __name__ == '__main__':
    app.run(debug=True)