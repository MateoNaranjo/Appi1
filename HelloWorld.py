from flask import Flask, request

app = Flask(__name__)
 
@app.route('/espanol/')
@app.route('/espanol/<nombre>')
def saludo_espanol(nombre='Bryan'):
    return f"Hola, Bienvenido, {nombre}"
 
@app.route('/ingles/')
@app.route('/ingles/<nombre>')
def saludo_ingles(nombre='Bryan'):
    return f"Hello, Welcome, {nombre}"
 
 
@app.route('/frances/', methods=['post'])
@app.route('/frances/<nombre>', methods=['post'])  
def saludo_frances(nombre='Bryan'):
    return f"Bonjour, Bienvenue, {nombre}"
 
@app.post('/ruso/')
@app.post('/ruso/<nombre>')
def saludo_ruso(nombre='Bryan'):
    
    return f"Привет, Добро пожаловать"



if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
