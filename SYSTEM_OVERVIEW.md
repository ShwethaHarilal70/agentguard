# 🛡️ AgentGuard: AI Agent Governance Platform
## System Description & Algorithm Explanation

---

## Executive Summary

**AgentGuard** is an enterprise-grade governance and monitoring platform that tracks AI agent actions in Jira, detects anomalies, performs threat analysis, and generates compliance reports. It solves the critical problem of **actor attribution** — distinguishing between AI-generated and human-generated Jira actions — to provide governance, security, and compliance visibility into autonomous agent activity.

**Core Innovation:** Uses **label-based governance tracking** in Jira (not a separate database) combined with multi-layered threat detection to achieve enterprise-scale AI governance.

---

## Problem Statement

When AI agents operate autonomously in enterprise systems (like Jira):
- ❌ **Attribution Problem:** All actions show creator as the system user (e.g., "Shwetha Harilal"), not the AI agent
- ❌ **Governance Gap:** No way to know which changes were AI vs human-driven
- ❌ **Compliance Risk:** Cannot audit, report, or control AI activity
- ❌ **Threat Blindness:** No detection of malicious prompts, data exfiltration attempts, or jailbreaks

**AgentGuard's Solution:**
- ✅ Label-based metadata tracking in Jira (`ai-generated`, `agent:classifier-v1`, `risk:high`, etc.)
- ✅ Multi-agent pipeline for classification, monitoring, analysis, and reporting
- ✅ Advanced threat detection via Lobster Trap security scanning
- ✅ Real-time governance dashboard with compliance reporting

---

## System Architecture

### High-Level Flow

```
Jira Activity Stream
       ↓
┌─────────────────────────────────────────┐
│  AgentGuard Multi-Agent Pipeline        │
├─────────────────────────────────────────┤
│ 1. Classifier Agent                     │
│    • Detects AI vs human actions        │
│    • Scores risk (Low/Medium/High)      │
│    • Applies governance labels          │
│                                         │
│ 2. Monitor Agent                        │
│    • Tracks anomalies                   │
│    • Detects velocity spikes            │
│    • Identifies suspicious patterns     │
│                                         │
│ 3. Threat Detector (Lobster Trap)       │
│    • Scans for prompt injections        │
│    • Detects data exfiltration          │
│    • Identifies jailbreak attempts      │
│                                         │
│ 4. Explainer Agent (Claude Haiku)       │
│    • Generates governance explanations  │
│    • Compliance-ready narratives        │
│                                         │
│ 5. Report Agent                         │
│    • Compiles metrics                   │
│    • Generates compliance reports       │
│    • Tracks governance KPIs             │
└─────────────────────────────────────────┘
       ↓
Streamlit Dashboard (5 Pages)
       ↓
Action Tracker | Governance Report | Prompt Inspection 
Policy Manager | AI Governance Dashboard
```

---

## Component Descriptions

### 1. **Classifier Agent** (`agents/classifier_agent.py`)

**Purpose:** Determine if an action is AI-originated and assign risk level

**Algorithm:**
```
Input: Jira action (CREATE, UPDATE, DELETE, etc.)

Step 1: Check explicit AI signals
├─ [AI-GENERATED] label in summary?
├─ Atlassian Intelligence template (Summary/Context/Acceptance Criteria)?
└─ If yes → Return is_ai=True, confidence=100%

Step 2: Multi-layer detection
├─ Content Analysis
│  ├─ AI language patterns (leverage, facilitate, ensure, deploy)
│  ├─ Enterprise keywords (governance, audit, compliance)
│  ├─ Perfect grammar (no informal language)
│  └─ Score: 0-40 points
│
├─ API Origin Detection
│  ├─ Action via API (not browser UI)?
│  ├─ Programmatic field modifications?
│  └─ Score: 0-40 points
│
├─ Velocity Analysis
│  ├─ Multiple actions in short timespan?
│  ├─ Patterns inhuman (off-hours, bursts)?
│  └─ Score: 0-40 points
│
└─ Structural Similarity
   ├─ Template reuse across tickets?
   ├─ Identical formatting?
   └─ Score: 0-20 points

Step 3: Aggregate & Threshold
├─ Total score ≥ 50 → is_ai=True
├─ Confidence = (score / 100) * 100%
├─ Risk Level: Low (🟢) / Medium (🟡) / High (🔴)
└─ Apply Jira labels: ai-generated, agent:X, risk:Y, governance-review

Output: 
{
  is_ai: Boolean,
  confidence: 0-100,
  risk_level: "LOW" | "MEDIUM" | "HIGH",
  signals: [...],
  layers: {content: 0-40, api_origin: 0-40, velocity: 0-40, ...}
}
```

---

### 2. **Monitor Agent** (`agents/monitor_agent.py`)

**Purpose:** Real-time activity monitoring and anomaly detection

**Algorithm:**
```
Input: Stream of classified actions

For each action:
├─ Compare against baseline patterns
├─ Check velocity (actions per minute)
├─ Detect off-hours activity
├─ Score anomaly (0-100)
└─ Flag if anomaly_score > 60

Anomaly Signals:
├─ Unusual time of day
├─ Burst activity (>10 actions/min)
├─ Repeated access to sensitive fields
├─ Rapid escalations
└─ Target expansion (accessing new projects)

Output: 
{
  activity: {...},
  anomaly_score: 0-100,
  is_anomaly: Boolean,
  flags: [...]
}
```

---

### 3. **Threat Detector** (Lobster Trap Integration)

**Purpose:** Security threat scanning for malicious content

**Algorithm:**
```
Input: Jira ticket description/content

Step 1: Parse text
Step 2: Run Lobster Trap.exe inspect command
Step 3: Analyze output for threat patterns
├─ Prompt Injection patterns
├─ Data Exfiltration keywords (export, extract, download, credential)
├─ Jailbreak attempts (ignore, override, bypass)
├─ SQL/Command injection (DROP, DELETE, execute)
├─ XXE/SSRF patterns
└─ Confidence scoring (0.0-1.0)

Step 4: Classify threat level
├─ CRITICAL (0.85+) → 🔴 DENY
├─ HIGH (0.65+)     → 🔴 FLAG
├─ MEDIUM (0.45+)   → 🟡 MONITOR
└─ LOW (<0.45)      → 🟢 ALLOW

Output:
{
  status: "ALLOW" | "DENY" | "TIMEOUT",
  threat_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL",
  threats_detected: [...],
  confidence: 0.0-1.0,
  recommendations: [...]
}
```

---

### 4. **Explainer Agent** (Claude Haiku)

**Purpose:** Generate human-readable governance explanations

**Algorithm:**
```
Input: Classified action with risk level + threat detection

Prompt Template:
"You are an enterprise AI governance analyst reviewing an 
 action taken inside Jira.
 
 Action details:
 - Actor: {agent_name}
 - Action type: {action}
 - Target: {target}
 - Risk level: {risk_level}
 - Threats detected: {threats}
 
 Write 2-3 sentences explaining:
 1. What happened and why it is {status}
 2. What the governance or security risk is
 3. What a compliance officer should do next"

Model: Claude 3.5 Haiku (fast, cost-effective)

Output: Compliance-ready narrative
Example:
"AI agent 'classifier-v1' created a new SCRUM ticket for 
payroll tracking with HIGH risk designation due to sensitive 
data scope. A governance officer must review the access 
permissions and verify the agent is authorized for payroll 
domain operations."
```

---

### 5. **Report Agent** (`agents/report_agent.py`)

**Purpose:** Aggregate metrics and generate compliance reports

**Algorithm:**
```
Input: All classified + monitored actions over time period

Metrics Calculation:
├─ Total AI Actions: Count(is_ai=True)
├─ High-Risk Actions: Count(risk_level="HIGH")
├─ Anomalies Detected: Count(anomaly_score > 60)
├─ Threats Blocked: Count(threat_status="DENY")
├─ Compliance Score: (allowed_actions / total_actions) * 100
└─ Trend Analysis: Actions over time

Report Sections:
1. Executive Summary
   - Total actions, AI vs human split
   - Risk distribution (pie chart)
   
2. Flagged Actions
   - List of HIGH/MEDIUM risk items
   - Threat detections
   - Required reviews
   
3. Governance Metrics
   - Compliance score
   - Anomaly count
   - Trend (improving/degrading)
   
4. Recommendations
   - Policy adjustments
   - Access reviews
   - Training needs

Output: PDF/CSV compliance report
```

---

## Label-Based Governance Tracking

**Instead of:** Separate database to track AI actions
**We use:** Jira labels as metadata tier

### Label Schema

| Label | Purpose | Example |
|-------|---------|---------|
| `ai-generated` | Marks ticket as AI-created | Automatic |
| `agent:X` | Identifies which AI agent | `agent:classifier-v1` |
| `risk:level` | Risk classification | `risk:high`, `risk:medium` |
| `governance-review` | Requires review | Automatic for HIGH risk |
| `threat:X` | Detected threat type | `threat:prompt-injection` |

### Query Examples

```jql
# Find all AI-generated tickets
project = SCRUM AND labels in (ai-generated)

# Find high-risk AI actions
project = SCRUM AND labels in (ai-generated, risk:high)

# Find specific agent actions
project = SCRUM AND labels in (agent:classifier-v1)

# Find tickets with threats
project = SCRUM AND labels in (threat:*)
```

---

## Streamlit Dashboard

### Page 1: Action Tracker
- List all classified actions
- Filter by: Source, Status, Action Type, Risk Level
- View: Timestamp, Agent, Summary, Risk, Status

### Page 2: Governance Report
- Metrics: Total AI actions, High-risk count, Anomalies
- Charts: Risk distribution, Trend over time
- Compliance score

### Page 3: Prompt Inspection
- Paste Jira ticket content
- Real-time threat detection
- Intent mismatch analysis
- Risk scoring

### Page 4: Policy Manager
- Create/edit governance rules
- Set risk thresholds
- Configure alerts
- Manage agent access

### Page 5: AI Governance Dashboard
- Executive overview
- KPIs and metrics
- Trend analysis
- Recommendations

---

## Data Flow Example

**Scenario:** AI agent creates a new Jira ticket for "Export Employee Payroll"

```
1. Jira API Hook
   └─ Detects SCRUM-42 created by system user "Shwetha Harilal"

2. Classifier Agent
   ├─ Analyzes: "export payroll data"
   ├─ Detects: Data exfiltration keyword
   ├─ Scores: AI confidence 92%, Risk HIGH
   └─ Action: Apply labels (ai-generated, agent:classifier-v1, risk:high, governance-review)

3. Threat Detector (Lobster Trap)
   ├─ Scans ticket description
   ├─ Detects: "Data Exfiltration Risk" (98% confidence)
   └─ Status: DENY

4. Monitor Agent
   ├─ Checks: Recent activity pattern
   ├─ Detects: Unusual early morning activity
   └─ Anomaly score: 72%

5. Explainer Agent
   ├─ Generates narrative:
   │  "AI agent 'classifier-v1' created SCRUM-42 with HIGH
   │   risk due to payroll data scope. Lobster Trap detected
   │   data exfiltration risk (98% confidence). Governance
   │   officer must BLOCK this ticket immediately."
   └─ Status: GOVERNANCE REVIEW REQUIRED

6. Report Agent
   ├─ Increments: HIGH_RISK_ACTIONS += 1
   ├─ Increments: THREATS_DETECTED += 1
   └─ Updates compliance score

7. Streamlit Dashboard
   ├─ Shows in "Prompt Inspection": CRITICAL threat
   ├─ Shows in "Governance Report": +1 high-risk action
   ├─ Alerts: "Action SCRUM-42 requires immediate review"
   └─ User: Clicks to review and take action
```

---

## Key Algorithms & Techniques

### 1. **Multi-Layer Detection**
Combines content, metadata, and behavioral signals to avoid false positives

### 2. **Confidence Scoring**
Returns confidence (0-100%) rather than binary yes/no for better decision-making

### 3. **Risk Stratification**
Labels actions as Low/Medium/High to prioritize governance review

### 4. **Anomaly Detection**
Compares current behavior against baseline to detect deviations

### 5. **Threat Confidence**
Uses 0.0-1.0 confidence scores for threat detection rather than binary

### 6. **Graceful Degradation**
If Lobster Trap unavailable, uses mock detection; if Claude unavailable, uses templates

---

## Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| Classify action | ~100ms | Fast detection |
| Threat scan | 0.5-2s | Per content |
| Generate explanation | ~2-5s | Claude Haiku call |
| Generate full report | ~10-30s | Batch processing |
| Dashboard load | ~1-2s | Cached queries |

---

## Security & Compliance

✅ **Features:**
- End-to-end AI governance tracking
- Threat detection and blocking
- Compliance-ready reporting
- Audit trail in Jira labels
- Real-time alerting
- Policy enforcement

✅ **Standards:**
- SOC 2 aligned (governance, monitoring, alerting)
- Auditable decision trail
- Non-repudiation (all actions logged)
- Segregation of duties (governance review required)

---

## Running the Application

### Option 1: Direct Streamlit (For Demo)
```bash
streamlit run app.py
```
Opens at: `http://localhost:8501`

### Option 2: With Startup Script (Recommended)
```bash
python startup.py
```
Performs pre-flight checks, then launches app

### Option 3: Docker (Production)
```bash
docker build -t agentguard:latest .
docker run -p 8501:8501 agentguard:latest
```

---

## Configuration

### Environment Variables (.env)
```
JIRA_URL=https://your-instance.atlassian.net
JIRA_EMAIL=user@company.com
JIRA_API_TOKEN=your_api_token
CLAUDE_API_KEY=your_anthropic_api_key
LOBSTER_TRAP_PATH=./lobstertrap.exe
```

### Key Settings (app.py)
```python
ENABLE_LOBSTER_TRAP = True      # Enable threat detection
ENABLE_CLAUDE_HAIKU = True      # Use Claude for explanations
CACHE_TTL = 300                 # Dashboard cache timeout
ANOMALY_THRESHOLD = 60          # Anomaly score threshold
```

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Web Framework | Streamlit | Dashboard UI |
| AI Analysis | Claude 3.5 Haiku | Governance explanations |
| Threat Detection | Lobster Trap | Security scanning |
| Jira Integration | Jira REST API v3 | Action tracking |
| Language | Python 3.13+ | Application code |
| Deployment | Docker/Systemd | Production hosting |

---

## Summary

**AgentGuard** provides enterprise-grade AI governance by:

1. **Detecting** AI actions automatically via multi-layer analysis
2. **Labeling** actions with metadata in Jira (not separate DB)
3. **Threat Detection** using Lobster Trap security scanning
4. **Explaining** governance implications via Claude Haiku
5. **Reporting** compliance metrics and trends
6. **Alerting** on high-risk or anomalous activity

**Result:** Complete visibility and control over autonomous AI agent activity in Jira.

---

**For more details, see:**
- Implementation: See individual agent files in `agents/`
- Usage: See `QUICK_START.md`
- Deployment: See `ENTERPRISE_DEPLOYMENT_GUIDE.md`
- Threat Detection: See `LOBSTER_TRAP_INTEGRATION.md`
