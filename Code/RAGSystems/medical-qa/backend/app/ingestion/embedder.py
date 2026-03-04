from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List, Annotated 
from langchain_core.documents import Document

class embedder :

    def __init__(self, chunks : List[Document]) :
        self.chunks = chunks
        
    # Faiss has two function .from_texts  and from_documents -> takes two parameters and require second parameter as Embeddings


    def embeddings(self) :
        
        Embeddings  = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
        return Embeddings



    def embed_text(self, query : str) :
        """create embeddings of a string -> returns vector """
        Embeddings = self.embeddings() 
        vector = FAISS.from_texts(query, Embeddings)
        return vector



    def emebed_document(self, document : List[Document]) :
        """ Converts documents into a vector store  """
        Embeddings = self.embeddings()
        vectorstore = FAISS.from_documents(document, Embeddings) 
        return vectorstore


    