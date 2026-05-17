POLICY_RULES = [
    {"id": "JIRA-NO-DELETE-001", "source": "Jira", "action": "DELETE", "risk": "high", "reason": "Permanent deletion violates audit trail preservation policy (GLBA 7-year retention)."},
    {"id": "CONF-HR-WRITE-002", "source": "Confluence", "action": "EDIT", "keyword": "Salary", "risk": "high", "reason": "HR-restricted pages require explicit human approval for any write action."},
    {"id": "CONF-SENSITIVE-READ-003", "source": "Confluence", "action": "READ", "keyword": "Compensation", "risk": "medium", "reason": "Sensitive compensation data accessed outside agent task scope."},
    {"id": "JIRA-PRIORITY-CRITICAL-004", "source": "Jira", "action": "EDIT", "keyword": "CRITICAL", "risk": "medium", "reason": "CRITICAL priority escalation triggers on-call paging and SLA workflows — requires human approval."},
    {"id": "CONF-INCIDENT-EDIT-005", "source": "Confluence", "action": "EDIT", "keyword": "Incident", "risk": "medium", "reason": "Editing incident response documentation requires change management approval."},
    {"id": "JIRA-MULTI-EDIT-006", "source": "Jira", "action": "EDIT", "keyword": "due date", "risk": "medium", "reason": "Multi-field edits affecting assignment and dates require PM review."},
]

ACTION_COLORS = {
    "READ": "#3B6D11",
    "CREATE": "#185FA5",
    "EDIT": "#854F0B",
    "DELETE": "#A32D2D",
    "COMMENT": "#3C3489",
    "ASSIGN": "#085041",
    "EXPORT": "#5F5E5A",
}

RISK_COLORS = {
    "low": "#3B6D11",
    "medium": "#BA7517",
    "high": "#A32D2D",
}

STATUS_COLORS = {
    "allowed": "#3B6D11",
    "flagged": "#BA7517",
    "blocked": "#A32D2D",
}

def get_triggered_rule(log):
    for rule in POLICY_RULES:
        if rule["source"] == log["source"] and rule["action"] == log["action"]:
            if "keyword" not in rule or rule["keyword"].lower() in log["target"].lower():
                return rule
    return None
