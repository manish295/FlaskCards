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
        if request.form["button"] == "login":
            db = Database()
            user_name = request.form["username"]
            password = request.form["password"]
            user_id = db.verify_password(user_name, password)
            db.close()
            if not user_id:
                flash("Invalid Credentials!/Account does not exist!", "warning")
                return redirect(url_for("main.login"))
            session["user_id"] = user_id
            session["user_name"] = user_name
            return redirect(url_for("main.home"))

        elif request.form["button"] == "register":
            return redirect(url_for("main.register"))

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
        if validate_user(user_id, set_id) == False:
            return redirect(url_for("main.home"))
    else:
        if validate_user(user_id, set_id, True) == False:
            return redirect(url_for("main.home"))
        c_mode = True

    cards = db.get_cards(set_id)
    db.close()    
    return render_template("flashcards.html", cards=cards, set_name=set_name, set_id=int(set_id), c_mode=c_mode)

@main.route("/profile", methods=["POST", "GET"])
def profile():
    if "user_id" not in session:
        return redirect(url_for("main.login"))
    name = session["user_name"]
    user_id = session["user_id"]
    db = Database()
    sets = db.get_sets(user_id)
    db.close()
    if sets != None:
        total = len(sets)
        published = 0
        unpublished = 0
        for id, set_name, p in sets:
            if p:
                published += 1
            else:
                unpublished += 1
    else:
        total = 0
        published = 0
        unpublished = 0
    if request.method == "POST":
        orig_password = request.form["orig-password"]

        db = Database()
        verify = db.verify_password(name, orig_password)
        db.close()
        if not verify:
            flash("Incorrect Password!", "warning")
            return redirect(url_for("main.profile"))

        if request.form["button"] == "update":
            user_name = request.form["new-username"]
            password = request.form["new-password"]
            confirm_password = request.form["password-confirm"]
            
            if user_name == "":
                user_name = None
            if password == "":
                if confirm_password != "":
                    flash("Fill out password fields completely!", "warning")
                    return redirect(url_for("main.profile"))
                else:
                    password = None
            if password != None and password != confirm_password:
                flash("Passwords do not match!", "warning")
                return redirect(url_for("main.profile"))
            db = Database()
            db.update_user_info(user_id=user_id, user_name=user_name, user_password=password)
            db.close()
            flash("Successfully updated credentials!", "success")
            return redirect(url_for("main.logout"))
        elif request.form["button"] == "delete":
            delete_confirm = request.form["delete-confirm"]
            if delete_confirm == "I WISH TO DELETE MY ACCOUNT":
                db = Database()
                db.delete_account(user_id)
                db.close()
                flash("Account Deleted!", "success")
                return redirect(url_for("main.logout"))
            else:
                flash("Please enter the phrase accurately if you wish to delete your account", "warning")

    return render_template("profile.html", username=name, total=total, published=published, unpublished=unpublished)

@main.route("/set/<set_id>/<set_name>/study")
@main.route("/<path:community>/set/<set_id>/<set_name>/study")
def study_mode(set_id, set_name, community=None):
    user_id = session["user_id"]
    db = Database()
    c_mode = False
    if community == None:
        if validate_user(user_id, set_id) == False:
            return redirect(url_for("main.home"))
    else:
        if validate_user(user_id, set_id, True) == False:
            return redirect(url_for("main.home"))
        c_mode = True

    cards = db.get_cards(set_id)
    db.close()    
    return render_template("study_mode.html", cards=cards, set_name=set_name, set_id=set_id, c_mode=c_mode)

def validate_user(user_id, set_id, community=False):
    db = Database()
    if community == False:
        set_list = []
        if db.get_sets(user_id) != None:
            for id in db.get_sets(user_id):
                set_list.append(id[0])
        if int(set_id) not in set_list:
            return False
    else:
        community_list = []
        if db.get_sets_community() != None:
            for id in db.get_sets_community():
                community_list.append(id[0])
        if int(set_id) not in community_list:
            return False
