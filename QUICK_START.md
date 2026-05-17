# 🚀 AgentGuard Enterprise — Quick Start Guide

## ✅ Status: Application Running!

Your AgentGuard platform is now **LIVE** at: **http://localhost:8501**

---

## Step-by-Step Usage

### Step 1: Connect to Jira (First Time Only)
1. When app starts, it checks your `.env` file
2. If configured correctly, you'll see the main dashboard
3. ✅ Jira connection verified: `https://shwethaharilal70.atlassian.net`
4. ✅ Account: `Shwetha Harilal`
5. ✅ Project: `SCRUM`

### Step 2: Select Your Project
- In the **left sidebar**, under "Jira Project"
- Select from: "All Projects" or specific project (e.g., SCRUM)
- The app will load activities for your selected project

### Step 3: Navigate the Dashboard
The left sidebar shows 5 main sections:

```
🔍 Action Tracker          — Real-time AI agent activity
📋 Governance Report       — Compliance & audit report
🔎 Prompt Inspection       — Anomaly detection
⚙️ Policy Manager          — Policy rules
🛡️ AI Governance (NEW)     — Comprehensive governance dashboard
```

---

## Dashboard Features

### 🔍 Action Tracker
**Purpose:** Monitor all AI agent actions in real-time

**What you see:**
- Total actions, allowed, flagged, blocked
- Compliance score (%)
- List of all activities with filters

**Filters available:**
```
Source:  Jira, Confluence, or All
Status:  Allowed, Flagged, Blocked, or All
Action:  READ, CREATE, EDIT, DELETE, ASSIGN, EXPORT
```

**Each action shows:**
- ✅/⚠️/🚫 Status
- 🟢/🟡/🔴 Risk level
- Actor (AI agent or Human)
- Target (Jira issue or document)
- Policy rule triggered (if any)
- 🤖 AI signals (if detected)

**Click "Analyze Action" to:**
- Get AI-generated explanation of risky actions
- See why it was flagged/blocked
- Understand potential threats

### 📋 Governance Report
**Purpose:** Generate compliance & audit reports

**Metrics shown:**
- Total actions summary
- Flagged & blocked events
- Policy violations
- Risk breakdown

**Generate full report:**
- Click "Generate Full Governance Report"
- Download as text file for compliance
- Share with auditors

### 🔎 Prompt Inspection
**Purpose:** Detect anomalous AI behavior

**Detects:**
- 🔐 Scope violations (agent accessing outside task)
- 📤 Data exfiltration (sensitive data reads/exports)
- 🚨 Intent mismatches (suspicious behavior patterns)
- 🤖 Adversarial manipulation (prompt injection attempts)

**For each flagged action:**
- Click "Run Intent Analysis"
- See declared vs detected intent
- Get risk score (0-10)
- Get recommendation (approve/block)

### ⚙️ Policy Manager
**Purpose:** Manage access control rules

**View existing rules:**
- Source: Jira or Confluence
- Action type: READ, CREATE, EDIT, DELETE, etc.
- Risk level: Low (🟢), Medium (🟡), High (🔴)
- Trigger keyword (optional)
- Policy reason

**Add new rule:**
- Fill in source, action, risk level
- Optional: add keyword trigger
- Enter policy reason
- Click "Add Rule"

### 🛡️ AI Governance Dashboard (NEW)
**Purpose:** Enterprise-grade AI agent tracking

**Sections:**

**1. Agent Activity Tracking**
- Lists each AI agent (e.g., classifier-v1, monitor-v2.1)
- Total actions per agent
- Risk distribution (High/Medium/Low)
- Last activity timestamp

**2. Security Alerts**
- Shows all high-risk AI actions
- Alerts when anomalies detected
- Recommended actions

**3. Compliance Metrics**
- AI vs Human action breakdown
- Risk distribution chart
- Governance review status

---

## Step-by-Step Walkthrough

### Scenario: Review Today's Activity

1. **Open app**
   ```bash
   http://localhost:8501
   ```

2. **Select project** (left sidebar)
   - Choose "SCRUM" project

3. **Go to Action Tracker**
   - See metrics at top
   - Review all actions listed

4. **Filter for AI actions**
   - Scroll through and note ones labeled "🤖 AI Agent"
   - These have `ai-generated` label

5. **Check high-risk actions**
   - Look for 🔴 (high risk)
   - Click expander to see details
   - Click "Analyze Action" for AI explanation

6. **Review policy hits**
   - See which policy rules were triggered
   - Understand why action was flagged/blocked

### Scenario: Generate Compliance Report

1. **Go to Governance Report** (left sidebar)
   - See summary metrics

2. **Review flagged events**
   - All problematic actions listed
   - Policy triggers shown

3. **Generate full report**
   - Click "Generate Full Governance Report"
   - Wait for AI to analyze
   - Review detailed report

4. **Download report**
   - Click "Download Report"
   - Share with compliance team

### Scenario: Detect Anomalies

1. **Go to Prompt Inspection**
   - See flagged anomalous actions

2. **Click "Run Intent Analysis"**
   - See what agent declared intent was
   - See what was actually detected
   - Get risk score

3. **Review risk score**
   - 0-3: Low (likely benign)
   - 4-6: Medium (needs review)
   - 7-10: High (likely adversarial)

4. **Check mismatch reason**
   - If intent mismatched, understand why
   - Decide to approve or block similar actions

### Scenario: Add Policy Rule

1. **Go to Policy Manager** (left sidebar)
   - See all existing rules

2. **Scroll to "Add Custom Rule"**
   - Source: Select Jira or Confluence
   - Action: Select action type
   - Risk Level: Low, Medium, or High
   - Keyword: Optional (leave blank if N/A)
   - Reason: Explain the policy

3. **Click "Add Rule"**
   - Confirmation message shown
   - Rule now active

---

## Key Metrics Explained

### Compliance Score
```
Formula: (Allowed Actions / Total Actions) × 100

High (>90%): Mostly compliant, few violations
Good (70-90%): Some violations, investigate
Poor (<70%): Many violations, needs review
```

### Risk Levels
```
🟢 LOW: Safe actions (reads, comments)
🟡 MEDIUM: Moderate risk (creates, assignments)
🔴 HIGH: High risk (deletes, exports, bulk operations)
```

### Action Status
```
✅ ALLOWED: Complies with policy, no risk
⚠️ FLAGGED: Violation detected, needs review
🚫 BLOCKED: Violates policy, prevented
```

### AI Indicators
```
🤖 AI: Performed by AI agent
👤 Human: Performed by human user
🤖 AI (X% confidence): AI with confidence level
```

---

## Troubleshooting

### Issue: "No activities found"
**Solution:**
1. Check project selection in sidebar
2. Make sure you selected a valid project
3. Try "All Projects"
4. Verify Jira permissions

### Issue: "Action Analyzer not available"
**Solution:**
- Gemini API key might be invalid
- Check `.env` file
- Regenerate API key at https://ai.google.dev

### Issue: App is slow/freezing
**Solution:**
1. Click different project (smaller dataset)
2. Use Status/Action filters to reduce results
3. Refresh browser (F5)
4. Restart app: `streamlit run app.py`

### Issue: "Policy Rule not appearing"
**Solution:**
1. Refresh page (F5)
2. New rules appear in list immediately
3. Check if keyword matches (case-sensitive)

### Issue: Port 8501 already in use
**Solution:**
```bash
# Use different port
streamlit run app.py --server.port=8502
```

---

## Running in the Background (Production)

### Option 1: Systemd (Linux/Mac)
```bash
sudo nano /etc/systemd/system/agentguard.service
```

```ini
[Unit]
Description=AgentGuard
After=network.target

[Service]
Type=simple
User=your-user
ExecStart=/usr/bin/python3 -m streamlit run /path/to/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start agentguard
sudo systemctl status agentguard
```

### Option 2: Docker (Any OS)
```bash
docker build -t agentguard .
docker run -d -p 8501:8501 --env-file .env agentguard
```

### Option 3: Streamlit Cloud (Easiest)
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your repo
4. Add `.env` values in "Secrets"
5. Deploy (auto-updates on push)

---

## Enterprise Checklist

- ✅ Application running: http://localhost:8501
- ✅ Jira connected: SCRUM project
- ✅ Gemini API available (with minor model issue)
- ✅ All agents loaded
- ✅ Policy engine active
- ✅ Governance client ready
- ✅ Streamlit dashboard responsive

### Before Production:
- [ ] Test with real Jira data
- [ ] Verify all agents are classifying correctly
- [ ] Approve/add custom policies
- [ ] Set up monitoring/alerts
- [ ] Schedule regular compliance reports
- [ ] Train team on dashboard features
- [ ] Set up backup/archival process
- [ ] Enable audit logging

---

## Quick Commands

```bash
# Start app (from project root)
python startup.py

# Or directly with Streamlit
streamlit run app.py

# Run with custom port
streamlit run app.py --server.port=8502

# Run in background (Linux/Mac)
nohup streamlit run app.py > agentguard.log 2>&1 &

# Stop app
Ctrl+C (in terminal)

# View logs
tail -f agentguard.log
```

---

## Next Steps

1. **Explore the Dashboard**
   - Spend 10 min on each section
   - Get familiar with UI

2. **Review Current Activity**
   - Check what agents are doing
   - Identify any flagged actions

3. **Customize Policies**
   - Add rules specific to your organization
   - Adjust risk levels

4. **Set Up Alerts**
   - Email notifications for high-risk actions
   - Slack integration (can be added)

5. **Generate Reports**
   - Create first compliance report
   - Share with leadership
   - Schedule weekly/monthly runs

6. **Deploy to Production**
   - Use Docker or Systemd
   - Set up monitoring
   - Enable backup process

---

## Support Resources

- **Documentation:** See `ENTERPRISE_DEPLOYMENT_GUIDE.md`
- **Code:** Check individual agent files
- **Issues:** Report on GitHub
- **API Docs:** https://developer.atlassian.com/

---

**🎉 AgentGuard is now live and ready for enterprise use!**

Your AI agent governance platform is monitoring Jira in real-time. Start reviewing activities and enforcing governance policies now!

For questions, refer to ENTERPRISE_DEPLOYMENT_GUIDE.md
