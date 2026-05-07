from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# Conexión Mongo Atlas
MONGO_URI = "mongodb+srv://anthonycastillopatron_db_user:contraseña123@cluster0.mrsxfnk.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI)

db = client["sistema_tareas"]
coleccion = db["tareas"]


# Página principal
@app.route('/')
def index():

    pendientes = list(
        coleccion.find({"completada": False})
    )

    completadas = list(
        coleccion.find({"completada": True})
    )

    return render_template(
        'index.html',
        pendientes=pendientes,
        completadas=completadas
    )


# Agregar tarea
@app.route('/agregar', methods=['POST'])
def agregar():

    nombre = request.form['tarea']

    nueva_tarea = {
        "nombre": nombre,
        "completada": False
    }

    coleccion.insert_one(nueva_tarea)

    return redirect('/')


# Completar tarea
@app.route('/completar/<id>')
def completar(id):

    coleccion.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"completada": True}}
    )

    return redirect('/')


# Eliminar tarea
@app.route('/eliminar/<id>')
def eliminar(id):

    coleccion.delete_one(
        {"_id": ObjectId(id)}
    )

    return redirect('/')


# Ejecutar aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
