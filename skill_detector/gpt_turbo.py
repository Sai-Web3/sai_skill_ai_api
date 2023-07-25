import os
import openai
# ../sai_skill_api/._important_keys.pyの内容を読み込む
from sai_skill_api._important_keys import *


# Load environment variables from .env file

def get_chatgpt35_turbo_response(input_text: str) -> str:
    response = openai.ChatCompletion.create(
        engine="gpt-35-turbo", # engine = "deployment_name".
        messages=[
            {"role": "system","content": "You are a helpful assistant."},
            {"role": "user", "content":  input_text},
            {"role": "system", "content": ""},
        ]
    )

    return response['choices'][0]['message']['content']

# 歓迎スキルと必須スキルを利用して、スキルを検出する
def get_chatgpt35_skillDetector_response(input_text: str) -> list[int]:

    response = openai.Completion.create(
        engine="gpt-35-turbo",
        messages=[
            {"role": "system","content": "You are a career consultant considering the skills needed for a project. From the text of your answer to the question, please obtain information on the specific skills needed for the project entered. The information to be obtained is as follows \n- Front-end development skills \n- Back-end development skills \n- Blockchain development \n- Cloud Infrastructure \n- AI Development \n- API/SDK Development \n- UX Design \n- Security. Please itemize the names of specific skills. \n e.g.) C, C#, Javascript"},
            {"role": "user", "content":  input_text},
        ],
    )

    return response['choices'][0]['text'].split(',')

    messages = [{"role":"system","content":"You are the lead engineer who performs the technology selection for the client's requirements.. Please itemize the names of 30 specific skills. \ne.g.) C, C#, Javascript. \nYou MUST return English.\n"},
                {"role":"user","content":"We want to create a platform for music that We automatically change the data of music submitted by users to the best data for streaming and distribute it."},
                {"role":"assistant","content":"Skill needed: API development, SDK development, AI integration, Data analysis, Database management, Web development, Cloud computing, Security protocols"},
                {"role":"user","content":"Skills should preferably be a reference to a programming language or framework."},
                {"role":"assistant","content":"Skill needed: Python, Django, Ruby, Ruby on Rails, JavaScript, TypeScript, Express, Node.js, React, Vue, Next.js, Azure, AWS"},
                {"role":"user","content":input_text},
                {"role":"assistant","content":summary['choices'][0]['message']['content']},
                {"role":"user","content":"Skills should preferably be a reference to a programming language or framework."}],
  temperature=0.7,
  max_tokens=2045,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None)
  

  # \nを削除する
    response = response.replace('\n', '')
  # 最後のピリオドを削除する
    response = response.rstrip('.')
  # Skill needed:を 削除する
    response = response.replace('Skill needed: ', '')
  # コンマで分割する
    response = response.split(',')