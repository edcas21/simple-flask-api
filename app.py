from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name': 'store1',
        'items': [
            {
                'name': 'item1',
                'price': 15.85
            }
        ]
    }
]

@app.route('/')
def home():
    return render_template('index.html')

# POST - user to retrieve data
# GET - used to send data back only (Default method is GET)

# POST /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>')
def get_store(name):
    # Iterate over stores
    for store in stores:
        if store['name'] == name:
            return jsonify(store)

    return jsonify({'message': f"{name} store doesn't exist"})

# GET /store
@app.route('/store')
def get_stores():
    # pass in stores as a dictionary since it is currently a list
    # Raw json is just a string, but it must be in the format of a dictionary
    return jsonify({ 'stores': stores })

# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):

    request_data = request.get_json()

    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)

    return jsonify({'message': f"store {name} was not found"})


# GET /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_from_store(name):

    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})

    return jsonify({'message': f"store {name} was not found"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
