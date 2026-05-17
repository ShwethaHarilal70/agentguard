# 🛡️ AgentGuard — Enterprise Deployment Guide

## Quick Start (5 Steps)

### Step 1: Verify Configuration
```bash
cd c:\Users\haril\agentguard
# Check .env file has all credentials
cat .env
```

Required variables:
```
GEMINI_API_KEY=<your_api_key>
JIRA_URL=https://yourcompany.atlassian.net
JIRA_EMAIL=your@email.com
JIRA_API_TOKEN=<your_token>
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Key packages:**
- streamlit — Web UI
- requests — Jira API
- python-dotenv — Configuration
- google-generativeai — Gemini API

### Step 3: Run the Application
```bash
streamlit run app.py
```

The app will start at: `http://localhost:8501`

### Step 4: Configure Jira Connection
1. The app will show a connection screen if credentials are missing
2. Add your Jira URL, email, and API token to `.env`
3. Restart the app with `streamlit run app.py`

### Step 5: Start Monitoring
1. Select your Jira project from the sidebar
2. Navigate to **🛡️ Action Tracker** to see AI agent activity
3. View **📋 Governance Report** for compliance metrics
4. Use **🔎 Prompt Inspection** to detect anomalies

---

## Enterprise Architecture

```
┌─────────────────────────────────────────────────────────┐
│         Streamlit Web Interface (app.py)                │
│    - Action Tracker      - Governance Dashboard         │
│    - Policy Manager      - Compliance Reports           │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────v──────────────────────────────────────┐
│         Multi-Agent Pipeline                            │
├──────────────────────────────────────────────────────────┤
│  • Classifier Agent  — Risk classification             │
│  • Monitor Agent     — Activity tracking               │
│  • Explainer Agent   — Intent analysis                 │
│  • Report Agent      — Compliance reporting            │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────v──────────────────────────────────────┐
│         Governance & Policy Engine                      │
├──────────────────────────────────────────────────────────┤
│  • Policy Engine     — Rule-based enforcement           │
│  • AI Detector       — ML-based anomaly detection       │
│  • Governance Client — Jira integration & tracking      │
└──────────────────┬──────────────────────────────────────┘
                   │
┌──────────────────v──────────────────────────────────────┐
│         Enterprise Systems                              │
├──────────────────────────────────────────────────────────┤
│  • Jira  — Primary tracking & ticket management         │
│  • Confluence — Document & access tracking              │
│  • External APIs — Additional integrations              │
└──────────────────────────────────────────────────────────┘
```

---

## File Structure (Enterprise)

```
agentguard/
├── app.py                           # Main Streamlit application
├── requirements.txt                 # Python dependencies
├── .env                             # Configuration (credentials)
├── README.md                        # Project documentation
│
├── agents/                          # Multi-agent pipeline
│   ├── __init__.py
│   ├── classifier_agent.py          # Risk classification
│   ├── monitor_agent.py             # Activity monitoring
│   ├── explainer_agent.py           # Intent analysis
│   └── report_agent.py              # Report generation
│
├── utils/                           # Core utilities
│   ├── __init__.py
│   ├── policy_engine.py             # Policy rules & enforcement
│   ├── ai_detector.py               # AI detection algorithms
│   └── governance_client.py         # Jira governance integration (NEW)
│
├── data/                            # Mock & reference data
│   ├── __init__.py
│   └── mock_logs.py                 # Test data
│
└── pages/                           # Multi-page Streamlit (optional)
    └── (future: advanced dashboards)
```

---

## Configuration Guide

### .env File

```bash
# Google Gemini API (for AI analysis)
GEMINI_API_KEY=AIzaSy...

# Jira Configuration
JIRA_URL=https://yourcompany.atlassian.net
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=ATATT3xFfGF0AC...

# Optional: Feature flags
DEBUG_MODE=false
LOG_LEVEL=INFO
```

### Getting Credentials

**Gemini API Key:**
1. Go to https://ai.google.dev/
2. Click "Get API Key"
3. Create a new project
4. Copy the API key

**Jira API Token:**
1. Go to https://id.atlassian.com/manage-api-tokens
2. Click "Create API token"
3. Name it "agentguard"
4. Copy the token

**Jira URL & Email:**
- URL: `https://yourcompany.atlassian.net`
- Email: Your Atlassian account email

---

## Running the Application

### Local Development
```bash
streamlit run app.py
```

Open: http://localhost:8501

### Production Deployment

**Option A: On-Premise (Recommended)**
```bash
# Create systemd service
sudo nano /etc/systemd/system/agentguard.service
```

```ini
[Unit]
Description=AgentGuard AI Governance Platform
After=network.target

[Service]
Type=simple
User=agentguard
WorkingDirectory=/opt/agentguard
ExecStart=/usr/bin/python3 -m streamlit run app.py --server.port=8501
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start agentguard
sudo systemctl enable agentguard
```

**Option B: Docker (Cloud-Ready)**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t agentguard:latest .
docker run -p 8501:8501 --env-file .env agentguard:latest
```

**Option C: Streamlit Cloud**
1. Push to GitHub
2. Go to https://share.streamlit.io
3. Connect your repo
4. Add env variables in Secrets
5. Deploy

---

## Dashboard Sections

### 1. 🔍 Action Tracker
**Purpose:** Real-time monitoring of all AI agent actions

**Features:**
- View all Jira/Confluence activities
- Filter by source, status, action type
- See AI vs human actions (labeled)
- View policy triggers
- Risk assessment (Low/Medium/High)

**Metrics:**
- Total Actions
- Allowed/Flagged/Blocked counts
- Compliance Score (%)

**Filters:**
```
Source:  All | Jira | Confluence
Status:  All | Allowed | Flagged | Blocked
Action:  All | READ | CREATE | EDIT | DELETE | ASSIGN | EXPORT
```

### 2. 📋 Governance Report
**Purpose:** Compliance and audit reporting

**Features:**
- Summary of all flagged/blocked events
- Policy rule triggers
- Generate full governance report
- Download as text file

**Report Includes:**
- Activity summary
- Risk analysis
- Policy violations
- Recommendations

### 3. 🔎 Prompt Inspection
**Purpose:** Detect anomalous AI behavior

**Features:**
- Scope violations detection
- Data exfiltration warnings
- Intent mismatch analysis
- Adversarial behavior detection

**AI Analysis:**
- Declared vs detected intent
- Risk score (0-10)
- Signal strength indicators

### 4. ⚙️ Policy Manager
**Purpose:** Access control rule management

**Features:**
- View all active policies
- Add custom rules
- Risk level classification
- Keyword triggers

**Rule Template:**
```
Source: Jira/Confluence
Action: READ/CREATE/EDIT/DELETE/ASSIGN/EXPORT
Risk Level: Low/Medium/High
Trigger: Optional keyword
Reason: Policy description
```

### 5. 🛡️ AI Governance (NEW)
**Purpose:** Comprehensive AI governance dashboard

**Sections:**
- Agent Activity Tracking
- High-Risk Actions Alert
- Governance Metrics
- Compliance Status

---

## API Integration

### Using the Governance Client

```python
from utils.governance_client import JiraGovernanceClient

# Initialize
gov = JiraGovernanceClient()

# Create tracked issue
ticket_key = gov.create_ai_tracked_issue(
    summary="Update Jira permissions",
    description="Review and update agent access",
    agent_name="monitor-v2.1",
    risk_level="High"
)

# Get metrics
metrics = gov.get_governance_metrics()
print(f"AI Actions: {metrics['total_ai_actions']}")
print(f"High-Risk: {metrics['high_risk_actions']}")
print(f"Pending Review: {metrics['pending_review']}")
```

### Example: Classifier Agent Integration

```python
from utils.governance_client import JiraGovernanceClient

class ClassifierAgent:
    def __init__(self):
        self.gov = JiraGovernanceClient()
    
    def classify_action(self, action):
        risk = self._assess_risk(action)
        
        if risk == "High":
            # Create tracked issue
            self.gov.create_ai_tracked_issue(
                summary=f"{action['type']} on {action['target']}",
                description=f"Risk assessment: {risk}",
                agent_name="classifier-v1",
                risk_level=risk
            )
```

---

## Monitoring & Maintenance

### Health Check
```bash
# Check if app is running
curl http://localhost:8501/_stcore/health

# View logs
journalctl -u agentguard -f  # systemd
docker logs -f agentguard     # docker
```

### Backup
```bash
# Backup configuration
tar -czf agentguard_backup_$(date +%Y%m%d).tar.gz .env

# Backup data (from Jira)
python -c "from utils.governance_client import JiraGovernanceClient; gov = JiraGovernanceClient(); issues = gov.get_ai_generated_issues(1000)"
```

### Performance Optimization
1. **Cache Jira queries:** Already implemented (60s TTL)
2. **Use projects filter:** Select specific projects to reduce data
3. **Archive old tickets:** Move old tickets to archive project
4. **Batch API calls:** Use background jobs for large data pulls

---

## Troubleshooting

### Issue: "Unbounded JQL queries are not allowed"
**Solution:** Add project filter to JQL query
```python
'jql': 'project = SCRUM AND labels in (ai-generated)'
```

### Issue: "API request failed 400/401"
**Solution:** Check credentials in .env
```bash
# Verify token is valid
curl -u your@email.com:YOUR_TOKEN https://yourcompany.atlassian.net/rest/api/3/myself
```

### Issue: "No activities found"
**Solution:** 
1. Check project key is correct
2. Verify Jira permissions
3. Try different project
4. Check if agents are actually creating tickets

### Issue: "Streamlit port already in use"
**Solution:** Use different port
```bash
streamlit run app.py --server.port=8502
```

---

## Security Best Practices

✅ **DO:**
- Store `.env` in secure vault (HashiCorp Vault, AWS Secrets Manager)
- Rotate API tokens every 90 days
- Use IP whitelisting for Jira API access
- Enable Jira activity logging
- Archive sensitive data regularly
- Require MFA for admin access

❌ **DON'T:**
- Commit `.env` to Git (add to .gitignore)
- Share credentials in logs
- Use admin token for all operations
- Disable Jira audit logging
- Store tokens in code comments

---

## Next Steps

1. **Verify Configuration**
   ```bash
   python -c "from utils.governance_client import JiraGovernanceClient; gov = JiraGovernanceClient(); print(gov.get_governance_metrics())"
   ```

2. **Test Agents**
   ```bash
   python -c "from agents.classifier_agent import classify; print(classify({'action': 'DELETE', 'target': 'project'}))"
   ```

3. **Run Dashboard**
   ```bash
   streamlit run app.py
   ```

4. **Monitor in Production**
   - Set up log aggregation (ELK, Splunk)
   - Configure alerts for high-risk actions
   - Generate weekly compliance reports
   - Review governance metrics

---

## Support & Documentation

- **GitHub:** https://github.com/ShwethaHarilal70/agentguard
- **Issues:** Report bugs in GitHub Issues
- **Docs:** See README.md and inline code comments
- **API Docs:** https://developer.atlassian.com/cloud/jira/rest/

---

**AgentGuard v1.0 — Enterprise AI Governance Platform**
Ready for production deployment! 🚀
