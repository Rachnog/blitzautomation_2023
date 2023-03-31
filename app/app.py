import streamlit as st

import openai
import yaml
import json
import boto3

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

from src.gpt_wrappers import ChatGPTWithMemory
from src.quality_checks import *
from src.xml_utils import *
from src.drawio_utils import *

from content import AppPromptsMindmap, AppPromptsQuestions

# Load config
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.yml')
with open(config_path) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

openai.api_key = config['OPENAI_KEY']

s3 = boto3.resource(
    's3',
    aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY']
)

app_prompts_mindmap = AppPromptsMindmap()
app_prompts_questions = AppPromptsQuestions()

st.title("Professor Copilot :sunglasses:")
st.subheader('Your study material here :books:')
text = st.text_area(value=
    """
        Richard Ward, 32, was fatally shot on February 22, 2022, by Pueblo County deputy Charles McWhorter during an incident in Liberty Point International Middle School in Pueblo West, Colorado.[1]
        Ward was questioned by the police after being observed attempting to enter a car that was not his in the middle school's parking lot.[2] He was asked for his identification and if he had any weapons on his person. After admitting that he may be armed with a knife, he appeared to put something in his mouth. McWhorter, one of two deputies at the scene, forcefully removed Ward out of the car and placed him on the ground, shortly before shooting him three times in the chest.[3]
        After reviewing the results, District Attorney Jeff Chostner determined that the deputies' actions were "rational and justified" because they "believed their lives or the lives of others were in jeopardy".[3] McWhorter earned a Purple Heart award from the Pueblo County Sheriff's Office for allegedly sustaining injuries during the incident. On February 21, 2023, Ward's family filed a federal lawsuit against McWhorter and his agency.[2]
    """, label=""
)

if st.button("Generate Mindmap and Questions"):

    chatgpt_mindmap = ChatGPTWithMemory(app_prompts_mindmap.system_prompt)
    chatgpt_mindmap.initialize_with_question_answer(app_prompts_mindmap.example_question, app_prompts_mindmap.example_answer)
    answer = chatgpt_mindmap.generate(
        app_prompts_mindmap.get_question_prompt(text)
    )
    save_xml_string_to_file(answer, '../data/text.xml')
    converter = XMLToDrawIOConverter(answer)
    drawio_xml = converter.convert()
    with open('../data/text.drawio', "w") as f:
        f.write(drawio_xml)

    chatgpt_questions = ChatGPTWithMemory(app_prompts_questions.system_prompt)
    chatgpt_questions.initialize_with_question_answer(app_prompts_questions.example_question, app_prompts_questions.example_answer)
    questions = chatgpt_questions.generate(
        app_prompts_questions.get_question_prompt(text)
    )

    # create hash for the text
    text_hash = hash(text)

    # make a JSON out of app_prompts_mindmap prompts
    app_prompts_mindmap_dict = app_prompts_mindmap.to_dict(text)
    app_prompts_questions_dict = app_prompts_questions.to_dict(text)
    answer_dict = {
        'xml': answer,
        'drawio_xml': drawio_xml
    }
    questions_dict = {
        'questions': questions
    }

    s3.Object(config['AWS_S3_BUCKET'], f'app_prompts_mindmap/{text_hash}.json').put(Body=json.dumps(app_prompts_mindmap_dict))
    s3.Object(config['AWS_S3_BUCKET'], f'app_prompts_questions/{text_hash}.json').put(Body=json.dumps(app_prompts_questions_dict))
    s3.Object(config['AWS_S3_BUCKET'], f'xmls/{text_hash}.json').put(Body=json.dumps(answer_dict))
    s3.Object(config['AWS_S3_BUCKET'], f'drawios/{text_hash}.drawio').put(Body=drawio_xml)
    s3.Object(config['AWS_S3_BUCKET'], f'questions/{text_hash}.json').put(Body=json.dumps(questions_dict))


    st.subheader(':computer: Mindmap XML')
    st.text_area("", value=answer)

    st.subheader(':brain: Mindmap draw.io')
    st.text_area("", value=drawio_xml)

    st.subheader(':tophat: Questions')
    st.text_area("", value=questions)

    st.subheader('Feedback :speech_balloon:')
    feedback_text = st.text_area("", value="")
    feedback_json = {
        'feedback': feedback_text
    }

    if st.button("Submit Feedback"):
        # upload feedback as a text file to a folder feedback
        s3.Object(config['AWS_S3_BUCKET'], f'feedbacks/{text_hash}.json').put(Body=json.dumps(feedback_json))