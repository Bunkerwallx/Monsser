from scraping import obtener_titulo, obtener_subdominios, obtener_elementos, obtener_metadatos, obtener_tecnologias
from classification import cargar_modelo, clasificar_texto
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, filename='logs/mosser.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def main():
    url = "https://www.ejemplo.com/"
    
    # Cargar el modelo y el tokenizer
    modelo, tokenizer = cargar_modelo()

    # Obtener datos
    try:
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
        
    except Exception as e:
        logging.error(f"Error en el proceso principal: {e}")

if __name__ == "__main__":
    main()
