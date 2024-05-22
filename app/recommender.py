import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix
from implicit.als import AlternatingLeastSquares
import pickle

#CSV 파일을 가져옴
saved_model_fname = "model/finalized_model.sav"
data_fname = "data/ratings.csv"
item_fname = "data/movies_final.csv"
weight = 10


def model_train():
    ratings_df = pd.read_csv(data_fname)
    ratings_df["userId"] = ratings_df["userId"].astype("category")
    ratings_df["movieId"] = ratings_df["movieId"].astype("category")

    # 영화 정보에 대한 행렬 생성
    rating_matrix = coo_matrix(
        (
            ratings_df["rating"].astype(np.float32),
            (
                ratings_df["movieId"].cat.codes.copy(),
                ratings_df["userId"].cat.codes.copy(),
            ),
        )
    )

    # AlternatingLeastSquares 모델(추천 기반 학습 알고리즘)을 초기화하고 학습시킨다.
    als_model = AlternatingLeastSquares(
        factors=50, regularization=0.01, dtype=np.float64, iterations=50
    )

    als_model.fit(weight * rating_matrix)

    #학습된 내용을 saved_model_fnam e파일로 생성 
    pickle.dump(als_model, open(saved_model_fname, "wb"))
    return als_model


#저장된 모델을 불러와 특정 영화와 유사한 영화를 추천
def calculate_item_based(item_id, items):
    loaded_model = pickle.load(open(saved_model_fname, "rb"))
    recs = loaded_model.similar_items(itemid=int(item_id), N=11)
    return [str(items[r]) for r in recs[0]]

#사용자 평점 기반 영화 추천
def item_based_recommendation(item_id):
    # 사용자 평점 데이터와 영화 정보를 불러옴.
    ratings_df = pd.read_csv(data_fname)
    ratings_df["userId"] = ratings_df["userId"].astype("category")
    ratings_df["movieId"] = ratings_df["movieId"].astype("category")
    movies_df = pd.read_csv(item_fname)

    items = dict(enumerate(ratings_df["movieId"].cat.categories))
    try:
        parsed_id = ratings_df["movieId"].cat.categories.get_loc(int(item_id))
        # 바로 위에서 선언한 calculate_item_based 함수를 호출하여 유사한 영화를 추천.
        result = calculate_item_based(parsed_id, items)
    except KeyError as e:
        result = []
    result = [int(x) for x in result if x != item_id]
    result_items = movies_df[movies_df["movieId"].isin(result)].to_dict("records")
    #추천된 영화 정보를 반환.
    return result_items

#저장된 모델(saved_model_fname)을 불러와 특정 사용자에게 맞춤 추천.
def calculate_user_based(user_items, items):
    loaded_model = pickle.load(open(saved_model_fname, "rb"))
    recs = loaded_model.recommend(
        userid=0, user_items=user_items, recalculate_user=True, N=10
    )
    return [str(items[r]) for r in recs[0]]

# 사용자 입력 평점을 기반으로 행렬을 생성.
def build_matrix_input(input_rating_dict, items):
    model = pickle.load(open(saved_model_fname, "rb"))
    # input rating list : {1: 4.0, 2: 3.5, 3: 5.0}

    item_ids = {r: i for i, r in items.items()}
    # 영화 평점 불러옴
    mapped_idx = [item_ids[s] for s in input_rating_dict.keys() if s in item_ids]
    #영화 정보 불러옴
    data = [weight * float(x) for x in input_rating_dict.values()]
    # print('mapped index', mapped_idx)
    # print('weight data', data)
    rows = [0 for _ in mapped_idx]
    shape = (1, model.item_factors.shape[0])
    # 매트릭스 생성
    return coo_matrix((data, (rows, mapped_idx)), shape=shape).tocsr()

#사용자 평점 데이터를 불러와 아이템 정보를 매핑하고, 사용자 맞춤 추천 결과를 반환.
def user_based_recommendation(input_ratings):
    ratings_df = pd.read_csv(data_fname)
    ratings_df["userId"] = ratings_df["userId"].astype("category")
    ratings_df["movieId"] = ratings_df["movieId"].astype("category")
    movies_df = pd.read_csv(item_fname)

    items = dict(enumerate(ratings_df["movieId"].cat.categories))
    input_matrix = build_matrix_input(input_ratings, items)
    result = calculate_user_based(input_matrix, items)
    result = [int(x) for x in result]
    result_items = movies_df[movies_df["movieId"].isin(result)].to_dict("records")
    return result_items


if __name__ == "__main__":
    model = model_train()
