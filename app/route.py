from flask import Blueprint, render_template, request, flash, url_for, redirect


main = Blueprint("main", __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template("home.html")

@main.route('/add', methods=['POST'])  #faulty atm...maybe with post
def add():
    return render_template("add.html")

@main.route("/breakfast")
def breakfast():
    return render_template("breakfast.html")

@main.route("/lunch")
def lunch():
    return render_template("lunch.html")


@main.route("/dinner")
def dinner():
    return render_template("dinner.html")

@main.route("/yum")
def yummy_my_tummy():
    return render_template("yum.html")

@main.route("/basket")
def basket():
    return render_template("basket.html")


#May cut down on pages (maybe 3 at most)