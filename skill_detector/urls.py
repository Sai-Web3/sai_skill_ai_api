from django.urls import path

from .apis import SkillElementPostView, SkillElementPutView

app_name = 'skill_detector'
urlpatterns = [
    path('skill_elements/', SkillElementPostView.as_view(), name="post_skill_elements"),
    path('skill_elements/<int:career_id>', SkillElementPutView.as_view(), name="put_skill_elements")
]
