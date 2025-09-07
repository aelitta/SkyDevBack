# src/hr_agent/graph_flow.py
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.utils.graph_utils import StateHrAgent
from src.agent.nodes import greet, human, router, compatibility_stub, interview_stub

memory = MemorySaver()

flow = StateGraph(StateHrAgent)

flow.add_node("greet", greet)
flow.add_node("human", human)
flow.add_node("router", router)
flow.add_node("compatibility_stub", compatibility_stub)
flow.add_node("interview_stub", interview_stub)
flow.set_entry_point("greet")
flow.compile(checkpointer=memory)

hr_graph = flow.compile(checkpointer=memory)
