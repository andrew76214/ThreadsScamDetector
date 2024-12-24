from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from config import LOCAL_LLM
from utils import filter_text

# External Knowledge
class retriever:
    1
class judge:
    def __init__(self, question, post_text, keyword):
        self.prompt = PromptTemplate(
            template="""
            問題: {question} 
            貼文文字: {post_text} 
            請回答是否為詐騙？你的原因？
            請提供你判斷的關鍵字
            'button': '是/否', 'reason': '你的回答', 'keyword': '關鍵字'
            """,
            input_variables=["question", "post_text", "keyword"],
        )
        self.pipeline = self.prompt | LOCAL_LLM | JsonOutputParser()
        self.question = question
        self.post_text = post_text
        self.keyword = keyword
        
    def response(self):
        response = self.pipeline.invoke({"question": self.question, "post_text": self.post_text, "keyword": self.keyword})
        print(response)
        
        if response == {}:
            return {"error": str("LLM didn\'t response")}
        
        return filter_text(response["button"]), filter_text(response["reason"]), filter_text(response["keyword"])
    
class coordinator:
    def __init__(self, judge_response, post_text, post_type):
        self.post_grader_prompt = PromptTemplate(
            template="""
            貼文文字: {post_text}
            貼文種類: {post_type}
            
            根據以上內容，需要尋求外部資料給LLM回答嗎？還是不用？
            使用以下這個格式
            'button': 'Yes/No'
            """,
            input_variables=["post_text", "post_type"],
        )
        self.answer_grader_prompt = PromptTemplate(
            template="""
            貼文文字: {post_text}
            貼文種類: {post_type}
            
            根據以上內容，判斷是否需要重新生成回答
            使用以下這個格式，
            'button': 'Yes/No'
            """,
            input_variables=["post_text", "post_type"],
        )
        self.summary_prompt = PromptTemplate(
            template="""
            問題: {question} 
            貼文文字: {post_text}
            貼文種類: {post_type}
            
            以下是兩個代理的回應：
            第一個代理的回應: {judge_1} 
            第二個代理的回應: {judge_2}
            第三個代理的回應: {judge_3}
            根據以上內容，請統整兩個回應，請回答是否為{post_type}詐騙？你的原因？
            使用以下這個格式
            'button': 'Yes/No', 'reason': '你的回答'
            """,
            input_variables=["post_text", "post_type", "judge_1", "judge_2", "judge_3"],
        )
        self.post_grader_pipeline = self.post_grader_prompt | LOCAL_LLM | JsonOutputParser()
        self.answer_grader_pipeline = self.answer_grader_prompt | LOCAL_LLM | JsonOutputParser()
        self.summary_pipeline = self.summary_prompt | LOCAL_LLM | JsonOutputParser()
        self.judge_response = judge_response
        self.post_text = post_text
        self.post_type = post_type
    
    def post_grader_response(self):
        response = self.post_grader_pipeline.invoke({"post_text": self.post_text, "post_type": self.post_type})
        print(response)
        
        if response == {}:
            return {"error": str("LLM didn\'t response")}

        return filter_text(response["button"])
    
    def answer_grader_response(self):
        response = self.answer_grader_pipeline.invoke({"post_text": self.post_text, "post_type": self.post_type})
        print(response)
        
        if response == {}:
            return {"error": str("LLM didn\'t response")}

        return filter_text(response["button"])
    
    def summary_response(self):
        judge_1, judge_2, judge_3 = self.judge_response
        print(self.judge_response[0])
        response = self.summary_pipeline.invoke({"post_text": self.post_text,
                                                 "post_type": self.post_type,
                                                 "judge_1": judge_1, 
                                                 "judge_2": judge_2,
                                                 "judge_3": judge_3})
        print(response)
        
        if response == {}:
            return {"error": str("LLM didn\'t response")}

        return filter_text(response["button"]), filter_text(response["reason"])