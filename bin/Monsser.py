from bs4 import BeautifulSoup
from requests import get
from scrapy import Selector
from wappalyzer import Wappalyzer
import logging

logging.basicConfig(level=logging.INFO, filename='mosser.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

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

def obtener_elementos(url):
    elementos = []
    try:
        respuesta = get(url, headers={"User-Agent": "Mozilla/5.0"})
        respuesta.raise_for_status()
        selector = Selector(text=respuesta.text)
        for elemento in selector.css("p"):
            texto = elemento.get()
            if texto and len(texto) > 50:
                elementos.append(texto)
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
