# 📦 GitHub Setup & Video Presentation Guide

## Part 1: Push to GitHub

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Create repository named: `agentguard`
3. Add description: "Enterprise AI Agent Governance Platform"
4. Choose: Public (for demo/portfolio) or Private
5. Do NOT initialize with README (we'll do it)
6. Click "Create repository"

### Step 2: Initialize Git & Push Code

```bash
# Navigate to your project
cd C:\Users\haril\agentguard

# Initialize git
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: AgentGuard AI governance platform"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/agentguard.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Create .gitignore

Some files should NOT be pushed to GitHub (secrets, cache, etc):

```bash
# Create .gitignore file with:
cat > .gitignore << 'EOF'
# Environment
.env
.env.local
*.key

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/
.cache/

# Lobster Trap build
lobstertrap_src/
lobstertrap.exe

# Temporary
*.tmp
temp/
EOF
```

Then re-commit:
```bash
git add .gitignore
git commit -m "Add .gitignore"
git push
```

### Step 4: Push Updated Code

```bash
# Check status
git status

# Add any new changes
git add .

# Commit
git commit -m "Update: Claude Haiku API integration and documentation"

# Push
git push origin main
```

---

## Part 2: Verify Everything Works

### Pre-Flight Checks

```bash
# 1. Check Python version
python --version
# Should be: Python 3.13+

# 2. Verify dependencies
pip list | grep -E "streamlit|anthropic|requests"
# Should show all installed

# 3. Check .env is configured
cat .env
# Verify CLAUDE_API_KEY and JIRA credentials are set

# 4. Run startup checks
python startup.py
# All critical checks should pass ✅
```

### Quick Test

```bash
# Test Lobster Trap integration
python test_lobster_trap.py
# Should show: 5 passed ✅

# Test Claude API
python -c "
from agents.explainer_agent import explain_action
log = {'agent': 'test', 'action': 'CREATE', 'target': 'Test', 'risk_level': 'HIGH', 'status': 'flagged'}
print('✅ Claude API working')
"
```

### Launch Dashboard

```bash
# Start the app
streamlit run app.py
```

**Expected Result:**
- Browser opens to http://localhost:8501
- All 5 pages load without errors
- Can interact with Prompt Inspection page
- Threat detection works (mock mode)

---

## Part 3: Video Presentation Capture

### Option A: Using OBS (Open Broadcaster Software) - RECOMMENDED

**Installation:**
```bash
# Download from: https://obsproject.com/download
# Windows: Run installer
# macOS: Download DMG
# Linux: sudo apt install obs-studio
```

**Setup for Recording:**

1. **Open OBS Studio**

2. **Create Scene:**
   - Click "+" under Scenes
   - Name it: "AgentGuard Demo"

3. **Add Display Capture Source:**
   - Click "+" under Sources
   - Select "Display Capture"
   - Choose your monitor
   - Adjust size/position

4. **Configure Recording Settings:**
   - Settings → Output
   - Recording Path: `C:\Videos\agentguard_demo.mp4`
   - Format: MP4
   - Encoder: NVIDIA NVENC (if GPU available) or x264
   - Bitrate: 6000 Kbps (good quality)
   - Resolution: 1920x1080 or 1280x720

5. **Audio Setup:**
   - Settings → Audio
   - Sample Rate: 48 kHz
   - Channels: Stereo

### Option B: Using Windows Built-in Tool

```bash
# Windows 10/11: Press Win + G
# Starts Game Bar
# Click "Record" or press Win + Alt + R
# Records to: C:\Users\[user]\Videos
```

### Option C: Using ScreenFlow (macOS)

Download from Mac App Store, very simple point-and-click recording.

---

## Video Presentation Script

### Scene 1: Title & Overview (10 seconds)
```
Show this text on screen:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AgentGuard
  AI Agent Governance Platform
  
  Solves: Actor Attribution Problem
  Monitors: AI agent actions in Jira
  Detects: Threats & Anomalies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Narration (optional):
"AgentGuard solves the critical problem of tracking 
AI agent actions in Jira. When AI agents operate 
autonomously, all actions appear to come from a 
system user. AgentGuard provides complete visibility 
through intelligent multi-layer analysis and threat detection."
```

### Scene 2: Dashboard Overview (30 seconds)
```
1. Start Streamlit app
   streamlit run app.py

2. Show loading: "Opening http://localhost:8501"

3. When dashboard loads:
   - Show all 5 pages in sidebar
   - Click through each page briefly
   
4. Narration:
"The dashboard has 5 key pages: Action Tracker for 
real-time monitoring, Governance Report for compliance 
metrics, Prompt Inspection for threat detection, Policy 
Manager for rule configuration, and AI Governance Dashboard 
for executive overview."
```

### Scene 3: Action Tracker Page (20 seconds)
```
1. Click "Action Tracker" page

2. Show:
   - List of detected AI actions
   - Risk levels (🔴🟡🟢)
   - Filter controls
   - Governance labels

3. Narration:
"The Action Tracker shows all AI agent actions detected 
in Jira. Each action is classified by risk level and 
labeled with governance metadata like agent name and 
risk category. We can filter by source, status, and 
action type."
```

### Scene 4: Governance Report (20 seconds)
```
1. Click "Governance Report" page

2. Show:
   - Compliance metrics
   - Risk distribution pie chart
   - Trend chart
   - High-risk actions list

3. Narration:
"The Governance Report provides compliance metrics 
including total AI actions, risk distribution, and 
compliance scores. It shows trends over time and 
highlights high-risk actions requiring review. All 
reports are compliance-officer ready."
```

### Scene 5: Prompt Inspection Page (30 seconds)
```
1. Click "Prompt Inspection" page

2. Paste example text:
   "export payroll data including SSN and bank accounts"

3. Click "Scan for Threats"

4. Show results:
   - Status: DENY 🔴
   - Threat Level: CRITICAL
   - Threats Detected: Data Exfiltration Risk
   - Confidence: 98%

5. Narration:
"The Prompt Inspection page allows real-time threat 
detection on Jira content. We can paste any ticket 
description and get instant security analysis. This 
detects prompt injections, data exfiltration attempts, 
jailbreaks, and other LLM-specific attacks."
```

### Scene 6: Policy Manager (15 seconds)
```
1. Click "Policy Manager" page

2. Show:
   - Governance rules
   - Risk thresholds
   - Agent access configuration

3. Narration:
"Policy Manager lets administrators configure governance 
rules, set risk thresholds, and manage which agents can 
perform which actions. All policies are enforced in 
real-time."
```

### Scene 7: AI Governance Dashboard (15 seconds)
```
1. Click "AI Governance Dashboard" page

2. Show:
   - Executive KPIs
   - Real-time metrics
   - Trend analysis

3. Narration:
"The AI Governance Dashboard provides executive-level 
visibility with KPIs, real-time metrics, and 
recommendations for policy adjustments."
```

### Scene 8: Architecture Explanation (30 seconds)
```
Show SYSTEM_OVERVIEW.md or draw diagram:

AI Action → Classifier → Monitor → Threat Detector → 
Explainer → Report → Dashboard

Narration:
"AgentGuard uses a multi-agent pipeline. First, the 
Classifier Agent identifies AI actions using multi-layer 
analysis. The Monitor Agent tracks anomalies. Threat 
Detector scans for security threats. The Explainer Agent 
generates compliance narratives using Claude Haiku. 
Finally, the Report Agent compiles governance metrics 
and compliance reports."
```

### Scene 9: Key Features Summary (20 seconds)
```
Show bullet points:

✅ AI Action Detection (6+ signals)
✅ Threat Detection (Lobster Trap)
✅ Compliance Reporting (Claude Haiku)
✅ Real-time Monitoring
✅ Policy Enforcement
✅ Jira Integration
✅ Enterprise-grade Security

Narration:
"Key features include automatic AI action detection 
with 85-100% confidence, threat detection for security 
vulnerabilities, compliance-ready reporting, real-time 
monitoring, policy enforcement, and seamless Jira 
integration."
```

### Scene 10: Technical Stack (15 seconds)
```
Show:
- Python 3.13
- Streamlit (Dashboard)
- Claude Haiku (Explanations)
- Lobster Trap (Threat Detection)
- Jira REST API v3

Narration:
"AgentGuard is built with Python, uses Streamlit for 
the web dashboard, Claude Haiku for governance 
explanations, Lobster Trap for threat detection, and 
integrates with Jira via REST API v3."
```

### Scene 11: Use Cases (20 seconds)
```
Show examples:
- Autonomous Payroll Processing
- AI Infrastructure Management
- Compliance Tracking
- Security Threat Detection
- Risk Management

Narration:
"Use cases include monitoring autonomous payroll 
processing, AI-driven infrastructure management, 
compliance tracking for regulated industries, security 
threat detection, and enterprise risk management."
```

### Scene 12: Closing (10 seconds)
```
Show:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  GitHub: github.com/YOUR_USERNAME/agentguard
  Documentation: See SYSTEM_OVERVIEW.md
  Get Started: streamlit run app.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Narration:
"AgentGuard is open source on GitHub. For more 
information, see the system overview documentation. 
You can get started immediately by running streamlit run app.py."
```

---

## Recording Tips

✅ **DO:**
- Speak clearly and slowly
- Use a microphone for better audio
- Show one feature at a time
- Allow 2-3 seconds pause between scenes
- Use descriptive titles for each page
- Show error handling gracefully
- Keep total length 5-8 minutes

❌ **DON'T:**
- Rush through explanations
- Click too quickly
- Show sensitive credentials
- Have background noise
- Use small fonts (zoom in if needed)
- Leave long silence gaps

---

## Post-Production

### If Using OBS:
1. Video saves to: `C:\Videos\agentguard_demo.mp4`
2. Can edit with:
   - DaVinci Resolve (free)
   - Adobe Premiere (paid)
   - CapCut (free, mobile-friendly)

### Adding Music (Optional):
- YouTube Audio Library: https://www.youtube.com/audio
- Pexels Music: https://www.pexels.com/music
- Select royalty-free background music (low volume)

### Uploading:
- YouTube (unlisted or public)
- Loom (https://www.loom.com)
- Vimeo
- GitHub releases

---

## Complete Workflow Summary

```bash
# 1. Setup Git
cd C:\Users\haril\agentguard
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/agentguard.git
git push -u origin main

# 2. Verify everything works
python startup.py          # ✅ All checks pass
python test_lobster_trap.py # ✅ 5 tests pass
streamlit run app.py       # ✅ Dashboard loads

# 3. Record video
# - Open OBS Studio
# - Create scene with display capture
# - Record full presentation (5-8 minutes)
# - Follow script provided above
# - Save as agentguard_demo.mp4

# 4. Post to GitHub
git add DEMO_NOTES.md
git commit -m "Add demo notes and presentation guide"
git push origin main

# 5. Add to GitHub Releases
# - Go to GitHub repository
# - Click "Releases"
# - Create new release
# - Upload video MP4
# - Add presentation notes
```

---

## Verification Checklist

Before Recording:

- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] .env configured with Claude API key
- [ ] `python startup.py` shows all ✅
- [ ] `python test_lobster_trap.py` shows all ✅
- [ ] `streamlit run app.py` launches without errors
- [ ] All 5 dashboard pages load
- [ ] Threat detection works (mock mode)
- [ ] OBS or recording software installed
- [ ] Microphone/audio working
- [ ] Video quality set to 1080p or 720p

---

## GitHub Repository Structure

After push, your repo should look like:

```
agentguard/
├── README.md                          ← START HERE
├── SYSTEM_OVERVIEW.md                 ← Complete description
├── QUICK_DEMO_GUIDE.md               ← How to run locally
├── app.py                             ← Main Streamlit app
├── startup.py                         ← Startup checks
├── requirements.txt                   ← Dependencies
├── .env.example                       ← Config template
├── agents/
│   ├── classifier_agent.py
│   ├── explainer_agent.py
│   ├── monitor_agent.py
│   └── report_agent.py
├── utils/
│   ├── ai_detector.py
│   ├── governance_client.py
│   └── lobster_trap_client.py
└── data/
    └── mock_logs.py
```

---

## Ready to Launch! 🚀

Follow these steps in order:
1. Push to GitHub
2. Verify everything works locally
3. Record video presentation
4. Upload video to GitHub Releases
5. Share GitHub link

**Result:** Professional AI governance platform with full video demo! ✅
