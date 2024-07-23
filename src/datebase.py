from sqlite3 import connect
import logging

def guardar_informacion(url, titulo, subdominios, elementos, metadatos, tecnologias):
    conexion = connect("mosser.db")
    cursor = conexion.cursor()
    try:
        cursor.execute("""
        INSERT INTO webs (url, titulo, subdominios, elementos, metadatos, tecnologias)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (url, titulo, ",".join(subdominios), ",".join(elementos), ",".join(f"{k}: {v}" for k, v in metadatos.items()), ",".join(tecnologias)))
        conexion.commit()
    except Exception as e:
        logging.error(f"Error al guardar la información de {url}: {e}")
    finally:
        conexion.close()
