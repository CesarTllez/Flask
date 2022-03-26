from flask import Flask, jsonify, request #If you don't have this -> pip install flask
from flask_cors import CORS #If you don't have this -> pip install flask-cors
from pymongo import MongoClient #If you don't this -> pip install pymongo dnspython
from bson import json_util, ObjectId

app = Flask(__name__)

#Allow all IPs
CORS(app)

"""MongoDB connection.
Add your connection string from Mongodb Atlas.
If you want to work locally use (mongodb://localhost:27017)"""
CONNECT_STRING = 'mongodb+srv://your_user:your_password@cluster0.2ijgn.mongodb.net/test' #<- Example
cursor = MongoClient(CONNECT_STRING)
#Create database with the cursor.
database = cursor['hardware_store']
#Create collection with the database.
collection = database['products']

"""CRUD about hardware store products"""
@app.route('/products/add', methods=['POST'])
def add():
    #Create dictionary to receive the corresponding data.
    product = {
        'name': request.json['name'],
        'price': int(request.json['price'])
    }
    #Insert product in the database.
    collection.insert_one(product)
    response = jsonify({
        'message': 'Product added successfully.'
    })
    response.status_code = 201
    return response

@app.route('/products/getAll', methods=['GET'])
def getAll():
    products = collection.find()
    return json_util.dumps(products)

@app.route('/products/getOneById/<_id>', methods=['GET'])
def getOneById(_id):
    product = collection.find_one({'_id': ObjectId(_id)})
    return json_util.dumps(product)

@app.route('/products/updateById/<_id>', methods=['PUT'])
def updateByid(_id):
    #Create dictionary to receive the corresponding data.
    product = {
        'name': request.json['name'],
        'price': int(request.json['price'])
    }
    #Update product with id.
    collection.update_one({'_id': ObjectId(_id)}, {'$set': {
        'name': product['name'],
        'price': product['price']
    }})
    return jsonify({
        'message': 'Product updated successfully.'
    })

@app.route('/products/deleteById/<_id>', methods=['DELETE'])
def deleteById(_id):
    collection.delete_one({'_id': ObjectId(_id)})
    response = jsonify()
    response.status_code = 204
    return response

if __name__ == '__main__':
    app.run(
        debug = True,
        host = 'localhost',
        port = '5001'
    )