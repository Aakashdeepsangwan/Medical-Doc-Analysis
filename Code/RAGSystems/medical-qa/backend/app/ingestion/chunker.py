from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings


from typing import List

class chunker :

    def __init__(self, path) :
        self.path = path


    """ 
    - docs  : loaded document will be a list
    - Each element inside the doc, is Document
    - Document has 1) metadata  2) page_content
    - Metadata is a dictionary : includes "source", "page"
    - page_content is of str type
    """

    def loaded_document(self) -> List[str]:
        """ Load the PDF document and returnt the page_content to apply semantic chunking """

        docs = PyPDFLoader(self.path).load() # now it's in the document form
        str_docs = [doc.page_content for doc in docs]
        return str_docs
    

    def semantic_chunks(self) -> List[Document] :
        Embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
        
        chunker = SemanticChunker(
            embeddings=Embeddings,
            breakpoint_threshold_type  = "percentile",
            breakpoint_threshold_amount = 95
        )

        chunks = chunker.create_documents(self.loaded_document()) 
        return chunks

        


    
chunk1 = chunker("/Users/akashdeepsangwan/Desktop/Code/RAGSystems/Can AI Build Systems (1).pdf")

semantic_chunks = chunk1.semantic_chunks()
print("Number of chunks : ", len(semantic_chunks))
print(semantic_chunks[1].page_content)
print("--------------------_____________-------------------------------------------\n\n\n")
print(semantic_chunks[2].page_content)




        



    





        

        
        



