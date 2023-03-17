import streamlit as st

import openai
import yaml
import boto3

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

from src.gpt_wrappers import ChatGPTWithMemory
from src.quality_checks import *
from src.xml_utils import *
from src.drawio_utils import *

from content import AppPrompts

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

app_prompts = AppPrompts()

st.title("Mindmaps automated")
st.subheader('Enter your text here')
text = st.text_area(value=
    """
        Our culture represents the set of ideas, knowledge and traditions that we stand for.
        It’s not by chance that we have a strong culture based on specific values. When in 2011, amidst the financial crisis, we left our safe jobs at a big corp to create a place we’d love to work at, we knew how privileged we were.
        We tirelessly work to put our skills and expertise to good use. In other words, we make sure we are playing an active role in building a better society.
        We have very clear red lines.
        Pursuing diversity or open source is smart; Honestly, even more important, we believe it's simply fair. 
    """, label=""
)

if st.button("Generate Mindmap"):

    st.write("Generating Mindmap...")

    question = \
    f"""
        Generate the mindmap from the following text:
        {text}
    """

    chatgpt = ChatGPTWithMemory(app_prompts.system_prompt)
    chatgpt.initialize_with_question_answer(app_prompts.example_question, app_prompts.example_answer)
    answer = chatgpt.generate(question)
    # save_xml_string_to_file(answer, '../data/text.xml')

    converter = XMLToDrawIOConverter(answer)
    drawio_xml = converter.convert()
    # with open('../data/text.drawio', "w") as f:
    #     f.write(drawio_xml)

    # create hash for the text
    text_hash = hash(text)

    # upload system_prompt as a text file to s3 to a folder queries
    s3.Object(config['AWS_S3_BUCKET'], f'queries/{text_hash}.txt').put(Body=app_prompts.system_prompt)
    # upload answer as XML file to a folder XMLs
    s3.Object(config['AWS_S3_BUCKET'], f'XMLs/{text_hash}.xml').put(Body=answer)
    # upload answer as drawio file to a folder drawios
    s3.Object(config['AWS_S3_BUCKET'], f'drawios/{text_hash}.drawio').put(Body=drawio_xml)

    st.subheader('Mindmap XML')
    st.text('S3 path: s3://'+config['AWS_S3_BUCKET']+'/XMLs/'+str(text_hash)+'.xml')
    st.text_area("", value=answer)

    st.subheader('Mindmap draw.io')
    st.text('S3 path: s3://'+config['AWS_S3_BUCKET']+'/drawios/'+str(text_hash)+'.drawio')
    st.text_area("", value=drawio_xml)