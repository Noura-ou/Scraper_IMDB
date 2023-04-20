import utils 
from utils import collection
import streamlit as st


st.set_page_config(
        page_icon=":film_frames:",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def main():
    st.markdown("<h1 style='color: #256550 ; text-align:center;'> Mon application de recherche de films </h1>", unsafe_allow_html=True)
  
    st.markdown(f"<h2 style='color: green;'>Les plus longs films : </h2>", unsafe_allow_html=True)
    longest = utils.longest_movie(collection)
    st.write(longest)


    st.markdown(f"<h2 style='color: green;'>Les 5 films les mieux notés : </h2>", unsafe_allow_html=True)
    top_film_note = utils.top_film_note(collection)
    st.write(top_film_note)


    st.markdown(f"<h2 style='color: green;'> Dans combien de films a joué Morgan Freeman ? Tom Cruise ?..... </h2>", unsafe_allow_html=True)
    actor = collection.distinct("acteurs")
    # affichage des genres sous forme de liste déroulante dans Streamlit
    actor = st.selectbox("Choisissez un acteur :", actor)
    count_movies = utils.count_movies(actor)
    st.write(count_movies)


    st.markdown(f"<h2 style='color: green;'>Meilleurs films par genre : </h2>", unsafe_allow_html=True)
    # récupération des genres disponibles dans la collection
    genre = collection.distinct("genre")
    genre = st.selectbox("Choisissez le genre du film :", genre)
    n = st.number_input("Nombre de résultats à afficher", min_value=1, max_value=50, value=10, step=1)
    st.write(utils.top_movies_by_genre(genre, n))


    st.markdown(f"<h2 style='color: green;'>Parmi les 100 films les mieux notés, quel pourcentage sont américains ? Français ?.... </h2>", unsafe_allow_html=True)
    pays = collection.distinct("pays")
    pays = st.selectbox("Choisissez un pays :", pays)
    n = st.number_input("Nombre de résultats à afficher", min_value=1, max_value=100, value=100, step=1)
    top_film_note = utils.percentage_by_country(pays,n)
    st.write(top_film_note)


    st.markdown(f"<h2 style='color: green;'>La durée moyenne d’un film en fonction du genre :</h2>", unsafe_allow_html=True)
    genre = collection.distinct("genre")
    genre = st.selectbox("Choisissez un genre pour le film :", genre)
    average_time_by_genre = utils.average_time_by_genre(genre)
    st.write(average_time_by_genre)


    st.markdown(f"<h2 style='color: green;'>En fonction du genre, afficher la liste des films les plus longs : </h2>", unsafe_allow_html=True)
    genre = collection.distinct("genre")
    genre = st.selectbox("Choisissez un genre de film :", genre)
    n = st.number_input("Nombre de résultats à afficher", min_value=1, max_value=100, value=5, step=1)
    longest_movies_by_genre = utils.longest_movies_by_genre(genre,n)
    st.write(longest_movies_by_genre)


    st.markdown(f"<h2 style='color: green;'>En fonction du genre, quel est le coût de tournage d’une minute de film ? </h2>", unsafe_allow_html=True)
    genre = collection.distinct("genre")
    genre = st.selectbox("Choisissez un genre de film dont vous voulez calculer le coût de tournage d’une minute ! ", genre)
    cout_tournage = utils.cost_per_minute_by_genre(genre)
    st.write(cout_tournage)


    #st.sidebar.title("Menu de recherche")
    st.sidebar.markdown("<h4 style='font-size: 24px; color: #256550;'> Menu de filtre des films : </h4>", unsafe_allow_html=True)
    search_option = st.sidebar.radio(
    "Choisissez le type de recherche :", 
    ("Par titre", "Par genre", "Par durée", "Par note")
      )
    

    st.markdown(f"<h2 style='color: green;'> Filtrer les films en utilisant pluieurs filtres  : </h2>", unsafe_allow_html=True)
    # affichage des résultats en fonction du choix de recherche
    if search_option == "Par titre":
        titre_original = collection.distinct("titre_original")
        titre_original = st.selectbox("Choisissez le titre du film :", titre_original)
        result = utils.search_movie_by_title(titre_original)
        for movie in result[1]:
            st.markdown(f"<h5 style='color: green;'>La date de sortie du film : </h5>", unsafe_allow_html=True)
            st.write(movie["date"])
            st.markdown(f"<h5 style='color: green;'>Acteurs : </h5>", unsafe_allow_html=True)
            for actor in movie["acteurs"]:
                st.write(actor)
            st.markdown(f"<h5 style='color: green;'>Description : </h5>", unsafe_allow_html=True)
            st.write(movie["desciption"])
            st.markdown(f"<h5 style='color: green;'>La Durée du film :</h5>", unsafe_allow_html=True)
            st.write(movie["durée"])
            st.markdown(f"<h5 style='color: green;'>Le genre du film :</h5>", unsafe_allow_html=True)
            for genre in movie["genre"]:
                st.write(genre)
            st.markdown(f"<h5 style='color: green;'>Le score du film :</h5>", unsafe_allow_html=True)
            st.write(movie["score"])
            st.markdown(f"<h5 style='color: green;'>Le nombre de personnes ayant voté pour le film:</h5>", unsafe_allow_html=True)
            st.write(movie["nbr_votants"])
            st.markdown(f"<h5 style='color: green;'>Le pays du film:</h5>", unsafe_allow_html=True)
            for pays in movie["pays"]:
              st.write(pays)
            st.markdown(f"<h5 style='color: green;'>La langue d'origine du film:</h5>", unsafe_allow_html=True)
            for lng in movie["langue_d_origine"]:
               st.write(lng)
            st.markdown(f"<h5 style='color: green;'>Le Budget du film:</h5>", unsafe_allow_html=True)
            st.write(movie["budget"])



    elif search_option == "Par genre":
        genre = collection.distinct("genre")
        # affichage des genres sous forme de liste déroulante dans Streamlit
        genre = st.selectbox("Choisissez un genre du film :", genre)
        result = utils.search_movie_by_genre(genre)
        compteur = 1
        for movie in result:
            st.markdown(f"<h3 style='color:blue;'> Film {compteur}: {movie['titre_original']} </h3>", unsafe_allow_html=True)
            st.markdown(f"<h5 style='color: green;'>La date de sortie du film : </h5>", unsafe_allow_html=True)
            st.write(movie["date"])
            st.markdown(f"<h5 style='color: green;'>Acteurs : </h5>", unsafe_allow_html=True)
            for actor in movie["acteurs"]:
                st.write(actor)
            st.markdown(f"<h5 style='color: green;'>Description : </h5>", unsafe_allow_html=True)
            st.write(movie["desciption"])
            st.markdown(f"<h5 style='color: green;'>La Durée du film :</h5>", unsafe_allow_html=True)
            st.write(movie["durée"])
            st.markdown(f"<h5 style='color: green;'>Le score du film :</h5>", unsafe_allow_html=True)
            st.write(movie["score"])
            st.markdown(f"<h5 style='color: green;'>Le nombre de personnes ayant voté pour le film:</h5>", unsafe_allow_html=True)
            st.write(movie["nbr_votants"])
            st.markdown(f"<h5 style='color: green;'>Le pays du film:</h5>", unsafe_allow_html=True)
            for pays in movie["pays"]:
              st.write(pays)
            st.markdown(f"<h5 style='color: green;'>La langue d'origine du film:</h5>", unsafe_allow_html=True)
            for lng in movie["langue_d_origine"]:
               st.write(lng)
            st.markdown(f"<h5 style='color: green;'>Le Budget du film:</h5>", unsafe_allow_html=True)
            st.write(movie["budget"])
            compteur += 1


    elif search_option == "Par durée":
        # affichage d'un slider pour sélectionner une plage de durée pour les films
        min_duration, max_duration = st.slider("Sélectionnez une plage de durée (en minutes) :", 0, 400, (0, 400), 10)
        result = utils.search_movie_by_duration(min_duration, max_duration)
        compteur = 1
        if not result:
            st.write("Aucun film ne correspond à cette durée.")
        else:
            for movie in result:
                st.markdown(f"<h3 style='color:blue;'> Film {compteur}: {movie['titre_original']} </h3>", unsafe_allow_html=True)
                st.markdown(f"<h5 style='color: green;'>La date de sortie du film : </h5>", unsafe_allow_html=True)
                st.write(movie["date"])
                st.markdown(f"<h5 style='color: green;'>Acteurs : </h5>", unsafe_allow_html=True)
                st.markdown(f"<h5 style='color: green;'>La Durée du film :</h5>", unsafe_allow_html=True)
                st.write(movie["durée"])
                for actor in movie["acteurs"]:
                    st.write(actor)
                st.markdown(f"<h5 style='color: green;'>Description : </h5>", unsafe_allow_html=True)
                st.write(movie["desciption"])
                st.markdown(f"<h5 style='color: green;'>Le score du film :</h5>", unsafe_allow_html=True)
                st.write(movie["score"])
                st.markdown(f"<h5 style='color: green;'>Le nombre de personnes ayant voté pour le film:</h5>", unsafe_allow_html=True)
                st.write(movie["nbr_votants"])
                st.markdown(f"<h5 style='color: green;'>Le pays du film:</h5>", unsafe_allow_html=True)
                st.markdown(f"<h5 style='color: green;'>Le genre du film :</h5>", unsafe_allow_html=True)
                for genre in movie["genre"]:
                    st.write(genre)
                for pays in movie["pays"]:
                    st.write(pays)
                st.markdown(f"<h5 style='color: green;'>La langue d'origine du film:</h5>", unsafe_allow_html=True)
                for lng in movie["langue_d_origine"]:
                    st.write(lng)
                st.markdown(f"<h5 style='color: green;'>Le Budget du film:</h5>", unsafe_allow_html=True)
                st.write(movie["budget"])
                compteur += 1

    elif search_option == "Par note":
        min_rating = st.slider('Note minimale', 1, 10, 5, 1)
        utils.search_movie_by_rating(min_rating)




if __name__ == "__main__":
    main()

