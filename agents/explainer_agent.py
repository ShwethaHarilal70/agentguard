import os
try:
    import anthropic
    HAS_CLAUDE = True
except ImportError:
    HAS_CLAUDE = False


def explain_action(log: dict) -> str:
    """
    Given a single agent action log, produce a plain-language
    governance explanation using Claude Haiku.
    """
    if not HAS_CLAUDE:
        return "Claude API not available. Install: pip install anthropic"
    
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        return "Claude API key not configured. Set CLAUDE_API_KEY in .env"

    raw = log.get("raw", {})
    prompt = f"""You are an enterprise AI governance analyst reviewing an action taken inside Jira.

Action details:
- Actor: {log.get('agent', 'Unknown')}
- Action type: {log.get('action')}
- Target: {log.get('target')}
- Field changed: {raw.get('field', 'N/A')}
- From value: {raw.get('from', 'N/A')}
- To value: {raw.get('to', 'N/A')}
- Risk level: {log.get('risk_level')}
- Status decision: {log.get('status')}

Write 2-3 sentences explaining:
1. What happened and why it is {log.get('status')}
2. What the governance or security risk is
3. What a compliance officer should do next

Be direct and enterprise-grade. No bullet points. No preamble."""

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text.strip()
    except Exception as e:
        return f"Explanation unavailable: {str(e)}"


def explain_batch(logs: list) -> dict:
    """
    Explain all flagged/blocked logs in batch.
    Returns dict of log_id -> explanation.
    """
    explanations = {}
    critical = [l for l in logs if l["status"] in ("flagged", "blocked")]
    for log in critical:
        explanations[log["id"]] = explain_action(log)
    return explanations


def detect_intent_mismatch(log: dict) -> dict:
    """
    Lobster Trap feature: compare declared intent vs detected action.
    Returns mismatch analysis.
    """
    if not HAS_CLAUDE:
        return {"mismatch": False, "reason": "Claude API not available"}
    
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        return {"mismatch": False, "reason": "API key not configured"}

    prompt = f"""You are an AI security analyst checking for intent mismatches in agent behavior.

Observed action:
- Action type: {log.get('action')}
- Target: {log.get('target')}
- Field changed: {log.get('raw', {}).get('field', 'N/A')}
- From: {log.get('raw', {}).get('from', 'N/A')}
- To: {log.get('raw', {}).get('to', 'N/A')}

Respond ONLY with a JSON object like this (no markdown, no backticks):
{{
  "declared_intent": "what a legitimate agent would claim this action is for",
  "detected_intent": "what this action actually appears to be doing",
  "mismatch": true or false,
  "mismatch_reason": "why this is suspicious or normal",
  "risk_score": 1-10
}}"""

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        import json
        text = message.content[0].text.strip()
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        return {
            "declared_intent": "Unable to analyze",
            "detected_intent": "Unable to analyze",
            "mismatch": False,
            "mismatch_reason": str(e),
            "risk_score": 0
        }
