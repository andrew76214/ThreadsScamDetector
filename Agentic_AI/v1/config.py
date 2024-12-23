from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnableConfig

WORK_SOURCE_PATH = "../../Datasets/data_1.json"
GAMBLE_SOURCE_PATH = "../../Datasets/data_2.json"
EMOTIONAL_SOURCE_PATH = "../../Datasets/data_3.json"
INVESTMENT_SOURCE_PATH = "../../Datasets/data_4.json"

RECURSION_LIMIT = RunnableConfig(recursion_limit=50)
LOCAL_LLM = ChatOllama(model="llama3.2:3b", format="json", temperature=0)