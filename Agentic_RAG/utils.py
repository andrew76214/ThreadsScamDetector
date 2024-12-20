from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_milvus import Milvus
from langchain_community.embeddings import HuggingFaceEmbeddings
from langgraph.graph import StateGraph, END
from nodes import GraphState

def process_and_store_documents(urls, chunk_size=250, chunk_overlap=0, collection_name="rag_milvus", milvus_uri="./milvus_rag.db"):
    """
    Process a list of URLs to load documents, split them into chunks, and store them in a Milvus vector store.

    Args:
        urls (list): List of URLs to load documents from.
        chunk_size (int): Size of text chunks for splitting. Defaults to 250.
        chunk_overlap (int): Overlap between chunks. Defaults to 0.
        collection_name (str): Name of the Milvus collection. Defaults to "rag_milvus".
        milvus_uri (str): URI for the Milvus database. Defaults to "./milvus_rag.db".

    Returns:
        retriever: A retriever instance for the stored vector store.
    """
    # Load documents from URLs
    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    doc_splits = text_splitter.split_documents(docs_list)

    # Store chunks in Milvus vector store
    vectorstore = Milvus.from_documents(
        documents=doc_splits,
        collection_name=collection_name,
        embedding=HuggingFaceEmbeddings(),
        connection_args={"uri": milvus_uri},
    )

    return vectorstore.as_retriever()


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