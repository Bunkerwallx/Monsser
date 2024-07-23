from src.scraper import obtener_titulo, obtener_subdominios, obtener_elementos, obtener_metadatos, obtener_tecnologias
from src.database import guardar_informacion

def main():
    url = "https://www.ejemplo.com/"
    titulo = obtener_titulo(url)
    subdominios = obtener_subdominios(url)
    elementos = obtener_elementos(url)
    metadatos = obtener_metadatos(url)
    tecnologias = obtener_tecnologias(url)

    # Imprimir resultados
    print(f"**Título:** {titulo}")
    print(f"**Subdominios:** {', '.join(subdominios)}")
    print(f"**Elementos de interés:** {', '.join(elementos)}")
    print(f"**Metadatos:** {', '.join(metadatos)}")
    print(f"**Tecnologías:** {', '.join(tecnologias)}")

    # Guardar en base de datos
    guardar_informacion(url, titulo, subdominios, elementos, metadatos, tecnologias)

if __name__ == "__main__":
    main()
