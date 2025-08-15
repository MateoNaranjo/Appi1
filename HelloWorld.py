from flask import Flask

app = Flask(__name__)

@app.route('/espanol/')
@app.route('/espanol/<nombre>')
def saludo_espanol(nombre='Bryan'):
    return f"Hola, Bienvenido, {nombre}"

@app.route('/ingles/')
@app.route('/ingles/<nombre>')
def saludo_ingles(nombre='Bryan'):
    return f"Hello, Welcome, {nombre}"


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=53)
