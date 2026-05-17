"""
AgentGuard AI-originated action detector.
Multi-signal detection engine to identify AI agent vs human actions in Jira.

Detection layers:
1. Content signals — language patterns, structure, grammar
2. Atlassian Intelligence — Jira's built-in AI template detection
3. API origin — programmatic vs browser behavior
4. Velocity — inhuman action speed
5. Structural similarity — templated descriptions
6. Off-hours — AI agents don't sleep
7. Threat detection — Lobster Trap security scanning
"""

import re
from datetime import datetime
from typing import Optional, Dict

# Optional Lobster Trap integration for threat detection
try:
    from utils.lobster_trap_client import LobsterTrapClient, classify_threat_level
    LOBSTER_TRAP_AVAILABLE = True
except ImportError:
    LOBSTER_TRAP_AVAILABLE = False
    LobsterTrapClient = None

# Global Lobster Trap client instance
_lobster_trap_client = None

def get_lobster_trap_client() -> Optional[LobsterTrapClient]:
    """Get or create Lobster Trap client"""
    global _lobster_trap_client
    if not LOBSTER_TRAP_AVAILABLE:
        return None
    
    if _lobster_trap_client is None:
        try:
            _lobster_trap_client = LobsterTrapClient()
        except:
            return None
    
    return _lobster_trap_client

def scan_for_threats(content: str) -> Optional[Dict]:
    """
    Scan content for threats using Lobster Trap
    
    Returns: Dict with threat info or None if Lobster Trap unavailable
    """
    if not LOBSTER_TRAP_AVAILABLE:
        return None
    
    client = get_lobster_trap_client()
    if not client:
        return None
    
    try:
        return client.inspect(content)
    except:
        return None

# ── Atlassian Intelligence Template Patterns ──────────────────────────────────
# Jira's "Improve Task" AI generates a very specific structure
ATLASSIAN_AI_PATTERNS = [
    r'\bSummary\b[\s\S]{0,200}\bContext\b',           # Summary → Context sections
    r'\bAcceptance [Cc]riteria\b',                     # Acceptance criteria section
    r'\bOther [Ii]nformation\b',                       # Other information section
    r'successfully (export|import|validate|configure|deploy|integrate)',
    r'(The task is related to|This issue involves|This ticket is)',
    r'(It is essential to ensure|ensure that the)',
]

# ── Explicit AI Labels ────────────────────────────────────────────────────────
EXPLICIT_AI_LABELS = [
    "[AI-GENERATED]",
    "[ATLASSIAN INTELLIGENCE]",
    "ai-generated",
    "auto-generated",
]

def is_ai_originated(action: dict, all_logs: list = None) -> dict:
    raw = action.get("raw", {})
    field = (raw.get("field") or "").lower()
    to_val = (raw.get("to") or "")
    from_val = (raw.get("from") or "")
    target = (action.get("target") or "")
    action_type = action.get("action", "")
    content_text = to_val + " " + target

    # ── Definitive signal 1 — explicit AI label in ticket name ────────────────
    for label in EXPLICIT_AI_LABELS:
        if label in target or label in to_val:
            return {
                "is_ai": True,
                "confidence": 100,
                "label": "🤖 AI-originated",
                "signals": [f"Explicit AI label detected: '{label}'"],
                "layers": {"content": 40, "atlassian_ai": 30, "api_origin": 20, "velocity": 10, "similarity": 0, "off_hours": 0},
                "source": "explicit_label"
            }

    # ── Definitive signal 2 — Atlassian Intelligence template ─────────────────
    atlassian_score = 0
    atlassian_signals = []

    for pattern in ATLASSIAN_AI_PATTERNS:
        if re.search(pattern, to_val, re.IGNORECASE | re.MULTILINE):
            atlassian_score += 25
            atlassian_signals.append(f"Atlassian Intelligence template pattern detected")
            break

    # Check for the exact Summary/Context/Acceptance criteria/Other information structure
    has_summary = bool(re.search(r'\bSummary\b', to_val, re.IGNORECASE))
    has_context = bool(re.search(r'\bContext\b', to_val, re.IGNORECASE))
    has_acceptance = bool(re.search(r'\bAcceptance [Cc]riteria\b', to_val, re.IGNORECASE))
    has_other_info = bool(re.search(r'\bOther [Ii]nformation\b', to_val, re.IGNORECASE))

    section_count = sum([has_summary, has_context, has_acceptance, has_other_info])
    if section_count >= 3:
        atlassian_score += 40
        atlassian_signals.append(
            f"Atlassian Intelligence 'Improve Task' structure detected "
            f"({section_count}/4 sections: Summary, Context, Acceptance Criteria, Other Information)"
        )
    elif section_count == 2:
        atlassian_score += 20
        atlassian_signals.append(f"Partial Atlassian Intelligence structure detected ({section_count}/4 sections)")

    # If strong Atlassian AI evidence — return immediately with high confidence
    if atlassian_score >= 40:
        return {
            "is_ai": True,
            "confidence": min(atlassian_score + 20, 100),
            "label": "🤖 Atlassian Intelligence",
            "signals": atlassian_signals,
            "layers": {"content": 20, "atlassian_ai": min(atlassian_score, 40), "api_origin": 20, "velocity": 0, "similarity": 0, "off_hours": 0},
            "source": "atlassian_intelligence"
        }

    # ── Standard multi-layer detection ───────────────────────────────────────
    signals = atlassian_signals.copy()
    score = atlassian_score
    layers = {"content": 0, "atlassian_ai": atlassian_score, "api_origin": 0, "velocity": 0, "similarity": 0, "off_hours": 0}

    # ── Layer 1: Content signals ───────────────────────────────────────────────
    content_score = 0

    AI_PHRASES = [
        r'(ensure|leverage|utilize|facilitate|streamline|configure|deploy|govern|audit)',
        r'(enterprise deployment|production environment|governance platform)',
        r'(setup and configure|design and implement|track, audit|monitor and govern)',
        r'(acceptance criteria|definition of done)',
        r'(as a user,? i want)',
        r'\*\*[A-Z][^*]+\*\*',
        r'^#{1,3}\s',
        r'^\s*[-•]\s.{30,}',
    ]
    for pattern in AI_PHRASES:
        if re.search(pattern, content_text, re.IGNORECASE | re.MULTILINE):
            content_score += 15
            signals.append("AI language/structure pattern detected")
            break

    AI_KEYWORDS = [
        "governance", "configure", "enterprise deployment", "audit trail",
        "track and govern", "operating in jira", "compliance framework",
        "observability", "policy enforcement", "agentic", "credential audit",
        "exporting payroll", "validation data"
    ]
    for kw in AI_KEYWORDS:
        if kw in content_text.lower():
            content_score += 20
            signals.append(f"AI domain keyword detected: '{kw}'")
            break

    # Perfect grammar — no informal language
    informal = r'\b(gonna|wanna|gotta|kinda|yeah|yep|nope|btw|fyi|ok\b)\b'
    if to_val and not re.search(informal, to_val, re.IGNORECASE):
        content_score += 10
        signals.append("No informal language — consistent with AI writing")

    layers["content"] = min(content_score, 40)
    score += layers["content"]

    # ── Layer 2: API origin signals ────────────────────────────────────────────
    api_score = 0

    if action_type == "CREATE":
        api_score += 20
        signals.append("Ticket created via API — not browser UI")

    if field == "description" and not from_val and to_val and len(to_val) > 50:
        api_score += 20
        signals.append("Full description set in single API operation")

    if field == "priority" and not from_val:
        api_score += 15
        signals.append("Priority auto-set on creation — programmatic behavior")

    layers["api_origin"] = min(api_score, 30)
    score += layers["api_origin"]

    # ── Layer 3: Velocity signals ──────────────────────────────────────────────
    if all_logs:
        try:
            current_ts = datetime.strptime(action["timestamp"], "%H:%M:%S")
            same_actor = [
                l for l in all_logs
                if l.get("agent") == action.get("agent") and l["id"] != action["id"]
            ]
            actions_in_window = sum(
                1 for l in same_actor
                if abs((current_ts - datetime.strptime(l["timestamp"], "%H:%M:%S")).total_seconds()) <= 30
            )
            if actions_in_window >= 3:
                layers["velocity"] = 25
                score += 25
                signals.append(f"{actions_in_window} actions within 30s — inhuman speed")
        except:
            pass

    # ── Layer 4: Structural similarity ────────────────────────────────────────
    if all_logs and to_val and len(to_val) > 30:
        similar_count = 0
        for l in all_logs:
            if l["id"] == action["id"]:
                continue
            other = l.get("raw", {}).get("to", "") or ""
            if len(other) > 30:
                s1 = len([s for s in to_val.split('.') if s.strip()])
                s2 = len([s for s in other.split('.') if s.strip()])
                if abs(s1 - s2) <= 1:
                    similar_count += 1
        if similar_count >= 1:
            layers["similarity"] = 15
            score += 15
            signals.append(f"Matches structural template of {similar_count} other action(s)")

    # ── Layer 5: Off-hours ─────────────────────────────────────────────────────
    try:
        ts = datetime.strptime(action["timestamp"], "%H:%M:%S")
        if ts.hour < 7 or ts.hour > 21:
            layers["off_hours"] = 10
            score += 10
            signals.append(f"Action at {action['timestamp']} — outside business hours")
    except:
        pass

    score = min(score, 100)
    is_ai = score >= 35

    # Determine label based on source
    if is_ai and atlassian_score > 0:
        label = "🤖 Atlassian Intelligence"
    elif is_ai:
        label = "🤖 AI-originated"
    else:
        label = "👤 Human"

    return {
        "is_ai": is_ai,
        "confidence": score,
        "label": label,
        "signals": list(dict.fromkeys(signals)),
        "layers": layers,
        "source": "atlassian_intelligence" if atlassian_score > 0 else "behavioral"
    }