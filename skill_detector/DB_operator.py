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

# Q: tupleとは？
# A: tupleはリストと同じように複数の値をまとめて扱うことができるデータ型
def get_skill_vectors() -> tuple[list[int], np.ndarray]:
    # DBからスキルのベクトルを取得
    # Q: with connection.cursor() as cursor: とは？
    # A: with connection.cursor() as cursor: はDBに接続するためのコード
    with connection.cursor() as cursor:
        # 実際のSQL文を実行する
        cursor.execute("select skill_id, skill_float_vector from skills")

        # 実行結果を取得する
        results = cursor.fetchall()

    skill_ids, vectors = [], []
    for skill_id, vector in results:
        # Q: skill_idは何？
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
    # Q: withはどのように使う？
    # A: withはファイルを開いたり、DBに接続したりするときに使う
    with connection.cursor() as cursor:
        try:
            # careerに入力値を保存する
            # Q: 以下のSQL文はどのような意味？
            # A: 以下のSQL文は、careerに入力値を保存するという意味
            query = "insert into careers " \
                    "(address, career_float_vector, input_text, started_at, finished_at) " \
                    "values (%s, %s, %s, %s, %s);"

            cursor.execute(query, (address, str_career_vector, input_text, started_at, finished_at))
            cursor.execute("select last_insert_id();")

            current_career_id = cursor.fetchone()[0]
            career_skill_values = [[current_career_id, skill_id, int(score)] for skill_id, score, in
                                   zip(skill_ids, skill_scores)]

            # career_skill_valuesにすべてのスキルの値を保存する
            query = "insert into career_skill_values (career_id, skill_id, value) " \
                    "values (%s, %s, %s);"
            # executemanyは複数の値を一度に保存する
            # executemanyの使い方は以下の通り
            # cursor.executemany(query, [(1, 2, 3), (4, 5, 6)])

            cursor.executemany(query, career_skill_values)

            # 保存した値をDBに反映させる

            connection.commit()
        except Exception as e:
            # 保存に失敗した場合はロールバックする
            connection.rollback()
            raise e

    return current_career_id

# update
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

            career_skill_values = [[int(score), career_id, skill_id] for skill_id, score, in
                                   zip(skill_ids, skill_scores)]

            # career_skill_valuesにすべてのスキルの値を保存する
            query = "update career_skill_values set value=%s where career_id=%s and skill_id=%s;"
            cursor.executemany(query, career_skill_values)
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e

    return career_id

# TODO: 発注のdatabaseにinsertする
# def insert_order
# high
# career_id, order_id, input_text, skill_ids, skill_scores, created_at, updated_at


# def update_order
# low
# 発注のdatabaseをupdateする


def init_skill_vectors():
    with connection.cursor() as cursor:
        try:
            query = "select id, query from skills"
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
    with open("result.txt", "w", encoding="utf-8") as f:
        f.write("complete")


def exist_career(career_id: int) -> bool:
    with connection.cursor() as cursor:
        query = "select * from careers where id=%s"
        cursor.execute(query, (career_id,))
        if cursor.fetchone() is None:
            return False
    return True

# 全てのcareer_idを取得する
def get_all_exist_career() -> list[int]:
    with connection.cursor() as cursor:
        query = "select id from careers"
        cursor.execute(query)
        career_ids = [career_id for career_id, in cursor.fetchall()]
    return career_ids

# 特定のcareer_idを取得する
# dictは辞書型
# どのような形式？
# {id: 1, address: "東京都", career_float_vector: "1,2,3,4,5", input_text: "テスト", started_at: "2021-01-01", finished_at: "2021-01-01"}
def get_one_career(career_id: int) -> dict:
    with connection.cursor() as cursor:
        query = "select * from orders where id=%s"
        cursor.execute(query, (career_id,))
        career = cursor.fetchone()
    return career

# 全てのorder_idを取得する
def get_exist_jobs() -> list[int]:
    with connection.cursor() as cursor:
        query = "select id from orders"
        cursor.execute(query)
        order_ids = [order_id for order_id, in cursor.fetchall()]
    return order_ids

def get_one_job(job_id: int) -> dict:
    with connection.cursor() as cursor:
        query = "select * from orders where id=%s"
        cursor.execute(query, (job_id,))
        job = cursor.fetchone()
    return job

def insert_job(sbt_id: int, input_text:str, is_finish_flag: bool, title: str) -> int:
    with connection.cursor() as cursor:
        try:
            query = "insert into jobs (sbt_id, input_text, is_finish_flag, title) values (%s, %s, %s, %s);"
            cursor.execute(query, (sbt_id, input_text, is_finish_flag, title))
            cursor.execute("select last_insert_id();")
            current_order_id = cursor.fetchone()[0]
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
    return current_order_id

def update_job(id: int, sbt_id: int, input_text:str, is_finish_flag: bool, title: str) -> int:
    with connection.cursor() as cursor:
        try:
            query = "update jobs set sbt_id=%s, input_text=%s, is_finish_flag=%s, title=%s where id=%s;"
            cursor.execute(query, (sbt_id, input_text, is_finish_flag, title, id))
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
    return id

# jobsを全て取得する
def get_all_jobs() -> list[dict]:
    with connection.cursor() as cursor:
        query = "select * from jobs"
        cursor.execute(query)
        jobs = cursor.fetchall()
    return jobs

# skillsを全て取得する
def get_all_skills() -> list[str]:
    with connection.cursor() as cursor:
        query = "select skill_name from skills"
        cursor.execute(query)
        skills = cursor.fetchone()
    return skills

# Takes a list of skill_name as an argument and returns a list of skill_id
def get_skill_ids(skill_names: list[str]) -> list[int]:
    with connection.cursor() as cursor:
        # skill_namesの各要素にダブルクォーテーションをつける
        skill_names = [f'"{skill_name}"' for skill_name in skill_names]
        skill_names = ",".join(skill_names)
        print(skill_names)
        query = "select id from skills where skill_name in " + "(" + skill_names + ")"
        cursor.execute(query)
        # skill_namesをqueryに入れた後のqueryを取得する

        skill_ids = cursor.fetchall()
    return skill_ids

