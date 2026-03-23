import json
import os
import hashlib

DATA_FILE = "data/users.json" # Path to the user data file

# Utility functions for authentication and data management
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load user data from file
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save user data to file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Authenticate user credentials
def authenticate_user(username, password):
    data = load_data()
    hashed = hash_password(password)
    if username in data and data[username]["password"] == hashed:
        return True, data[username]
    return False, None

# Register a new user
def register_user(username, password):
    data = load_data()
    if username in data:
        return False, "User already exists."
    
    data[username] = {
        "password": hash_password(password),
        "balance": 1000.0,
        "history": []
    }
    save_data(data)
    return True, "Account created!"