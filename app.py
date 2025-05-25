import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_option("client.toolbarMode", "minimal")  # Oculta botón 'Deploy'
# Ocultar barra superior con botón "Deploy"
hide_streamlit_style = """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        button[kind="headerButton"] {display: none;}
        .stDeployButton {display: none;}
    </style>
"""

st.set_page_config(page_title="Prueba Técnica DS", layout="wide")

st.title("📊 Visualización de Resultados - Prueba Técnica Data Science")

# Pregunta 2 - Pareto
st.subheader("Pregunta 2: Top productos por volumen vendido (litros)")

try:
    
    df_pareto = pd.read_csv("output/pregunta_2_productos_pareto.csv")
    
    top_pareto = df_pareto.sort_values("litros", ascending=False).head(20)

    fig1, ax1 = plt.subplots(figsize=(20, 5))
    
    sns.barplot(data=top_pareto, x="codigo_barras", y="litros", ax=ax1, palette="Blues_r")
    
    ax1.set_title("Top productos por litros vendidos")
    
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha="right", fontsize=8)
    
    st.pyplot(fig1)
    
except Exception as e:
    
    st.warning("No se pudo cargar la salida de pregunta 2.")

# Pregunta 3 - Frecuencia
st.subheader("Pregunta 3: Frecuencia de venta por producto")

try:
    
    df_frec = pd.read_csv("output/pregunta_3_frecuencia_por_producto.csv")
    
    top_frec = df_frec.sort_values("frecuencia").head(20)

    fig2, ax2 = plt.subplots(figsize=(20, 5))
    
    sns.barplot(data=top_frec, x="codigo_barras", y="frecuencia", ax=ax2, palette="viridis")
    
    ax2.set_title("Top productos más frecuentes (menor frecuencia = más venta)")
    
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha="right", fontsize=8)
    
    st.pyplot(fig2)
    
except Exception as e:
    st.warning("No se pudo cargar la salida de pregunta 3.")

# Pregunta 4 - Variación de ventas
st.subheader("Pregunta 4: Variación de ventas entre períodos")

try:
    
    with open("output/pregunta_4_variacion_ventas.txt", encoding="utf-8") as f:
        
        st.text(f.read())
        
except FileNotFoundError:
    
    st.warning("No se encontró el archivo de variación de ventas.")

# Pregunta 5 - Crecimiento específico
st.subheader("Pregunta 5: Crecimiento de SALUS FRUTTE CERO ANANA 1.65L")

try:
    df_ventas_objetivo = pd.read_csv("output/pregunta_5_ventas_producto_objetivo.csv")
    
    df_ventas_objetivo["mes"] = df_ventas_objetivo["mes"].astype(str)

    fig3, ax3 = plt.subplots(figsize=(10, 4))
    
    sns.barplot(data=df_ventas_objetivo, x="mes", y="cant_vta", palette="rocket", ax=ax3)
    
    ax3.set_title("Ventas mensuales del producto")
    
    ax3.set_xlabel("Mes")
    
    ax3.set_ylabel("Unidades vendidas")
    
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=0, fontsize=9)
    
    st.pyplot(fig3)

    with open("output/pregunta_5_causa_crecimiento.txt", encoding="utf-8") as f:
        
        st.text(f.read())
        
except Exception:
    
    st.warning("No se pudieron cargar los resultados de la pregunta 5.")