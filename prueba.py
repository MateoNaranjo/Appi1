from flask import Flask


app = Flask(__name__)

@app.post('/')

def saludo_ingles():
    return "Hello, Welcome,"

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")