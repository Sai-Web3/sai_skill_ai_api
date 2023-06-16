import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import minmax_scale


# スキルのベクトルと経歴のベクトルのコサイン類似度を算出する
# 扱う値はすべてnumpyのarrayに基づいている
def get_skill_similarity(skill_vectors_dict: dict[int: np.ndarray], career_vector: np.ndarray) -> dict[int: np.ndarray]:
    skill_ids = skill_vectors_dict.keys()
    skill_vectors = np.stack(list(skill_vectors_dict.values()))

    career_vector = career_vector[np.newaxis, :]

    cosine_similarities = cosine_similarity(career_vector, skill_vectors)[0, :]
    return {label: score for label, score in zip(skill_ids, cosine_similarities)}


# スキルの類似度を正規化して, スコアを算出する
def similarities_to_scores(skill_similarities_dict: dict[int, np.ndarray], scaling_point: float) -> dict[int: int]:
    skill_ids = skill_similarities_dict.keys()
    skill_similarities = np.array(list(skill_similarities_dict.values()))

    # Max100とscaling pointでスケーリング
    skill_scores = minmax_scale(skill_similarities) * 100 * scaling_point
    skill_scores = skill_scores.astype(np.uint16).tolist()

    return {label: score for label, score in zip(skill_ids, skill_scores)}
