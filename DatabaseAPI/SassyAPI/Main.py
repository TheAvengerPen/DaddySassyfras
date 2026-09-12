from flask import Flask, request, jsonify
from DBCommunication import SassSQLCall

app = Flask(__name__)

@app.route("/get-user/<user_id>")
def getUser(user_id):
    if user_id == "1":
        userData = {"user_id": user_id,
                    "name": "Bobby",
                    "is_streamer": 0}

        return jsonify(userData), 200
    else:
        con = SassSQLCall("APenguinsLullab", "DaddySassyfras")
        con.execute("select * from People")

        return jsonify("Unknown"), 403

@app.route("/create-user", methods=["POST"])
def createUser():
    data = request.get_json()
    if data:
        return jsonify(data), 201
    return False, 401

if __name__ == "__main__":
    app.run(debug=True)
