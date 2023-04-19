import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import re


load_dotenv()
ATLAS_KEY = os.getenv('ATLAS_KEY')


ATLAS_KEY = os.getenv('ATLAS_KEY')
client = MongoClient(ATLAS_KEY,socketTimeoutMS=5000)
db = client.Db_scraped_IMDB
collection = db.Db_film


def longest_movie(collection) -> str:
        longest_movie = collection.find_one(sort=[("durée", pymongo.DESCENDING)])
        return "Le film le plus long est : ' {} ' avec une durée de {} minutes.".format(longest_movie["titre_original"], longest_movie["durée"])


def top_film_note(collection)-> str:
    top_rated = collection.find().sort([("score", pymongo.DESCENDING)]).limit(5)
    top_movies = [movie["titre_original"] for movie in top_rated]
    return "Les cinq meilleurs films sont : {}".format (top_movies)


def count_movies(actor: str) -> str:
        count = collection.count_documents({"acteurs": {"$regex": actor}})
        return "L'acteur ' {} ' a joué dans {} films".format (actor,count)


def top_movies_by_genre(genre: str, n: int) -> str:
        top_movies = collection.find({"genre": {"$regex": genre}}).sort([("score", pymongo.DESCENDING)]).limit(n)
        movie_titles = [movie["titre_original"] for movie in top_movies]
        result = "Les {} meilleurs films de genre ' {} ' sont:\n".format(n, genre)
        for i, title in enumerate(movie_titles):
            result += "{} - {}\n".format(i+1, title)  
        return result


def percentage_by_country(country: str, n: int) -> str:
        top_rated = list(collection.find().sort([("score", pymongo.DESCENDING)]).limit(n))
        total_count = len(top_rated)
        count_by_country = collection.count_documents({"pays": {"$regex": country}, "_id": {"$in": [movie["_id"] for movie in top_rated]}})
        percentage = count_by_country / total_count * 100
        return f"Parmi les {n} films les mieux notés, {percentage:.2f}% sont de {country}."


def average_time_by_genre(collection) -> str:
        result = ""
        genres = collection.distinct("genre")
        for genre in genres:
            time_list = [movie["durée"] for movie in collection.find({"genre": {"$regex": genre}})]
            if time_list:
                average_runtime = sum(time_list) / len(time_list)
                result += f"La durée moyenne d'un film de genre {genre} est de {average_runtime:.2f} minutes.\n"
        return result


def longest_movies_by_genre(genre: str, n: int) -> str:
        top_movies = collection.find({"genre": {"$regex": genre}}).sort([("durée", pymongo.DESCENDING)]).limit(n)
        movie_titles = [movie["titre_original"] for movie in top_movies]
        result = f"Les {n} films les plus longs de genre '{genre}' sont : \n"
        for i, title in enumerate(movie_titles):
            result += f"{i+1}. {title}\n"
        return result


def cost_per_minute_by_genre(genre):
        genre_movies = [movie for movie in collection.find({"genre": genre})]
        total_budget = 0
        total_runtime = 0
        for movie in genre_movies:
            budget_str = movie["budget"]
            if budget_str is None:
                continue
            budget_str = budget_str.split()[0].replace(",", "")
            budget_str = re.sub('[^0-9]', '', budget_str)  # extract only digits
            if not budget_str.isdigit():  # check if the string contains only digits
                continue
            budget = int(budget_str)
            runtime = int(movie["durée"])
            total_budget += budget
            total_runtime += runtime
        cost_per_minute = total_budget / (total_runtime // 60)
        return cost_per_minute

