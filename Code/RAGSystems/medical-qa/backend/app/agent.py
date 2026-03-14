from ssl import CHANNEL_BINDING_TYPES
import anthropic
from anthropic.types import tool_param
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from typing import TypedDict, Annotated, List
import operator
import json

from langgraph.prebuilt.chat_agent_executor import AgentState
from urllib3 import response
from app.retrieval import retrieval
from app.database import get_db, Conversation
from app.config import settings
import uuid

from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_anthropic import ChatAnthropic

# Groq
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv




class agent :
    """ 
    - Define tools (Search medical docs, clarify terms)
    - Build LangGraph State Machine
    - Nodes : router - planner - toolsloop - synthesizer
    - Return final answer + citations + confidence 
    """
    
    # LLM - Initialise 
    groq = ChatGroq(
    model = "qwen/qwen3-32b",
    api_key = os.getenv("groqAPI"))





    class AgentState(TypedDict) :
        question : str
        message : Annotated[List, operator.add]
        retrieved_chunks : list[str]
        answer : str
        confidence : float
        citations : list[str]   #source reference
        iteration_count = int    # prevent infinite loops
        is_medical : bool   # safety router flag




    @tool
    def search_medical_docs(query : str, top_k : int = 5) -> str :
        """ Search the medical document database for relevant information 
        Use this for any question about symptoms, diagnoses, treatments, dosages
        or medical conditions
        """

        results = retrieval(query, top_k= top_k)
        if not results :
            return "No relevant information found!!"
        
        return "\n\n --- \n\n".join(results)


    @tool
    # This can be better refined, if this question is directly given to LLM and then that question is retrived from the vectoreStore

    def refine_search(query : str) -> str :
        """ 
        Run a more specific search when first results were insufficient.
        Use different or more specific keywords than the previous search
        """ 

        results = retrieval(query, top_k=5)

        if not results :
            return "No additional information found!"
        return "\n ---- \n".join(results)



    #_-------- LLM + TOOLS  ---- Binding tool with LLM
    tools = [search_medical_docs, refine_search]
    tool_node = ToolNode(tools) #  Handles the execution Automatically
    llm_with_tools = groq.bind_tools(tools)







    #----- Define Nodes

    def agent_node(state : AgentState) :
        response = agent.llm.invoke(state['message'])
        return {"messages" : [response]}
        

    

    # ------- Graph ----------
    def build_agent()  :
        builder  = StateGraph(AgentState)

        # add nodes
        builder.add_node("agent", agent.agent_node)
        builder.add_node("tools", agent.tool_node)
        

        builder.set_entry_point("agent")


        builder.add_conditional_edges(
            "agent",
            agent.should_continue,
            {"tools" : "tools", "end" : END}

        )




        
    