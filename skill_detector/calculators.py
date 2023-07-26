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

# Function to combine multiple lists into one
def flatten_list(nested_list: list[list]) -> list:
    return [item for sublist in nested_list for item in sublist]

# Get common elements from two lists
def get_common_elements(A: list, B: list) -> list:
    return list(set([a.lower() for a in A]).intersection(set([b.lower() for b in B])))