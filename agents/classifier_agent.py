import os
try:
    import anthropic
    HAS_CLAUDE = True
except ImportError:
    HAS_CLAUDE = False

def classify_and_explain(log: dict) -> str:
    if not HAS_CLAUDE:
        return "Claude API not available. Install: pip install anthropic"
    
    api_key = os.getenv("CLAUDE_API_KEY")
    if not api_key:
        return "Claude API key not configured. Set CLAUDE_API_KEY in .env"

    prompt = f"""You are an enterprise AI governance analyst.

An AI agent performed the following action:
- Source system: {log['source']}
- Agent: {log['agent']}
- Action type: {log['action']}
- Target: {log['target']}
- Risk level: {log['risk_level']}
- Status: {log['status']}

In 2-3 sentences explain:
1. Why this action is {log['status']}
2. What the specific governance or security risk is
3. What a compliance officer should do next

Be direct, enterprise-grade, and specific. No bullet points."""

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text.strip()
    except Exception as e:
        return f"Unable to generate explanation: {str(e)}"
