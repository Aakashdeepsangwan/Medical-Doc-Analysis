
class retrieval :
    """This class takes the query and return the top_k outputs for that query """

    def __init__(self, vector_store, query, top_k) :
        self.vector_store = vector_store
        self.query = query
        self.top_k = top_k

    def retriever(self) :
        output = self.vector_store.as_retriever(search_kwargs={"k": self.top_k})
        array = output.invoke(self.query)
        
        top_results = [doc.page_content for doc in array]
        return top_results
        
        
        

    

    