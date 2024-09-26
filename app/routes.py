from flask import Blueprint, render_template, request, flash, url_for, redirect, session, get_flashed_messages
from flask_login import login_user, logout_user, current_user, login_required
from app.models import Product, Category, db, User, CartItem, Cart, Order, OrderItem
from app.forms import RegistrationForm, LoginForm

main = Blueprint("main", __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template("home.html")

# @main.route('/add', methods=['POST'])  #faulty atm...maybe with post
# def add():
#     return render_template("add.html")

@main.route('/yum')
def yum():
    products = Product.query.join(Category).all()
    return render_template('yum.html', products=products)


# @main.route("/catalog", methods=['GET', 'POST'])
# def catalog():
#     # below works but wrong in category name section
#     # products = Product.query.join(Category).all()
#     products = Product.query.join(Category, Product.category_id == Category.id).add_columns(Category.name).all()
#     return render_template("catalog.html", products=products, flash_messages=get_flashed_messages())

@main.route('/catalog')
def catalog():
    products = db.session.query(Product, Category.name) \
                  .join(Category, Product.category_id == Category.id) \
                  .all()
    return render_template('catalog.html', products=products)



@main.route('/catalog/new', methods=['GET', 'POST'])
@login_required
def new_catalog_item():
    if not current_user.is_admin:
        flash('You do not have permission to add new products.', 'danger')
        return redirect(url_for('main.catalog'))

    categories = Category.query.all()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        category_id = request.form['category_id']
        category = Category.query.get(category_id)

        new_product = Product(name=name, description=description, price=price, category=category)
        db.session.add(new_product)
        db.session.commit()
        flash('New product added successfully.', 'success')
        return redirect(url_for('main.catalog'))

    return render_template('new_catalog_item.html', categories=categories)





# ---------------------------------------------------------------------------------------

# @main.route("/login")
# def membership():
#     return render_template("login.html")

# @main.route('/admin')
# @login_required
# def admin():
#     if not current_user.is_admin:
#         flash('You do not have permission to access the admin panel.', 'danger')
#         return redirect(url_for('main.admin'))
#     return render_template('admin.html')

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


# second login------------------------------------------------------------
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
#         elif user and user.is_admin:
#             flash('Admin user already exists.', 'danger')
#         else:
#             flash('Invalid username or password', 'danger')
#     return render_template('login.html', title='Login', form=form)



# @main.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         if current_user.is_admin:
#             return redirect(url_for('main.admin'))
#         else:
#             return redirect(url_for('main.catalog'))
#
#     form = LoginForm()
#
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#
#         if user and user.check_password(form.password.data):
#             if user.is_admin:
#                 login_user(user)
#                 flash('Login successful!', 'success')
#                 return redirect(url_for('main.admin'))
#             else:
#                 flash('You do not have permission to access the admin panel. Login here for non-admin users', 'danger')
#                 return redirect(url_for('main.login'))
#         else:
#             flash('Invalid username or password', 'danger')
#
#     return render_template('login.html', title='Login', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.catalog'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.catalog'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html', title='Login', form=form)


@main.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('You do not have permission to access the admin panel.', 'danger')
        return redirect(url_for('main.admin'))
    return render_template('admin.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.login'))



#UPDATE & DELETE ROUTES
@main.route('/products/<int:product_id>/update', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    if not current_user.is_admin:
        flash('You do not have permission to update products.', 'danger')
        return redirect(url_for('main.catalog'))

    product = Product.query.get_or_404(product_id)
    categories = Category.query.all()

    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        category_id = request.form.get('category_id', product.category.id)  # Default to current category if not provided
        product.category = Category.query.get(category_id)
        db.session.commit()

        flash('Product updated successfully.', 'success')
        return redirect(url_for('main.catalog'))

    return render_template('update_product.html', product=product, categories=categories)


@main.route('/products/<int:product_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        flash('You do not have permission to delete products.', 'danger')
        return redirect(url_for('main.catalog'))

    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully.', 'success')
        return redirect(url_for('main.catalog'))

    return render_template('confirm_delete.html', product=product)


# SHOPPING CART

@main.route('/cart')
def cart():
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        cart_items = CartItem.query.filter_by(cart_id=cart.id).all() if cart else []
        total_price = sum(item.total_price for item in cart_items)
        return render_template('cart.html', cart_items=cart_items, total_price=total_price)
    else:
        flash('Please log in to access your cart.', 'warning')
        return redirect(url_for('main.login'))

@main.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_product_to_cart(product_id):
    if current_user.is_authenticated:
        product = Product.query.join(Category).filter(Product.id == product_id).first()
        if product:
            cart = Cart.query.filter_by(user_id=current_user.id).first()
            if not cart:
                cart = Cart(user_id=current_user.id)
                db.session.add(cart)
                db.session.commit()

            cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()
            if cart_item:
                cart_item.quantity += 1
            else:
                cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=1)
                db.session.add(cart_item)

            db.session.commit()
            flash(f'{product.name} added to cart.', 'success')
        else:
            flash('Product not found.', 'warning')
    else:
        flash('Please log in to add items to your cart.', 'warning')
    return redirect(url_for('main.yum'))


@main.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
            if cart_item:
                product_name = cart_item.product.name
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    db.session.commit()
                    flash(f'One item of {product_name} removed from cart.', 'success')
                else:
                    db.session.delete(cart_item)
                    db.session.commit()
                    flash(f'{product_name} removed from cart.', 'success')
            else:
                flash('Product not found in cart.', 'warning')
        else:
            flash('Cart not found.', 'warning')
    else:
        flash('Please log in to access your cart.', 'warning')

    return redirect(url_for('main.cart'))

@main.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        cart_items = CartItem.query.filter_by(cart_id=cart.id).all() if cart else []
        total_price = sum(item.total_price for item in cart_items)

        if request.method == 'POST':
            # Process payment and place order
            # ...
            flash('Order placed successfully.', 'success')
            return redirect(url_for('main.catalog'))

        return render_template('checkout.html', cart_items=cart_items, total_price=total_price)
    else:
        flash('Please log in to access the checkout.', 'warning')
        return redirect(url_for('main.login'))


@main.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_confirmation.html', order=order)


@main.route('/checkout', methods=['GET', 'POST'])
def process_checkout():
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        cart_items = CartItem.query.filter_by(cart_id=cart.id).all() if cart else []
        total_price = sum(item.total_price for item in cart_items)

        if request.method == 'POST':
            # Process payment and place order
            order = Order(user_id=current_user.id, total_price=total_price)
            db.session.add(order)
            for item in cart_items:
                order_item = OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity)
                db.session.add(order_item)
            db.session.commit()

            # Clear the cart
            if cart:
                for item in cart_items:
                    db.session.delete(item)
                db.session.commit()

            flash('Order placed successfully.', 'success')
            return redirect(url_for('main.order_confirmation', order_id=order.id))

        return render_template('checkout.html', cart_items=cart_items, total_price=total_price)
    else:
        flash('Please log in to access the checkout.', 'warning')
        return redirect(url_for('main.login'))


