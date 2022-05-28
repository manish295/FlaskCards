from back_end.database import Database
from flask import Blueprint, flash, redirect, url_for, render_template, request, session

main = Blueprint('main', __name__)



@main.route("/")
@main.route("/<path:community>")
def home(community=None):
    if "user_id" not in session:
        return redirect(url_for("main.login"))
    
    db = Database()
    user_id = session["user_id"]
    if community == None:
        set_info = db.get_sets(user_id)
        db.close()
        return render_template("home.html", message="Your Card sets", set_info=set_info, c_mode=False)
    else:
        set_info = db.get_sets_community()
        db.close()
        return render_template("home.html", message="Community Curated Sets", set_info=set_info, c_mode=True)


@main.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        db = Database()
        user_name = request.form["username"]
        password = request.form["password"]
        user_id = db.verify_password(user_name, password)
        db.close()
        if not user_id:
            flash("Invalid Credentials!/Account does not exist!", "warning")
            return redirect(url_for("main.login"))
        session["user_id"] = user_id
        return redirect(url_for("main.home"))

    return render_template("login.html")

@main.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        user_name = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["password-confirm"]
        if password != confirm_password:
            flash("Passwords don't match!", "warning")
            return redirect(url_for("main.register"))
        db = Database()
        db.add_user(user_name, password)
        db.close()
        flash("User Created!", "success")
        return redirect(url_for("main.login"))
    return render_template("register.html")


@main.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("main.login"))

@main.route("/set/<set_id>/<set_name>")
@main.route("/<path:community>/<set_id>/<set_name>")
def flash_cards(set_id, set_name, community=None):
    user_id = session["user_id"]
    db = Database()
    c_mode = False
    if community == None:
        set_list = []
        for id in db.get_sets(user_id):
            set_list.append(id[0])
        if int(set_id) not in set_list:
            return redirect(url_for("main.home"))
    else:
        community_list = []
        for id in db.get_sets_community():
            community_list.append(id[0])
        if int(set_id) not in community_list:
            return redirect(url_for("main.home"))
        c_mode = True

    cards = db.get_cards(set_id)
    db.close()    
    return render_template("flashcards.html", cards=cards, set_name=set_name, set_id=int(set_id), c_mode=c_mode)

@main.route("/set/<set_id>/<set_name>/study")
@main.route("/<path:community>/set/<set_id>/<set_name>/study")
def study_mode(set_id, set_name, community=None):
    user_id = session["user_id"]
    db = Database()
    c_mode = False
    if community == None:
        set_list = []
        for id in db.get_sets(user_id):
            set_list.append(id[0])
        if int(set_id) not in set_list:
            return redirect(url_for("main.home"))
    else:
        community_list = []
        for id in db.get_sets_community():
            community_list.append(id[0])
        if int(set_id) not in community_list:
            return redirect(url_for("main.home"))
        c_mode = True

    cards = db.get_cards(set_id)
    db.close()    
    return render_template("study_mode.html", cards=cards, set_name=set_name, set_id=set_id, c_mode=c_mode)