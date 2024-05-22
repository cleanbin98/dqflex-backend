from distutils.command import config
from typing import List, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

from recommender import item_based_recommendation, user_based_recommendation
from resolver import random_genres_items, random_items

#백엔드에서 접근 허용가능한 사이트 모음
origins = [
     "http://localhost",
     "http://localhost:3000",
     "http://hibin.link:8080",
     "http://dqflex-frontend.pages.dev",
     "https://hibin.link:8080"
     "https://dqflexx.web.app",
    # "http://api.dqflex.kro.kr:8080",
    # "http://api.dqflex.kro.kr",
    "*",
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)

#밑에서부터는 라우팅

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/all/")
async def all_movies():
    result = random_items()
    return {"result": result}


@app.get("/genres/{genre}")
async def genre_movies(genre: str):
    result = random_genres_items(genre)
    return {"result": result}


@app.get("/user-based/")
async def user_based(params: Optional[List[str]] = Query(None)):
    input_ratings_dict = dict(
        (int(x.split(":")[0]), float(x.split(":")[1])) for x in params
    )
    result = user_based_recommendation(input_ratings_dict)
    return {"result": result}


@app.get("/item-based/{item_id}")
async def item_based(item_id: str):
    result = item_based_recommendation(item_id)
    return {"result": result}
