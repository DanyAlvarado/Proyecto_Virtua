from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)
CORS(app)

# Configuración de MongoDB usando variables de entorno y nombre de servicio
MONGO_USER = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_PASS = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
# 'mongo' es el nombre del servicio en docker-compose
client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASS}@mongo:27017/")
db = client.planificador_viajes
trips_collection = db.viajes

@app.route('/trips', methods=['GET'])
def get_trips():
    trips = []
    for trip in trips_collection.find():
        trips.append({
            "id": str(trip["_id"]),
            "destino": trip["destino"],
            "fecha": trip["fecha"]
        })
    return jsonify(trips)

@app.route('/trips', methods=['POST'])
def add_trip():
    data = request.json
    nuevo_viaje = {
        "destino": data['destino'],
        "fecha": data['fecha']
    }
    result = trips_collection.insert_one(nuevo_viaje)
    return jsonify({"id": str(result.inserted_id), "status": "Viaje creado"}), 201

@app.route('/trips/<id>', methods=['PUT'])
def update_trip(id):
    data = request.json
    trips_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"destino": data['destino'], "fecha": data['fecha']}}
    )
    return jsonify({"status": "Viaje actualizado"})

@app.route('/trips/<id>', methods=['DELETE'])
def delete_trip(id):
    trips_collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"status": "Viaje eliminado"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)