## Easy setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd sai_skill_api
python manage.py runserver
```

## Apis
ユーザの入力を元にスキルの値を算出し, DBに保存する

method: post

url: https://~/api/skill_elements/  
body: {  
  "input_text": str,  // 職歴   
  "sbt_id": int,  // sbtのid  
  "started_at": str,  // 働きはじめの年と月. example: "2016-5"  
  "finished_at": 働き終わりの年と月  
}

response: {  
  "status": 200,  
  "career_id": int  // 追加した経歴のid  
}  

---
職歴の変更を行う場合に再びスキルの値を算出し, DBに上書きする

method: put  

url: https://~/api/skill_elements/?career_id=int  
body: {  
  "input_text": str,  // 職歴  
  "sbt_id": int,  // sbtのid  
  "started_at": str,  // 働きはじめの年と月. example: "2016-5"  
  "finished_at": str,  // 働き終わりの年と月  
}  

response: {  
  "status": 200,  
  "career_id": int  // 変更した経歴のid  
}  