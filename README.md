# Online Store
 Online Store created with Flask and other libraries.

install requirements on cmd: pip install flask Flask-Session pymongo Flask-Testing pytest

if you want use all methods,do the following steps in order.
Some security measures, strong password, authentication, manually register as admin with post and role cannot be entered (ineffective if entered), werkzeug.security library is used, if the user is not admin or active user, user cannot access many methods.
Create user,change user's role to 'admin' and is_admin=True from directly DB, login, create category, create product, create cart.



#CREATE USER:
run main.py and request json like: req link=http://127.0.0.1:5000/register
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
#CREATE CATEGORY:
POST /categories
 
 
{
  "name": "Electronics"
}

#UPDATE CATEGORY:
PUT /categories/{category_id}
 
 
{
  "name": "Electronics"
}

#DELETE CATEGORY:
DELETE /categories/{category_id}
(No request body needed)


#CREATE PRODUCT:

POST /products

{
  "name": "MYPHONE12",
  "amount_in_stock": 10,
  "price": 999.99,
  "category_id": "category_id_here"
}

#UPDATE PRODUCT:

PUT /products/{product_id}
 
 
{
  "name": "iPhone 13",
  "amount_in_stock": 20,
  "price": 1099.99,
  "category_id": "category_id_here"
}

#DELETE PRODUCT:
DELETE /products/{product_id}
(No request body needed)


#CREATE CART:

POST /cart

{
  "user_id": "user_id_here",
  "product_id": "product_id_here",
  "count": 2
}

#DELETE CART:
DELETE /cart/{cart_item_id}
(No request body needed)

#ACTIVE/DEACTIVE USER:

PUT /users/{user_id}

{
  "is_active": false
}



