import os

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret_key'

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True, nullable = False)
    password = db.Column(db.String(200), nullable = False)

@app.route('/register', methods = ['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    
    new_user = User(username = username, password = password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'message': 'User Registered'
    }), 201

@app.route('/login', methods = ['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username = username, password = password).first()
    
    if user:
        access_token = create_access_token(identity = user.id)
        
        return jsonify(access_token = access_token), 200
    
    return jsonify({
        'message': 'Invalid Credentials'
    }), 401

@app.route('/users', methods = ['GET'])
def get_users():
    users = User.query.all()
    
    return jsonify([{
        'id': user.id,
        'name': user.username
    } for user in users]), 200

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('user_db.sqlite3'):
            db.create_all()
    
    app.run(port = 5001, debug = True)