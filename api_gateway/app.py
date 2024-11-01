import requests

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SERVICES = {
    'user_service': 'http://127.0.0.1:5001',
    'pet_service': 'http://127.0.0.1:5002',
    'appointment_service': 'http://127.0.0.1:5003',
    'veterinarian_service': 'http://127.0.0.1:5004',
    'billing_service': 'http://127.0.0.1:5005'
}

@app.route('/<service>/<path:path>', methods = ['GET', 'POST'])
def proxy(service, path):
    req_method = request.method
    url = f'{SERVICES[service]}/{path}'
    
    if req_method == 'GET':
        resp = requests.request(method = req_method, url = url)
    
    else:
        resp = requests.request(method = request.method, url = url, json = request.get_json())
    
    return (resp.content, resp.status_code)

if __name__ == '__main__':
    app.run(port = 5000, debug = True)