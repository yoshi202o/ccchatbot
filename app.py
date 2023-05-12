from flask import Flask , render_template , request , jsonify
import text_sentiment_prediction
from predict_bot_response import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# API escuchando los requerimientos POST y prediciendo sentimientos.
@app.route('/predict' , methods = ['POST'])
def predict():

    response = ""
    review = request.json.get('customer_review')
    if not review:
        response = {'status' : 'error',
                    'message' : 'Opinión vacía'}
    
    else:

        # Llamar al método de predicción 'predict' desde el módulo prediction.py.
        sentiment , path = text_sentiment_prediction.predict(review)
        response = {'status' : 'success',
                    'message' : 'Enviado',
                    'sentiment' : sentiment,
                    'path' : path}

    return jsonify(response)


# Crear una API para guardar la opinión, el usuario hace clic en el botón de guardar.
@app.route('/save' , methods = ['POST'])
def save():

    # Extraer la fecha, nombre del producto, opinión, y sentimiento asociado desde los datos JSON.
    date = request.json.get('date')
    product = request.json.get('product')
    review = request.json.get('review')
    sentiment = request.json.get('sentiment')

    # Crear una variable final separada por comas.
    data_entry = date + "," + product + "," + review + "," + sentiment

    # Abrir el archivo en el modo 'append'.
    f = open('./static/assets/datafiles/data_entry.csv' , 'a')

    # Registrar los datos en el archivo.
    f.write(data_entry + '\n')

    # Cerrar el archivo.
    f.close()

    # Devolver un mensaje de éxito.
    return jsonify({'status' : 'success' , 
                    'message' : 'Datos registrados'})


# Escribir una API para el chatbot.
@app.route("/bot-response", methods=["POST"])
def bot():
    # Obtener la entrada del usuario.
    input_text = request.json.get("user_bot_input_text")
   
    # Llamar al método para obtener la respuesta del bot.
    bot_res = bot_response(input_text)

    response = {
            "bot_response": bot_res
        }

    return jsonify(response)
     
if __name__ == '__main__':
    app.run(debug=True)