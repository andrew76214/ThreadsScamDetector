from typing_extensions import TypedDict
from typing import List
from langchain.schema import Document

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        input: post text or other features
        Coordinator: consolidate the opinions of various agents and generate a response.
        Judge: LLM generation and extract the keyword about fraud, and then restore into Keyword Memory.
        Keyword_Memory: Store the keywords about fraud.
        *Evaluator: Evaluate the response from Coordinator, and give some advise back.
        *output: return the post is or is not fraud.
    """
    input: List[str]
    Coordinator: str
    Judge: str
    Keyword_Memory: List[str]
    Evaluator: str
    output: str
    
class Nodes:
    def __init__(self):
        1
        
    def input(self, state):
        1