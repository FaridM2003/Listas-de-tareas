from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Archivo donde se guardarán los datos (sin extensión)
FILE_NAME = "datos_guardados"

@app.route('/')
def index():
    return render_template("index.html")
    
# Función para cargar los datos desde el archivo
def cargar_datos():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return file.read().splitlines()

# Función para guardar los datos en el archivo
def guardar_datos(datos):
    with open(FILE_NAME, "w") as file:
        file.write("\n".join(datos))

# Ruta para obtener todos los datos
@app.route("/datos", methods=["GET"])
def obtener_datos():
    datos = cargar_datos()
    return jsonify(datos), 200

# Ruta para agregar un nuevo dato
@app.route("/datos", methods=["POST"])
def agregar_dato():
    nuevo_dato = request.json.get("dato")
    if not nuevo_dato:
        return jsonify({"error": "El campo 'dato' es obligatorio."}), 400

    datos = cargar_datos()
    datos.append(nuevo_dato)
    guardar_datos(datos)
    return jsonify({"mensaje": "Dato agregado correctamente."}), 201

# Ruta para borrar un dato específico
@app.route("/datos/<string:dato>", methods=["DELETE"])
def borrar_dato(dato):
    datos = cargar_datos()
    if dato not in datos:
        return jsonify({"error": "El dato no existe en la lista."}), 404

    datos.remove(dato)
    guardar_datos(datos)
    return jsonify({"mensaje": "Dato borrado correctamente."}), 200

#Buscar los datos especificos
@app.route("/datos/buscar", methods=["GET"])
def buscar_dato():
    consulta = request.args.get("q", "")
    if not consulta:
        return jsonify({"error": "La consulta de búsqueda está vacía."}), 400

    datos = cargar_datos()
    resultados = [dato for dato in datos if consulta.lower() in dato.lower()]

    return jsonify(resultados), 200


if __name__ == "__main__":
    app.run(debug=True)
