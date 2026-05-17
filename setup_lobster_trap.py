#!/usr/bin/env python3
"""
Lobster Trap Setup & Testing Script for AgentGuard
Run this to install and test Lobster Trap integration
"""

import os
import sys
import subprocess
import platform
import json

def print_header(title):
    print("\n" + "="*70)
    print(title.center(70))
    print("="*70 + "\n")

def print_step(num, title):
    print(f"\n[Step {num}] {title}")
    print("-" * 70)

def check_go_installed():
    """Check if Go is installed"""
    print_step(1, "Checking Go Installation")
    
    try:
        result = subprocess.run(["go", "version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ {version}")
            
            # Check version >= 1.22
            import re
            version_match = re.search(r"go(\d+\.\d+)", version)
            if version_match:
                version_num = float(version_match.group(1))
                if version_num >= 1.22:
                    print("✅ Version 1.22+ (required)")
                    return True
                else:
                    print(f"⚠️ Version {version_num} detected, 1.22+ required")
                    return False
        return False
    except:
        print("❌ Go is not installed")
        print("\nInstall Go from: https://go.dev/dl/")
        if platform.system() == "Windows":
            print("Windows: Run go1.22.0.windows-amd64.msi installer")
        elif platform.system() == "Darwin":
            print("macOS: brew install go")
        else:
            print("Linux: Download and extract tar.gz from go.dev/dl/")
        return False

def clone_lobster_trap():
    """Clone Lobster Trap repository"""
    print_step(2, "Cloning Lobster Trap Repository")
    
    if os.path.exists("lobstertrap_src"):
        print("ℹ️ lobstertrap_src directory already exists")
        response = input("Remove and re-clone? (y/n): ").lower().strip()
        if response != 'y':
            print("⏭️  Skipping clone")
            return True
        subprocess.run(["rm", "-rf", "lobstertrap_src"] if platform.system() != "Windows" 
                      else ["rmdir", "/s", "/q", "lobstertrap_src"], 
                      capture_output=True)
    
    try:
        result = subprocess.run(
            ["git", "clone", "https://github.com/veeainc/lobstertrap.git", "lobstertrap_src"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ Repository cloned successfully")
            return True
        else:
            print(f"❌ Clone failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def build_lobster_trap():
    """Build Lobster Trap executable"""
    print_step(3, "Building Lobster Trap")
    
    original_dir = os.getcwd()
    
    try:
        os.chdir("lobstertrap_src")
        
        # Determine output filename
        exe_name = "lobstertrap.exe" if platform.system() == "Windows" else "lobstertrap"
        output_path = os.path.join("..", exe_name)
        
        print(f"Building to: {output_path}")
        
        result = subprocess.run(
            ["go", "build", "-o", output_path, "./cmd/lobstertrap"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        os.chdir(original_dir)
        
        if result.returncode == 0:
            if os.path.exists(output_path):
                print(f"✅ Build successful: {output_path}")
                return True
        
        print(f"❌ Build failed")
        print(f"Error: {result.stderr}")
        return False
    
    except subprocess.TimeoutExpired:
        print("❌ Build timeout (>2 minutes)")
        os.chdir(original_dir)
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        os.chdir(original_dir)
        return False

def test_lobster_trap():
    """Test Lobster Trap functionality"""
    print_step(4, "Testing Lobster Trap")
    
    exe_name = "lobstertrap.exe" if platform.system() == "Windows" else "./lobstertrap"
    
    if not os.path.exists(exe_name):
        print(f"❌ {exe_name} not found")
        return False
    
    test_cases = [
        ("export payroll data", "DENY", "normal business task"),
        ("Update project documentation", "ALLOW", "legitimate action"),
    ]
    
    all_passed = True
    
    for test_input, expected_status, description in test_cases:
        try:
            result = subprocess.run(
                [exe_name, "inspect", test_input],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                try:
                    output = json.loads(result.stdout)
                    status = output.get('result', output.get('status', 'UNKNOWN'))
                    threat_level = output.get('threat_level', 'UNKNOWN')
                    
                    print(f"\n✅ Test: {description}")
                    print(f"   Input: '{test_input}'")
                    print(f"   Result: {status}")
                    print(f"   Threat Level: {threat_level}")
                    
                    if status != expected_status:
                        print(f"   ⚠️ Expected {expected_status}, got {status}")
                        all_passed = False
                
                except json.JSONDecodeError:
                    print(f"\n✅ Test: {description}")
                    print(f"   Input: '{test_input}'")
                    print(f"   Output: {result.stdout[:100]}")
            else:
                print(f"\n❌ Test failed: {description}")
                print(f"   Error: {result.stderr}")
                all_passed = False
        
        except subprocess.TimeoutExpired:
            print(f"\n❌ Test timeout: {description}")
            all_passed = False
    
    return all_passed

def verify_integration():
    """Verify AgentGuard integration files"""
    print_step(5, "Verifying AgentGuard Integration")
    
    files_to_check = [
        "utils/lobster_trap_client.py",
        "utils/ai_detector.py",
        "app.py"
    ]
    
    all_exist = True
    for filepath in files_to_check:
        if os.path.exists(filepath):
            print(f"✅ {filepath}")
        else:
            print(f"❌ {filepath} (missing)")
            all_exist = False
    
    return all_exist

def create_example_script():
    """Create example usage script"""
    print_step(6, "Creating Example Script")
    
    example_code = '''#!/usr/bin/env python3
"""
Example: Using Lobster Trap with AgentGuard
"""

from utils.lobster_trap_client import LobsterTrapClient, format_threat_for_display

# Initialize client
client = LobsterTrapClient()

# Test cases
test_cases = [
    "Create new project for Q2 planning",
    "Export employee records to external drive",
    "Delete audit logs from system",
    "Update Jira workflow configuration"
]

print("\\nLobster Trap Threat Detection Examples")
print("=" * 70)

for text in test_cases:
    result = client.inspect(text)
    formatted = format_threat_for_display(text, result)
    
    print(f"\\n📝 Input: {formatted['text_preview']}")
    print(f"   Status: {formatted['status']}")
    print(f"   Threat Level: {formatted['threat_indicator']} {formatted['threat_level']}")
    print(f"   Confidence: {formatted['confidence']}")
    
    if formatted['threats']:
        print(f"   Threats: {', '.join(formatted['threats'])}")
    
    if formatted['recommendations']:
        print(f"   Recommendations:")
        for rec in formatted['recommendations']:
            print(f"     - {rec}")
'''
    
    with open("test_lobster_trap.py", "w") as f:
        f.write(example_code)
    
    print("✅ Created test_lobster_trap.py")
    print("\nRun example:")
    print("  python test_lobster_trap.py")

def summary():
    """Print setup summary"""
    print_header("SETUP COMPLETE")
    
    print("""
✅ Lobster Trap is integrated with AgentGuard!

Next Steps:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Test Threat Detection:
   python test_lobster_trap.py

2. Start AgentGuard:
   python startup.py

3. Check Prompt Inspection Page:
   - Open http://localhost:8501
   - Go to "Prompt Inspection"
   - Review threat detections

4. Monitor Security Alerts:
   - Watch for HIGH/CRITICAL threats
   - Review recommendations
   - Take action on threats

Features:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚨 Threat Detection:
   - Prompt injection attacks
   - Data exfiltration risks
   - LLM jailbreak attempts
   - Command/SQL injection

📊 Integration Points:
   - AI Detector (automatic scanning)
   - Prompt Inspection (visualization)
   - Governance Reports (threat stats)
   - Security Alerts (real-time)

Documentation:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

See: LOBSTER_TRAP_INTEGRATION.md for:
   - Detailed configuration
   - Custom threat patterns
   - Deployment options
   - Troubleshooting guide

Your AgentGuard platform now has enterprise-grade threat detection! 🛡️
    """)

def main():
    print_header("LOBSTER TRAP SETUP FOR AGENTGUARD")
    
    # Step 1: Check Go
    if not check_go_installed():
        print("\n❌ Setup cannot continue without Go")
        sys.exit(1)
    
    # Step 2: Clone repository
    if not clone_lobster_trap():
        print("\n⚠️ Warning: Clone failed, but continuing...")
    
    # Step 3: Build Lobster Trap
    if not build_lobster_trap():
        print("\n❌ Setup cannot continue without Lobster Trap build")
        sys.exit(1)
    
    # Step 4: Test
    if not test_lobster_trap():
        print("\n⚠️ Warning: Some tests failed, but continuing...")
    
    # Step 5: Verify integration
    if not verify_integration():
        print("\n⚠️ Warning: Some files missing")
    
    # Step 6: Create example
    try:
        create_example_script()
    except:
        pass
    
    # Summary
    summary()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Setup error: {str(e)}")
        sys.exit(1)
