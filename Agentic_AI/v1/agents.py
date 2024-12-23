from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from config import LOCAL_LLM
from utils import filter_text

class judge:
    def __init__(self, question, post_text):
        self.prompt = PromptTemplate(
            template="""
            問題: {question} 
            貼文文字: {post_text} 
            回答: 
            """,
            input_variables=["question", "post_text"],
        )
        self.pipeline = self.prompt | LOCAL_LLM | JsonOutputParser()
        self.question = question
        self.post_text = post_text
        
    def response(self):
        response = (self.pipeline.invoke({"question": self.question, "post_text": self.post_text}))['content']
        response = filter_text(response)
        return response