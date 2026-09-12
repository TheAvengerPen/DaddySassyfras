from flask import request, jsonify, Blueprint
from fns import PeopleFns

app_user = Blueprint("app_user", __name__)


@app_user.route("/get-user/<user_id>")
def getUser(user_id):
    output = PeopleFns.get_person_data(user_id)

    if output == -1:
        return "Error running SQL. Please see logs", 400

    if len(output) == 0:
        return "User not found", 404

    return jsonify(output), 200


@app_user.route("/get-user-from-name/<twitch_name>")
def get_user_from_twitch(twitch_name):
    output = PeopleFns.get_person_data_twitch_id(twitch_name)

    if output == -1:
        return "Error running SQL. Please see logs", 400

    if len(output) == 0:
        return "User not found", 404

    return jsonify(output), 200


@app_user.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()

    new_id = PeopleFns.create_new_user(data["TwitchName"], data["IsStreamer"])

    if new_id == -1:
        return jsonify("Failed to add person"), 400

    output = PeopleFns.get_person_data(new_id)

    if output == -1:
        return "Error running SQL. Please see logs", 400

    if len(output) == 0:
        return "User not found", 404

    return jsonify(output), 200


@app_user.route("/update-user", methods=["PUT"])
def update_user():
    data = request.get_json()

    new_id = PeopleFns.update_user_info(data["PersonID"], data["TwitchName"], data["PersonID"])

    if new_id == -1:
        return jsonify("Failed to update person"), 400

    output = PeopleFns.get_person_data(data["PersonID"])

    if output == -1:
        return "Error running SQL. Please see logs", 400

    if len(output) == 0:
        return "User not found", 404

    return jsonify(output), 200


@app_user.route("/get-all-users", methods=["GET"])
def get_all_users():
    output = PeopleFns.get_all_users()

    if output == -1:
        return "Error running SQL. Please see logs", 400

    if len(output) == 0:
        return "User not found", 404

    return jsonify(output), 200


@app_user.route("/delete-user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    output = PeopleFns.delete_user(user_id)

    if output == -1:
        return "Error running SQL. Please see logs", 400

    if output == 0:
        return "Failed to delete user. Record not found.", 404

    return f"User deleted successfully.", 200