import streamlit as st
from conexion import cargar_datos
from indicadores import *
from graficos import *


df= cargar_datos() #utilizando la funcion que nos devuelve el dataframe

#---------------------------------------------------------
#configuracion de dashboard con streamlit
st.set_page_config(page_title = "Wigo Motors", 
                   layout="wide")      # Configuración de la pestaña / ajuste de pantalla


st.title("WIGO MOTORS S.A.C.")
st.subheader("By: Elena Ramos")                       # NOMBRE
st.subheader("Buscador comercial de vehículos")       # SUB TÍTULO 


#LABORATORIO 3

st.sidebar.header("Filtros")

# Copia del DataFrame
df_filtrado = df.copy()

# ==========================
# FILTRO 1 - MARCA
# ==========================
marca = st.sidebar.selectbox(
    "Marca",
    ["Todas"] + sorted(df["marca"].dropna().unique().tolist())
)

if marca != "Todas":
    df_filtrado = df_filtrado[df_filtrado["marca"] == marca]


# ==========================
# FILTRO 2 - SEDE
# ==========================
sede = st.sidebar.selectbox(
    "Sede",
    ["Todas"] + sorted(df["tienda"].dropna().unique().tolist())
)

if sede != "Todas":
    df_filtrado = df_filtrado[df_filtrado["tienda"] == sede]


# ==========================
# FILTRO 3 - ASESOR
# ==========================
asesor = st.sidebar.selectbox(
    "Asesor comercial",
    ["Todos"] + sorted(df["asesor_comercial"].dropna().unique().tolist())
)

if asesor != "Todos":
    df_filtrado = df_filtrado[df_filtrado["asesor_comercial"] == asesor]


# ==========================
# FILTRO 4 - MÉTODO DE PAGO
# ==========================
metodo = st.sidebar.selectbox(
    "Método de pago",
    ["Todos"] + sorted(df["metodo_pago"].dropna().unique().tolist())
)

if metodo != "Todos":
    df_filtrado = df_filtrado[df_filtrado["metodo_pago"] == metodo]


precio_min = int(df_filtrado["precio_venta"].min())
precio_max = int(df_filtrado["precio_venta"].max())

rango = st.sidebar.slider(
    "Rango de precio",
    min_value=precio_min,
    max_value=precio_max,
    value=(precio_min, precio_max)
)

df_filtrado = df_filtrado[
    (df_filtrado["precio_venta"] >= rango[0]) &
    (df_filtrado["precio_venta"] <= rango[1])
]


#MOSTRAR RESULTADOS
st.success(f"Registros encontrados: {len(df_filtrado)}")
st.dataframe(df_filtrado)


#INDICADORES GENERALES:
st.subheader("Indicadores:")

c1, c2, c3, c4 = st.columns(4)  


c1.metric("Precio Total",f"S/{precio_total(df_filtrado):,.2f}") 
c2.metric("Unidades vendidas",f"{unidades_vendidas(df_filtrado)}") 
c3.metric("Precio Promedio",f"S/{precio_promedio(df_filtrado):,.2f}") 
c4.metric("Operaciones", operaciones(df_filtrado))


c5, c6, c7, c8 = st.columns(4)  

c5.metric("Precio más alto", f"S/{precio_maximo(df_filtrado):,.2f}")
c6.metric("Precio más bajo", f"S/{precio_minimo(df_filtrado):,.2f}")

#GRAFICOS = DASHBOARD

st.plotly_chart(grafico_ventas(df_filtrado))
st.plotly_chart(grafico_promedio(df_filtrado))
