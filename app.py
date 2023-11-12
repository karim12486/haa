from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["haadb"]  # Your database name
items_collection = db["inventory"]  # Your collection name

@app.route('/')
def index():
    return "Inventory Management System"

@app.route('/item', methods=['POST'])
def create_item():
    item = request.json
    items_collection.insert_one(item)  #muliple parameters must be passed
    return jsonify(item), 201

@app.route('/items', methods=['GET'])
def get_items():
    items = list(items_collection.find({}, {'_id': 0}))  # Excluding the _id field
    return jsonify(items)

@app.route('/item/<string:item_id>', methods=['PUT'])
def update_item(item_id):
    item_data = request.json
    items_collection.update_one({'id': item_id}, {'$set': item_data})
    return jsonify(item_data)

@app.route('/item/<string:item_id>', methods=['DELETE'])
def delete_item(item_id):
    items_collection.delete_one({'id': item_id})
    return jsonify({'message': 'Item deleted'})

if __name__ == '__main__':
    app.run(debug=True)
