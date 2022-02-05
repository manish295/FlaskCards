from database import Database
from flask import Flask, redirect, url_for, render_template, request, session, json

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
    db = Database()
    if request.method == "POST":
        user_name = request.form["username"]
        password = request.form["password"]
        user_id = db.handle_user(user_name, password)[0][0]
        session["user_id"] = user_id
        db.close()
        return redirect(url_for("home"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

@app.route("/set/<set_id>")
def flash_cards(set_id):
    db = Database()
    cards = db.get_cards(set_id)
    db.close()
    return render_template("flashcards.html", cards=cards)


@app.route("/add-set", methods=["POST", "GET"])
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

@app.route("/add-card",  methods=["POST", "GET"])
def add_card():
    print("Incoming...")
    print(request.get_json())
    data = request.get_json()
    question  = data["question"]
    answer = data["answer"]
    set_id = int(data["path"][5:])
    print(set_id)
    db = Database()
    db.add_card(set_id, question, answer)
    db.close()
    return json.dumps({"question": question, "answer": answer})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
