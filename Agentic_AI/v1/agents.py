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
            請回答是否為詐騙？你的原因？
            'button': '是/否', 'reason': '你的回答'
            """,
            input_variables=["question", "post_text"],
        )
        self.pipeline = self.prompt | LOCAL_LLM | JsonOutputParser()
        self.question = question
        self.post_text = post_text
        
    def response(self):
        response = self.pipeline.invoke({"question": self.question, "post_text": self.post_text})
        print(response)
        
        if response == {}:
            return {"error": str("LLM didn\'t response")}
        
        response = response["reason"]
        response = filter_text(response)
        return response
    
class coordinator:
    def __init__(self, judge_response, question, post_text):
        self.summary_prompt = PromptTemplate(
            template="""
            問題: {question} 
            貼文文字: {post_text}
            
            以下是兩個代理的回應：
            第一個代理的回應: {judge_1} 
            第二個代理的回應: {judge_2}
            根據以上內容，請統整兩個回應，請回答是否為詐騙？你的原因？
            使用以下這個格式
            'button': '是/否', 'reason': '你的回答'
            """,
            input_variables=["question", "post_text", "judge_1", "judge_2"],
        )
        self.pipeline = self.summary_prompt | LOCAL_LLM | JsonOutputParser()
        self.judge_response = judge_response
        self.question = question
        self.post_text = post_text
        
    def response(self):
        judge_1, judge_2 = self.judge_response
        print(self.judge_response[0])
        response = self.pipeline.invoke({"question": self.question, "post_text": self.post_text, "judge_1": judge_1, "judge_2": judge_2})
        print(response)
        
        if response == {}:
            return {"error": str("LLM didn\'t response")}

        response = response["reason"]
        response = filter_text(response)
        return response