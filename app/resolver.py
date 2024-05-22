import pandas as pd

item_fname = 'data/movies_final.csv'

#RANDOM 영화 반환
def random_items():
    movies_df = pd.read_csv(item_fname)
    movies_df = movies_df.fillna('')
    result_items = movies_df.sample(n=10).to_dict("records")
    return result_items

#RANDOM 장르의 영화 반환
def random_genres_items(genre):
    movies_df = pd.read_csv(item_fname)
    genre_df = movies_df[movies_df['genres'].apply(lambda x: genre in x.lower())]
    genre_df = genre_df.fillna('')
    result_items = genre_df.sample(n=10).to_dict("records")
    return result_items
