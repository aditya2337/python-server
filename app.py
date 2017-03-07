from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from bson.objectid import ObjectId
from flask_pymongo import PyMongo

app = Flask(__name__)

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
        output.append({'title' : t['title'], 'description' : t['description'], 'done' : t['done']})
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
    if not request.form or not 'title' in request.form:
        abort(400)
    task = mongo.db.tasks
    title = request.form['title']
    description = request.form['description']
    done = request.form['done']
    task_id = task.insert({
        'title': title,
        'description': description,
        'done': done
    })
    new_task = task.find_one({"_id": ObjectId(task_id)})
    output = {'title' : new_task['title'], 'description' : new_task['description'], 'done' : new_task['done']}
    return jsonify({'task': output}), 201

@app.route('/todo/api/v1.0/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    if not request.form or not 'title' in request.form:
        abort(400)
    print request.form
    task = mongo.db.tasks
    output = []
    title = request.form['title']
    description = request.form['description']
    done = request.form['done']
    t = task.update_one({"_id" : ObjectId(task_id)}, {
    "$set": {
        "title": title,
        "description": description,
        "done": done
        }
    })
    new_task = task.find_one({"_id": ObjectId(task_id)})
    output = {'title' : new_task['title'], 'description' : new_task['description'], 'done' : new_task['done']}
    return jsonify({'task': output}), 201

@app.route('/todo/api/v1.0/tasks/delete/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = mongo.db.tasks
    output = []
    t = task.remove({"_id" : ObjectId(task_id)})
    output = {'status': 'done'}
    return jsonify({'task': output}), 201

if __name__ == '__main__':
    app.run(debug=True)
