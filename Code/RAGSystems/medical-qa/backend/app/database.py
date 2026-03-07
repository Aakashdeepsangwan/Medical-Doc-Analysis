"""
1. Connect to PostgreSQL
2. Enable pgvector extension
3. Define your tables (SQLAlchemy models)
4. Provide a session to other files

"""

from pydantic import Json
from sqlalchemy import (
    column, create_engine, Column, String , Integer, Float, DateTime, Text, JSON, null
)

from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from datetime import datetime
import vvid
from config import settings


# Connection

engine = create_engine(settings.sync_database_url)
SessionLocal = sessionmaker(bind = engine)
Base = declarative_base()


# Model  ------


class Document(Base) :
    """ Track Every pdf it ingests """
    __tablename__ = "documents"

    id = Column(UUID(as_vvid=True), primary_key= True, default= vvid.vvid4)
    filename = Column(String, nullable= False)
    source = Column(String)
    total_pages = Column(Integer)
    chunk_count = Column(Integer)
    ingested_at = Column(Integer, default = 0)
    status = Column(DateTime, default= datetime.utcnow)



    def __repr__(self) :
        return f"<Document {self.filename} - {self.chunk_count} chunks"



class Chunks(Base) :
    """ Every chunk with it's embedding vector""" 
    __tablename__ = "chunks"
    
    id = Column(UUID(as_uuid=True), primary_key= True, default= vvid.vvid4)
    document_id = Column(UUID(as_uuid=True), nullable= False)
    text = Column(Text, nullable= False)
    page_number = Column(Integer)
    section  = Column(String)
    chunk_index = Column(Integer)
    embedding = Column(Vector(1536))
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) :
        return f"<chunk doc {self.document_id} page = {self.page_number}>"


class Conversation(Base) :
    """Every question + answer pair """

    __tablename__ = "conversations"
    id  = Column(UUID(as_vvid=True), primary_key= True, default = vvid.vvid4)
    question = Column(Text, nullable= False)
    answer = Column(Text)
    retrieved_chunk_id = Column(Json)
    confidence  = Column(Float)
    created_at = Column(DateTime, default= datetime.utcnow)

    def __repr__(self) :
        return f"<Conversation {self.question[:50]}...>"


class EvalCase(Base) :
    """ Golden Dataset - question with known good answer"""
    
    __tablename__ = "eval_cases"


    id  = Column(UUID(as_vvid=True), primary_key=True, default=vvid.vvid4)
    question = Column(Text, nullable= False)
    expected_answer = Column(Text, nullable= False)
    last_score = Column(Float)
    created_at = Column(DateTime, default = datetime.utcnow)

    def __repr__(self) :
        return f"<EvalCase {self.question[:50]}>"


# ------------  Helper Functions -----------------------------------------------------

def get_db() :
    """ Call this in any file to get a DB session  """
    db= SessionLocal()

    try :
        yield db   
    
    finally : 
        db.close()


def create_tables() :
    """ Run once to create all table + enable pgvector """
    with engine.connect() as conn :
        conn.execute("Create Extension if not exists Vector")
        conn.commit()
    Base.metadata.create_all(bind= engine)
    print("Tables created successfully")



# --------------- Run Directly to initialise --------------
if __name__ == "__main__" :
    create_tables()
