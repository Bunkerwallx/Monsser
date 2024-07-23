
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding

def preparar_modelo():
    # Datos de ejemplo (reemplaza con tus datos reales para entrenamiento)
    textos = ['ejemplo de texto positivo', 'otro ejemplo negativo']
    etiquetas = [1, 0]  # 1 para positivo, 0 para negativo

    tokenizer = Tokenizer(num_words=1000)
    tokenizer.fit_on_texts(textos)
    secuencias = tokenizer.texts_to_sequences(textos)
    X = pad_sequences(secuencias, maxlen=100)
    y = np.array(etiquetas)

    modelo = Sequential()
    modelo.add(Embedding(input_dim=1000, output_dim=64, input_length=100))
    modelo.add(LSTM(64))
    modelo.add(Dense(1, activation='sigmoid'))

    modelo.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    modelo.fit(X, y, epochs=5)

    modelo.save('model/text_classifier.h5')
    
    # Guardar configuración del tokenizer
    with open('model/tokenizer_config.json', 'w') as f:
        json.dump(tokenizer.to_json(), f)

    return modelo, tokenizer

def cargar_modelo():
    modelo = tf.keras.models.load_model('model/text_classifier.h5')
    with open('model/tokenizer_config.json') as f:
        tokenizer_json = json.load(f)
    tokenizer = Tokenizer.from_json(tokenizer_json)
    return modelo, tokenizer

def clasificar_texto(texto, modelo, tokenizer):
    secuencia = tokenizer.texts_to_sequences([texto])
    secuencia_pad = pad_sequences(secuencia, maxlen=100)
    prediccion = modelo.predict(secuencia_pad)
    return 'Positivo' if prediccion[0] > 0.5 else 'Negativo'
