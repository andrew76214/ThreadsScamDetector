from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain.schema import HumanMessage

class Router:
    def __init__(self, model, format="json", temperature=0):
        self.llm = ChatOllama(model=model, format=format, temperature=temperature)
        self.prompt = PromptTemplate(
            template="""You are an expert at routing a 
            user question to a vectorstore or web search. Use the vectorstore for questions on LLM  agents, 
            prompt engineering, and adversarial attacks. You do not need to be stringent with the keywords 
            in the question related to these topics. Otherwise, use web-search. Give a binary choice 'web_search' 
            or 'vectorstore' based on the question. Return the a JSON with a single key 'datasource' and 
            no premable or explaination. 
            
            Question to route: 
            {question}""",
            input_variables=["question"],
        )
        self.output_parser = JsonOutputParser()

    def route_question(self, question):
        pipeline = self.prompt | self.llm | self.output_parser
        return pipeline.invoke({"question": question})

'''
# Example usage
local_llm = "your_llm_model_here"  # Replace with your model
router = Router(model=local_llm)

question = "llm agent memory"
docs = retriever.get_relevant_documents(question)  # Ensure 'retriever' is defined
print(router.route_question(question))
'''