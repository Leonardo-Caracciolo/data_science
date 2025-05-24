import pandas as pd

def load_data(productos_path, ventas_path):
    """
    Carga los datos de productos y ventas.
    """
    df_productos = pd.read_csv(productos_path)
    df_ventas = pd.read_csv(ventas_path, parse_dates=["fecha_comercial"])
    return df_productos, df_ventas
