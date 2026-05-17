import requests
from requests.auth import HTTPBasicAuth
import os
from datetime import datetime
from utils.ai_detector import is_ai_originated

def fetch_jira_activity(project_key: str = None) -> list:
    """
    Fetch real Jira issues and their changelogs.
    Treats each changelog entry as an AI agent action.
    """
    url = os.getenv("JIRA_URL")
    email = os.getenv("JIRA_EMAIL")
    token = os.getenv("JIRA_API_TOKEN")

    if not all([url, email, token]):
        return []

    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    # Build JQL query
    jql = f"project = {project_key} ORDER BY updated DESC" if project_key else "ORDER BY updated DESC"
    
    search_url = f"{url}/rest/api/3/search/jql"
    params = {
        "jql": jql,
        "maxResults": 20,
        "expand": "changelog",
        "fields": "summary,status,priority,assignee,creator,updated,created,issuetype"
    }

    try:
        response = requests.get(search_url, headers=headers, auth=auth, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Jira API error: {e}")
        return []

    logs = []
    log_id = 1

    for issue in data.get("issues", []):
        key = issue["key"]
        summary = issue["fields"].get("summary", "")
        changelog = issue.get("changelog", {}).get("histories", [])

        for history in changelog:
            author = history.get("author", {}).get("displayName", "Unknown")
            timestamp = history.get("created", "")
            
            # Format timestamp
            try:
                dt = datetime.strptime(timestamp[:19], "%Y-%m-%dT%H:%M:%S")
                ts_formatted = dt.strftime("%H:%M:%S")
            except:
                ts_formatted = timestamp[:8] if timestamp else "00:00:00"

            for item in history.get("items", []):
                field = item.get("field", "")
                from_val = item.get("fromString", "") or ""
                to_val = item.get("toString", "") or ""

                # Map Jira field changes to action types
                action = map_to_action(field, from_val, to_val)
                target = f"Ticket {key} — {summary[:50]} | {field}: {from_val} → {to_val}"
                risk = assess_risk(action, field, to_val, summary)

                logs.append({
                    "id": log_id,
                    "timestamp": ts_formatted,
                    "source": "Jira",
                    "agent": f"Actor: {author}",
                    "action": action,
                    "target": target,
                    "risk_level": risk,
                    "status": classify_status(risk),
                    "raw": {
                        "issue_key": key,
                        "field": field,
                        "from": from_val,
                        "to": to_val,
                        "author": author
                    }
                })
                # Detect AI-originated actions
                logs[-1]["ai_detection"] = is_ai_originated(logs[-1])
                log_id += 1

        # Also log the issue creation itself
        creator = issue["fields"].get("creator", {}).get("displayName", "Unknown")
        created = issue["fields"].get("created", "")
        try:
            dt = datetime.strptime(created[:19], "%Y-%m-%dT%H:%M:%S")
            ts_formatted = dt.strftime("%H:%M:%S")
        except:
            ts_formatted = "00:00:00"

        logs.append({
            "id": log_id,
            "timestamp": ts_formatted,
            "source": "Jira",
            "agent": f"Actor: {creator}",
            "action": "CREATE",
            "target": f"Ticket {key} — {summary[:60]}",
            "risk_level": "low",
            "status": "allowed",
            "raw": {"issue_key": key, "field": "creation", "from": "", "to": "", "author": creator}
        })
        log_id += 1

    # Sort by timestamp
    logs.sort(key=lambda x: x["timestamp"])
    return logs


def map_to_action(field: str, from_val: str, to_val: str) -> str:
    field_lower = field.lower()
    if field_lower == "status":
        return "EDIT"
    elif field_lower == "priority":
        return "EDIT"
    elif field_lower == "assignee":
        return "ASSIGN"
    elif field_lower == "description":
        return "EDIT"
    elif field_lower == "comment":
        return "COMMENT"
    elif field_lower == "attachment":
        return "CREATE" if to_val else "DELETE"
    elif not to_val and from_val:
        return "DELETE"
    else:
        return "EDIT"


def assess_risk(action: str, field: str, to_val: str, summary: str) -> str:
    field_lower = field.lower()
    to_lower = (to_val or "").lower()
    summary_lower = summary.lower()

    # High risk
    if action == "DELETE":
        return "high"
    if "salary" in summary_lower or "confidential" in summary_lower or "credential" in summary_lower:
        return "high"

    # Medium risk
    if field_lower == "priority" and "critical" in to_lower:
        return "medium"
    if field_lower == "assignee":
        return "medium"
    if "security" in summary_lower or "compliance" in summary_lower or "audit" in summary_lower:
        return "medium"

    return "low"


def classify_status(risk: str) -> str:
    if risk == "high":
        return "blocked"
    elif risk == "medium":
        return "flagged"
    return "allowed"


def get_jira_projects() -> list:
    """Fetch available Jira projects for the dropdown."""
    url = os.getenv("JIRA_URL")
    email = os.getenv("JIRA_EMAIL")
    token = os.getenv("JIRA_API_TOKEN")

    if not all([url, email, token]):
        return []

    auth = HTTPBasicAuth(email, token)
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(
            f"{url}/rest/api/3/project",
            headers=headers, auth=auth
        )
        response.raise_for_status()
        projects = response.json()
        return [{"key": p["key"], "name": p["name"]} for p in projects]
    except Exception as e:
        print(f"Could not fetch projects: {e}")
        return []

