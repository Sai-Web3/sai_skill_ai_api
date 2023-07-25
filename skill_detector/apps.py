from django.apps import AppConfig
from .DB_operator import init_skill_vectors, get_skill_vectors

# Q: classを作成する意味は？
# A: Djangoの仕様で、AppConfigを継承したclassを作成することで、
#    Djangoが自動的に設定を読み込んでくれるようになる

class SkillDetectorConfig(AppConfig):

    # Q: default_auto_fieldは新たに追加されているようだが?
    # A: Django3.2から追加されたもので、Django2.2以前のバージョンでは
    #    使えないので注意
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'skill_detector'


# init_skill_vectors()
SKILL_IDS, SKILL_VECTORS = get_skill_vectors()
