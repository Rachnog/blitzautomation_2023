import streamlit as st

import openai
import json
import yaml
import boto3

import sys
import os

import wandb

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

from src.gpt_wrappers import ChatGPTWithMemory
from src.quality_checks import *
from src.xml_utils import *
from src.drawio_utils import *

# Load config
with open('../config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

openai.api_key = config['OPENAI_KEY']

s3 = boto3.resource(
    's3',
    aws_access_key_id=config['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=config['AWS_SECRET_ACCESS_KEY']
)

system_prompt = \
"""
    You are a mindmaps expert. You are specialist in using XMind app and you excel in XML.
    You help humans to structure their knowledge in a compact way so they can remember and learn things faster.
    Also, you are a great teacher and you love to share your knowledge with others. 
    You use mindmaps to speed up learnning process and to share your knowledge with others.
    When you are asked to create a mindmap given a text, you analyze the text, select main topics and entities and then you create a mindmap as an XML file.
"""

example_question = \
"""
Generate the mindmap from the following text:

We spent 6 months making GPT-4 safer and more aligned. GPT-4 is 82% less likely to respond to requests for disallowed content and 40% more likely to produce factual responses than GPT-3.5 on our internal evaluations.
We incorporated more human feedback, including feedback submitted by ChatGPT users, to improve GPT-4’s behavior. We also worked with over 50 experts for early feedback in domains including AI safety and security.
We’ve applied lessons from real-world use of our previous models into GPT-4’s safety research and monitoring system. Like ChatGPT, we’ll be updating and improving GPT-4 at a regular cadence as more people use it.
GPT-4’s advanced reasoning and instruction-following capabilities expedited our safety work. We used GPT-4 to help create training data for model fine-tuning and iterate on classifiers across training, evaluations, and monitoring.
"""

example_answer = \
"""
<map>
    <node text="GPT-4 release">
        <node text="Metrics imrpovement">
            <node text="82% less disallowed content responses"></node>
            <node text="40% more factual"></node>
        </node>
        <node text="Human feedback and improvement">
            <node text="50 experts worked on behavior"></node>
            <node text="Improvements based on real use like ChatGPT"></node>
        </node>
        <node text="Safety research">
            <node text="GPT-4 used to create training data"></node>
            <node text="Classifiers used during training, evaluation, monitoring"></node>
        </node>
    </node>
</map>
"""


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

    chatgpt = ChatGPTWithMemory(system_prompt)
    chatgpt.initialize_with_question_answer(example_question, example_answer)
    answer = chatgpt.generate(question)
    save_xml_string_to_file(answer, '../data/text.xml')

    converter = XMLToDrawIOConverter(answer)
    drawio_xml = converter.convert()
    with open('../data/text.drawio', "w") as f:
        f.write(drawio_xml)

    # create hash for the text
    text_hash = hash(text)

    # upload system_prompt as a text file to s3 to a folder queries
    s3.Object(config['AWS_S3_BUCKET'], f'queries/{text_hash}.txt').put(Body=system_prompt)
    # upload answer as XML file to a folder XMLs
    s3.Object(config['AWS_S3_BUCKET'], f'XMLs/{text_hash}.xml').put(Body=answer)
    # upload answer as drawio file to a folder drawios
    s3.Object(config['AWS_S3_BUCKET'], f'drawios/{text_hash}.drawio').put(Body=drawio_xml)

    st.subheader('Mindmap XML')
    st.text_area("", value=answer)

    st.subheader('Mindmap draw.io')
    st.text_area("", value=drawio_xml)