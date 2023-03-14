import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import os
import numpy as np
import codecs

doc = 'https://firebasestorage.googleapis.com/v0/b/heroes-5bb27.appspot.com/o/datasets%2Ftracks.csv?alt=media&token=0c6da1bb-2f5a-4fd6-8c4a-1f78aa604901'


@st.cache
def load_data(nrows):
    data = pd.read_csv(doc, index_col=0, encoding='latin-1', nrows=nrows)
    return data


def load_data_bydirector(name):
    filtered_data_bydirector = data[data["artists"].str.contains(name)]
    return filtered_data_bydirector


def load_data_byname(name):
    filtered_data_byname = data[data["name"].str.upper().str.contains(name)]
    return filtered_data_byname


# --- PAGE CONFIG ---#
st.set_page_config(page_title="Spotify songs",
                   page_icon=":busts_in_silhouette:")
st.title("Spotify songs")

data = load_data(500)

# --- LOGO ---#
st.sidebar.image("credencial.jpg")
st.sidebar.write("Ruben Castillo Ramirez")
st.sidebar.write("zS20020314")
st.sidebar.markdown("##")

# --- SIDEBAR FILTERS ---#
if st.sidebar.checkbox("Mostrar todas las canciones"):
    st.write(data)

buscadorTitulo = st.sidebar.title("Titulo de canción")
buscador = st.sidebar.text_input("Titulo canción")
botonTitulo = st.sidebar.button("Buscar canción")

autor = st.sidebar.selectbox("Selecciona el nombre",
                             options=data['artists'].unique())
botonName = st.sidebar.button("Buscar por nombre")

# Para Scatter
save_data_for_Scatter = pd.DataFrame(data)
rng = np.random.RandomState(0)

save_data_for_Scatter_duration = save_data_for_Scatter['duration_ms'].astype(
    float)

save_data_for_Scatter_popularity = save_data_for_Scatter['popularity'].astype(
    float)

if st.sidebar.checkbox('Mostrar grafica de dispersión'):
    dataframe, axis = plt.subplots()
    axis.scatter(save_data_for_Scatter_duration,
                 save_data_for_Scatter_popularity,
                 color='blue',
                 alpha=0.4,
                 cmap='viridis')

    st.pyplot(dataframe)


# Para barras
# Agrupar los datos por género

save_data_for_Barras = pd.DataFrame(data)

save_data_for_Barras_duration = save_data_for_Barras['duration_ms'].astype(
    float)
save_data_for_Barras_name = save_data_for_Barras['name'].astype(
    str)

save_data_for_Barras_duration = np.array(
    save_data_for_Barras_duration)

save_data_for_Barras_name = np.array(
    save_data_for_Barras_name)

if st.sidebar.checkbox('Mostrar grafica de barras'):
    dataframe, axis = plt.subplots()
    axis.bar(save_data_for_Barras_name,
             save_data_for_Barras_duration, color='blue')
    axis.set_xlabel('Nombre')
    axis.set_ylabel('Duracion')
    axis.set_title('Duracion de música')

    st.pyplot(dataframe)

##### Guardar datos de episodios para el histograma ####################
save_data_forHistrograma = pd.DataFrame(data)

save_data_forHistrograma_ep = save_data_forHistrograma['popularity'].astype(
    float)
save_data_forHistrograma_ep = np.array(
    save_data_forHistrograma_ep).astype(float)

limite_Histograma = save_data_forHistrograma_ep.max()
limite_Histograma = int(limite_Histograma)

if st.sidebar.checkbox('Mostrar histograma'):
    mostrar = np.histogram(save_data_forHistrograma_ep, bins=limite_Histograma,
                           range=(save_data_forHistrograma_ep.min(),
                                  save_data_forHistrograma_ep.max()),
                           weights=None,
                           density=False)[0]
    st.bar_chart(mostrar)


if botonTitulo:
    filterbyname = load_data_byname(buscador.upper())
    rows = filterbyname.shape[0]
    st.dataframe(filterbyname)

if botonName:
    filterbyname = load_data_bydirector(autor)
    rows = filterbyname.shape[0]
    st.dataframe(filterbyname)
