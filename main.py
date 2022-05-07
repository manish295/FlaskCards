from database import Database
from flask import Flask, flash, redirect, url_for, render_template, request, session, json

app = Flask(__name__)
app.secret_key = "supersecret"


@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    db = Database()
    user_id = session["user_id"]
    set_info = db.get_sets(user_id)
    db.close()
    return render_template("home.html", set_info=set_info)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        db = Database()
        user_name = request.form["username"]
        password = request.form["password"]
        user_id = db.verify_password(user_name, password)
        db.close()
        if not user_id:
            flash("Invalid Credentials!/Account does not exist!", "warning")
            return redirect(url_for("login"))
        session["user_id"] = user_id
        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        db = Database()
        user_name = request.form["username"]
        password = request.form["password"]
        db.add_user(user_name, password)
        db.close()
        flash("User Created!", "success")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

@app.route("/set/<set_id>/<set_name>")
def flash_cards(set_id, set_name):
    user_id = session["user_id"]
    set_list = []
    db = Database()
    for id in db.get_sets(user_id):
        set_list.append(id[0])
    if int(set_id) not in set_list:
        return redirect(url_for("home"))
    cards = db.get_cards(set_id)
    db.close()
    return render_template("flashcards.html", cards=cards, set_name=set_name)


@app.route("/add-set", methods=["POST"])
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

@app.route("/add-card",  methods=["POST"])
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

@app.route("/delete-set", methods=["POST"])
def delete_set():
    print("Incoming...")
    print(request.get_json())
    data = request.get_json()
    set_id = data["set_id"]
    db = Database()
    db.delete_set(int(set_id))
    db.close()
    return json.dumps({"success":True}), 200

@app.route("/delete-card", methods=["POST"])
def delete_card():
    print("Incoming...")
    print(request.get_json())
    data = request.get_json()
    card_id = data["card_id"]
    db = Database()
    db.delete_card(int(card_id))
    db.close()
    return json.dumps({"success":True}), 200

@app.route("/update-card", methods=["POST"])
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

@app.route("/update-set", methods=["POST"])
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
    

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
