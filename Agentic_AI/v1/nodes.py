from typing_extensions import TypedDict
from typing import List
from langchain.schema import Document

class GraphState(TypedDict):
    """
    Represents the state of our multi-agents scam detection.

    Attributes:
        post: The Threads post or text content to be analyzed (list of strings if needed).
        coordinator: The coordinator's decision or instruction.
        judge: The judge's reasoning or partial output (list of strings).
        keyword_memory: The shared scam keyword knowledge base (list of strings).
        evaluator: The final evaluation or verdict.
    """
    post: List[str]
    coordinator: str
    judge: List[str]
    keyword_memory: List[str]
    evaluator: str
    
class Nodes:
    def __init__(
        self, 
        retriever,        # Could be used to retrieve external knowledge or vectorstore
        rag_chain,        # If you still want an LLM chain for RAG style generation
        retrieval_grader, # Could be used to assess knowledge retrieval quality
        post_grader,
        judge,            # LLM or rule-based module that decides "is scam?" + reason
        keyword_memory,   # Module that stores/updates known scam keywords
        answer_grader,    # Additional grader if needed (or remove if not used)
        evaluator         # Final evaluator to confirm correctness or to provide a final verdict
    ):
        self.retriever = retriever
        self.rag_chain = rag_chain
        self.retrieval_grader = retrieval_grader
        self.post_grader = post_grader
        self.judge = judge
        self.keyword_memory = keyword_memory
        self.answer_grader = answer_grader
        self.evaluator = evaluator
        
    def grade_post(self, state: GraphState) -> GraphState:
        """
        Coordinator decides if we need external knowledge or existing keyword memory
        before passing the post to the Judge for a scam decision.
        
        Args:
            state (GraphState): The current graph state
        
        Returns:
            GraphState: Updated state with coordinator instructions
        """
        
        print("---POST GRADER STEP---")
        # Example: decide if we want to retrieve external knowledge
        # or just rely on the existing keyword memory based on the post length, etc.
        
        post_text = state["post"]["text"]
        post_type = state["post"]["type"]
        
        post_grader_response = self.post_grader.invoke({"post_text": post_text, "post_type": post_type})
        
        if post_grader_response['button'].lower() == "yes":
            print("---Need External Knowledge---")
            coordinator_decision = "Need External Knowledge"
        else:
            print("---LLM call---")
            coordinator_decision = "LLM call"

        state["coordinator"] = coordinator_decision
        return state

    def judge_step(self, state: GraphState) -> GraphState:
        """
        The Judge (LLM or other module) checks whether the post is scam or not, 
        possibly referencing existing scam keywords or external info.
        
        Args:
            state (GraphState): The current graph state
        
        Returns:
            GraphState: Updated state with the judge's reasoning
        """
        print("---JUDGE STEP---")
        post_content = "\n".join(state["post"])
        coordinator_decision = state["coordinator"]

        # Example: pass post_content + coordinator_decision to an LLM for classification
        judge_response = self.judge.invoke({
            "post": post_content,
            "coordinator_decision": coordinator_decision
        })
        # judge_response could be something like: {"is_scam": "Yes", "reason": "High paying job scam..."}
        # For simplicity, store reason or partial output in state["judge"]
        state["judge"] = [str(judge_response)]
        return state

    def update_keyword_memory(self, state: GraphState) -> GraphState:
        """
        Update or retrieve known scam keywords from the memory module.
        Could also add newly detected suspicious phrases from the post.
        
        Args:
            state (GraphState): The current graph state
        
        Returns:
            GraphState: Updated keyword_memory in state
        """
        print("---UPDATE KEYWORD MEMORY STEP---")
        # Example logic: 
        # 1. Extract any suspicious phrases from judge output
        # 2. Insert them into the shared keyword memory if not already there

        judge_output = state["judge"]
        # Suppose we look for a 'new_keywords' field from judge's response
        # This is pseudo-code, actual structure depends on judge's output
        suspicious_phrases = []
        
        # (Pseudo) parse or guess from judge output:
        for line in judge_output:
            if "new_keywords:" in line:
                # parse out keywords
                suspicious_phrases.append("some_suspicious_term")

        # Update the state's keyword_memory (avoid duplicates)
        for phrase in suspicious_phrases:
            if phrase not in state["keyword_memory"]:
                state["keyword_memory"].append(phrase)

        # Optional: also have self.keyword_memory module do something more advanced
        # e.g. self.keyword_memory.invoke({"add_keywords": suspicious_phrases})

        return state
    
    def grade_answer(self, state: GraphState) -> GraphState:
        """
        Coordinator decides the response from judge is good or bad.
        If answer is bad, then return back to regenerate.
        
        Args:
            state (GraphState): The current graph state
        
        Returns:
            GraphState: Updated state with coordinator instructions
        """
        print("---POST GRADER STEP---")

        
        
        # Example: decide if we want to retrieve external knowledge
        # or just rely on the existing keyword memory based on the post length, etc.
        if len(state["post"]) > 100:
            # Suppose we decide to retrieve external knowledge
            coordinator_decision = "Need External Knowledge"
            # Could do something like: external_docs = self.retriever.invoke(...)

        else:
            coordinator_decision = "Use Keyword Memory"

        state["coordinator"] = coordinator_decision
        return state

    def evaluate_step(self, state: GraphState) -> GraphState:
        """
        The Evaluator agent checks if the judge's decision is correct and finalizes the verdict.
        
        Args:
            state (GraphState): The current graph state
        
        Returns:
            GraphState: Final state with evaluator decision
        """
        print("---EVALUATOR STEP---")
        # Example logic:
        # 1. Evaluate judge's output, check if it contradicts known keywords
        # 2. Possibly request clarifications or chain-of-thought from the judge
        # 3. Produce final verdict: "是詐騙" or "不是詐騙"

        judge_output = state["judge"]
        # We can pass the judge output + post to self.evaluator
        evaluation = self.evaluator.invoke({
            "judge_output": judge_output,
            "post": state["post"]
        })
        
        # Suppose the evaluator returns something like: {"verdict": "是詐騙", "reason": "..."}
        state["evaluator"] = str(evaluation["verdict"])
        return state