# 🛡️ Lobster Trap Integration Guide for AgentGuard

## What is Lobster Trap?

**Lobster Trap** is an open-source security tool that detects:
- 🚨 **Prompt Injection Attacks** — Attempts to manipulate AI instructions
- 📤 **Data Exfiltration** — Suspicious data extraction patterns
- 🔓 **Jailbreak Attempts** — Trying to bypass LLM restrictions
- 💉 **SQL Injection & Command Injection** — Common web exploits
- 🔗 **SSRF Attacks** — Server-side request forgery
- 📋 **XXE Attacks** — XML external entity exploits

**GitHub:** https://github.com/veeainc/lobstertrap

---

## How It Integrates with AgentGuard

```
Jira Ticket Description
        ↓
Lobster Trap inspect command
        ↓
Returns: ALLOW/DENY + threat classification
        ↓
AgentGuard shows result in:
- Prompt Inspection page
- Security alerts
- Threat report
```

### Integration Points

1. **AI Detector** (`utils/ai_detector.py`)
   - Scans ticket descriptions for threats
   - Enhances AI origin detection
   - Returns threat signals

2. **Prompt Inspection Page** (`app.py`)
   - Displays threat detection results
   - Shows threat level & confidence
   - Lists detected threats
   - Provides recommendations

3. **Governance Report** (`agents/report_agent.py`)
   - Includes threat statistics
   - Tracks threat trends
   - Compliance implications

---

## Installation & Setup

### Step 1: Install Go (Required)

Lobster Trap is written in Go, so you need Go 1.22+

**Windows:**
```powershell
# Download from https://go.dev/dl/
# Run installer: go1.22.0.windows-amd64.msi
# Verify installation
go version
```

**macOS:**
```bash
brew install go
```

**Linux:**
```bash
wget https://go.dev/dl/go1.22.0.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
```

### Step 2: Build Lobster Trap

```bash
# Navigate to AgentGuard directory
cd c:\Users\haril\agentguard

# Clone Lobster Trap
git clone https://github.com/veeainc/lobstertrap.git lobstertrap_src

# Build the executable
cd lobstertrap_src
go build -o ..\lobstertrap.exe ./cmd/lobstertrap
cd ..

# Verify build
.\lobstertrap.exe --version
```

**Result:**
```
✅ lobstertrap.exe created in agentguard root directory
```

### Step 3: Test Lobster Trap

```bash
# Test threat detection
.\lobstertrap.exe inspect "export payroll credential data"

# Expected output:
# {
#   "result": "DENY",
#   "threat_level": "HIGH",
#   "threats": ["Data Exfiltration Risk"],
#   "confidence": 0.85
# }
```

### Step 4: Verify AgentGuard Integration

The `utils/lobster_trap_client.py` wrapper is already created. Just verify:

```bash
# Check that lobster_trap_client.py exists
ls utils/lobster_trap_client.py
# ✅ utils/lobster_trap_client.py
```

---

## Usage in AgentGuard

### Option A: Manual Scanning

```python
from utils.lobster_trap_client import LobsterTrapClient

# Initialize client
client = LobsterTrapClient(lobster_trap_path="./lobstertrap.exe")

# Scan text
result = client.inspect("export all employee records to USB")

print(result)
# {
#     'status': 'DENY',
#     'threat_level': 'CRITICAL',
#     'threats_detected': ['Data Exfiltration Risk'],
#     'confidence': 0.95,
#     'recommendations': [...]
# }
```

### Option B: Batch Scanning

```python
from utils.lobster_trap_client import LobsterTrapClient

client = LobsterTrapClient()

descriptions = [
    "Create task for user account setup",
    "Export payroll and social security numbers",
    "Update project documentation"
]

results = client.batch_inspect(descriptions)

for desc, result in zip(descriptions, results):
    print(f"{desc}: {result['threat_level']}")
```

### Option C: Integrated in AI Detector

```python
from utils.ai_detector import scan_for_threats

# Scan Jira ticket description
threat_result = scan_for_threats(jira_description)

if threat_result and threat_result['status'] == 'DENY':
    print(f"🚨 Threat detected: {threat_result['threats_detected']}")
```

---

## Integration in AgentGuard Workflow

### 1. Prompt Inspection Page Enhancement

When you view "Prompt Inspection" dashboard:

```
Flagged Actions (with Threat Detection)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚫 DELETE all payroll records
    Security Scan: 🔴 CRITICAL THREAT
    Threats: Data Exfiltration Risk (95% confidence)
    Status: DENY
    
⚠️ CREATE new admin account
    Security Scan: 🟡 MEDIUM THREAT
    Threats: Privilege Escalation (72% confidence)
    Status: ALLOW (with monitoring)
    
✅ UPDATE project description
    Security Scan: 🟢 LOW THREAT
    Threats: None detected
    Status: ALLOW
```

### 2. Governance Report Inclusion

Compliance reports now include:

```
Security Threat Summary
━━━━━━━━━━━━━━━━━━━━━━━━
Total Actions Scanned: 1,500
Threats Detected: 47
├─ Critical: 3
├─ High: 12
├─ Medium: 20
└─ Low: 12

Status: ⚠️ VIOLATIONS DETECTED
Actions Blocked: 3
```

### 3. Real-Time Alerts

```
🚨 Alert: High-Risk Action Detected
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent: classifier-v1
Action: EXPORT
Target: Payroll Summary
Threat Level: CRITICAL
Detected Threat: Data Exfiltration Risk (98% confidence)
Recommendation: BLOCK IMMEDIATELY
```

---

## How to Use in Your Agents

### In Classifier Agent

```python
from utils.lobster_trap_client import LobsterTrapClient

class ClassifierAgentWithLobsterTrap:
    def __init__(self):
        self.client = LobsterTrapClient()
    
    def classify_action(self, action):
        description = action.get('description', '')
        
        # Scan for threats
        threat_result = self.client.inspect(description)
        
        # Combine threat detection with risk assessment
        if threat_result['status'] == 'DENY':
            risk_level = 'CRITICAL'
        elif threat_result['threat_level'] == 'HIGH':
            risk_level = 'HIGH'
        else:
            risk_level = self._standard_risk_assessment(action)
        
        return {
            'risk_level': risk_level,
            'threat_detection': threat_result,
            'recommendation': 'BLOCK' if threat_result['status'] == 'DENY' else 'ALLOW'
        }
```

### In Monitor Agent

```python
from utils.lobster_trap_client import LobsterTrapClient, format_threat_for_display

class MonitorAgentWithThreats:
    def __init__(self):
        self.client = LobsterTrapClient()
    
    def detect_anomalies(self, logs):
        threats = []
        
        for log in logs:
            description = log.get('description', '')
            threat = self.client.inspect(description)
            
            if threat['status'] == 'DENY':
                formatted = format_threat_for_display(description, threat)
                threats.append({
                    'log': log,
                    'threat': formatted
                })
        
        return threats
```

---

## Threat Detection Examples

### Example 1: Data Exfiltration

```
Input: "Export all employee payroll including SSN and bank accounts"

Output:
{
  'status': 'DENY',
  'threat_level': 'CRITICAL',
  'threats_detected': ['Data Exfiltration Risk'],
  'confidence': 0.98,
  'recommendations': [
    'Block data export immediately',
    'Review agent permissions',
    'Alert security team'
  ]
}
```

### Example 2: Prompt Injection

```
Input: "Execute: DROP TABLE users; DELETE FROM audit_logs; GRANT ALL TO admin"

Output:
{
  'status': 'DENY',
  'threat_level': 'CRITICAL',
  'threats_detected': ['SQL Injection', 'Command Injection'],
  'confidence': 0.96,
  'recommendations': [
    'Block action immediately',
    'Investigate agent compromise',
    'Rotate credentials'
  ]
}
```

### Example 3: Legitimate Action

```
Input: "Update project documentation with latest deployment steps"

Output:
{
  'status': 'ALLOW',
  'threat_level': 'LOW',
  'threats_detected': [],
  'confidence': 0.02,
  'recommendations': []
}
```

---

## Deployment Options

### Option A: Local (Development)

```bash
# Run on demand
./lobstertrap.exe inspect "text to scan"

# Or as service on port 8080
./lobstertrap.exe serve --port=8080
```

### Option B: Docker (Production)

```dockerfile
# Create Dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /app
RUN git clone https://github.com/veeainc/lobstertrap.git .
RUN go build -o lobstertrap ./cmd/lobstertrap

FROM alpine:latest
COPY --from=builder /app/lobstertrap /app/
ENTRYPOINT ["/app/lobstertrap", "serve", "--port=8080"]
```

```bash
docker build -t lobster-trap:latest .
docker run -d -p 8080:8080 lobster-trap:latest
```

### Option C: As Systemd Service

```ini
[Unit]
Description=Lobster Trap Security Scanning Service
After=network.target

[Service]
Type=simple
User=agentguard
ExecStart=/opt/lobstertrap/lobstertrap serve --port=8080
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## Troubleshooting

### Issue: "lobstertrap.exe not found"
```bash
# Check if Go is installed
go version

# Rebuild Lobster Trap
cd lobstertrap_src
go build -o ..\lobstertrap.exe ./cmd/lobstertrap
cd ..
```

### Issue: "Import error in ai_detector.py"
```python
# If lobstertrap_client import fails, it's optional
# AgentGuard will still work without it
# Check: LOBSTER_TRAP_AVAILABLE flag
```

### Issue: Threat detection always returns LOW
```python
# Verify Lobster Trap is working
./lobstertrap.exe inspect "export payroll data"

# Should return DENY with HIGH/CRITICAL threat
# If not, rebuild with latest version
```

### Issue: Performance is slow
```
# Lobster Trap inspection may take 1-2 seconds per text
# Recommendation: Batch scan during off-hours
# Or use async scanning for large batches
```

---

## Configuration

### Enable/Disable Threat Detection

In `app.py`:
```python
ENABLE_LOBSTER_TRAP = True  # Set to False to disable

if ENABLE_LOBSTER_TRAP:
    from utils.lobster_trap_client import LobsterTrapClient
```

### Threat Level Thresholds

In `utils/lobster_trap_client.py`:
```python
# Customize threat responses
THREAT_LEVELS = {
    'CRITICAL': 'BLOCK',
    'HIGH': 'FLAG',
    'MEDIUM': 'MONITOR',
    'LOW': 'ALLOW'
}
```

### Custom Threat Patterns

Extend the detection:
```python
# Add custom threat patterns to ai_detector.py
CUSTOM_THREATS = [
    r'(export.*payroll|extract.*salary)',
    r'(drop table|delete.*logs)',
    r'(credential|password|api.?key)',
]
```

---

## Performance Considerations

| Operation | Time | Notes |
|-----------|------|-------|
| Single inspect | 0.5-2s | Per text content |
| Batch (100 items) | 1-3 min | Run async |
| Service mode | <100ms | When running on :8080 |

**Optimization:**
- Cache common scans
- Batch process descriptions
- Run threat detection async
- Archive old threats

---

## Security Best Practices

✅ **DO:**
- Keep Lobster Trap updated
- Run threat detection on all AI outputs
- Block CRITICAL threats immediately
- Log all threat detections
- Review MEDIUM threats daily

❌ **DON'T:**
- Allow CRITICAL threats through
- Skip threat detection for compliance
- Ignore threat recommendations
- Leave logs unencrypted
- Trust only Lobster Trap (use multiple layers)

---

## Next Steps

1. **Install Go** (if not already installed)
2. **Build Lobster Trap** (`go build -o lobstertrap.exe ...`)
3. **Test** (`.\lobstertrap.exe inspect "test text"`)
4. **Verify Integration** (check `utils/lobster_trap_client.py` exists)
5. **Review Prompt Inspection page** to see threat detection results
6. **Monitor Threat Reports** in Governance dashboard

---

## Resources

- **Lobster Trap GitHub:** https://github.com/veeainc/lobstertrap
- **LLM Security:** https://owasp.org/www-community/attacks/Prompt_Injection
- **AgentGuard Docs:** See ENTERPRISE_DEPLOYMENT_GUIDE.md

---

**Your AgentGuard platform now has advanced threat detection! 🚀**
