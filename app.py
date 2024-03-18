from flask import Flask, request, jsonify
from models.tasks import Task, TaskNotFoundException

app = Flask(__name__)
host = "0.0.0.0"
port = 3000


@app.route("/task", methods=["POST"])
def create_task():
    data = request.get_json()
    new_task = Task.create_task_by_json(**data)
    return jsonify(new_task.to_dict()), 201


@app.route("/task", methods=["GET"])
def get_tasks():
    tasks_response = [task.to_dict() for task in Task.tasks]
    response_data = {
        "tasks": tasks_response,
        "total": len(tasks_response)
    }
    return jsonify(response_data), 200


@app.route("/task/<int:slug>", methods=["GET"])
def get_task_by_id(slug):
    for task in Task.tasks:
        if task.slug == slug:
            return jsonify(task.to_dict()), 200

    return jsonify({"message": f"Not Found Task by slug: {slug}"}), 404


@app.route("/task/<int:slug>", methods=["PUT"])
def update_task(slug):
    data = request.get_json()

    try:
        response_data = Task.update_task_by_json(slug, **data)
    except TaskNotFoundException:
        return jsonify({"message": f"Not Found Task by slug: {slug}"})
    else:
        return jsonify(response_data.to_dict()), 200


@app.route("/task/<int:slug>", methods=["DELETE"])
def delete_task(slug):
    try:
        Task.delete_task_id(slug)
    except TaskNotFoundException:
        return jsonify({"message": f"Not Found Task by slug: {slug}"})
    else:
        return jsonify({"message": f"Deleted with Success!"}), 200


if __name__ == "__main__":
    app.run(debug=True, host=host, port=port)
