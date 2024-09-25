from flask import Blueprint, render_template, request, flash, url_for, redirect, session
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Product, db, User
from app.forms import RegistrationForm, LoginForm

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



# AUTHORISATION CHECKS

# def is_admin():
#     if 'user_id' not in session:
#         return False
#     user = User.query.get(session['user_id'])
#     return user.is_admin if user else False


# @main.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(username=form.username.data, email=form.email.data, password=form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Registration successful! You can now log in.', 'success')
#         return redirect(url_for('main.login'))
#     return render_template('register.html', title='Register', form=form)

# SHOPPING
@main.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    item_id = request.form['item_id']
    quantity = int(request.form['quantity'])

    # Add the item to the shopping cart
    if 'cart' not in session:
        session['cart'] = {}
    cart = session['cart']

    if item_id in cart:
        cart[item_id]['quantity'] += quantity
    else:
        cart[item_id] = {'quantity': quantity}

    session.modified = True
    flash('Item added to cart!', 'success')
    return redirect(url_for('main.yummy_my_tummy'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Checking if the user being registered is an admin
        is_admin = False  # Set to True if you want to register an admin user

        user = User(username=form.username.data, email=form.email.data, password=form.password.data, is_admin=is_admin)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')

        # Redirecting to the appropriate page based on the user's role
        if is_admin:
            return redirect(url_for('main.admin'))
        else:
            return redirect(url_for('main.login'))

    return render_template('register.html', title='Register', form=form)

# @main.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user and user.check_password(form.password.data):
#             login_user(user)
#             flash('Login successful!', 'success')
#             return redirect(url_for('main.home'))
#         flash('Invalid username or password', 'danger')
#     return render_template('login.html', title='Login', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        elif user and user.is_admin:
            flash('Admin user already exists.', 'danger')
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))



#UPDATE & DELETE ROUTES
@main.route('/products/<int:product_id>/update', methods=['GET', 'POST'])
def update_product(product_id):
    # if not is_admin():
    #     return redirect(url_for('main.basket'))

    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        product.category = request.form['category']
        db.session.commit()

        return redirect(url_for('main.basket'))

    return render_template('update_product.html', product=product)

@main.route('/products/<int:product_id>/delete', methods=['GET', 'POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('main.basket'))

    return render_template('confirm_delete.html', product=product)


