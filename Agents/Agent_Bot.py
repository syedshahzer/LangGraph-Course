from os import getenv
from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv # used to store secret stuff like API keys or configuration values
from chat_openrouter import ChatOpenRouter

load_dotenv()
# print("OpenRouter API Key:", getenv("OPENROUTER_API_KEY"))  # For debugging, remove in production
class AgentState(TypedDict):
    messages: List[HumanMessage]

# llm = ChatOpenAI(
#     model_name='mistralai/devstral-small:free',
#     openai_api_key=getenv("OPENROUTER_API_KEY"),
#     openai_api_base="https://openrouter.ai/api/v1"
# )
llm = ChatOpenRouter(
    model_name='mistralai/devstral-small:free'
)    

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])  # call the model directly
    print(f"\nAI: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END) 
agent = graph.compile()

user_input = input("Enter: ")
while user_input != "exit":
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input("Enter: ")
