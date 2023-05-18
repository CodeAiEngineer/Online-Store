from flask import Flask
from pymongo import MongoClient
from flask_session import Session
from register import Register
from login import Login
from categories import Categories
from products import Products
from carts import Carts


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

client = MongoClient('mongodb://localhost:27017')
db = client['online_store']

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.sessions'

Session(app)


#REGISTER, LOGIN, ACTIVATE/DEACTIVATE
@app.route('/register', methods=['POST'])
def register():
    register_instance = Register()
    return register_instance.register()

@app.route('/login', methods=['POST'])
def login():
    login_instance = Login()
    return login_instance.login()

@app.route('/users/<user_id>', methods=['PUT'])
def activate_deactivate_user(user_id):
    login_instance = Login()
    return login_instance.activate_deactivate_user(user_id)

#CATEGORY
@app.route('/categories', methods=['POST'])
def create_category():
    categories_instance = Categories()
    return categories_instance.create_category()

@app.route('/categories/<category_id>', methods=['PUT'])
def update_category(category_id):
    categories_instance = Categories()
    return categories_instance.update_category(category_id)

@app.route('/categories/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    categories_instance = Categories()
    return categories_instance.delete_category(category_id)

@app.route('/products/category/<category_id>', methods=['GET'])
def filter_products_by_category(category_id):
    categories_instance = Categories()
    return categories_instance.filter_products_by_category(category_id)

#PRODUCTS
@app.route('/products', methods=['POST'])
def create_product():
    products_instance = Products()
    return products_instance.create_product()

@app.route('/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    products_instance = Products()
    return products_instance.update_product(product_id)


@app.route('/products/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    products_instance = Products()
    return products_instance.delete_product(product_id)


@app.route('/products', methods=['GET'])
def display_products():
    products_instance = Products()
    return products_instance.display_products()


#CARTS

@app.route('/cart', methods=['POST'])
def add_to_cart():
    cart_instance = Carts()
    return cart_instance.add_to_cart()

@app.route('/cart/<cart_item_id>', methods=['DELETE'])
def remove_from_cart(cart_item_id):
    cart_instance = Carts()
    return cart_instance.remove_from_cart(cart_item_id)

@app.route('/cart/<user_id>', methods=['GET'])
def get_products_in_cart(user_id):
    cart_instance = Carts()
    return cart_instance.get_products_in_cart(user_id)


if __name__ == '__main__':
    app.run()
