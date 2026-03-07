# Run from backend directory (not from app/):
#   From RAGSystems:  cd medical-qa/backend && python3 -m app.main
#   From app/:       cd .. && python3 -m app.main

from app.Data_ingestion import data_ingestion
from app.retrieval import retrieval

# async function let your program do other work while waiting on slow operations(I/0)
# Instead of Blocking until each one finishes
class main :
    
    def __init__(self, query : str, top_k : int):
        self.query = query
        self.top_k  = top_k

    def test(self, path: str):
        data_instance = data_ingestion(path)
        vs = data_instance.vector_store()
        answer = retrieval(vs, self.query, self.top_k).retriever()

        return answer[1]


if __name__ == "__main__":
    query = "what are encoders and how they are related to transformers?"
    k = 2
    path = "/Users/akashdeepsangwan/Desktop/Code/RAGSystems/NIPS-2017-attention-is-all-you-need-Paper.pdf"
    instance = main(query, k)
    print(instance.test(path))


