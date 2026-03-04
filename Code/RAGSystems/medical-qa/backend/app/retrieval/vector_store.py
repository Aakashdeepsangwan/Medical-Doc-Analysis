### Cosine Similarity Search  and top 20 chunks   
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List, Annotated 
from langchain_core.documents import Document

# Import the embedder class
from ingestion.embedder import embedder # this is the wrong import


class vector_store :
    
    def __init__ (self, embedder) :
        self.embedder = embedder


    def retriever(self, query : str, top_k :int, document : List[Document] ) -> List[Document] :
        """ Will return the top k outputs from the FAISS Vector store """
        retriever =  self.embedder.embedded_documnet(document).as_retriever(search_kwargs={"k": 5} )
        return retriever.invoke(query) # this will return the top k outputs, 


    
    

    if __name__ == '__main__':
        print("Hey, Akash! You are AI Software Developer now, How you feeling ?")

