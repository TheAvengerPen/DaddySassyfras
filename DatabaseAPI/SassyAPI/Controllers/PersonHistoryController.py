from flask import request, jsonify, Blueprint
from fns import PersonHistoryFns

app_person_history = Blueprint("app_person_history", __name__)


@app_person_history.route("/get-history-item/<history_id>", methods=["GET"])
def get_history_item(history_id):
    output = PersonHistoryFns.get_history_item(history_id)

    if output == -1:
        return "Error running SQL. Please see logs.", 400

    if len(output) == 0:
        return "", 204

    return jsonify(output), 200


@app_person_history.route("/get-histories", methods=["GET"])
def get_histories():
    output = PersonHistoryFns.get_all_histories()

    if output == -1:
        return "Error running SQL. Please see logs.", 400

    if len(output) == 0:
        return "", 204

    return jsonify(output), 200


@app_person_history.route("/get-person-history/<person_id>", methods=["GET"])
def get_person_history(person_id):
    output = PersonHistoryFns.get_person_history_items(person_id)

    if output == -1:
        return "Error running SQL. Please see logs.", 400

    if len(output) == 0:
        return "", 204

    return jsonify(output), 200


@app_person_history.route("/get-command-history/<command_id>", methods=["GET"])
def get_command_history_item(command_id):
    output = PersonHistoryFns.get_command_history_items(command_id)

    if output == -1:
        return "Error running SQL. Please see logs.", 400

    if len(output) == 0:
        return "", 204

    return jsonify(output), 200


@app_person_history.route("/get-response-history/<response_id>", methods=["GET"])
def get_response_history_item(response_id):
    output = PersonHistoryFns.get_response_history_items(response_id)

    if output == -1:
        return "Error running SQL. Please see logs.", 400

    if len(output) == 0:
        return "", 204

    return jsonify(output), 200


@app_person_history.route("/create-history-item", methods=["POST"])
def create_history_item():
    data = request.get_json()

    try:
        output = PersonHistoryFns.create_history_item(data["PersonID"], data["CommandID"], data["ResponseID"])
    except:
        return jsonify("Bad Request"), 400

    if output == -1:
        return jsonify("Error running SQL. Please see logs."), 400

    output = PersonHistoryFns.get_history_item(output)

    if output == -1:
        return "Error running SQL. Please see logs.", 400

    if len(output) == 0:
        return "Command not found", 404

    return jsonify(output), 201
