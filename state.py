from typing import TypedDict, Optional

class InvoiceState(TypedDict, total=False):
    # Input
    invoice_payload: dict
    
    # From INTAKE (Step 1)
    raw_id: str
    ingest_ts: str
    validated: bool

    # From UNDERSTAND (Step 2)
    parsed_invoice: dict

    # From PREPARE (Step 3)
    vendor_profile: dict
    normalized_invoice: dict
    flags: dict

    # From RETRIEVE (Step 4)
    matched_pos: list
    matched_grns: list
    history: list

    # From MATCH_TWO_WAY (Step 5)
    match_score: float
    match_result: str
    tolerance_pct: float
    match_evidence: dict

    # From CHECKPOINT_HITL (Step 6)
    hitl_checkpoint_id: str
    review_url: str
    paused_reason: str

    # From HITL_DECISION (Step 7)
    human_decision: str
    reviewer_id: str
    resume_token: str
    next_stage: str

    # From RECONCILE (Step 8)
    accounting_entries: list
    reconciliation_report: dict

    # From APPROVE (Step 9)
    approval_status: str
    approver_id: str

    # From POSTING (Step 10)
    posted: bool
    erp_txn_id: str
    scheduled_payment_id: str

    # From NOTIFY (Step 11)
    notify_status: dict
    notified_parties: list

    # From COMPLETE (Step 12)
    final_payload: dict
    audit_log: list
    status: str