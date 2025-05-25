import os
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def guardar_csv(df: pd.DataFrame, nombre_archivo: str) -> None:
    """Guarda un DataFrame como CSV en la carpeta output."""
    try:
        os.makedirs("output", exist_ok=True)
        ruta = os.path.join("output", nombre_archivo)
        df.to_csv(ruta, index=False)
        logger.info("Archivo guardado correctamente: %s", ruta)
    except Exception as e:
        logger.error("Error al guardar archivo CSV '%s': %s", nombre_archivo, str(e))

def escribir_txt(texto: str, nombre_archivo: str) -> None:
    """Escribe contenido en un archivo .txt en la carpeta output."""
    try:
        os.makedirs("output", exist_ok=True)
        ruta = os.path.join("output", nombre_archivo)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(texto)
        logger.info("Archivo TXT guardado correctamente: %s", ruta)
    except Exception as e:
        logger.error("Error al escribir archivo TXT '%s': %s", nombre_archivo, str(e))

def formato_miles(valor) -> str:
    """Devuelve el número formateado con punto como separador de miles."""
    return f"{valor:,.0f}".replace(",", ".")
