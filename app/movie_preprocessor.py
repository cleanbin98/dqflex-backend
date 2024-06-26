import pandas as pd
import requests
import sys
from tqdm import tqdm


def add_url(row):
    return f"http://www.imdb.com/title/tt{row}/"


def add_rating(df):
    ratings_df = pd.read_csv('data/ratings.csv')
    #id를 문자로 인식할 수 있도록 type을 변경
    ratings_df['movieId'] = ratings_df['movieId'].astype(str)
    agg_df = ratings_df.groupby('movieId').agg(
        #컬럼 추가.
        rating_count=('rating', 'count'),
        rating_avg=('rating', 'mean')
    ).reset_index()

    rating_added_df = df.merge(agg_df, on='movieId')
    return rating_added_df


#api 키를 가져와서 이미지 불러오기.
def add_poster(df):
    for i, row in tqdm(df.iterrows(), total=df.shape[0]):
        tmdb_id = row["tmdbId"]
        tmdb_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key=80decdd361d7c8da2f4674a6d1da6513&language=en-US"
        result = requests.get(tmdb_url)
        # final url : https://image.tmdb.org/t/p/original/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg
        try:
            df.at[i, "poster_path"] = "https://image.tmdb.org/t/p/original" + result.json()['poster_path']
        except (TypeError, KeyError) as e:
            # toy story poster as default
            df.at[i, "poster_path"] = "https://image.tmdb.org/t/p/original/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg"
    return df


if __name__ == "__main__":
    movies_df = pd.read_csv('data/movies.csv')
    movies_df['movieId'] = movies_df['movieId'].astype(str)
    links_df = pd.read_csv('data/links.csv', dtype=str)
    merged_df = movies_df.merge(links_df, on='movieId', how='left')
    merged_df['url'] = merged_df['imdbId'].apply(lambda x: add_url(x))
    result_df = add_rating(merged_df)
    result_df['poster_path'] = None
    result_df = add_poster(result_df)
    # 전처리 완료 파일 생성
    result_df.to_csv("data/movies_final.csv", index=None)
