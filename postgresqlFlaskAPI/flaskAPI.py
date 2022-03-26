from flask import Flask, jsonify, request #If you don't have this -> pip install flask
from flask_cors import CORS #If you don't have this -> pip install flask-cors

import connectionDB #File containing the connection to the database.

app = Flask(__name__)

#Allow all IPs
CORS(app)

"""CRUD about hardware store products"""
@app.route('/products/add', methods=['POST'])
def addContainer():
    """Create tuple to receive the corresponding data.
    This is done as the SQL query only receives data sequence"""
    product = (
        request.json['name'], 
        int(request.json['price'])
    )
    connectionDB.cursor.execute(connectionDB.sqlCommands["insertSQL"], product)
    #Upload changes to the database.
    connectionDB.connectionDB.commit()
    response = jsonify({
        "message": "Product added successfully"
    })
    response.status_code = 201
    return response

@app.route('/products/getAll', methods=['GET'])
def getAll():
    connectionDB.cursor.execute(connectionDB.sqlCommands['selectAllSQL'])
    products = []
    #Move through the cursor and save each product in the "products" list.
    for _id, name, price in connectionDB.cursor:
        products.append({
            '_id': _id,
            'name': name,
            'price': price
        })
    return jsonify(products)

@app.route('/products/getOneById/<int:_id>', methods=['GET'])
def getOneById(_id):
    connectionDB.cursor.execute(connectionDB.sqlCommands['selectOneByIdSQL'], [_id])
    product = {
        '_id': None,
        'name': None,
        'price': None
    }
    for idP, name, price in connectionDB.cursor:
        product['_id'] = idP
        product['name'] = name
        product['price'] = price
    return product

@app.route('/products/updateById/<int:_id>', methods=['PUT'])
def updateById(_id):
    product = (
        request.json['name'],
        request.json['price'],
        _id
    )
    connectionDB.cursor.execute(connectionDB.sqlCommands['updateSQL'], product)
    #Upload changes to the database.
    connectionDB.connectionDB.commit()
    return jsonify({
        'message': 'Product updated successfully.'
    })

@app.route('/products/deleteById/<int:_id>', methods=['DELETE'])
def deleteById(_id):
    connectionDB.cursor.execute(connectionDB.sqlCommands['deleteSQL'], [_id])
    #Upload changes to the database.
    connectionDB.connectionDB.commit()
    response = jsonify()
    response.status_code = 204
    return response

if __name__ == '__main__':
    app.run(
        debug = True,
        host = 'localhost',
        port = '5000'
    )