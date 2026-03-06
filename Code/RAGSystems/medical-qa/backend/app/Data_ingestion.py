from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings
from typing import List
from langchain_community.vectorstores import FAISS


class data_ingestion :


    def __init__(self, path) :
        self.path  = path



    # document loader

    def loader(self) :
        load= PyPDFLoader(self.path).load()
        str_doc = [doc.page_content for doc in load]
        return str_doc

    def embeddings(self) :
        Embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        return Embeddings

    def semantic_chunking(self) -> List[Document]:
        
        chunker = SemanticChunker(
            embeddings=self.embeddings(),
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=95
        )
        # Error : create_document
        chunks = chunker.create_documents(self.loader())
        return chunks


    def vector_store(self) :
        vs = FAISS.from_documents(self.semantic_chunking(), self.embeddings())
        return vs

    


    
    