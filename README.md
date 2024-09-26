# The Flour Artisans App

The Flour Artisans is a web application built using the Python Flask framework as part of amazon software development apprenticeship project. 
This application allows users to browse through a menu of bakery items, remove and add items to their cart, and place orders.
It also includes an admin panel for managing products and categories.

**Prerequisites**

Before running the application, make sure you have the following software installed on your machine:

Python 3.x
pip (Python package installer)

**Getting Started**

Follow these steps to set up and run the application locally:

**Clone the repository from GitHub:**
git clone https://github.com/seysey01/FlourArtisansApp.git

Navigate to the project directory:
cd FlourArtisansApp

**Create a virtual environment (recommended):**

python -m venv env

**Activate the virtual environment:**

        On Windows:
        
        env\Scripts\activate
        
        On Unix or macOS:
        
        source env/bin/activate


**Install the required Python packages:**

pip install -r requirements.txt

**Set up the database:**

Create the database by running the following command:
flask db init
flask db migrate
flask db upgrade

**Run the application:**

First, run the sql script bakery.db to generate the relevant tables for the products

flask run

The application should now be running locally at http://localhost:5000.

**Login**
To login as admin, register username: admin && password: admin_password

**Usage**

Register a new account: Click on the "Register" link in the navigation bar and fill out the registration form with your details.

Browse the menu: Once logged in, you'll be directed to the catalog through which you can also access shopping page, where you can browse through various categories and bakery items.

Add items to cart: Click the "Add to Cart" button on any item you wish to purchase.

View cart: Click on the "View Cart" button in the navigation bar to review your cart and proceed with the order.

Checkout: On the cart page, review your order and proceed to checkout. Remove or add more items and then place your order.

Admin panel: If you're an admin user, you'll have access to the admin panel, where you can manage products and categories.


**License**

The Flour Artisans is released under the [MIT License](https://opensource.org/license/MIT).