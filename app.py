from flask import Flask, render_template, request, jsonify
import os, re, datetime
import db
from models import Book

app = Flask(__name__)

# Crear la base de datos y la tabla. Insertar 10 libros de prueba en la base de datos.
# Hacer esto solo una vez para evitar insertar los libros múltiples veces.
if not os.path.isfile('books.db'):
    db.connect()

# Ruta para la página principal
# Revisa la carpeta "template" para el archivo index.html
# Revisa la carpeta "static" para los archivos CSS y JS
@app.route("/")
def index():
    return render_template("index.html")

def es_valido(email):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    return bool(re.fullmatch(regex, email))

@app.route("/request", methods=['POST'])
@app.route("/request", methods=['POST'])
def postRequest():
    if not request.is_json:
        return jsonify({
            'status': '415',
            'res': 'fallido',
            'error': 'Tipo de medio no soportado. Por favor envíe JSON con Content-Type: application/json'
        }), 415

    req_data = request.get_json()
    email = req_data['email']
    if not es_valido(email):
        return jsonify({
            'status': '422',
            'res': 'fallido',
            'error': 'Formato de correo electrónico inválido. Por favor ingrese una dirección válida'
        })

    titulo = req_data['title']
    libros = [b.serialize() for b in db.view()]
    for libro in libros:
        if libro['title'] == titulo:
            return jsonify({
                'res': f'Error: ¡Ya existe un libro con el título {titulo} en la biblioteca!',
                'status': '404'
            })

    nuevo_libro = Book(db.getNewId(), True, titulo, datetime.datetime.now())
    db.insert(nuevo_libro)
    return jsonify({
        'res': nuevo_libro.serialize(),
        'status': '200',
        'msg': 'Libro creado exitosamente'
    })

@app.route('/request', methods=['GET'])
def getRequest():
    content_type = request.headers.get('Content-Type')
    libros = [b.serialize() for b in db.view()]
    if content_type == 'application/json':
        json = request.json
        for libro in libros:
            if libro['id'] == int(json['id']):
                return jsonify({
                    'res': libro,
                    'status': '200',
                    'msg': 'Consulta exitosa de libro por ID'
                })
        return jsonify({
            'error': f"Error: No se encontró el libro con ID '{json['id']}'",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
            'res': libros,
            'status': '200',
            'msg': 'Consulta exitosa de todos los libros en la biblioteca',
            'no_of_books': len(libros)
        })

@app.route('/request/<id>', methods=['GET'])
def getRequestId(id):
    req_args = request.view_args
    libros = [b.serialize() for b in db.view()]
    if req_args:
        for libro in libros:
            if libro['id'] == int(req_args['id']):
                return jsonify({
                    'res': libro,
                    'status': '200',
                    'msg': 'Consulta exitosa de libro por ID'
                })
        return jsonify({
            'error': f"Error: No se encontró el libro con ID '{req_args['id']}'",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
            'res': libros,
            'status': '200',
            'msg': 'Consulta exitosa de libro por ID',
            'no_of_books': len(libros)
        })

@app.route("/request", methods=['PUT'])
def putRequest():
    req_data = request.get_json()
    disponibilidad = req_data['available']
    titulo = req_data['title']
    el_id = req_data['id']
    libros = [b.serialize() for b in db.view()]
    for libro in libros:
        if libro['id'] == el_id:
            actualizado = Book(
                el_id,
                disponibilidad,
                titulo,
                datetime.datetime.now()
            )
            print('Libro actualizado: ', actualizado.serialize())
            db.update(actualizado)
            nuevos_libros = [b.serialize() for b in db.view()]
            print('Libros en biblioteca: ', nuevos_libros)
            return jsonify({
                'res': actualizado.serialize(),
                'status': '200',
                'msg': f'Libro con título {titulo} actualizado correctamente'
            })
    return jsonify({
        'res': f'Error: No se pudo actualizar el libro con título: {titulo}',
        'status': '404'
    })

@app.route('/request/<id>', methods=['DELETE'])
def deleteRequest(id):
    req_args = request.view_args
    print('req_args: ', req_args)
    libros = [b.serialize() for b in db.view()]
    if req_args:
        for libro in libros:
            if libro['id'] == int(req_args['id']):
                db.delete(libro['id'])
                libros_actualizados = [b.serialize() for b in db.view()]
                print('Libros actualizados: ', libros_actualizados)
                return jsonify({
                    'res': libros_actualizados,
                    'status': '200',
                    'msg': 'Libro eliminado correctamente por ID',
                    'no_of_books': len(libros_actualizados)
                })
    else:
        return jsonify({
            'error': "Error: No se envió el ID del libro",
            'res': '',
            'status': '404'
        })

if __name__ == '__main__':
    app.run()
