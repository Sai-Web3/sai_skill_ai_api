import numpy as np
from openai.embeddings_utils import get_embedding
from sai_skill_api.settings import OPENAI_QUERY_EMBEDDING_ENGINE, OPENAI_DOC_EMBEDDING_ENGINE


# 履歴を引数として受け取り, 埋め込みベクトルを返す
def get_career_vector(input_text: str) -> np.ndarray:
    additional_prompt = "\r\n\r\nAbove is a question and the answer about someone's work history. We would like to " \
                        "calculate the skills a person would have based on the " \
                        "work history using the cosine similarity, so please output a vector for this purpose."

    with open("input_text.txt", "w", encoding="utf-8") as f:
        f.write(input_text + additional_prompt)

    embedding = get_embedding(input_text + additional_prompt, engine=OPENAI_DOC_EMBEDDING_ENGINE)
    return np.array(embedding)


# skill名を引数として受け取り, 埋め込みベクトルを返す
def get_skill_vector(query: str) -> np.ndarray:
    embedding = get_embedding(query, engine=OPENAI_QUERY_EMBEDDING_ENGINE)
    return np.array(embedding)


