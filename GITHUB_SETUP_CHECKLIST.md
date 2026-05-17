# ✅ GitHub & Video Setup Checklist

## Step-by-Step Instructions

### Phase 1: Prepare Repository (5 minutes)

- [ ] **Create GitHub Account** (if you don't have one)
  - Go to https://github.com/signup
  - Verify email

- [ ] **Create New Repository**
  - Go to https://github.com/new
  - Repository name: `agentguard`
  - Description: "Enterprise AI Agent Governance Platform"
  - Choose: Public (for portfolio) or Private
  - **DO NOT** initialize with README
  - Click "Create repository"

- [ ] **Configure Git Locally**
  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "your-email@example.com"
  ```

### Phase 2: Push Code to GitHub (10 minutes)

- [ ] **Navigate to Project**
  ```bash
  cd C:\Users\haril\agentguard
  ```

- [ ] **Initialize Git Repository**
  ```bash
  git init
  ```

- [ ] **Add All Files**
  ```bash
  git add .
  ```

- [ ] **Create Initial Commit**
  ```bash
  git commit -m "Initial commit: AgentGuard AI governance platform with multi-agent pipeline, threat detection, and compliance reporting"
  ```

- [ ] **Add Remote Origin** (replace YOUR_USERNAME)
  ```bash
  git remote add origin https://github.com/YOUR_USERNAME/agentguard.git
  ```

- [ ] **Rename Branch & Push**
  ```bash
  git branch -M main
  git push -u origin main
  ```

  This will prompt for GitHub credentials. Use:
  - **Username**: Your GitHub username
  - **Password**: Your personal access token (Settings → Developer settings → Personal access tokens)

- [ ] **Verify on GitHub**
  - Go to https://github.com/YOUR_USERNAME/agentguard
  - Verify all files are uploaded

### Phase 3: Verify Everything Works (15 minutes)

- [ ] **Check Installation**
  ```bash
  python --version
  # Should be Python 3.13+
  
  pip list | grep -E "streamlit|anthropic|requests"
  # Should show installed packages
  ```

- [ ] **Verify Configuration**
  ```bash
  cat .env
  # Check CLAUDE_API_KEY is set
  # Check JIRA credentials are set
  ```

- [ ] **Run Pre-flight Checks**
  ```bash
  python startup.py
  # Should show all ✅ checks passing
  ```

- [ ] **Test Threat Detection**
  ```bash
  python test_lobster_trap.py
  # Should show 5 tests passed
  ```

- [ ] **Launch Dashboard**
  ```bash
  streamlit run app.py
  ```
  
  Verify:
  - [ ] Browser opens to http://localhost:8501
  - [ ] Dashboard loads without errors
  - [ ] All 5 pages appear in sidebar
  - [ ] Can click through each page
  - [ ] Threat detection works

- [ ] **Test Each Page**
  - [ ] Action Tracker: Shows with mock data
  - [ ] Governance Report: Displays metrics and charts
  - [ ] Prompt Inspection: Can paste text and detect threats
  - [ ] Policy Manager: Shows governance rules
  - [ ] AI Governance Dashboard: Shows KPIs

### Phase 4: Record Video Presentation (45 minutes - 1 hour)

- [ ] **Install Recording Software**
  ```bash
  # Option 1: OBS Studio (recommended)
  # Download: https://obsproject.com/download
  # Install and launch
  
  # Option 2: Windows Built-in
  # Windows 10/11: Press Win + G
  
  # Option 3: ScreenFlow (macOS)
  # Download from App Store
  ```

- [ ] **Configure Recording**
  - [ ] Choose recording location (e.g., `C:\Videos\`)
  - [ ] Set resolution: 1920x1080 or 1280x720
  - [ ] Set bitrate: 6000 Kbps
  - [ ] Enable audio input (microphone)
  - [ ] Test audio levels

- [ ] **Prepare Recording Environment**
  - [ ] Close unnecessary windows
  - [ ] Disable notifications
  - [ ] Zoom browser to 125% (for readability)
  - [ ] Have SYSTEM_OVERVIEW.md open for reference

- [ ] **Record Video (Follow Script)**
  
  Follow the script in `GITHUB_SETUP_AND_VIDEO_GUIDE.md`:
  
  1. Title slide (10s)
  2. Dashboard overview (30s)
  3. Action Tracker demo (20s)
  4. Governance Report demo (20s)
  5. Prompt Inspection demo (30s)
  6. Policy Manager demo (15s)
  7. AI Governance Dashboard demo (15s)
  8. Architecture explanation (30s)
  9. Key features (20s)
  10. Technical stack (15s)
  11. Use cases (20s)
  12. Closing slide (10s)
  
  **Total: 5-8 minutes**

- [ ] **Review Recording**
  - [ ] Audio is clear
  - [ ] Screen is readable
  - [ ] No long pauses
  - [ ] All pages shown
  - [ ] Threat detection demo works

### Phase 5: Post-Production (Optional, 15 minutes)

- [ ] **Edit Video (Optional)**
  - [ ] Add title/intro slide
  - [ ] Add background music (royalty-free)
  - [ ] Trim silence
  - [ ] Add captions
  - [ ] Export as MP4

- [ ] **Upload Recording**
  ```bash
  # Option 1: GitHub Releases
  # - Go to https://github.com/YOUR_USERNAME/agentguard/releases
  # - Click "Create a new release"
  # - Attach MP4 file
  
  # Option 2: YouTube
  # - Go to https://youtube.com/upload
  # - Upload MP4
  # - Title: "AgentGuard: AI Agent Governance Platform Demo"
  # - Description: [Full description from SYSTEM_OVERVIEW.md]
  # - Set to Unlisted or Public
  
  # Option 3: Loom
  # - Go to https://www.loom.com/
  # - Sign up (free or paid)
  # - Upload video
  ```

### Phase 6: Final GitHub Updates (5 minutes)

- [ ] **Create Release Notes**
  ```bash
  # In GitHub Releases section:
  - Title: "v1.0.0 - Initial Release"
  - Description: [Copy from SYSTEM_OVERVIEW.md Long Description]
  - Attach: Video MP4 file (if space allows)
  - Attach: Setup guide (QUICK_DEMO_GUIDE.md)
  ```

- [ ] **Update README Badges** (Optional)
  ```bash
  # In README.md, update badges with:
  # - Release version
  # - Stars count
  # - Download count
  ```

- [ ] **Add Demo Link to README**
  ```markdown
  ## 🎬 Demo Video
  
  [Watch Demo on YouTube](YOUR_VIDEO_LINK)
  
  or
  
  [Watch Demo on GitHub Releases](YOUR_GITHUB_RELEASE_LINK)
  ```

- [ ] **Push Updates**
  ```bash
  git add README.md
  git commit -m "Add demo video link"
  git push origin main
  ```

### Phase 7: Verify Final Setup (5 minutes)

- [ ] **GitHub Repository**
  - [ ] All code uploaded
  - [ ] README displays correctly
  - [ ] Links work
  - [ ] Demo video accessible

- [ ] **Documentation Complete**
  - [ ] SYSTEM_OVERVIEW.md present
  - [ ] QUICK_DEMO_GUIDE.md present
  - [ ] QUICK_START.md present
  - [ ] ENTERPRISE_DEPLOYMENT_GUIDE.md present
  - [ ] GITHUB_SETUP_AND_VIDEO_GUIDE.md present

- [ ] **App Working**
  - [ ] `streamlit run app.py` launches
  - [ ] All 5 pages load
  - [ ] Threat detection works
  - [ ] No errors in console

---

## Quick Reference Commands

```bash
# Clone repository locally
git clone https://github.com/YOUR_USERNAME/agentguard.git

# Make changes and push
git add .
git commit -m "Description of changes"
git push origin main

# Check status
git status

# View commit history
git log --oneline

# Revert last commit (if needed)
git reset --soft HEAD~1
```

---

## Submission Links to Share

Once complete, you can share:

**GitHub Repository**: 
```
https://github.com/YOUR_USERNAME/agentguard
```

**Demo Video**:
```
https://youtube.com/YOUR_VIDEO_ID
# or
https://github.com/YOUR_USERNAME/agentguard/releases/tag/v1.0.0
```

**Quick Start**:
```
1. Clone: git clone https://github.com/YOUR_USERNAME/agentguard.git
2. Install: pip install -r requirements.txt
3. Configure: cp .env.example .env  # Add API keys
4. Run: streamlit run app.py
```

---

## Submission Content Templates

### For Portfolio/LinkedIn

```
🛡️ AgentGuard: AI Agent Governance Platform

Solved the "actor attribution" problem for autonomous AI agents in enterprise systems.

Features:
✅ Multi-agent AI pipeline (Classifier → Monitor → Threat Detector → Explainer → Report)
✅ 7+ threat type detection (Prompt injection, data exfiltration, jailbreaks)
✅ Claude Haiku explanations & compliance reporting
✅ Real-time Jira integration with label-based governance tracking
✅ Streamlit dashboard (5 interactive pages)

Tech: Python 3.13 | Streamlit | Claude Haiku | Lobster Trap | Jira API

GitHub: https://github.com/YOUR_USERNAME/agentguard
Demo: [Your video link]
```

### For Hackathon/Competition

```
Project: AgentGuard - AI Agent Governance Platform
Track: Agent Security & AI Governance
Team: [Your name]
GitHub: https://github.com/YOUR_USERNAME/agentguard

Problem: When AI agents operate autonomously, all actions appear from system user with no governance visibility

Solution: Multi-agent pipeline with 6+ AI detection signals + 7+ threat types = Complete visibility

Innovation: Label-based governance tracking (no external database needed)

Results: 
- 85-100% AI action detection confidence
- 98%+ threat detection accuracy
- Production-ready enterprise platform

Video Demo: [Your video link]
```

---

## Troubleshooting

**Git push fails with authentication error**
```bash
# Generate personal access token:
# Settings → Developer settings → Personal access tokens
# Then use token as password when prompted
```

**Streamlit won't start**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version  # Should be 3.8+

# Try different port
streamlit run app.py --server.port 8502
```

**Claude API returns error**
```bash
# Verify API key
echo $CLAUDE_API_KEY

# Check quota in Anthropic console
# https://console.anthropic.com/account/usage
```

**Video won't upload to GitHub**
```bash
# File size limit: 2GB
# File format: MP4, AVI, MOV, etc.
# Use: GitHub Releases (not regular files)
```

---

## Success Indicators ✅

You're done when:

- [ ] Repository is public on GitHub
- [ ] All files uploaded without .env exposure
- [ ] README renders beautifully
- [ ] `streamlit run app.py` works perfectly
- [ ] Video demonstrates all 5 pages
- [ ] Documentation is complete
- [ ] Links are working
- [ ] You can share GitHub repo URL with confidence

---

## Estimated Total Time

| Phase | Time |
|-------|------|
| Repository Setup | 5 min |
| Push to GitHub | 10 min |
| Verification | 15 min |
| Video Recording | 45-60 min |
| Post-Production | 15 min |
| Final Updates | 5 min |
| **TOTAL** | **~2 hours** |

---

**You're now ready to showcase AgentGuard to the world! 🚀**
