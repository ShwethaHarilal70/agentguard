import os
try:
    import anthropic
    HAS_CLAUDE = True
except ImportError:
    HAS_CLAUDE = False

def generate_governance_report(logs: list, stats: dict) -> str:
    if not HAS_CLAUDE:
        return "Claude API not available. Install: pip install anthropic"
    
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        return "Claude API key not configured. Set CLAUDE_API_KEY in .env"

    flagged = [l for l in logs if l["status"] in ("flagged", "blocked")]
    flagged_summary = "\n".join([
        f"- [{l['status'].upper()}] {l['source']} | {l['action']} | {l['target']}"
        for l in flagged
    ])

    prompt = f"""You are an enterprise AI governance officer generating a formal compliance report.

Session statistics:
- Total agent actions: {stats['total']}
- Allowed: {stats['allowed']}
- Flagged: {stats['flagged']}
- Blocked: {stats['blocked']}
- Compliance score: {stats['compliance_score']}%

Flagged and blocked events:
{flagged_summary}

Write a formal governance report with these sections:
1. Executive Summary (3 sentences)
2. Key Risk Findings (explain each flagged/blocked event)
3. Governance Principles Violated (map to: Accountability, Transparency, Fairness, Compliance)
4. Recommended Policy Changes (3-4 specific actionable items)
5. Compliance Officer Action Items (immediate next steps)

Use formal enterprise language. Be specific and actionable."""

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text.strip()
    except Exception as e:
        return f"Report generation failed: {str(e)}"
