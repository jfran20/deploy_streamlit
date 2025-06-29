import streamlit as st
import pandas as pd
from firebase_admin import firestore
import json

key_dict = json.loads(st.secrets['textkey'])

db =  firestore.Client.from_service_account_json("/content/firebase_keys.json")
ref = list(db.collection(u'movies').stream())

@st.cache_data
def get_data():
  dic = list(map(lambda x: x.to_dict(), ref))
  df = pd.DataFrame(dic)
  return df

df = get_data()

@st.cache_data
def load_by_title(title):
  df_filtered = df[df["name"].str.contains(title,case=False)]
  return df_filtered

@st.cache_data
def load_by_director(director):
  df_filtered = df[df["director"]==director]
  return df_filtered

def create_movie(name,company,director,genre):
  doc_ref = db.collection(u'movies').add({
      u'name': name,
      u'company': company,
      u'director': director,
      u'genre': genre
  })


# SIDEBAR ===================
sidebar = st.sidebar
show_datasets = sidebar.checkbox("Mostrar todos las películas")
## Buscar por nombre de la película
movieSearch = sidebar.text_input("Nombre de la película")
search_by_title = sidebar.button("Buscar")
## Seleccionar director
selected_director = sidebar.selectbox("Seleccionar director",df["director"].unique())
search_by_director = sidebar.button("Filtrar director")
## Nuevo filme
sidebar.title('Agregar pelicula')
name = sidebar.text_input('Name:')
company = sidebar.selectbox("Company",df["company"].unique())
director = sidebar.selectbox("Director",df["director"].unique())
genre = sidebar.selectbox("Genre",df["genre"].unique())
crear = sidebar.button("Crear nuevo fillme")

# BODY ===================
st.title("Netflix app")


if show_datasets:
  st.dataframe(df)

if search_by_title:
  doc = load_by_title(movieSearch)
  count_row = doc.shape[0]
  st.write(f"Se encontraron {count_row} películas")
  st.dataframe(doc)

if search_by_director:
  doc = load_by_director(selected_director)
  count_row = doc.shape[0]
  st.write(f"Se encontraron {count_row} películas")
  st.dataframe(doc)

if crear:
  create_movie(name,company,director,genre)
  st.write('Se guardo correctamente la película')
