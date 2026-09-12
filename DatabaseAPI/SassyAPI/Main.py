from flask import Flask, request, jsonify, json

import PeopleFns
from DBCommunication import DBConnector

app = Flask(__name__)


@app.route("/get-user/<user_id>")
def getUser(user_id):
    output = PeopleFns.get_person_data(user_id)

    if output == -1:
        return "Error running SQl. Please see logs", 400

    if len(output) == 0:
        return "User not found", 404

    return jsonify(output), 200


@app.route("/get-user-from-name/<twitch_name>")
def get_user_from_twitch(twitch_name):
    output = PeopleFns.get_person_data_twitch_id(twitch_name)

    if output == -1:
        return "Error running SQl. Please see logs", 400

    if len(output) == 0:
        return "User not found", 404

    return jsonify(output), 200


@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()

    new_id = PeopleFns.create_new_user(data["twitch_name"], data["is_streamer"])

    if new_id == -1:
        return jsonify("Failed to add person"), 400

    output = PeopleFns.get_person_data(new_id)

    if output == -1:
        return "Error running SQl. Please see logs", 400

    if len(output) == 0:
        return "User not found", 404

    return jsonify(output), 200


if __name__ == "__main__":
    app.run(debug=True)
