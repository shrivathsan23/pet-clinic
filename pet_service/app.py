import os

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pet_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    owner_id = db.Column(db.Integer, nullable = False)

@app.route('/pets', methods = ['POST'])
def add_pet():
    name = request.json.get('name')
    owner_id = request.json.get('owner_id')
    
    new_pet = Pet(name = name, owner_id = owner_id)
    db.session.add(new_pet)
    db.session.commit()
    
    return jsonify({
        'message': 'Pet Added'
    }), 201

@app.route('/pets', methods = ['GET'])
def get_pets():
    pets = Pet.query.all()
    
    return jsonify([{
        'id': pet.id,
        'name': pet.name,
        'owner_id': pet.owner_id
    } for pet in pets]), 200

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('pet_db.sqlite3'):
            db.create_all()
    
    app.run(port = 5002, debug = True)