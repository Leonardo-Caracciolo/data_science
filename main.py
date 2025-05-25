import logging
import pandas as pd
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.modelo_datos import (
    filtrar_productos_vendidos_en_mas_del_80_por_ciento_de_pdv,
    obtener_productos_que_representan_el_80_por_ciento_del_volumen,
    calcular_frecuencia_de_venta_por_producto_y_pdv,
    calcular_variacion_ventas_entre_periodos,
    analizar_crecimiento_ventas_producto_anana
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    logger.info("Inicio del análisis...")

    try:
        df_productos = pd.read_csv("datos/productos.csv")
        
        df_ventas = pd.read_csv("datos/ventas.csv")
        
    except FileNotFoundError as e:
        
        logger.error("Error al cargar archivos de datos: %s", e)
        
        return

    # Pregunta 1
    productos_filtrados_80 = filtrar_productos_vendidos_en_mas_del_80_por_ciento_de_pdv(df_productos, df_ventas)

    # Pregunta 2
    productos_pareto = obtener_productos_que_representan_el_80_por_ciento_del_volumen(df_productos, df_ventas)

    # Pregunta 3
    calcular_frecuencia_de_venta_por_producto_y_pdv(df_ventas, productos_filtrados_80, productos_pareto)

    # Pregunta 4
    variacion_trimestral = calcular_variacion_ventas_entre_periodos(df_ventas)
    
    logger.info("Variación de ventas entre trimestres: %.2f%%", variacion_trimestral)

    # Pregunta 5
    ventas_producto_anana = analizar_crecimiento_ventas_producto_anana(df_productos, df_ventas)
    
    if ventas_producto_anana is not None and not ventas_producto_anana.empty:
        
        logger.info("Resumen de crecimiento del producto Ananá generado correctamente.")
        
    else:
    
        logger.warning("❌No se generó el resumen de crecimiento del producto Ananá.")

    logger.info("✅Análisis finalizado.")

if __name__ == "__main__":
    main()
