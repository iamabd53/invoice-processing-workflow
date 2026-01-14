from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class MyState(TypedDict):
    message: str

def intake(state):
    return {"message": state["message"] + " → passed through INTAKE"}

def understand(state):
    return {"message": state["message"] + " → passed through UNDERSTAND"}

def prepare(state):
    return {"message": state["message"] + " -> passed through PREPARE"}

def retrieve(state):
    return {"message": state["message"] +  " -> passed through RETRIEVE"}

def match_two_way(state):
    return {
        "message": state["message"] +  " -> passed through MATCH_TWO_WAY",
        "match_result": "FAILED"}


def decision(state):
    if state["match_result"] == "MATCHED":
        return "RECONCILE"
    else:
        return "CHECKPOINT_HITL" 

def reconcile(state):
    return {"message": state["message"] + "passed through RECONCILE"} 

def checkpoint_hitl(state):
    return {
        "message": state["message"] + "passed through CHECKPOINT_HITL",
        "match_result": "REJECT"} 

def hitl_decision(state):
    if state["match_result"] == "ACCEPT":
        return "ACCEPT"
    else:
        return "REJECT"

def approve(state):
    return {"message": state["message"] + "passed through APPROVE"} 

def posting(state):
    return {"message": state["message"] + "passed through POSTING"} 

def notify(state):
    return {"message": state["message"] + "passed through NOTIFY"}

def complete(state):
    return {"message": state["message"] + "passed through COMPLETE"}  

graph = StateGraph(MyState)
graph.add_node("INTAKE", intake)
graph.add_node("UNDERSTAND", understand)
graph.add_node("PREPARE", prepare)
graph.add_node("RETRIEVE", retrieve)
graph.add_node("MATCH_TWO_WAY", match_two_way)
#graph.add_node("DECISION", decision)
graph.add_node("RECONCILE", reconcile)
graph.add_node("CHECKPOINT_HITL", checkpoint_hitl)


graph.add_node("APPROVE", approve)
graph.add_node("POSTING", posting)
graph.add_node("NOTIFY", notify)
graph.add_node("COMPLETE", complete)

graph.add_edge(START, "INTAKE")
graph.add_edge("INTAKE", "UNDERSTAND")
graph.add_edge("UNDERSTAND", "PREPARE")
graph.add_edge("PREPARE", "RETRIEVE")
graph.add_edge("RETRIEVE", "MATCH_TWO_WAY")

graph.add_conditional_edges("MATCH_TWO_WAY", decision, 
                            {"RECONCILE": "RECONCILE",
                            "CHECKPOINT_HITL": "CHECKPOINT_HITL"} )

graph.add_conditional_edges("CHECKPOINT_HITL", hitl_decision,
                            {"ACCEPT": "RECONCILE",
                            "REJECT": END})

graph.add_edge("RECONCILE", "APPROVE")
graph.add_edge("APPROVE", "POSTING")
graph.add_edge("POSTING", "NOTIFY")
graph.add_edge("NOTIFY", "COMPLETE")
graph.add_edge("COMPLETE", END)






app = graph.compile()
result = app.invoke({"message" : "hello"})
print(result)