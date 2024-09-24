from flask import Blueprint, render_template, request, flash, url_for, redirect

from app.models import Product, db

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

# CRUD - CREATE
# @main.route("/basket")
# def basket():
#     return render_template("basket.html")

@main.route("/basket", methods=['GET', 'POST'])
def basket():
    products = Product.query.all()
    print(products, "productsssssss")

    return render_template("basket.html", products=products)


@main.route('/basket/new', methods=['GET', 'POST'])
def new_basket_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category = request.form['category']

        new_product = Product(name=name, description=description, price=price, category=category)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('main.basket'))

    return render_template('new_basket_item.html')



# ---------------------------------------------------------------------------------------

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

