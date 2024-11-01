import os

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///veterinarian_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Veterinarian(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)

@app.route('/veterinarians', methods = ['POST'])
def add_veterinarian():
    name = request.json.get('name')

    new_vet = Veterinarian(name = name)
    db.session.add(new_vet)
    db.session.commit()

    return jsonify({
        'message': 'Veterinarian Added'
    }), 201

@app.route('/veterinarians', methods = ['GET'])
def get_veterinarians():
    vets = Veterinarian.query.all()

    return jsonify([{
        'id': vet.id,
        'name': vet.name
    } for vet in vets]), 200

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('veterinarian_db.sqlite3'):
            db.create_all()
    
    app.run(port = 5004, debug = True)