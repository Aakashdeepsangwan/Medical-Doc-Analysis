from langchain_core.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List, Annotated 
from langchain_core.documents import Document



def __init__(self, chunks : List[Document]) :
    self.chunks = chunks
    


def vectore_store(self) :

    Embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-minilm-l6-v2")
    vectorstore = FAISS.from_document(self.chunks, Embeddings)
    return vectorstore
    
    