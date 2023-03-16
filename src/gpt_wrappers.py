import openai

class ChatGPTWithMemory:
    """
        A wrapper for the OpenAI Chat API that allows for a memory to be maintained
        between calls to the API. This is useful for a chatbot that is maintaining
        a conversation with a user.
    """
    def __init__(self, system_prompt, model="gpt-3.5-turbo"):
        self.messages = []
        self.model = model
        self.system_prompt = system_prompt

    def initialize_with_question_answer(self, question, answer):
        self.messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": question
            },
            {
                "role": "assistant",
                "content": answer
            }
        ]
        
    def generate(self, question):
        self.messages.append(
            {
                "role": "user",
                "content": question
            }
        )
        response = openai.ChatCompletion.create(
            model=self.model,
            messages = self.messages
        )
        self.messages.append(
            {
                "role": "assistant",
                "content": response['choices'][0]['message']['content']
            }
        )
        return response['choices'][0]['message']['content']