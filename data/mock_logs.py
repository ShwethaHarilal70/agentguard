from datetime import datetime, timedelta
import random

BASE_TIME = datetime(2026, 5, 8, 9, 41, 0)

JIRA_EVENTS = [
    {"source": "Jira", "agent": "Jira Ops Agent", "action": "READ", "target": "Ticket #JRA-1041 — Sprint planning notes", "risk_level": "low"},
    {"source": "Jira", "agent": "Jira Ops Agent", "action": "CREATE", "target": "New ticket — Deploy v2.3 to staging env", "risk_level": "low"},
    {"source": "Jira", "agent": "Jira Ops Agent", "action": "ASSIGN", "target": "Ticket #JRA-1038 assigned to Dev Team", "risk_level": "low"},
    {"source": "Jira", "agent": "Jira Ops Agent", "action": "COMMENT", "target": "Ticket #JRA-1039 — added blocker note", "risk_level": "low"},
    {"source": "Jira", "agent": "Jira Ops Agent", "action": "EDIT", "target": "Ticket #JRA-0892 — changed priority to CRITICAL", "risk_level": "medium"},
    {"source": "Jira", "agent": "Jira Ops Agent", "action": "EDIT", "target": "Ticket #JRA-0711 — modified due date + assignee", "risk_level": "medium"},
    {"source": "Jira", "agent": "Jira Ops Agent", "action": "DELETE", "target": "Ticket #JRA-0550 — permanent delete attempted", "risk_level": "high"},
]

CONFLUENCE_EVENTS = [
    {"source": "Confluence", "agent": "Confluence Agent", "action": "READ", "target": "Page — Engineering Onboarding Guide", "risk_level": "low"},
    {"source": "Confluence", "agent": "Confluence Agent", "action": "READ", "target": "Page — Q3 Sprint Retrospective", "risk_level": "low"},
    {"source": "Confluence", "agent": "Confluence Agent", "action": "CREATE", "target": "New page — Release Notes v2.3 in Engineering space", "risk_level": "low"},
    {"source": "Confluence", "agent": "Confluence Agent", "action": "READ", "target": "Page — Executive Compensation 2026 — restricted space", "risk_level": "medium"},
    {"source": "Confluence", "agent": "Confluence Agent", "action": "EDIT", "target": "Page — Incident Response Playbook — section removed", "risk_level": "medium"},
    {"source": "Confluence", "agent": "Confluence Agent", "action": "EDIT", "target": "Page — Salary Bands Confidential — HR restricted", "risk_level": "high"},
    {"source": "Confluence", "agent": "Confluence Agent", "action": "EXPORT", "target": "Page — Release Notes v2.3 exported as PDF", "risk_level": "low"},
]

def get_all_logs():
    logs = []
    t = BASE_TIME
    all_events = JIRA_EVENTS + CONFLUENCE_EVENTS
    random.seed(42)
    shuffled = all_events[:]
    random.shuffle(shuffled)
    for i, event in enumerate(shuffled):
        t = t + timedelta(minutes=random.randint(1, 3))
        status = classify_status(event)
        logs.append({
            "id": i + 1,
            "timestamp": t.strftime("%H:%M:%S"),
            "source": event["source"],
            "agent": event["agent"],
            "action": event["action"],
            "target": event["target"],
            "risk_level": event["risk_level"],
            "status": status,
        })
    return logs

def classify_status(event):
    if event["risk_level"] == "high":
        return "blocked"
    elif event["risk_level"] == "medium":
        return "flagged"
    return "allowed"

def get_session_stats(logs):
    total = len(logs)
    allowed = sum(1 for l in logs if l["status"] == "allowed")
    return {
        "total": total,
        "allowed": allowed,
        "flagged": sum(1 for l in logs if l["status"] == "flagged"),
        "blocked": sum(1 for l in logs if l["status"] == "blocked"),
        "jira_count": sum(1 for l in logs if l["source"] == "Jira"),
        "confluence_count": sum(1 for l in logs if l["source"] == "Confluence"),
        "compliance_score": round((allowed / total) * 100),
    }
