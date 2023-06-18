import numpy as np
from django.db import connection
from datetime import datetime

from .openai_apis import get_skill_vector


def str_to_float_array(float_array_str: str) -> np.ndarray:
    float_array = list(map(float, float_array_str.split(",")))

    return np.array(float_array)


def float_array_to_str(float_array: np.ndarray) -> str:
    float_array_str = ",".join(map(str, float_array))

    return float_array_str


def get_skill_vectors() -> tuple[list[int], np.ndarray]:
    with connection.cursor() as cursor:
        cursor.execute("select skill_id, skill_float_vector from skills")
        results = cursor.fetchall()

    skill_ids, vectors = [], []
    for skill_id, vector in results:
        skill_ids.append(skill_id)
        vectors.append(str_to_float_array(vector))

    return skill_ids, np.stack(vectors)


def insert_career(
        address: str,
        career_vector: np.ndarray,
        input_text: str,
        started_at: datetime,
        finished_at: datetime,
        skill_ids: list[int],
        skill_scores: np.ndarray,
) -> int:
    str_career_vector = float_array_to_str(career_vector)
    started_at = started_at.strftime("%Y-%m-%d")
    finished_at = finished_at.strftime("%Y-%m-%d")

    with connection.cursor() as cursor:
        try:
            # careerに入力値を保存する
            query = "insert into careers " \
                    "(address, career_float_vector, input_text, started_at, finished_at) " \
                    "values (%s, %s, %s, %s, %s);"

            cursor.execute(query, (address, str_career_vector, input_text, started_at, finished_at))
            cursor.execute("select last_insert_id();")

            current_career_id = cursor.fetchone()[0]
            career_skill_values = [[current_career_id, skill_id, score] for skill_id, score, in
                                   zip(skill_ids, skill_scores)]

            # career_skill_valuesにすべてのスキルの値を保存する
            query = "insert into career_skill_values (career_id, skill_id, value) " \
                    "values (%s, %s, %s);"
            cursor.executemany(query, career_skill_values)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e

    return current_career_id


def update_career(
        address: str,
        career_vector: np.ndarray,
        input_text: str,
        started_at: datetime,
        finished_at: datetime,
        skill_ids: list[int],
        skill_scores: np.ndarray,
        career_id: int
) -> int:
    str_career_vector = float_array_to_str(career_vector)
    started_at = started_at.strftime("%Y-%m-%d")
    finished_at = finished_at.strftime("%Y-%m-%d")

    with connection.cursor() as cursor:
        try:
            # careerに入力値を保存する
            query = "update careers set address=%s, career_float_vector=%s, input_text=%s, " \
                    "started_at=%s, finished_at=%s where id=%s;"

            cursor.execute(query, (address, str_career_vector, input_text, started_at, finished_at, career_id))

            career_skill_values = [[score, career_id, skill_id] for skill_id, score, in
                                   zip(skill_ids, skill_scores)]

            # career_skill_valuesにすべてのスキルの値を保存する
            query = "update career_skill_values set value=%s where career_id=%s and skill_id=%s;"
            cursor.executemany(query, career_skill_values)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e

    return career_id


def init_skill_vectors():
    with connection.cursor() as cursor:
        try:
            query = "select id, skill_name from skills"
            cursor.execute(query)
            skills_dict = {label: skill_name for label, skill_name in cursor.fetchall()}

            for label, skill_name in skills_dict.items():
                skill_vector = get_skill_vector(skill_name)
                str_skill_vector = float_array_to_str(skill_vector)
                query = "update skills set skill_float_vector=%s where id=%s"
                cursor.execute(query, (str_skill_vector, label))
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e

    print("Complete init skill vectors")


def exist_career(career_id: int) -> bool:
    with connection.cursor() as cursor:
        query = "select * from careers where id=%s"
        cursor.execute(query, (career_id,))
        if cursor.fetchone() is None:
            return False
    return True
