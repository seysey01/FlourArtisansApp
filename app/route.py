from flask import Blueprint, render_template, request, flash, url_for, redirect


main = Blueprint("main", __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template("index.html")

@main.route('/add', methods=['POST'])  #faulty atm...maybe with post
def add():
    return render_template("add.html")

@main.route("/view")
def view():
    return render_template("view.html")

@main.route("/success")
def success():
    return render_template("success.html")

@main.route("/delete")
def delete():
    return render_template("delete.html")
