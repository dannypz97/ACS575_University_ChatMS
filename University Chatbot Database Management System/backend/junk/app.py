from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data for demonstration purposes
admin_credentials = {'username': 'admin', 'password': 'admin123'}
staff_credentials = {'username': 'staff', 'password': 'staff123'}

# Sample model training function
def train_model(data):
    # Train model logic here
    return "Model trained successfully with data: " + data

# Authentication endpoints
@app.route('/login', methods=['POST'])
def login():
    user_type = request.json['user_type']
    username = request.json['username']
    password = request.json['password']

    if user_type == 'admin' and username == admin_credentials['username'] and password == admin_credentials['password']:
        return jsonify({'message': 'Admin login successful'}), 200
    elif user_type == 'staff' and username == staff_credentials['username'] and password == staff_credentials['password']:
        return jsonify({'message': 'Staff login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Data submission endpoints
@app.route('/submit_data', methods=['POST'])
def submit_data():
    user_type = request.json['user_type']
    data = request.json['data']

    if user_type == 'admin':
        # Logic to handle admin data submission
        return jsonify({'message': 'Admin data submitted successfully'}), 200
    elif user_type == 'staff':
        # Logic to handle staff data submission
        return jsonify({'message': 'Staff data submitted successfully'}), 200
    else:
        return jsonify({'message': 'Invalid user type'}), 400

# Chatbot interaction endpoint
@app.route('/chat', methods=['POST'])
def chat():
    user_type = request.json['user_type']
    message = request.json['message']

    if user_type == 'student':
        # Logic to interact with the chatbot
        response = "Chatbot response to student's message: " + message
        return jsonify({'response': response}), 200
    else:
        return jsonify({'message': 'Invalid user type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
