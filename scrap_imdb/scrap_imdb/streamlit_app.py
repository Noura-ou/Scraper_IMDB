import pipelines 
import streamlit as st

pipeline = pipelines.ScrapImdbPipeline()

def main():
    st.title("Mon application de recherche de films")

    longest = pipeline.longest_movie()
    st.write(longest)


if __name__ == "__main__":
    main()

