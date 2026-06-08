from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

# Conexión MongoDB Atlas
MONGO_URI = os.environ.get(
    "MONGO_URI",
    "mongodb+srv://anthonycastillopatron_db_user:contraseña123@cluster0.mrsxfnk.mongodb.net/?retryWrites=true&w=majority"
)

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

    coleccion.insert_one({
        "nombre": nombre,
        "completada": False
    })

    return redirect('/')


# Actualizar nombre de tarea
@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):

    nuevo_nombre = request.form['nuevo_nombre']

    coleccion.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"nombre": nuevo_nombre}}
    )

    return redirect('/')


# Marcar como completada
@app.route('/completar/<id>')
def completar(id):

    coleccion.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"completada": True}}
    )

    return redirect('/')

@app.route("/editar/<id>", methods=["POST"])
def editar(id):
    nuevo_nombre = request.form["nuevo_nombre"]

    tareas.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"nombre": nuevo_nombre}}
    )

    return redirect("/")
    
# Eliminar tarea
@app.route('/eliminar/<id>')
def eliminar(id):

    coleccion.delete_one(
        {"_id": ObjectId(id)}
    )

    return redirect('/')


# Ejecutar aplicación
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
