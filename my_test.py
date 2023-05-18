import pytest
from flask import Flask
from pymongo import MongoClient
from main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["MONGO_URI"] = "mongodb://localhost:27017/online_store"

    client = MongoClient(app.config["MONGO_URI"])
    database = client.get_default_database()

    with app.app_context():
        # Clear the database before running tests
        client.drop_database(database)

    yield client

    # Clean up the test database after running tests
    client.drop_database(database)

  
def test_register():
    app.testing = True
    client = app.test_client()
    N = 6

    data = {
  "username": "TestBravo",
  "password": "PAsswrd+",
  "email": "TestBravo@example.com",
  "name": "Test",
  "surname": "Bravo"
}

    response = client.post('/register', json=data)

    # client = MongoClient('mongodb://localhost:27017')
    # db = client['online_store']
    # result = db.users.delete_one({'username': 'Test 33User'})

    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"
    assert response.get_json() == {'message': 'Registration successful.'}, "Unexpected response JSON"
  
def test_login():
    app.testing = True
    client = app.test_client()

    # Test case 1: Successful login
    data = {'username': 'TestBravo', 'password': 'PAsswrd+'}
    response = client.post('/login', json=data)

    # client = MongoClient('mongodb://localhost:27017')
    # db = client['online_store']
    # result = db.users.delete_one({'username': 'Test 33User'})    

    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    response_json = response.get_json()
    assert 'message' in response_json and response_json['message'] == 'Login successful.', "Unexpected response JSON"


def test_create_product():
    # log in as an admin user
    client = MongoClient('mongodb://localhost:27017')
    db = client['online_store']
    user = db.users.find_one({'username': 'TestBravo'})
    if user:
        user['role'] = 'admin'
        user['is_admin'] = True
        db.users.update_one({'_id': user['_id']}, {'$set': {'role': 'admin', 'is_admin': True}})
        print("User updated successfully.")
    else:
        print("User not found.")
    
    app.testing = True
    client = app.test_client()
    data = {'username': 'TestBravo', 'password': 'PAsswrd+'}
    response = client.post('/login', json=data)

    # create a dictionary with the product data
    product_data = {
        'name': 'test 2produ6c2t',
        'amount_in_stock': 10,
        'price': 10.99,
        'category_id': '6465d2cc873b469de0537b45'
    }

    # send a POST request to the create_product endpoint with the product data
    response = client.post('/products', json=product_data)


    # check that the response status code is 201
    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"

    # check that the response contains the 'product_id' key
    assert 'product_id' in response.json

    # check that the product was created in the database
    client = MongoClient('mongodb://localhost:27017')
    db = client['online_store']
    product = db.products.find_one({'name': 'test 2produ6c2t'})



    assert product is not None
    client = MongoClient('mongodb://localhost:27017')
    db = client['online_store']
    result = db.users.delete_one({'username': 'TestBravo'})    

