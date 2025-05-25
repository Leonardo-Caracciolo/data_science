import pandas as pd
import logging
from src.utils import guardar_csv, escribir_txt

logger = logging.getLogger(__name__)

def filtrar_productos_vendidos_en_mas_del_80_por_ciento_de_pdv(df_productos: pd.DataFrame, df_ventas: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna productos vendidos en al menos el 80% de los puntos de venta.
    """
    df = df_ventas.dropna(subset=["codigo_barras", "pdv_codigo"])
    total_pdv = df["pdv_codigo"].nunique()
    producto_pdv_count = df.groupby("codigo_barras")["pdv_codigo"].nunique()
    umbral = 0.8 * total_pdv
    productos_80 = producto_pdv_count[producto_pdv_count >= umbral].index.tolist()
    productos_filtrados = df_productos[df_productos["codigo_barras"].isin(productos_80)]
    guardar_csv(productos_filtrados, "pregunta_1_productos_80_por_ciento.csv")
    logger.info("✔ Pregunta 1: %d productos vendidos en al menos el 80%% de los PDV.", len(productos_filtrados))
    return productos_filtrados


def obtener_productos_que_representan_el_80_por_ciento_del_volumen(df_productos: pd.DataFrame, df_ventas: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica regla de Pareto: productos que representan el 80% del volumen (litros).
    """
    df = df_ventas.merge(df_productos[["codigo_barras", "contenido"]], on="codigo_barras")
    df["litros"] = (df["cant_vta"] * df["contenido"]) / 1000
    ventas_litros = df.groupby("codigo_barras")["litros"].sum().reset_index()
    ventas_litros = ventas_litros.sort_values(by="litros", ascending=False)
    ventas_litros["litros_pct"] = ventas_litros["litros"] / ventas_litros["litros"].sum()
    ventas_litros["litros_acum"] = ventas_litros["litros_pct"].cumsum()
    productos_pareto = ventas_litros[ventas_litros["litros_acum"] <= 0.8]
    guardar_csv(productos_pareto, "pregunta_2_productos_pareto.csv")
    logger.info("✔ Pregunta 2: %d productos representan el 80%% del volumen.", len(productos_pareto))
    return productos_pareto


def calcular_frecuencia_de_venta_por_producto_y_pdv(df_ventas: pd.DataFrame, productos_p1: pd.DataFrame, productos_p2: pd.DataFrame) -> pd.DataFrame:
    """
    Determina para cada producto en común el PDV donde más frecuentemente se vendió.
    """
    productos_comunes = set(productos_p1["codigo_barras"]) & set(productos_p2["codigo_barras"])
    df_filtrado = df_ventas[df_ventas["codigo_barras"].isin(productos_comunes)]
    dias_abiertos = df_filtrado.groupby("pdv_codigo")["fecha_comercial"].nunique().reset_index(name="dias_abierto")
    dias_con_venta = df_filtrado.groupby(["codigo_barras", "pdv_codigo"])["fecha_comercial"].nunique().reset_index(name="dias_con_venta")
    df_frecuencia = dias_con_venta.merge(dias_abiertos, on="pdv_codigo")
    df_frecuencia["frecuencia"] = df_frecuencia["dias_abierto"] / df_frecuencia["dias_con_venta"]
    idx = df_frecuencia.groupby("codigo_barras")["frecuencia"].idxmin()
    resultado = df_frecuencia.loc[idx, ["codigo_barras", "pdv_codigo", "frecuencia"]]
    guardar_csv(resultado, "pregunta_3_frecuencia_por_producto.csv")
    logger.info("✔ Pregunta 3: %d productos con frecuencia calculada.", len(resultado))
    return resultado


def calcular_variacion_ventas_entre_periodos(df_ventas: pd.DataFrame) -> float:
    """
    Calcula la variación porcentual de ventas entre dos trimestres y guarda un reporte.
    """
    df_ventas["fecha_comercial"] = pd.to_datetime(df_ventas["fecha_comercial"])
    p1 = df_ventas[(df_ventas["fecha_comercial"] >= "2020-06-01") & (df_ventas["fecha_comercial"] <= "2020-08-31")]
    p2 = df_ventas[(df_ventas["fecha_comercial"] >= "2020-09-01") & (df_ventas["fecha_comercial"] <= "2020-11-30")]
    total_1 = p1["cant_vta"].sum()
    total_2 = p2["cant_vta"].sum()
    variacion = ((total_2 - total_1) / total_1) * 100 if total_1 else float("inf")

    reporte = (
        f"📊 Variación de ventas\n\n"
        f"Junio-Agosto: {total_1:,.0f} unidades\n"
        f"Septiembre-Noviembre: {total_2:,.0f} unidades\n"
        f"📈 Variación porcentual: {variacion:+.2f}%\n"
    )
    escribir_txt(reporte, "pregunta_4_variacion_ventas.txt")
    logger.info("✔ Pregunta 4: variación de %.2f%% entre trimestres.", variacion)
    return variacion


def analizar_crecimiento_ventas_producto_anana(df_productos: pd.DataFrame, df_ventas: pd.DataFrame) -> pd.DataFrame:
    """
    Evalúa el crecimiento del producto SALUS FRUTTE CERO ANANA 1,65L entre agosto y septiembre.
    """
    producto = df_productos[df_productos["descripcion"].str.contains("SALUS FRUTTE CERO ANANA 1,65L", case=False)]
    if producto.empty:
        logger.warning("❌ Pregunta 5: producto no encontrado.")
        return None

    codigo = producto["codigo_barras"].values[0]
    df = df_ventas[df_ventas["codigo_barras"] == codigo].copy()
    df["fecha_comercial"] = pd.to_datetime(df["fecha_comercial"])
    df["mes"] = df["fecha_comercial"].dt.to_period("M")
    resumen = df.groupby("mes")["cant_vta"].sum().reset_index()
    guardar_csv(resumen, "pregunta_5_ventas_producto_objetivo.csv")

    agosto = resumen[resumen["mes"] == "2020-08"]
    septiembre = resumen[resumen["mes"] == "2020-09"]
    cant_agosto = int(agosto["cant_vta"].values[0]) if not agosto.empty else 0
    cant_sept = int(septiembre["cant_vta"].values[0]) if not septiembre.empty else 0
    crecimiento = ((cant_sept - cant_agosto) / cant_agosto) * 100 if cant_agosto > 0 else float("inf")

    reporte = (
        f"🔍 Análisis de crecimiento – Producto Ananá\n\n"
        f"Agosto: {cant_agosto:,} unidades\n"
        f"Septiembre: {cant_sept:,} unidades\n"
        f"📈 Crecimiento: {crecimiento:+.2f}%\n"
    )
    escribir_txt(reporte, "pregunta_5_causa_crecimiento.txt")
    logger.info("✔ Pregunta 5: crecimiento en septiembre = %.2f%%", crecimiento)
    return resumen
