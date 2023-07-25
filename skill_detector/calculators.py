import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import minmax_scale


# スキルのベクトルと経歴のベクトルのコサイン類似度を算出する
# 扱う値はすべてnumpyのarrayに基づいている
def get_skill_similarity(skill_vectors: np.ndarray, career_vector: np.ndarray) -> np.ndarray:
    career_vector = career_vector[np.newaxis, :]

    # スキルのベクトルと経歴のベクトルのコサイン類似度を算出
    cosine_similarities = cosine_similarity(career_vector, skill_vectors)[0, :]
    return cosine_similarities


# スキルの類似度を正規化して, スコアを算出する
def similarities_to_scores(skill_similarities: np.ndarray, scaling_point: float) -> np.ndarray:
    # Max100とscaling pointでスケーリング
    skill_scores = minmax_scale(skill_similarities) * 100 * scaling_point

    # スコアを整数に変換
    skill_scores = skill_scores.astype(np.uint16)

    return skill_scores

# 

def calculate_common_elements_percentage(A, B):
    # set()関数を使って、リストを集合に変換する
    # Q: set関数とは？
    # A: set関数は、重複する要素を削除する関数
    set_A = set(A)
    set_B = set(B)
    # intersection()関数を使って、2つの集合の共通要素を取得する
    # Q: intersection()関数とは？
    # A: intersection()関数は、2つの集合の共通要素を取得する関数
    common_elements = set_A.intersection(set_B)
    percent = (len(common_elements) / len(set_B)) * 100
    print(f"The percentage of elements in B that are also present in A is: {percent}%")

# 二重のリストをフラットにする
def flatten_list(nested_list: list[list]) -> list:
    return [item for sublist in nested_list for item in sublist]

# 大文字小文字を区別せずに、2つのリストの共通要素を取得する
def get_common_elements(A: list, B: list) -> list:
    # Q: lower()関数とは？
    # A: lower()関数は、文字列を小文字に変換する関数
    # Q: set関数とは？
    # A: set関数は、重複する要素を削除する関数
    # Q: intersection()関数とは？
    # A: intersection()関数は、2つの集合の共通要素を取得する関数
    return list(set([a.lower() for a in A]).intersection(set([b.lower() for b in B])))