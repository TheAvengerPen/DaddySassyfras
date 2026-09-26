from flask import request, jsonify, Blueprint
from fns import CommandFns

app_commands = Blueprint("app_commands", __name__)


@app_commands.route("/get-command/<command_id>")
def get_command(command_id):
    output = CommandFns.get_command(command_id)

    if output == -1:
        return "Error running SQL. Please see logs", 400

    if len(output) == 0:
        return "Command not found", 404

    return jsonify(output), 200


@app_commands.route("/create_command", methods=["POST"])
def create_command():
    data = request.get_json()

    new_id = CommandFns.create_new_command(data["CommandName"], data["CommandTypeID"], data["CommandDescription"], data["ProbabilityActivate"])

    if new_id == -1:
        return jsonify("Failed to add command"), 400

    output = CommandFns.get_command(new_id)

    if output == -1:
        return "Error running SQL. Please see logs", 400

    if len(output) == 0:
        return "Command not found", 404

    return jsonify(output), 200


@app_commands.route("/update_command", methods=["PUT"])
def create_user():
    data = request.get_json()

    new_id = CommandFns.update_command_info(data["CommandID"], data["CommandName"], data["CommandTypeID"], data["CommandDescription"], data["ProbabilityActivate"])

    if new_id == -1:
        return jsonify("Failed to update command"), 400

    output = CommandFns.get_command(data["CommandID"])

    if output == -1:
        return "Error running SQL. Please see logs", 400

    if len(output) == 0:
        return "Command not found", 404

    return jsonify(output), 200


@app_commands.route("/get_commands", methods=["GET"])
def get_all_commands():
    output = CommandFns.get_all_commands()

    if output == -1:
        return "Error running SQL. Please see logs", 400

    if len(output) == 0:
        return "Command not found", 404

    return jsonify(output), 200


@app_commands.route("/delete_command/<user_id>", methods=["DELETE"])
def delete_command(user_id):
    output = CommandFns.delete_command(user_id)

    if output == -1:
        return "Error running SQL. Please see logs", 400

    if output == 0:
        return "Failed to delete user. Record not found.", 404

    return "Command deleted successfully.", 200
