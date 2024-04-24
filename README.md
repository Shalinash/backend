# Deployed onto: 
http://shalinash.pythonanywhere.com/ 

# Get object by ID: 
curl http://shalinash.pythonanywhere.com/objects/0

# Get all objects: 
curl http://shalinash.pythonanywhere.com/objects

# Add object: 
curl -X POST -H "Content-Type: application/json" -d '{"name": "New User", "email": "new@example.com", "phone": "1234567890"}' http://shalinash.pythonanywhere.com/objects

# Delete object: 
curl -X DELETE http://shalinash.pythonanywhere.com/objects/1

# Hardcoded list of JSON objects
{"id": 0, "name": "Amy", "email": "amy@email.com", "phone": "00000000"},
{"id": 1, "name": "Ben", "email": "ben@email.com", "phone": "11111111"}
