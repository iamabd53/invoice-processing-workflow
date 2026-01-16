from langgraph.graph import StateGraph, START, END
from typing import TypedDict
from state import InvoiceState


def intake(state):
    return {"raw_id": "INV-001", "ingest_ts": "2025-01-15" , "validated": True} #{"message": state["invoice_payload"]}

def understand(state):
    return {"parsed_invoice": {} }

def prepare(state):
    return {"vendor_profile": {},  "normalised_invoice":{}, "flags": {}}

def retrieve(state):
    return {
        "matched_pos": [],
        "matched_grns": [],
        "history": []
    }

def match_two_way(state):
    return {
        "match_score": 0.95,
        "match_result": "MATCHED",  # or "FAILED"
        "tolerance_pct": 0.05,
        "match_evidence": {}
    }

def decision(state):
    if state["match_result"] == "MATCHED":
        return "RECONCILE"
    else:
        return "CHECKPOINT_HITL" 

def checkpoint_hitl(state):
    return {
        "hitl_checkpoint_id": "HITL-001",
        "review_url": "http://review.com/123",
        "paused_reason": "Manual review required"
    }

def hitl_decision(state):
    if state["match_result"] == "ACCEPT":
        return "ACCEPT"
    else:
        return "REJECT"

def reconcile(state):
    return {
        "accounting_entries": [],
        "reconciliation_report": {}
    }

def approve(state):
    return {
        "approval_status": "AUTO_APPROVED",
        "approver_id": "SYSTEM"
    }

def posting(state):
    return {
        "posted": True,
        "erp_txn_id": "TXN-12345",
        "scheduled_payment_id": "PAY-001"
    }

def notify(state):
    return {
        "notify_status": {"email": "sent"},
        "notified_parties": ["vendor", "finance"]
    }

def complete(state):
    return {
        "final_payload": state,
        "audit_log": [],
        "status": "COMPLETED"
    }  

graph = StateGraph(InvoiceState)
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
result = app.invoke({"invoice_payload": {"invoice_id": "INV-001", "vendor_name": "Acme Corp", "amount": 1000}})
print(result)