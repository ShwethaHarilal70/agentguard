# 🛡️ AgentGuard: AI Agent Governance Platform

**Enterprise-grade governance and monitoring platform for AI agents operating in Jira**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/Python-3.13%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.33%2B-FF4B4B)](https://streamlit.io/)

---

## 🎯 The Problem

When AI agents operate autonomously in enterprise systems:
- ❌ All actions appear to come from a system user (no actor attribution)
- ❌ No visibility into which changes were AI vs human-driven
- ❌ Impossible to audit autonomous activity
- ❌ No protection against malicious prompts or data exfiltration
- ❌ Non-compliant with governance requirements

**AgentGuard solves this with intelligent multi-layer analysis and enterprise-grade threat detection.**

---

## ✨ The Solution

### 🤖 Multi-Agent Pipeline

Five specialized agents work together:

1. **Classifier Agent** — AI vs human detection with 6+ signals (85-100% confidence)
2. **Monitor Agent** — Real-time anomaly detection (velocity, patterns, off-hours)
3. **Threat Detector** — Lobster Trap security scanning (7+ threat types)
4. **Explainer Agent** — Claude Haiku governance narratives
5. **Report Agent** — Compliance metrics and formal reporting

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/agentguard.git
cd agentguard

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials
```

### Configuration

Edit `.env` with:
```bash
CLAUDE_API_KEY=sk-ant-YOUR_KEY           # Get from: https://console.anthropic.com/
JIRA_URL=https://your-instance.atlassian.net
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=your-token                # Get from: https://id.atlassian.com/manage/
```

### Run the App

```bash
# Direct Streamlit (for demos)
streamlit run app.py

# With startup verification (recommended)
python startup.py
```

Opens at: **http://localhost:8501**

---

## 📊 Dashboard Features

### 5 Interactive Pages

| Page | Features |
|------|----------|
| **Action Tracker** | Real-time AI action monitoring with risk classification |
| **Governance Report** | Compliance metrics, risk distribution, trend analysis |
| **Prompt Inspection** | Live threat detection on Jira content |
| **Policy Manager** | Configure governance rules and risk thresholds |
| **AI Governance Dashboard** | Executive KPIs and recommendations |

---

## 🔍 How It Works

### AI Detection (6+ Signals)

Identifies AI-generated actions with confidence scoring:

```
Input: Jira action
  ↓
Explicit AI label?  [0-100 pts]
Atlassian template? [0-100 pts]
Content analysis?   [0-40 pts]
API origin?         [0-40 pts]
Velocity spike?     [0-40 pts]
Similar patterns?   [0-20 pts]
  ↓
Aggregate score + confidence → Decision
  ↓
Output: is_ai, confidence%, risk_level, signals
```

### Threat Detection (7+ Types)

Scans for security vulnerabilities:

- 🚨 Prompt Injection
- 📤 Data Exfiltration  
- 🔓 Jailbreak Attempts
- 💉 SQL Injection
- 🔧 Command Injection
- 🔗 SSRF Attacks
- 📋 XXE Attacks

**Result:** ALLOW/DENY with confidence (0-1.0)

### Label-Based Governance Tracking

Uses Jira labels (no external database):

```jql
# Find all AI-generated tickets
labels in (ai-generated)

# Find high-risk AI actions
labels in (ai-generated, risk:high)

# Find threats
labels in (threat:*)
```

---

## 🎬 Demo Video

Full video walkthrough available in GitHub Releases showing:
- Dashboard overview (all 5 pages)
- Live threat detection demo
- AI action detection examples
- Compliance reporting
- Architecture walkthrough

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [**SYSTEM_OVERVIEW.md**](SYSTEM_OVERVIEW.md) | **START HERE** — Complete description & algorithms |
| [**QUICK_DEMO_GUIDE.md**](QUICK_DEMO_GUIDE.md) | How to run and interact with dashboard |
| [**QUICK_START.md**](QUICK_START.md) | Usage guide and walkthroughs |
| [**ENTERPRISE_DEPLOYMENT_GUIDE.md**](ENTERPRISE_DEPLOYMENT_GUIDE.md) | Production deployment options |
| [**LOBSTER_TRAP_INTEGRATION.md**](LOBSTER_TRAP_INTEGRATION.md) | Threat detection setup |
| [**GITHUB_SETUP_AND_VIDEO_GUIDE.md**](GITHUB_SETUP_AND_VIDEO_GUIDE.md) | Repository & video setup |

---

## 🛠 Technology Stack

- **Web Framework**: Streamlit 1.33+
- **AI Analysis**: Claude Haiku (Anthropic)
- **Threat Detection**: Lobster Trap
- **Jira Integration**: REST API v3
- **Language**: Python 3.13+
- **Deployment**: Docker / Systemd

---

## ✨ Key Features

✅ **AI Action Detection** — Multi-signal analysis with confidence scoring
✅ **Threat Detection** — 7+ security threat types
✅ **Governance Reporting** — Compliance-ready narratives
✅ **Real-time Monitoring** — Live action tracking & anomaly detection
✅ **Policy Enforcement** — Configurable governance rules
✅ **Enterprise Integration** — Seamless Jira integration
✅ **Production Ready** — Docker & Systemd deployment

---

## 🚀 Deployment

### Local
```bash
streamlit run app.py
```

### Docker
```bash
docker build -t agentguard:latest .
docker run -p 8501:8501 agentguard:latest
```

### Production
See [ENTERPRISE_DEPLOYMENT_GUIDE.md](ENTERPRISE_DEPLOYMENT_GUIDE.md)

---

## 📊 Use Cases

- **Autonomous Payroll** — Monitor AI handling sensitive employee data
- **Infrastructure Management** — Govern AI-driven cloud provisioning
- **Compliance Tracking** — Meet regulatory AI governance requirements
- **Threat Detection** — Identify malicious prompts & data exfiltration
- **Risk Management** — Enterprise-scale AI activity tracking

---

## 🧪 Testing

```bash
# Test Lobster Trap integration
python test_lobster_trap.py

# Run startup checks
python startup.py

# Verify installations
pip list | grep -E "streamlit|anthropic|requests"
```

---

## 📈 Performance

| Operation | Time |
|-----------|------|
| AI detection | ~100ms |
| Threat scan | 0.5-2s |
| Claude explanation | 2-5s |
| Report generation | 10-30s |
| Dashboard load | 1-2s |

---

## 🔐 Security

✅ Credentials managed via .env (never in code)
✅ Jira labels for metadata (no external storage)
✅ Thread-safe operations
✅ Comprehensive error handling
✅ Compliance-friendly architecture

---

## 📝 License

MIT License — See LICENSE file

---

## 🏆 Project Highlights

- **Problem Solved**: AI agent actor attribution in enterprise systems
- **Architecture**: 5-agent governance pipeline
- **Threat Detection**: 7+ security threat types
- **Detection Quality**: 85-100% AI action confidence
- **Integration**: Seamless Jira + Claude Haiku + Lobster Trap
- **Documentation**: 10+ comprehensive guides

---

## 🚀 Quick Links

- **Live Demo**: Run `streamlit run app.py`
- **Documentation**: Start with [SYSTEM_OVERVIEW.md](SYSTEM_OVERVIEW.md)
- **Setup Guide**: See [GITHUB_SETUP_AND_VIDEO_GUIDE.md](GITHUB_SETUP_AND_VIDEO_GUIDE.md)
- **Threat Detection**: Read [LOBSTER_TRAP_INTEGRATION.md](LOBSTER_TRAP_INTEGRATION.md)

---

## 📞 Support

- **Issues**: GitHub Issues tab
- **Questions**: Check documentation files
- **Examples**: See `agents/` and `utils/` directories

---

**AgentGuard: Making AI Governance Possible** 🛡️

Built for enterprise security and compliance teams

Last Updated: May 16, 2026 | Version: 1.0.0
