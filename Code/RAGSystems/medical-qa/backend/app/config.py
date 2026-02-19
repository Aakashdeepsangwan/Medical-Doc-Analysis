from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    openai_embedding_model: str = "text-embedding-3-small"
    openai_llm_model: str = "gpt-4o-mini"
    cohere_api_key: str
    database_url: str
    sync_database_url: str
    redis_url: str = "redis://localhost:6379/0"
    app_env: str = "development"
    secret_key: str
    chunk_size: int = 512
    chunk_overlap: int = 50
    top_k_retrieval: int = 20
    top_k_rerank: int = 5

    class Config:
        env_file = ".env"

settings = Settings()