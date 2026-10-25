
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de ventas",
    layout="wide"
)

@st.cache_data
def cargar_datos(ruta):
    df = pd.read_excel(ruta)

    df["Fecha"] = pd.to_datetime(
        df["Fecha"],
        errors="coerce",
        dayfirst=True
    )

    df["Mes"] = df["Fecha"].dt.to_period("M").astype(str)

    return df


# Cargar el archivo Excel
df = cargar_datos(
    r"D:\DATA\proyectos26\pyprueba\venta.xlsx"
)

st.title("📊 Dashboard de ventas")

# Indicadores principales
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Facturación total",
        f"${df['Total_Venta'].sum():,.2f}"
    )

with col2:
    st.metric(
        "Unidades vendidas",
        int(df["Cantidad"].sum())
    )

with col3:
    st.metric(
        "Clientes diferentes",
        df["ID_Cliente"].nunique()
    )

# Gráfico 1: productos más vendidos
st.subheader("Productos más vendidos")

ventas_producto = (
    df.groupby("Producto", as_index=False)["Cantidad"]
    .sum()
    .sort_values("Cantidad", ascending=False)
)

figura1 = px.bar(
    ventas_producto,
    x="Producto",
    y="Cantidad",
    title="Unidades vendidas por producto",
    color="Cantidad"
)

st.plotly_chart(figura1, use_container_width=True)

# Gráfico 2: facturación mensual
st.subheader("Facturación mensual")

ventas_mes = (
    df.groupby("Mes", as_index=False)["Total_Venta"]
    .sum()
    .sort_values("Mes")
)

figura2 = px.line(
    ventas_mes,
    x="Mes",
    y="Total_Venta",
    markers=True,
    title="Evolución de las ventas mensuales"
)

st.plotly_chart(figura2, use_container_width=True)

# Mostrar la tabla completa
st.subheader("Datos completos de ventas")
st.dataframe(df, use_container_width=True)
