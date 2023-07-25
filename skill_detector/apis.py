import json
import datetime
from typing import Optional
import time

from rest_framework import views, status, permissions
from rest_framework.response import Response

from .openai_apis import get_career_vector
from .DB_operator import insert_career, exist_career, update_career, get_all_exist_career, get_one_job, get_exist_jobs,get_one_career, insert_job, update_job
from .calculators import get_skill_similarity, similarities_to_scores, calculate_common_elements_percentage
from .apps import SKILL_IDS, SKILL_VECTORS
from .gpt_turbo import get_chatgpt35_turbo_response

# 仕事データを作成するための関数
# @param started_at: 開始日
# @param finished_at: 終了日
# @param input_text: 仕事内容
# @param address: walletのアドレス
# @param career_id: 仕事データのID

# Q: Optional[int]とは？
# A: Optional[int]はint型もしくはNoneを返すという意味
def record_career(
        started_at: datetime.datetime,
        finished_at: datetime.datetime,
        input_text: str,
        address: str,
        career_id: Optional[int] = None
) -> int:
    # 仕事内容からベクトルを取得
    career_vector = get_career_vector(input_text)

    # 仕事の期間を取得
    term = finished_at - started_at
    # 1年を1ポイントとしてスケーリング
    scaling_point = term.days / 365

    # 仕事内容とスキルの類似度を計算
    skill_similarities = get_skill_similarity(SKILL_VECTORS, career_vector)

    # 類似度をスコアに変換
    skill_scores = similarities_to_scores(skill_similarities, scaling_point)

    start = time.time()

    # 仕事データをDBに保存
    if career_id is None:
        current_career_id = insert_career(
            career_vector=career_vector,
            skill_ids=SKILL_IDS,
            skill_scores=skill_scores,
            finished_at=finished_at,
            started_at=started_at,
            input_text=input_text,
            address=address
        )
    else:
        current_career_id = update_career(
            career_vector=career_vector,
            skill_ids=SKILL_IDS,
            skill_scores=skill_scores,
            finished_at=finished_at,
            started_at=started_at,
            input_text=input_text,
            address=address,
            career_id=career_id
        )

    # 仕事データのIDを返す
    return current_career_id

# 仕事データを取得するための関数

# 仕事データを取得するための関数
class SkillElementPostView(views.APIView):

    # どのユーザーでもアクセスできるようにする
    permission_classes = (permissions.AllowAny,)

    # POSTメソッドでアクセスされたときに呼び出される関数
    def post(self, request):
        try:
            body = json.loads(request.body)
            started_at = datetime.datetime.strptime(body["started_at"], "%Y-%m")
            finished_at = datetime.datetime.strptime(body["finished_at"], "%Y-%m")

            # Q:body["input_text"]とは？
            # A:bodyはjson形式のデータで、body["input_text"]はその中のinput_textというキーの値を取得する
            input_text = body["input_text"]
            if not isinstance(input_text, str):
                raise ValueError()
            address = body["address"]
            if not isinstance(address, str):
                raise ValueError()

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        current_career_id = record_career(
            started_at,
            finished_at,
            input_text,
            address
        )

        context = {
            "status": 200,
            "career_id": current_career_id
        }

        return Response(context, status=status.HTTP_200_OK)


class SkillElementsGetView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self):

        careers = get_all_exist_career()

        # 空の配列が返ってきた場合は404を返す
        if len(careers) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)

        context = {
            "status": 200,
            "careers": careers
        }

        return Response(context, status=status.HTTP_200_OK)

class SkillElementGetView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, career_id):

        career = get_one_career(career_id)

        # 空の配列が返ってきた場合は404を返す
        if career is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        context = {
            "status": 200,
            "careers": career
        }

        return Response(context, status=status.HTTP_200_OK)

# postと同じように仕事データを取得するためのclass
# I wonder it's little difference from post and put.
class SkillElementPutView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    # PUTメソッドでアクセスされたときに呼び出される関数
    # この関数はフロントのどこで呼び出されるのか調べておく必要がありそう
    def put(self, request, career_id=None):
        try:
            body = json.loads(request.body)
            started_at = datetime.datetime.strptime(body["started_at"], "%Y-%m")
            finished_at = datetime.datetime.strptime(body["finished_at"], "%Y-%m")
            input_text = body["input_text"]
            if not isinstance(input_text, str):
                raise ValueError()
            address = body["address"]
            if not isinstance(address, str):
                raise ValueError()
            if exist_career(career_id) is False:
                raise ValueError()

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        current_career_id = record_career(
            started_at,
            finished_at,
            input_text,
            address,
            career_id
        )

        context = {
            "status": 200,
            "career_id": current_career_id
        }

        return Response(context, status=status.HTTP_200_OK)

# GPT-3.5を使って、文章からスキルを抽出する関数
class SkillElementGPTView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    # POSTメソッドでアクセスされたときに呼び出される関数
    def post(self, request):
        try:
            body = json.loads(request.body)
            print(body)
            input_text = body["input_text"]
            print(input_text)
            if not isinstance(input_text, str):
                raise ValueError()

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        response = get_chatgpt35_turbo_response(input_text)

        context = {
            "status": 200,
            "response": response
        }

        return Response(context, status=status.HTTP_200_OK)
    
# 発注を行うための関数
# Q: views.APIViewとは？
# A: APIViewはDjango REST Frameworkのクラスで、APIのエンドポイントを作成するためのクラス
class JobPostView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    # POSTメソッドでアクセスされたときに呼び出される関数
    def post(self, request):
        try:
            body = json.loads(request.body)
            job_id = body["job_id"]
            if not isinstance(job_id, int):
                raise ValueError()
            input_text = body["input_text"]
            if not isinstance(input_text, str):
                raise ValueError()
            is_finish_flag = body["is_finish_flag"]
            if not isinstance(is_finish_flag, str):
                raise ValueError()

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        id = insert_job(
            job_id,
            input_text,
            is_finish_flag
        )

        context = {
            "status": 200,
            "order_id": id
        }

        return Response(context, status=status.HTTP_200_OK)

# 発注を取得するための関数
class JobsView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    # データベースから発注を取得する関数
    def get(self, request):
        try:
            job_ids = get_exist_jobs()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        context = {
            "status": 200,
            "order_data": job_ids
        }

        return Response(context, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            body = json.loads(request.body)
            sbt_id = body["sbt_id"]
            if not isinstance(sbt_id, int):
                raise ValueError()
            input_text = body["input_text"]
            if not isinstance(input_text, str):
                raise ValueError()
            is_finish_flag = body["is_finish_flag"]
            if not isinstance(is_finish_flag, bool):
                raise ValueError()
            title = body["title"]
            if not isinstance(title, str):
                raise ValueError()
        
        except:
            # エラーの原因を調べるために、エラーの内容を出力する
            print(ValueError)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        id = insert_job(
            sbt_id,
            input_text,
            is_finish_flag,
            title
        )

        context = {
            "status": 200,
            "order_id": id
        }

        return Response(context, status=status.HTTP_200_OK)

class JobView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    # データベースから発注を取得する関数
    def get(self, request, job_id):
        try:
                job_id = int(job_id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        job_data = get_one_job(job_id)

        context = {
            "status": 200,
            "order_data": job_data
        }

        return Response(context, status=status.HTTP_200_OK)
    
    def put(self, request, job_id):
        try:
            body = json.loads(request.body)
            job_id = body["id"]
            sbt_id = body["sbt_id"]
            if not isinstance(sbt_id, int):
                raise ValueError()
            input_text = body["input_text"]
            if not isinstance(input_text, str):
                raise ValueError()
            is_finish_flag = body["is_finish_flag"]
            if not isinstance(is_finish_flag, bool):
                raise ValueError()
            title = body["title"]
            if not isinstance(title, str):
                raise ValueError()
        
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        id = update_job(
            job_id,
            sbt_id,
            input_text,
            is_finish_flag,
            title
        )

        context = {
            "status": 200,
            "order_id": id
        }

        return Response(context, status=status.HTTP_200_OK)

class MatchView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, career_id, job_id):
        try:
            job_id = int(job_id)
            career_id = int(career_id)
            
            career = get_one_career(career_id)
            job = get_one_job(job_id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        match_data = calculate_common_elements_percentage(career, job)

        context = {
            "status": 200,
            "match_data": match_data
        }

        return Response(context, status=status.HTTP_200_OK)