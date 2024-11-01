import os

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///billing_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pet_id = db.Column(db.Integer, nullable = False)
    amount = db.Column(db.Float, nullable = False)

@app.route('/bills', methods = ['POST'])
def create_bill():
    pet_id = request.json.get('pet_id')
    amount = request.json.get('amount')

    new_bill = Bill(pet_id = pet_id, amount = amount)
    db.session.add(new_bill)
    db.session.commit()

    return jsonify({
        'message': 'Bill Created'
    }), 201

@app.route('/bills', methods = ['GET'])
def get_bills():
    bills = Bill.query.all()

    return jsonify([{
        'id': bill.id,
        'pet_id': bill.pet_id,
        'amount': bill.amount
    } for bill in bills]), 200

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('billing_db.sqlite3'):
            db.create_all()
    
    app.run(port = 5005, debug = True)