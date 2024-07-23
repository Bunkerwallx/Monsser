



import logging
import numpy as np
from bs4 import BeautifulSoup
from requests import get
from scrapy import Selector
from wappalyzer import Wappalyzer
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding

# Configuración de logging
logging.basicConfig(level=logging.INFO, filename='mosser.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

# Cargar y preparar el modelo de clasificación
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

    modelo.save('text_classifier.h5')
    return modelo, tokenizer

def cargar_modelo():
    modelo = tf.keras.models.load_model('text_classifier.h5')
    tokenizer = Tokenizer(num_words=1000)
    return modelo, tokenizer

def clasificar_texto(texto, modelo, tokenizer):
    secuencia = tokenizer.texts_to_sequences([texto])
    secuencia_pad = pad_sequences(secuencia, maxlen=100)
    prediccion = modelo.predict(secuencia_pad)
    return 'Positivo' if prediccion[0] > 0.5 else 'Negativo'

def obtener_titulo(url):
    try:
        respuesta = get(url, headers={"User-Agent": "Mozilla/5.0"})
        respuesta.raise_for_status()
        sopa = BeautifulSoup(respuesta.content, "html.parser")
        return sopa.title.string.strip()
    except Exception as e:
        logging.error(f"Error al obtener el título de {url}: {e}")
        return None

def obtener_subdominios(url):
    subdominios = set()
    try:
        respuesta = get(url, headers={"User-Agent": "Mozilla/5.0"})
        respuesta.raise_for_status()
        selector = Selector(text=respuesta.text)
        for enlace in selector.css("a"):
            href = enlace.attrib.get("href")
            if href and "://" in href:
                subdominio = href.split("://")[1].split("/")[0]
                subdominios.add(subdominio)
    except Exception as e:
        logging.error(f"Error al obtener los subdominios de {url}: {e}")
    return subdominios

def obtener_elementos(url, modelo, tokenizer):
    elementos = []
    try:
        respuesta = get(url, headers={"User-Agent": "Mozilla/5.0"})
        respuesta.raise_for_status()
        selector = Selector(text=respuesta.text)
        for elemento in selector.css("p"):
            texto = elemento.get()
            if texto and len(texto) > 50:
                clasificacion = clasificar_texto(texto, modelo, tokenizer)
                elementos.append((texto, clasificacion))
    except Exception as e:
        logging.error(f"Error al obtener los elementos de {url}: {e}")
    return elementos

def obtener_metadatos(url):
    metadatos = {}
    try:
        respuesta = get(url, headers={"User-Agent": "Mozilla/5.0"})
        respuesta.raise_for_status()
        selector = Selector(text=respuesta.text)
        for meta in selector.css("meta"):
            nombre = meta.attrib.get("name")
            contenido = meta.attrib.get("content")
            if nombre and contenido:
                metadatos[nombre] = contenido
    except Exception as e:
        logging.error(f"Error al obtener los metadatos de {url}: {e}")
    return metadatos

def obtener_tecnologias(url):
    tecnologias = set()
    try:
        respuesta = get(url, headers={"User-Agent": "Mozilla/5.0"})
        respuesta.raise_for_status()
        wappalyzer = Wappalyzer.latest()
        tecnologias.update(wappalyzer.analyze(respuesta.content))
    except Exception as e:
        logging.error(f"Error al obtener las tecnologías de {url}: {e}")
    return tecnologias

def main():
    url = "https://www.ejemplo.com/"

    # Preparar o cargar el modelo
    try:
        modelo, tokenizer = cargar_modelo()
    except:
        modelo, tokenizer = preparar_modelo()

    titulo = obtener_titulo(url)
    subdominios = obtener_subdominios(url)
    elementos = obtener_elementos(url, modelo, tokenizer)
    metadatos = obtener_metadatos(url)
    tecnologias = obtener_tecnologias(url)

    # Imprimir resultados
    print(f"**Título:** {titulo}")
    print(f"**Subdominios:** {', '.join(subdominios)}")
    print(f"**Elementos de interés:** {', '.join([f'{text[:30]}... ({label})' for text, label in elementos])}")
    print(f"**Metadatos:** {', '.join(['%s: %s' % (k, v) for k, v in metadatos.items()])}")
    print(f"**Tecnologías:** {', '.join(tecnologias)}")

if __name__ == "__main__":
    main()
