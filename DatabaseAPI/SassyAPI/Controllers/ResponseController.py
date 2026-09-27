from flask import request, jsonify, Blueprint
from fns import ResponseFns

app_responses = Blueprint("app_responses", __name__)


@app_responses.route("/get-responses", methods=["GET"])
def get_responses():
    output = ResponseFns.get_responses()

    if output == -1:
        return "Error running SQL. Please see logs."

    if len(output) == 0:
        return "", 204

    return jsonify(output), 200


@app_responses.route("/get-command-responses/<command_id>", methods=["GET"])
def get_command_responses(command_id):
    output = ResponseFns.get_command_responses(command_id)

    if output == -1:
        return "Error running SQL. Please see logs."

    if len(output) == 0:
        return "", 204

    return jsonify(output)


@app_responses.route("/create-response", methods=["POST"])
def create_response():
    data = request.get_json()
    new_id = ResponseFns.create_response(data["ResponseText"], data["CommandID"], data["ResponseProbability"])

    if new_id == -1:
        return jsonify("Failed to add response"), 400

    output = ResponseFns.get_response(new_id)

    if output == -1:
        return "Error running SQL. Please see logs", 400

    if len(output) == 0:
        return "Response not created", 404

    return jsonify(output), 201


@app_responses.route("/update-response", methods=["PUT"])
def update_response():
    data = request.get_json()
    output = ResponseFns.update_response(data["ResponseID"], data["ResponseText"],
                                         data["CommandID"], data["ResponseProbability"])

    if output == -1:
        return jsonify("Failed to update response. See logs for details.")

    output = ResponseFns.get_response(output)

    if output == -1:
        return "Error running SQL. Please see logs", 400

    if len(output) == 0:
        return "Response not found", 404

    return jsonify(output), 201


@app_responses.route("/delete-response/<response_id>", methods=["DELETE"])
def delete_response(response_id):
    output = ResponseFns.delete_response(response_id)

    if output == -1:
        return "Error running SQL. Please see logs.", 400

    if output == 0:
        return "Failed to delete response. Record not found.", 404

    return "Response deleted successfully.", 201
