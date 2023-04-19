import utils 
from utils import collection
import streamlit as st



def main():
    st.title("Mon application de recherche de films")
    st.write("## Les plus longs films")
    longest = utils.longest_movie(collection)
    st.write(longest)


    st.write("## Les 5 films les mieux notés")
    top_film_note = utils.top_film_note(collection)
    st.write(top_film_note)

    st.write("## Dans combien de films a joué Morgan Freeman ? Tom Cruise ?.....")
    actor = collection.distinct("acteurs")
    # affichage des genres sous forme de liste déroulante dans Streamlit
    actor = st.selectbox("Choisissez un acteur :", actor)
    count_movies = utils.count_movies(actor)
    st.write(count_movies)


    st.write("## Meilleurs films par genre")
    # récupération des genres disponibles dans la collection
    genre = collection.distinct("genre")
    genre = st.selectbox("Choisissez le genre du film :", genre)
    n = st.number_input("Nombre de résultats à afficher", min_value=1, max_value=50, value=10, step=1)
    st.write(utils.top_movies_by_genre(genre, n))


    st.write("## Parmi les 100 films les mieux notés, quel pourcentage sont américains ? Français ?")
    pays = collection.distinct("pays")
    pays = st.selectbox("Choisissez un pays :", pays)
    n = st.number_input("Nombre de résultats à afficher", min_value=1, max_value=100, value=100, step=1)
    top_film_note = utils.percentage_by_country(pays,n)
    st.write(top_film_note)


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

