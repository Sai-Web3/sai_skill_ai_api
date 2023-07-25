from django.urls import path

from .apis import SkillElementPostView, SkillElementPutView, SkillElementsGetView, JobsView, JobView, SkillElementGPTView

app_name = 'skill_detector'

# Q: as_view()は何？
# A: as_view()は、クラスベースのViewを関数ベースのViewに変換する
urlpatterns = [
    path('skill_elements/', SkillElementPostView.as_view(), name="post_skill_elements"),
    path('skill_elements/<int:career_id>', SkillElementPutView.as_view(), name="put_skill_elements"),
    path('skill_elements/', SkillElementsGetView.as_view(), name="get_skill_elements"),
    path('jobs/', JobsView.as_view(), name="jobs"),
    path('jobs/<int:job_id>', JobView.as_view(), name="job"),
    path('chat_gpt/', SkillElementGPTView.as_view(), name="chat_gpt"),
    
]


