import utils 
from utils import collection
import streamlit as st
import pymongo



def main():
    st.title("Mon application de recherche de films")
    longest = utils.longest_movie(collection)
    st.write(longest)

    
    st.write("# Meilleurs films par genre")
    # récupération des genres disponibles dans la collection
    genres = collection.distinct("genre")
    # affichage des genres sous forme de liste déroulante dans Streamlit
    genre = st.selectbox("Choisissez un genre :", genres)
    n = st.number_input("Nombre de résultats à afficher", min_value=1, max_value=50, value=10, step=1)
    st.write(utils.top_movies_by_genre(genre, n))



if __name__ == "__main__":
    main()

