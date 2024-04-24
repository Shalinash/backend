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

# Service class for handling object operations
class ObjectService:
    def get_object_by_id(self, object_id):
        print("\nObject after get_object; ", next((obj for obj in objects if obj['id'] == object_id), None)) # Print objects after getting 
        return next((obj for obj in objects if obj['id'] == object_id), None)

    def add_object(self, data):
        max_id = max(obj['id'] for obj in objects) if objects else -1
        new_object = {
            'id': max_id + 1,
            'name': data['name'],
            'email': data['email'],
            'phone': data['phone']
        }
        objects.append(new_object)
        print("\nObjects after add_object:", objects)  # Print object list after adding
        return new_object

    def delete_object(self, object_id):
        objects[:] = [obj for obj in objects if obj['id'] != object_id]
        print("\nObjects after delete_object:", objects)  # Print object list after deleting

object_service = ObjectService()

# Endpoint to get list of all objects
@app.route('/objects', methods=['GET'])
def get_all_objects():
    return jsonify(objects)

# Endpoint to get an object by ID
@app.route('/objects/<int:object_id>', methods=['GET'])
def get_object(object_id):
    obj = object_service.get_object_by_id(object_id)
    if obj:
        return jsonify(obj)
    return jsonify({'error': 'Object not found'}), 404

# Endpoint to add a new object
@app.route('/objects', methods=['POST'])
def add_object():
    data = request.json
    new_object = object_service.add_object(data)
    return jsonify(new_object), 201

# Endpoint to delete an object
@app.route('/objects/<int:object_id>', methods=['DELETE'])
def delete_object(object_id):
    object_service.delete_object(object_id)
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
