import streamlit as st
import os
from dotenv import load_dotenv
from agents.monitor_agent import fetch_jira_activity, get_jira_projects
from agents.explainer_agent import explain_action, detect_intent_mismatch
from agents.report_agent import generate_governance_report
from utils.policy_engine import get_triggered_rule, POLICY_RULES

load_dotenv()

st.set_page_config(
    page_title="AgentGuard — AI Governance Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.block-container { padding-top: 1.5rem; }
.connect-box {
    border: 1.5px dashed #dee2e6;
    border-radius: 12px;
    padding: 3rem 2rem;
    text-align: center;
    margin: 4rem auto;
    max-width: 560px;
}
.connect-title { font-size: 22px; font-weight: 600; color: #1a1a2e; margin-bottom: 8px; }
.connect-sub { font-size: 14px; color: #6c757d; line-height: 1.6; }
.env-block {
    background: #f1f3f5;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    font-family: monospace;
    font-size: 13px;
    color: #2d2d2d;
    text-align: left;
    margin-top: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Check Jira config ─────────────────────────────────────────────────────────
jira_configured = all([
    os.getenv("JIRA_URL"),
    os.getenv("JIRA_EMAIL"),
    os.getenv("JIRA_API_TOKEN")
])

# ── Not configured — show connect screen ─────────────────────────────────────
if not jira_configured:
    st.markdown("""
    <div class="connect-box">
        <div style="font-size:48px; margin-bottom:16px;">🛡️</div>
        <div class="connect-title">Connect AgentGuard to Your Jira</div>
        <div class="connect-sub">
            AgentGuard monitors AI agent activity across your enterprise systems.<br>
            To get started, add your Jira credentials to the <code>.env</code> file.
        </div>
        <div class="env-block">
            GEMINI_API_KEY=your_api_key<br>
            JIRA_URL=https://yourcompany.atlassian.net<br>
            JIRA_EMAIL=you@company.com<br>
            JIRA_API_TOKEN=your_jira_api_token
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### How to get your Jira API token")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Step 1**\n\nGo to [id.atlassian.com/manage-api-tokens](https://id.atlassian.com/manage-api-tokens)")
    with c2:
        st.markdown("**Step 2**\n\nClick **Create API token** and name it `agentguard`")
    with c3:
        st.markdown("**Step 3**\n\nPaste token into `.env` and restart the app")
    st.stop()

# ── Sidebar — only shown when configured ─────────────────────────────────────
with st.sidebar:
    st.markdown("### 🛡️ AgentGuard")
    st.markdown("*AI Agent Governance Platform*")
    st.divider()

    st.markdown("**Jira Connection**")
    jira_url = os.getenv("JIRA_URL", "")
    st.success(f"✅ Connected\n\n{jira_url}")

    st.divider()
    st.markdown("**Jira Project**")
    projects = get_jira_projects()
    project_key = None
    if projects:
        project_names = ["All Projects"] + [f"{p['key']} — {p['name']}" for p in projects]
        selected = st.selectbox("Project", project_names)
        if selected != "All Projects":
            project_key = selected.split(" — ")[0]
    else:
        project_key = st.text_input("Project key (e.g. KAN)", "")

    st.divider()
    page = st.radio("Navigate", [
        "🔍 Action Tracker",
        "📋 Governance Report",
        "🔎 Prompt Inspection",
        "⚙️ Policy Manager"
    ])
    st.divider()
    st.caption("AgentGuard v1.0")

# ── Load live Jira data ───────────────────────────────────────────────────────
@st.cache_data(ttl=60, show_spinner=False)
def load_logs(project_key):
    return fetch_jira_activity(project_key)

with st.spinner("Fetching Jira activity..."):
    logs = load_logs(project_key)

if not logs:
    st.warning("⚠️ No activity found for the selected project. Try selecting a different project or check your Jira permissions.")
    st.stop()

def get_session_stats(logs):
    total = len(logs)
    allowed = sum(1 for l in logs if l["status"] == "allowed")
    return {
        "total": total,
        "allowed": allowed,
        "flagged": sum(1 for l in logs if l["status"] == "flagged"),
        "blocked": sum(1 for l in logs if l["status"] == "blocked"),
        "compliance_score": round((allowed / total) * 100) if total else 0,
    }

stats = get_session_stats(logs)

# ── ACTION TRACKER ────────────────────────────────────────────────────────────
if page == "🔍 Action Tracker":
    st.title("🛡️ Action Tracker")
    st.caption("Real-time AI agent activity monitoring across enterprise systems")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Actions", stats["total"])
    c2.metric("✅ Allowed", stats["allowed"])
    c3.metric("⚠️ Flagged", stats["flagged"])
    c4.metric("🚫 Blocked", stats["blocked"])
    c5.metric("Compliance Score", f"{stats['compliance_score']}%")

    st.divider()

    f1, f2, f3 = st.columns(3)
    source_filter = f1.selectbox("Source", ["All", "Jira", "Confluence"])
    status_filter = f2.selectbox("Status", ["All", "allowed", "flagged", "blocked"])
    action_filter = f3.selectbox("Action", ["All", "READ", "CREATE", "EDIT", "DELETE", "ASSIGN", "COMMENT", "EXPORT"])

    filtered = logs
    if source_filter != "All":
        filtered = [l for l in filtered if l["source"] == source_filter]
    if status_filter != "All":
        filtered = [l for l in filtered if l["status"] == status_filter]
    if action_filter != "All":
        filtered = [l for l in filtered if l["action"] == action_filter]

    st.markdown(f"**{len(filtered)} actions** shown")
    st.divider()

    for log in filtered:
        s_emoji = {"allowed": "✅", "flagged": "⚠️", "blocked": "🚫"}[log["status"]]
        r_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}[log["risk_level"]]
        ai_h = log.get("ai_detection", {})
        ai_tag = " · 🤖 AI" if ai_h and ai_h.get("is_ai") else ""
        with st.expander(f"{s_emoji} `{log['timestamp']}` · **{log['source']}** · {log['action']} · {log['target'][:52]}{ai_tag}"):
            c1, c2, c3, c4 = st.columns(4)
            ai = log.get("ai_detection", {})
            ai_label = ai.get("label", "👤 Human") if ai else "👤 Human"
            ai_confidence = ai.get("confidence", 0) if ai else 0
            actor_display = f"{log['agent']}\n\n{ai_label}"
            if ai and ai.get("is_ai"):
                actor_display = f"{log['agent']}\n\n{ai_label} ({ai_confidence}% confidence)"
            c1.markdown(f"**Actor**\n\n{actor_display}")
            c2.markdown(f"**Action**\n\n`{log['action']}`")
            c3.markdown(f"**Risk**\n\n{r_emoji} {log['risk_level'].title()}")
            c4.markdown(f"**Status**\n\n{s_emoji} {log['status'].title()}")
            st.markdown(f"**Target:** {log['target']}")

            rule = get_triggered_rule(log)
            if rule:
                st.markdown(f"**Policy Rule:** `{rule['id']}`")
                st.info(f"📋 {rule['reason']}")

            # Show AI detection details
            ai = log.get("ai_detection", {})
            if ai and ai.get("is_ai"):
                with st.expander("🤖 AI-originated signals detected"):
                    st.markdown(f"**Confidence:** {ai.get('confidence', 0)}%")
                    for signal in ai.get("signals", []):
                        st.markdown(f"- {signal}")

            if log["status"] in ("flagged", "blocked"):
                if st.button("🔍 Analyze Action", key=f"explain_{log['id']}"):
                    with st.spinner("Analyzing..."):
                        result = explain_action(log)
                    st.success(result)

# ── GOVERNANCE REPORT ─────────────────────────────────────────────────────────
elif page == "📋 Governance Report":
    st.title("📋 Governance Report")
    st.caption("AI-generated compliance and audit report")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Actions", stats["total"])
    c2.metric("Flagged", stats["flagged"])
    c3.metric("Blocked", stats["blocked"])
    c4.metric("Compliance Score", f"{stats['compliance_score']}%")

    st.divider()
    st.markdown("### ⚠️ Flagged & Blocked Events")
    critical = [l for l in logs if l["status"] in ("flagged", "blocked")]
    if not critical:
        st.success("No flagged or blocked events in this session.")
    else:
        for log in critical:
            emoji = "⚠️" if log["status"] == "flagged" else "🚫"
            st.markdown(f"{emoji} **{log['source']}** · `{log['action']}` · {log['target']}")
            rule = get_triggered_rule(log)
            if rule:
                st.caption(f"Rule `{rule['id']}` — {rule['reason']}")

    st.divider()
    if st.button("📄 Generate Full Governance Report", type="primary", use_container_width=True):
        with st.spinner("Generating enterprise governance report..."):
            report = generate_governance_report(logs, stats)
        st.markdown("### Report")
        st.markdown(report)
        st.download_button(
            "⬇️ Download Report",
            data=report,
            file_name="agentguard_governance_report.txt",
            mime="text/plain"
        )

# ── PROMPT INSPECTION ─────────────────────────────────────────────────────────
elif page == "🔎 Prompt Inspection":
    st.title("🔎 Prompt Inspection")
    st.caption("Detect anomalous agent behavior — actions that exceed scope, exfiltrate data, or show intent mismatch")

    # Only show genuinely suspicious actions — blocked or high-risk edits/deletes
    # Simple policy flags like ASSIGN are NOT prompt injection candidates
    SUSPICIOUS_ACTIONS = ["DELETE", "EDIT"]
    SUSPICIOUS_RISK = ["high"]

    suspicious_logs = [
        l for l in logs
        if l["status"] == "blocked"
        or (l["status"] == "flagged" and l["risk_level"] == "high")
        or (l["action"] in SUSPICIOUS_ACTIONS and l["risk_level"] in ["medium", "high"])
    ]

    # Deduplicate by target
    seen = set()
    unique_suspicious = []
    for l in suspicious_logs:
        key = f"{l['action']}_{l['target'][:40]}"
        if key not in seen:
            seen.add(key)
            unique_suspicious.append(l)

    if not unique_suspicious:
        st.info("No anomalous actions detected. Prompt inspection monitors for scope violations, data exfiltration attempts, and adversarial behavior — not routine policy flags like assignments.")
        st.markdown("#### What triggers Prompt Inspection?")
        c1, c2, c3 = st.columns(3)
        c1.markdown("**🚫 Blocked actions**\n\nHigh-risk actions the policy engine stopped")
        c2.markdown("**🔐 Scope violations**\n\nAgent accessing systems outside its task context")
        c3.markdown("**📤 Exfiltration risk**\n\nSensitive data reads or unexpected exports")
    else:
        st.markdown(f"**{len(unique_suspicious)} actions** flagged for intent analysis")
        st.caption("These actions show behavior inconsistent with expected agent scope — review for prompt injection or adversarial manipulation.")
        st.divider()

        for log in unique_suspicious:
            s_emoji = "🚫" if log["status"] == "blocked" else "⚠️"
            with st.expander(f"{s_emoji} {log['action']} · {log['target'][:70]}"):
                st.markdown(f"**Status:** {log['status'].title()} · **Risk:** {log['risk_level'].title()}")
                st.markdown(f"**Actor:** {log['agent']}")
                st.markdown(f"**Target:** {log['target']}")

                if st.button("🔎 Run Intent Analysis", key=f"trap_{log['id']}"):
                    with st.spinner("Analyzing declared vs detected intent..."):
                        result = detect_intent_mismatch(log)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**📢 Declared Intent**")
                        st.info(result.get("declared_intent", "N/A"))
                    with col2:
                        st.markdown("**🔍 Detected Intent**")
                        if result.get("mismatch"):
                            st.error(result.get("detected_intent", "N/A"))
                        else:
                            st.success(result.get("detected_intent", "N/A"))

                    risk_score = result.get("risk_score", 0)
                    st.markdown(f"**Risk Score: {risk_score}/10**")
                    st.progress(risk_score / 10)

                    if result.get("mismatch"):
                        st.error(f"🚨 INTENT MISMATCH DETECTED: {result.get('mismatch_reason', '')}")
                    else:
                        st.success(f"✅ Intent aligned: {result.get('mismatch_reason', '')}")

# ── POLICY MANAGER ────────────────────────────────────────────────────────────
elif page == "⚙️ Policy Manager":
    st.title("⚙️ Policy Manager")
    st.caption("Access control rules governing AI agent permissions")

    st.markdown(f"**{len(POLICY_RULES)} active rules**")
    st.divider()

    for rule in POLICY_RULES:
        r_emoji = {"low": "🟢", "medium": "🟡", "high": "🔴"}[rule["risk"]]
        with st.expander(f"{r_emoji} `{rule['id']}` — {rule['source']} · {rule['action']}"):
            st.markdown(f"**Source:** {rule['source']}")
            st.markdown(f"**Action:** `{rule['action']}`")
            st.markdown(f"**Risk Level:** {rule['risk'].title()}")
            if "keyword" in rule:
                st.markdown(f"**Keyword Trigger:** `{rule['keyword']}`")
            st.info(f"📋 {rule['reason']}")

    st.divider()
    st.markdown("### ➕ Add Custom Rule")
    with st.form("new_rule"):
        c1, c2 = st.columns(2)
        new_source = c1.selectbox("Source", ["Jira", "Confluence"])
        new_action = c2.selectbox("Action", ["READ", "CREATE", "EDIT", "DELETE", "ASSIGN", "EXPORT"])
        new_keyword = st.text_input("Keyword trigger (optional)")
        new_risk = st.selectbox("Risk level", ["low", "medium", "high"])
        new_reason = st.text_area("Policy reason")
        if st.form_submit_button("Add Rule") and new_reason:
            st.success(f"✅ Rule added: {new_source} · {new_action} · {new_risk.title()} risk")
