from src.cargar_archivos import load_data
from src.preguntas import pregunta_1, pregunta_2, pregunta_3,pregunta_4,pregunta_5

def main():
    print("[DEBUG] main.py ejecutándose...")
    print("[DEBUG] Ejecutando desde __main__")

    df_productos, df_ventas = load_data("datos/productos.csv", "datos/ventas.csv")

    print("[DEBUG] Entrando en función main()")
    productos_p1 = pregunta_1(df_productos, df_ventas)
    productos_p2 = pregunta_2(df_productos, df_ventas)
    pregunta_3(df_ventas, productos_p1, productos_p2)
    pregunta_4(df_ventas)
    pregunta_5(df_productos, df_ventas)
    
    
if __name__ == "__main__":
    main()
