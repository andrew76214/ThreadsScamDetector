from nodes import GraphState

from langgraph.graph import StateGraph, END

def build_graph(nodes):
    workflow = StateGraph(GraphState)

    # Define the nodes
    workflow.add_node("websearch", nodes.web_search) # web search
    workflow.add_node("retrieve", nodes.retrieve) # retrieve
    workflow.add_node("grade_documents", nodes.grade_documents) # grade documents
    workflow.add_node("generate", nodes.generate) # generate
    
    # Build graph
    workflow.set_conditional_entry_point(
        nodes.route_question,
        {
            "websearch": "websearch",
            "vectorstore": "retrieve",
        },
    )

    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_conditional_edges(
        "grade_documents",
        nodes.decide_to_generate,
        {
            "websearch": "websearch",
            "generate": "generate",
        },
    )
    workflow.add_edge("websearch", "generate")
    workflow.add_conditional_edges(
        "generate",
        nodes.grade_generation_v_documents_and_question,
        {
            "not supported": "generate",
            "useful": END,
            "not useful": "websearch",
        },
    )
    
    return workflow