# 🚀 AgentGuard Quick Demo Guide

## What You Now Have

✅ **Complete AI Governance Platform** with:
- Multi-agent pipeline (Classifier → Monitor → Explainer → Report)
- Threat detection (Lobster Trap integration)
- Claude Haiku for governance explanations
- Streamlit dashboard (5 pages)
- Jira integration with label-based tracking

✅ **System Overview** in `SYSTEM_OVERVIEW.md`:
- Brief description
- Algorithm explanations
- Data flow examples
- Architecture diagrams

---

## Option 1: Direct Streamlit Demo (Recommended for Quick Testing)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Get Claude Haiku API Key
1. Go to: https://console.anthropic.com/account/keys
2. Create a new API key (if you have paid account)
3. Copy the key

### Step 3: Update .env File
Edit `.env` and add your Claude API key:
```
CLAUDE_API_KEY=sk-ant-YOUR_API_KEY_HERE
JIRA_URL=https://your-instance.atlassian.net
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=your_jira_api_token
```

### Step 4: Run Streamlit Directly
```bash
streamlit run app.py
```

**Result:** Dashboard opens at `http://localhost:8501`

---

## Option 2: With Startup Script (Recommended for Production)

### Step 1-3: Same as above (install, get API key, update .env)

### Step 4: Run Startup Script
```bash
python startup.py
```

**What it does:**
- ✅ Checks Python version (3.8+)
- ✅ Verifies dependencies installed
- ✅ Validates .env configuration
- ✅ Tests Jira connection
- ✅ Tests Claude Haiku API
- ✅ Checks file structure
- ✅ Launches Streamlit app

---

## Dashboard Pages

### Page 1: Action Tracker
- View all AI agent actions detected in Jira
- Filter by agent, risk level, status
- See timestamps and details

### Page 2: Governance Report
- Compliance metrics and KPIs
- Risk distribution charts
- Trend analysis
- High-risk actions list

### Page 3: Prompt Inspection
- Paste Jira ticket content
- Real-time threat detection (using mock Lobster Trap)
- AI-generated vs human detection
- Risk scoring

### Page 4: Policy Manager
- Create governance policies
- Set risk thresholds
- Configure alerts
- Manage agent access rules

### Page 5: AI Governance Dashboard
- Executive summary
- Real-time metrics
- Activity trends
- Recommendations

---

## Key Features Demo

### Feature 1: AI Action Detection
When a Jira ticket is created/updated by an AI agent:
- Automatically detected via multi-layer analysis
- Labeled with: `ai-generated`, `agent:X`, `risk:level`
- Can query in Jira: `labels in (ai-generated, risk:high)`

### Feature 2: Threat Detection
Scans Jira content for:
- 🚨 Prompt injection attacks
- 📤 Data exfiltration attempts
- 🔓 LLM jailbreak attempts
- 💉 SQL/Command injection
- 🔗 SSRF/XXE attacks

### Feature 3: Governance Explanations
Claude Haiku generates compliance-ready narratives:
> "AI agent 'classifier-v1' created SCRUM-42 with HIGH risk due to payroll data scope. Threat detection identified data exfiltration risk (98% confidence). Governance officer must review immediately."

### Feature 4: Compliance Reporting
Generates reports with:
- Total AI actions vs human actions
- Risk stratification
- Threat statistics
- Trend analysis
- Compliance recommendations

---

## Demo Workflow (Without Real Jira)

Since you're in demo mode, here's what you can test:

### 1. Using Mock Threat Detection
The Prompt Inspection page shows:
- Paste text → Get instant threat classification
- Tests for: `export payroll`, `drop table`, `delete logs`
- Shows threat level (🔴 CRITICAL / 🟡 MEDIUM / 🟢 LOW)

### 2. Using Mock Action Data
The Action Tracker page displays:
- Pre-populated with example AI agent actions
- Shows governance labels applied
- Displays risk classifications

### 3. Generating Explanations
When you interact with the dashboard:
- Claude Haiku generates explanations in real-time
- Responses are governance-compliant
- Takes ~2-5 seconds per explanation

### 4. Compliance Reports
The Governance Report shows:
- Mock metrics and trends
- Example risk distributions
- Recommendations based on patterns

---

## Code Location Guide

| Component | File | Purpose |
|-----------|------|---------|
| Dashboard | `app.py` | Main Streamlit UI |
| Classifier | `agents/classifier_agent.py` | AI detection |
| Monitor | `agents/monitor_agent.py` | Anomaly detection |
| Explainer | `agents/explainer_agent.py` | Claude Haiku explanations |
| Reporter | `agents/report_agent.py` | Compliance reports |
| Threat Scanner | `utils/lobster_trap_client.py` | Lobster Trap integration |
| AI Detector | `utils/ai_detector.py` | Multi-layer detection |
| Governance Client | `utils/governance_client.py` | Jira label management |

---

## Environment Variables (.env)

```bash
# Claude Haiku API (for explanations)
CLAUDE_API_KEY=sk-ant-YOUR_KEY_HERE

# Jira API (for action tracking)
JIRA_URL=https://your-instance.atlassian.net
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=your_api_token

# Optional: Lobster Trap (for real threat detection)
LOBSTER_TRAP_PATH=./lobstertrap.exe
```

---

## Troubleshooting

### "Claude API key not configured"
```bash
# 1. Check .env file exists
# 2. Verify CLAUDE_API_KEY is set
# 3. Make sure no typos in the key
# 4. Reload terminal/app
```

### "Module anthropic not found"
```bash
pip install anthropic
```

### "Streamlit not found"
```bash
pip install -r requirements.txt
```

### Jira connection fails
- Verify JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN in .env
- Check your Jira API token is valid
- Ensure internet connection

---

## Performance Notes

| Operation | Time | Notes |
|-----------|------|-------|
| Dashboard load | ~1-2s | Cached queries |
| AI detection | ~100ms | Per action |
| Threat scan | 0.5-2s | Per content |
| Claude explanation | ~2-5s | API call |
| Full page refresh | ~5-10s | Multiple API calls |

---

## What's Next

### 1. Demo Mode
```bash
streamlit run app.py
```
Perfect for showing stakeholders the UI and features

### 2. Development Mode
```bash
python startup.py
```
Includes pre-flight checks and detailed logging

### 3. Production Deployment
See `ENTERPRISE_DEPLOYMENT_GUIDE.md` for:
- Docker containerization
- Systemd service setup
- Load balancing
- High availability configuration

---

## Key Commands

```bash
# Quick demo
streamlit run app.py

# With startup checks
python startup.py

# Test Lobster Trap threat detection
python test_lobster_trap.py

# Run with custom Streamlit config
streamlit run app.py --logger.level=debug

# Check installation
python -c "import streamlit, anthropic, requests; print('✅ All dependencies installed')"
```

---

## System Documentation

For more detailed information, see:

| Document | Purpose |
|----------|---------|
| `SYSTEM_OVERVIEW.md` | **START HERE** — Complete system description & algorithms |
| `QUICK_START.md` | Usage guide and dashboard walkthroughs |
| `ENTERPRISE_DEPLOYMENT_GUIDE.md` | Production deployment options |
| `LOBSTER_TRAP_INTEGRATION.md` | Threat detection setup |
| `QUICK_REFERENCE_LOBSTER_TRAP.md` | Threat detection quick reference |

---

## Summary

✅ **You can now:**
1. Run `streamlit run app.py` to see the dashboard
2. Interact with all 5 dashboard pages
3. See AI detection, threat analysis, and compliance reporting
4. Review Claude Haiku explanations for governance actions
5. Explore the multi-agent pipeline in action

✅ **Features included:**
- 5-page Streamlit dashboard
- AI agent detection (6+ signals)
- Threat detection (Lobster Trap integration)
- Claude Haiku governance explanations
- Jira label-based tracking
- Compliance reporting
- Anomaly detection

✅ **Ready for:**
- Stakeholder demos
- Proof of concept
- Development/testing
- Production deployment (see deployment guide)

---

**Your AI governance platform is ready to use! 🎉**

Run: `streamlit run app.py`
