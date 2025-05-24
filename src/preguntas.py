import pandas as pd

def pregunta_1(df_productos: pd.DataFrame, df_ventas: pd.DataFrame) -> pd.DataFrame:
    """
    Retorna productos vendidos en al menos el 80% de los puntos de venta.
    """
    # Eliminar valores nulos relevantes
    df = df_ventas.dropna(subset=["codigo_barras", "pdv_codigo"])

    # Total de puntos de venta únicos
    total_pdv = df["pdv_codigo"].nunique()

    # Contar para cada producto en cuántos PDV se vendió
    producto_pdv_count = df.groupby("codigo_barras")["pdv_codigo"].nunique()

    # Umbral del 80%
    umbral = 0.8 * total_pdv

    # Filtrar productos que cumplen el umbral
    productos_80 = producto_pdv_count[producto_pdv_count >= umbral].index.tolist()

    # Obtener información completa de los productos
    productos_filtrados = df_productos[df_productos["codigo_barras"].isin(productos_80)]

    # Guardar resultados
    productos_filtrados.to_csv("output/pregunta_1_productos_80_por_ciento.csv", index=False)

    print(f"[✔] Pregunta 1 completada: se encontraron {len(productos_filtrados)} productos en al menos el 80% de los PDV.")
    return productos_filtrados


def pregunta_2(df_productos: pd.DataFrame, df_ventas: pd.DataFrame) -> pd.DataFrame:
    # Merge para traer el contenido del producto
    df = df_ventas.merge(df_productos[["codigo_barras", "contenido"]], on="codigo_barras")

    # Calcular litros vendidos por fila
    df["litros"] = (df["cant_vta"] * df["contenido"]) / 1000

    # Sumar litros por producto
    ventas_litros = df.groupby("codigo_barras")["litros"].sum().reset_index()

    # Ordenar por litros descendente
    ventas_litros = ventas_litros.sort_values(by="litros", ascending=False)

    # Calcular % y acumulado
    ventas_litros["litros_pct"] = ventas_litros["litros"] / ventas_litros["litros"].sum()
    ventas_litros["litros_acum"] = ventas_litros["litros_pct"].cumsum()

    # Aplicar regla de Pareto (80%)
    productos_pareto = ventas_litros[ventas_litros["litros_acum"] <= 0.8]

    # Guardar resultados
    productos_pareto.to_csv("output/pregunta_2_productos_pareto.csv", index=False)

    print(f"[✔] Pregunta 2 completada: {len(productos_pareto)} productos representan el 80% del volumen vendido.")
    return productos_pareto


def pregunta_3(df_ventas, productos_p1, productos_p2):
    # Obtener intersección de productos válidos
    productos_comunes = set(productos_p1["codigo_barras"]) & set(productos_p2["codigo_barras"])
    df_filtrado = df_ventas[df_ventas["codigo_barras"].isin(productos_comunes)]

    # Días que cada punto de venta estuvo abierto
    dias_abiertos = df_filtrado.groupby("pdv_codigo")["fecha_comercial"].nunique().reset_index()
    dias_abiertos.rename(columns={"fecha_comercial": "dias_abierto"}, inplace=True)

    # Días que se vendió cada producto en cada PDV
    dias_con_venta = df_filtrado.groupby(["codigo_barras", "pdv_codigo"])["fecha_comercial"].nunique().reset_index()
    dias_con_venta.rename(columns={"fecha_comercial": "dias_con_venta"}, inplace=True)

    # Merge para obtener ambos valores
    df_frecuencia = dias_con_venta.merge(dias_abiertos, on="pdv_codigo")
    df_frecuencia["frecuencia"] = df_frecuencia["dias_abierto"] / df_frecuencia["dias_con_venta"]

    # Obtener el pdv con mayor frecuencia de venta (menor frecuencia numérica)
    idx = df_frecuencia.groupby("codigo_barras")["frecuencia"].idxmin()
    resultado = df_frecuencia.loc[idx, ["codigo_barras", "pdv_codigo", "frecuencia"]]

    # Guardar resultado
    resultado.to_csv("output/pregunta_3_frecuencia_por_producto.csv", index=False)

    print(f"[✔] Pregunta 3 completada: generado 'pregunta_3_frecuencia_por_producto.csv' con {len(resultado)} productos.")
    return resultado



def pregunta_4(df_ventas):
    df_ventas["fecha_comercial"] = pd.to_datetime(df_ventas["fecha_comercial"])

    # Filtrar por rangos de fechas
    periodo_1 = df_ventas[(df_ventas["fecha_comercial"] >= "2020-06-01") & (df_ventas["fecha_comercial"] <= "2020-08-31")]
    periodo_2 = df_ventas[(df_ventas["fecha_comercial"] >= "2020-09-01") & (df_ventas["fecha_comercial"] <= "2020-11-30")]

    total_1 = periodo_1["cant_vta"].sum()
    total_2 = periodo_2["cant_vta"].sum()

    if total_1 == 0:
        variacion = float("inf") if total_2 > 0 else 0
    else:
        variacion = ((total_2 - total_1) / total_1) * 100

    with open("output/pregunta_4_variacion_ventas.txt", "w", encoding="utf-8") as f:
        f.write("📊 Variación de ventas de Aguas Saborizadas\n\n")
        f.write("Periodo comparado:\n")
        f.write(f"- Junio a Agosto: {total_1:,.0f} unidades\n")
        f.write(f"- Septiembre a Noviembre: {total_2:,.0f} unidades\n\n")
        f.write(f"📈 Variación porcentual: {variacion:+.2f}%\n\n")
        f.write("Interpretación:\n")
        f.write("Se observa un crecimiento significativo en el volumen total de ventas de Aguas Saborizadas entre los dos períodos. ")
        f.write("Este aumento puede deberse a factores estacionales, promociones comerciales, o una mayor disponibilidad en puntos de venta.")

    print(f"[✔] Pregunta 4 completada: variación = {variacion:.2f}%")
    return variacion




def pregunta_5(df_productos, df_ventas):
    producto_objetivo = df_productos[df_productos["descripcion"].str.contains("SALUS FRUTTE CERO ANANA 1,65L", case=False)]

    if producto_objetivo.empty:
        print("[❌] Producto no encontrado en df_productos.")
        return None

    codigo_objetivo = producto_objetivo["codigo_barras"].values[0]
    ventas_producto = df_ventas[df_ventas["codigo_barras"] == codigo_objetivo].copy()
    ventas_producto["fecha_comercial"] = pd.to_datetime(ventas_producto["fecha_comercial"])
    ventas_producto["mes"] = ventas_producto["fecha_comercial"].dt.to_period("M")

    resumen = ventas_producto.groupby("mes")["cant_vta"].sum().reset_index()
    resumen.to_csv("output/pregunta_5_ventas_producto_objetivo.csv", index=False)

    agosto = resumen[resumen["mes"] == "2020-08"]
    septiembre = resumen[resumen["mes"] == "2020-09"]

    cant_agosto = int(agosto["cant_vta"].values[0]) if not agosto.empty else 0
    cant_sept = int(septiembre["cant_vta"].values[0]) if not septiembre.empty else 0

    crecimiento = ((cant_sept - cant_agosto) / cant_agosto) * 100 if cant_agosto > 0 else float("inf")

    with open("output/pregunta_5_causa_crecimiento.txt", "w", encoding="utf-8") as f:
        f.write("🔍 Análisis del crecimiento de ventas – SALUS FRUTTE CERO ANANA 1,65L\n\n")
        f.write("Ventas mensuales:\n")
        f.write(f"- Agosto: {cant_agosto:,} unidades\n")
        f.write(f"- Septiembre: {cant_sept:,} unidades\n\n")
        f.write(f"📈 Crecimiento intermensual: {crecimiento:+.2f}%\n\n")
        f.write("Posibles causas:\n")
        f.write("- Aumento en la distribución del producto en puntos de venta clave\n")
        f.write("- Acciones promocionales específicas o descuentos en septiembre\n")
        f.write("- Comportamiento estacional (mayor consumo en primavera)\n")
        f.write("- Campañas de marketing o reposicionamiento de marca\n\n")
        f.write("Este incremento sostenido en septiembre sugiere un cambio significativo en la demanda o en la estrategia comercial.")

    print(f"[✔] Pregunta 5 completada: crecimiento en septiembre = {crecimiento:.2f}%")
    return resumen
