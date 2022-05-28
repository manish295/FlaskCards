from back_end.database import Database
from flask import Blueprint, request, session, json

api = Blueprint('api', __name__)

@api.route("/add-set", methods=["POST"])
def add_set():
    print("Incoming...")
    print(request.get_json())
    data = request.get_json()
    set_name = data["set_name"]
    user_id = session["user_id"]
    db = Database()
    set_id, name = db.add_set(user_id, set_name)[0]
    db.close()
    return json.dumps({"id": set_id, "name":name})

@api.route("/add-card",  methods=["POST"])
def add_card():
    print("Incoming...")
    print(request.get_json())
    data = request.get_json()
    question  = data["question"]
    answer = data["answer"]
    set_id = data["path"][5:]
    set_id = int(set_id[:set_id.index("/")])
    print(set_id)
    db = Database()
    card_id = db.add_card(set_id, question, answer)[0][0]
    db.close()
    return json.dumps({"question": question, "answer": answer, "card_id": card_id})


@api.route("/delete-set", methods=["POST"])
def delete_set():
    print("Incoming...")
    print(request.get_json())
    data = request.get_json()
    set_id = data["set_id"]
    db = Database()
    db.delete_set(int(set_id))
    db.close()
    return json.dumps({"success":True}), 200

@api.route("/delete-card", methods=["POST"])
def delete_card():
    print("Incoming...")
    print(request.get_json())
    data = request.get_json()
    card_id = data["card_id"]
    db = Database()
    db.delete_card(int(card_id))
    db.close()
    return json.dumps({"success":True}), 200

@api.route("/update-card", methods=["POST"])
def update_card():
    print("Incoming...")
    print(request.get_json())
    data = request.get_json()
    card_id = data["card_id"]
    question = data["question"]
    answer = data["answer"]
    db = Database()
    db.update_card(card_id, question, answer)
    db.close()
    return json.dumps({"success":True}), 200

@api.route("/update-set-community", methods=["POST"])
def update_set_community():
    print("Incoming...")
    data = request.get_json()
    print(data)
    set_id = data["set_id"]
    value = data["value"]
    db = Database()
    if value and db.get_cards(set_id) == None:
        return json.dumps({"success": False}), 200
    db.update_community(set_id, value)
    db.close()
    return json.dumps({"success": True}), 200

@api.route("/update-set", methods=["POST"])
def update_set():
    print("Incoming...")
    print(request.get_json())
    data = request.get_json()
    set_id = data["set_id"]
    set_name = data["set_name"]
    db = Database()
    db.update_set_name(set_id, set_name)
    db.close()
    return json.dumps({"success":True}), 200