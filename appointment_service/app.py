import os

from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointment_db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pet_id = db.Column(db.Integer, nullable = False)
    date = db.Column(db.String(80), nullable = False)
    desc = db.Column(db.String(200))

@app.route('/appointments', methods = ['POST'])
def create_appointment():
    pet_id = request.json.get('pet_id')
    date = request.json.get('date')
    desc = request.json.get('desc')
    
    new_appointment = Appointment(pet_id = pet_id, date = date, desc = desc)
    db.session.add(new_appointment)
    db.session.commit()
    
    return jsonify({
        'message': 'Appointment Created'
    }), 201

@app.route('/appointments', methods = ['GET'])
def get_appointments():
    appointments = Appointment.query.all()
    
    return jsonify([{
        'id': appointment.id,
        'pet_id': appointment.pet_id,
        'date': appointment.date,
        'desc': appointment.desc
    } for appointment in appointments]), 200

if __name__ == '__main__':
    with app.app_context():
        if not os.path.exists('appointment_db.sqlite3'):
            db.create_all()
    
    app.run(port = 5003, debug = True)