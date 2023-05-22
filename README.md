# Online Store
 Online Store created with Flask and other libraries.

1-)install requirements on cmd: pip install flask Flask-Session pymongo Flask-Testing pytest

2-)install MongoDB.
Localhost used for this project but you can use Atlas for online host.

3-)Run main.py for running app(Use request app for sending request.). Write "pytest" for running automated test.

Some security measures are: strong password, authentication, manually register as admin with post and role cannot be entered (ineffective if entered), werkzeug.security library is used, if the user is not admin or active user, user cannot access many methods.

if you want use all methods,do the following steps in order.
Create user,change user's role to 'admin' and is_admin=True from directly DB, login, create category, create product, create cart.

You MUST login for many methods, otherwise you will get error.


# EXAMPLE JSON REQUESTS:

# CREATE USER:
run main.py and request json like: 

request link=http://127.0.0.1:5000/register


POST /register


{
"username": "JohnnyTaylorise",
"password": "pW95fJ2@KXb",
"email": "JohnnyTaylorise@JohnnyTaylorise.com",
"name": "Johnny",
"surname": "JohnnyTaylorise"
}



POST /login


{
  "username": "JohnnyTaylorise",
  "password": "pW95fJ2@KXb"
}
# CREATE CATEGORY:
POST /categories


{
  "name": "Electronics"
}

# UPDATE CATEGORY:
PUT /categories/{category_id}


{
  "name": "Electronics"
}

# DELETE CATEGORY:
DELETE /categories/{category_id}
(No request body needed)


# CREATE PRODUCT:

POST /products

{
  "name": "MYPHONE12",
  "amount_in_stock": 10,
  "price": 999.99,
  "category_id": "category_id_here"
}

# UPDATE PRODUCT:

PUT /products/{product_id}


{
  "name": "iPhone 13",
  "amount_in_stock": 20,
  "price": 1099.99,
  "category_id": "category_id_here"
}

# DELETE PRODUCT:
DELETE /products/{product_id}
(No request body needed)


# CREATE CART:

POST /cart

{
  "user_id": "user_id_here",
  "product_id": "product_id_here",
  "count": 2
}

# DELETE 1 ITEM IN CART:
DELETE /cart/{cart_item_id}
(No request body needed)

# ACTIVE/DEACTIVE USER:

PUT /users/{user_id}

{
  "is_active": false
}

# GET CART:

GET /cart/{user_id}

