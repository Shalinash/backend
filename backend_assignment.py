from flask import Flask, request, jsonify 
import logging
import unittest
import json

app = Flask(__name__)

# Logging configuration
logging.basicConfig(filename='backend.log', level=logging.INFO)

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

# Endpoint to get an object by ID
@app.route('/objects/<id>', methods=['GET'])
def get_object(id):
    obj = next((obj for obj in objects if obj['id'] == int(id)), None)
    if obj:
        return jsonify(obj)
    return jsonify({'error': 'Object not found'}), 404

# Endpoint to add a new object
@app.route('/objects', methods=['POST'])
def add_object():
    data = request.json
    if not validate_add_object(data):
        return jsonify({'error': 'Invalid request data'}), 400
    new_object = {
        'id': len(objects),
        'name': data['name'],
        'email': data['email'],
        'phone': data['phone']
    }
    objects.append(new_object)
    return jsonify(new_object), 201

# Endpoint to delete an object
@app.route('/objects/<int:id>', methods=['DELETE'])
def delete_object(id):
    if not validate_delete_object(objects, id):
        return jsonify({'error': 'Object not found'}), 404
    objects[:] = [obj for obj in objects if obj['id'] != id]
    return jsonify({'message': 'Object deleted successfully'})

# Unit tests
class TestBackendAPI(unittest.TestCase):

    def setUp(self):
        print("\n Objects before test:", objects)

    def tearDown(self):
        print("\n Objects after test:", objects)

    def test_get_object(self):
        with app.test_client() as client:
            # Try to get an object with ID 1
            response = client.get('/objects/1')
            if response.status_code == 200:
                data = json.loads(response.data)
                self.assertEqual(data['id'], 1)
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
    # Hardcoded list of JSON objects
    objects = [
        {"id": 0, "name": "Amy", "email": "amy@email.com", "phone": "00000000"},
        {"id": 1, "name": "Ben", "email": "ben@email.com", "phone": "11111111"},
    ]
    unittest.main()
