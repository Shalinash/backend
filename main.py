from flask import Flask, request, jsonify
import logging
import json
import unittest

app = Flask(__name__)

# Logging configuration
logging.basicConfig(filename='backend.log', level=logging.INFO)

# Hardcoded list of JSON objects
objects = [
    {"id": 0, "name": "Amy", "email": "amy@email.com", "phone": "00000000"},
    {"id": 1, "name": "Ben", "email": "ben@email.com", "phone": "11111111"},
]

# Logging middleware
@app.before_request
def log_request_info():
    logging.info('Request URL: %s', request.url)
    logging.info('Request method: %s', request.method)
    logging.info('Request data: %s', request.data)

# Validate request data for adding an object
def validate_add_object(data):
    if 'name' not in data or 'email' not in data or 'phone' not in data:
        return False
    return True

# Validate request data for deleting an object
def validate_delete_object(objects, id):
    return any(obj['id'] == id for obj in objects)

# Endpoint to get list of all objects
@app.route('/objects', methods=['GET'])
def get_all_objects():
    return jsonify(objects)

# Endpoint to get an object by ID
@app.route('/objects/<id>', methods=['GET'])
def get_object(id):
    obj = next((obj for obj in objects if obj['id'] == int(id)), None)
    if obj:
        print("\nObjects after get_object:", objects)  # Print object list
        return jsonify(obj)
    return jsonify({'error': 'Object not found'}), 404

# Endpoint to add a new object
@app.route('/objects', methods=['POST'])
def add_object():
    data = request.json
    if not validate_add_object(data):
        return jsonify({'error': 'Invalid request data'}), 400

    max_id = max(obj['id'] for obj in objects) if objects else -1
    new_object = {
        'id': max_id + 1,
        'name': data['name'],
        'email': data['email'],
        'phone': data['phone']
    }
    objects.append(new_object)
    print("\nObjects after add_object:", objects)  # Print object list
    return jsonify(new_object), 201

# Endpoint to delete an object
@app.route('/objects/<int:id>', methods=['DELETE'])
def delete_object(id):
    if not validate_delete_object(objects, id):
        return jsonify({'error': 'Object not found'}), 404
    objects[:] = [obj for obj in objects if obj['id'] != id]
    print("\nObjects after delete_object:", objects)  # Print object list
    return jsonify({'message': 'Object deleted successfully'})


# Unit tests
class TestBackendAPI(unittest.TestCase):

    def test_get_object(self):
        with app.test_client() as client:
            # Try to get an object with ID 0
            response = client.get('/objects/0')
            if response.status_code == 200:
                data = json.loads(response.data)
                self.assertEqual(data['id'], 0)
            else:
                self.assertEqual(response.status_code, 404)

    def test_add_object(self):
        with app.test_client() as client:
            data = {'name': 'Test User', 'email': 'test@example.com', 'phone': '12345678'}
            response = client.post('/objects', json=data)
            self.assertEqual(response.status_code, 201)
            new_object = json.loads(response.data)
            self.assertIn('id', new_object)

    def test_delete_object(self):
        with app.test_client() as client:
            response = client.delete('/objects/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'deleted successfully', response.data)

if __name__ == '__main__':
    unittest.main()
