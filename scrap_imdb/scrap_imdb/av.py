import utils 
import numpy as np
from utils import collection
import streamlit as st
import matplotlib.pyplot as plt
from pymongo import MongoClient




def main():
    st.title("Analyse des films sur IMDB")

    client = MongoClient("mongodb+srv://arnaudvila:xxxxxxxx@cluster0.mongodb.net/arnaud?retryWrites=true&w=majority")
    collection = client["arnaud"]["films"]

    st.write("## Les N films les mieux notés")
    n = st.number_input("Nombre de résultats à afficher", min_value=1, max_value=100, value=10, step=1)
    top_n_movies = utils.get_top_n_movies(collection, n)
    display_movies(top_n_movies)

    st.write("## Parmi les N films les mieux notés, quel pourcentage provient de chaque pays sélectionné ?")
    all_countries = collection.distinct("pays")
    selected_countries = st.multiselect("Choisissez des pays :", all_countries)
    n_country = st.number_input("Nombre de résultats à afficher pour les pays", min_value=1, max_value=100, value=100, step=1)

    percentages = []
    labels = []

    for country in selected_countries:
        percentage = utils.percentage_by_country(country, n_country)
        if not np.isnan(percentage):
            percentages.append(percentage)
            labels.append(country)

    if percentages and labels:
        fig, ax = plt.subplots()
        filtered_percentages = [p for p in percentages if not np.isnan(p)]
        ax.pie(filtered_percentages, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        st.pyplot(fig)
    else:
        st.write("Aucun pourcentage valide à afficher.")




    st.write("## la durée moyenne d’un film en fonction du genre")
    genre = collection.distinct("genre")
    genre = st.selectbox("Choisissez un genre pour le film :", genre)
    average_time_by_genre = utils.average_time_by_genre(genre)
    st.write(average_time_by_genre)


    st.write("## En fonction du genre, afficher la liste des films les plus longs.")
    genre = collection.distinct("genre")
    genre = st.selectbox("Choisissez un genre de film :", genre)
    n = st.number_input("Nombre de résultats à afficher", min_value=1, max_value=100, value=5, step=1)
    longest_movies_by_genre = utils.longest_movies_by_genre(genre,n)
    st.write(longest_movies_by_genre)


    st.write("## En fonction du genre, quel est le coût de tournage d’une minute de film ?")
    genre = collection.distinct("genre")
    genre = st.selectbox("Choisissez un genre de film dont vous voulez calculer le coût de tournage d’une minute ! ", genre)
    cout_tournage = utils.cost_per_minute_by_genre(genre)
    st.write(cout_tournage)


if __name__ == "__main__":
    main()
