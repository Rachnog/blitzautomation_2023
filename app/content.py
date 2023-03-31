class AppPromptsMindmap:
    """
    This class contains all the mindmap prompts that will be used in the app.
    """
    def __init__(self):

        self.system_prompt = \
            """
                You are a mindmaps expert. You are specialist in using XMind app and you excel in XML.
                You help humans to structure their knowledge in a compact way so they can remember and learn things faster.
                Also, you are a great teacher and you love to share your knowledge with others. 
                You use mindmaps to speed up learnning process and to share your knowledge with others.
                When you are asked to create a mindmap given a text, you analyze the text, select main topics and entities and then you create a mindmap as an XML file.
            """
        self.example_question = \
            """
            Generate the mindmap from the following text:

            We spent 6 months making GPT-4 safer and more aligned. GPT-4 is 82% less likely to respond to requests for disallowed content and 40% more likely to produce factual responses than GPT-3.5 on our internal evaluations.
            We incorporated more human feedback, including feedback submitted by ChatGPT users, to improve GPT-4’s behavior. We also worked with over 50 experts for early feedback in domains including AI safety and security.
            We’ve applied lessons from real-world use of our previous models into GPT-4’s safety research and monitoring system. Like ChatGPT, we’ll be updating and improving GPT-4 at a regular cadence as more people use it.
            GPT-4’s advanced reasoning and instruction-following capabilities expedited our safety work. We used GPT-4 to help create training data for model fine-tuning and iterate on classifiers across training, evaluations, and monitoring.
            """
        self.example_answer = \
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
        
    def get_question_prompt(self, text):
        return f"""
            Generate the mindmap from the following text:
            {text}
        """
    
    def to_dict(self, text):
        return {
            "system_prompt": self.system_prompt,
            "example_question": self.example_question,
            "example_answer": self.example_answer,
            "question_prompt": self.get_question_prompt(text)
        }
        
class AppPromptsQuestions:
    """
    This class contains all the questions prompts that will be used in the app.
    """

    def __init__(self):

        self.system_prompt = \
            """
                You are a teacher, educator and practitioner. 
                Your goal is to prepare questions for the students that are engaging, motivating and challenging.
                You can take texts from the internet, books, articles, etc. and use them to create questions.
                For each piece of text you can generate set of questions with indicated difficulty level and answers.
                You can generate tests with single or multiple choice questions.
                You can generate open-ended questions. You can generate debate topics.
                You can generate provocative topics for the essays that students can write.
                You can generate ideas for practical group projects or even business ideas based on the text.
                IMPORTANT: design questions in such a way, that ChatGPT and similar AI systems cannot answer them.
            """
        self.example_question = ""
        self.example_answer = ""

    def get_question_prompt(self, text):
        return f"""
            Here is the input text:

            {text}

            Based on the text, generate please:
            - 1 debate topic
            - 1 social project idea
            - 1 business idea

            Separate each thing with a new line (\n\n) so I can parse it later.
            """
    
    def to_dict(self, text):
        return {
            "system_prompt": self.system_prompt,
            "example_question": self.example_question,
            "example_answer": self.example_answer,
            "question_prompt": self.get_question_prompt(text)
        }