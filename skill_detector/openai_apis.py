import numpy as np
from openai.embeddings_utils import get_embedding
from sai_skill_api.settings import OPENAI_QUERY_EMBEDDING_ENGINE, OPENAI_DOC_EMBEDDING_ENGINE


# 履歴を引数として受け取り, 埋め込みベクトルを返す
def get_career_vector(input_text: str) -> np.ndarray:
    embedding = get_embedding(input_text, engine=OPENAI_DOC_EMBEDDING_ENGINE)
    return np.array(embedding)


# skill名を引数として受け取り, 埋め込みベクトルを返す
def get_skill_vector(query: str) -> np.ndarray:
    embedding = get_embedding(query, engine=OPENAI_QUERY_EMBEDDING_ENGINE)
    return np.array(embedding)
