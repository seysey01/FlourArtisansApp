from flask import Blueprint, render_template, request, flash, url_for, redirect


main = Blueprint("main", __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template("home.html")

# @main.route('/add', methods=['POST'])  #faulty atm...maybe with post
# def add():
#     return render_template("add.html")

@main.route("/yum")
def yummy_my_tummy():
    return render_template("yum.html")

@main.route("/basket")
def basket():
    return render_template("basket.html")

@main.route("/login")
def membership():
    return render_template("login.html")

@main.route("/admin")
def admin():
    return render_template("admin.html")

@main.route("/contact")
def contact():
    return render_template("contact.html")


# WATCH THIS SPACE - nice to have
@main.route("/discounts")
def discounts():
    return render_template("watchthisspace.html")

@main.route("/recommendations")
def recommendations():
    return render_template("watchthisspace.html")

@main.route("/events")
def events():
    return render_template("watchthisspace.html")




#May cut down on pages (maybe 3 at most)