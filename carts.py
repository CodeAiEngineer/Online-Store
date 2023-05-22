from flask import Blueprint, request, jsonify, session, abort
from pymongo import MongoClient
from functools import wraps
from bson.objectid import ObjectId


class Carts:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017')
        self.db = self.client['online_store']
        
            
    #Add to cart
    item_total_prices = []
    def add_to_cart(self):
        data = request.get_json()
        user_id = data['user_id']
        product_id = data['product_id']
        count = data['count']
        if isinstance(count, str):
            count = int(count)
        user = self.db.users.find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'message': 'Invalid user ID.'}), 400

        product = self.db.products.find_one({'_id': ObjectId(product_id)})
        if not product:
            return jsonify({'message': 'Invalid product ID.'}), 400

        if int(product['amount_in_stock']) < int(count):
            return jsonify({'message': 'Product is out of stock.'}), 400

        if not product['in_stock']:
            return jsonify({'message': 'Product is not available.'}), 400

        if count <= 0:
            return jsonify({'message': 'Count must be greater than zero.'}), 400

        if "username" not in session:
            return jsonify({'message': 'You are not authorized to perform this action. Please login'}), 400
        else:
            user3 = self.db.users.find_one({'username': session['username']})

        if user3 != user:
            return jsonify({'message': 'You are not authorized to perform this action. Please login and use correct login ID'}), 400

        # Calculate total_price based on product price and count
        total_price = product['price'] * count

        # Check if user already has a cart
        user_cart = self.db.cart.find_one({'user_id': ObjectId(user_id), 'checked_out': False})
        if user_cart:
            # Check if product already in cart
            product_already_in_cart = False
            for item in user_cart['items']:
                if item['product_id'] == ObjectId(product_id):
                    item['count'] += count
                    item['total_price'] += total_price
                    product_already_in_cart = True
                    break
            if not product_already_in_cart:
                cart_item = {
                    'product_id': ObjectId(product_id),
                    'count': count,
                    'total_price': total_price
                }
                user_cart['items'].append(cart_item)
            self.db.cart.update_one({'_id': user_cart['_id']}, {'$set': {'items': user_cart['items']}})

        else:
            cart_item = {
                'user_id': ObjectId(user_id),
                'items': [{
                    'product_id': ObjectId(product_id),
                    'count': count,
                    'total_price': total_price
                }],
                'checked_out': False
            }
            self.db.cart.insert_one(cart_item)
            user_cart = cart_item

        # Calculate total price for each product
        product_total_price = {}
        for item in user_cart['items']:
            product_id = str(item['product_id'])
            if product_id in product_total_price:
                product_total_price[product_id] += int(item['total_price'])
            else:
                product_total_price[product_id] = int(item['total_price'])

        # Calculate total cart price
        total_cart_price = sum(int(value) for value in product_total_price.values())


        # Update cart document in the database with total cart price
        self.db.cart.update_one({'_id': user_cart['_id']}, {'$set': {'total_cart_price': total_cart_price}})

        # Return response
        return jsonify({'message': 'Item added to cart.', 'product_total_price': product_total_price, 'total_cart_price': total_cart_price}), 201


    def remove_from_cart(self, cart_item_id):
        cart_item_id = ObjectId(cart_item_id)
        cart = self.db.cart.find_one({'items.product_id': cart_item_id})
        if not cart:
            return jsonify({'message': 'Cart item not found.'}), 404

        cart['items'] = [item for item in cart['items'] if item['product_id'] != cart_item_id]
        self.db.cart.update_one({'_id': cart['_id']}, {'$set': {'items': cart['items']}})

        return jsonify({'message': 'Item removed from cart.'}), 200
        
    #Get products in cart.    

    def get_products_in_cart(self,user_id):
        print("user_id:", user_id)

        user = self.db.users.find_one({'_id': ObjectId(user_id)})
        # user = self.db.users.find_one({'username': session['username']})
        print(user)
        if not user:
            return jsonify({'message': 'Invalid user ID.'}), 400    
        
        cart_items = self.db.cart.find({'user_id': user['_id']})
        # print(cart_items)
        
        user = self.db.users.find_one({'username': session['username']})
        if user['is_active'] != True:  
            return jsonify({'message': 'Deactive users cannot access this method..'}), 401

        response = []
        for cart_item in cart_items:
            cart_item_response = []  # Initialize a list to store items for each cart item
            for item in cart_item['items']:
                product = self.db.products.find_one({'_id': item['product_id']})
                category = self.db.categories.find_one({'_id': product['category_id']})
                cart_item_response.append({
                    'id': str(product['_id']),
                    'name': product['name'],
                    'amount_in_stock': product['amount_in_stock'],
                    'price': product['price'],
                    'category': category['name'],
                    'count': item['count'],
                    'total_price': item['total_price']
                })
            response.extend(cart_item_response)  # Append the items for this cart item to the overall response

        return jsonify({'cart_items': response}), 200


            
    def clear_cart(self):
        user = self.db.users.find_one({'username': session['username']})
        print('123*/*/*/*')
        print(user)
        # user = self.db.users.find_one({'_id': ObjectId(user_id)})
        if not user:
            return jsonify({'message': 'Invalid user ID.'}), 400
        
        if "username" not in session:
            return jsonify({'message': 'You are not authorized to perform this action. Please login'}), 400
        else:
            user3 = self.db.users.find_one({'username': session['username']})

        if user3 != user:
            return jsonify({'message': 'You are not authorized to perform this action. Please login and use correct login ID'}), 400

        if user['is_active'] != True:  
            return jsonify({'message': 'Deactive users cannot access this method..'}), 401
        
        cart = self.db.cart.find_one({'user_id': ObjectId(user['_id'])})
        if not cart:
            return jsonify({'message': 'Cart not found.'}), 404

        self.db.cart.delete_one({'_id': cart['_id']})

        return jsonify({'message': 'Cart cleared.'}), 200
        

    
