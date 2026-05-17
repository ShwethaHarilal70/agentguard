#!/usr/bin/env python3
"""
AgentGuard Enterprise Startup Script
Verifies configuration and runs pre-flight checks before starting the application
"""

import os
import sys
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

def print_header(title):
    print("\n" + "="*70)
    print(title.center(70))
    print("="*70 + "\n")

def print_step(step_num, description):
    print(f"\n[Step {step_num}] {description}")
    print("-" * 70)

def check_python_version():
    """Check Python version"""
    print_step(1, "Checking Python Version")
    version = sys.version_info
    required = (3, 8)
    
    if version >= required:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} (required >= 3.8)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} (required >= 3.8)")
        return False

def check_dependencies():
    """Check required packages"""
    print_step(2, "Checking Dependencies")
    
    required_packages = [
        'streamlit',
        'requests',
        'dotenv',
        'anthropic'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} — NOT INSTALLED")
            all_installed = False
    
    if not all_installed:
        print("\n⚠️  Missing packages detected!")
        print("Install with: pip install -r requirements.txt")
    
    return all_installed

def check_env_file():
    """Check .env file"""
    print_step(3, "Checking Configuration (.env file)")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        print("   Create one with: cp .env.example .env")
        return False
    
    print("✅ .env file found")
    
    load_dotenv()
    
    required_vars = [
        'CLAUDE_API_KEY',
        'JIRA_URL',
        'JIRA_EMAIL',
        'JIRA_API_TOKEN'
    ]
    
    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            masked = value[:10] + "..." if len(value) > 10 else "***"
            print(f"✅ {var} = {masked}")
        else:
            print(f"❌ {var} = (not set)")
            all_set = False
    
    return all_set

def test_jira_connection():
    """Test Jira API connection"""
    print_step(4, "Testing Jira Connection")
    
    load_dotenv()
    
    jira_url = os.getenv('JIRA_URL')
    jira_email = os.getenv('JIRA_EMAIL')
    jira_token = os.getenv('JIRA_API_TOKEN')
    
    if not all([jira_url, jira_email, jira_token]):
        print("⚠️  Skipping (credentials not set)")
        return False
    
    try:
        auth = HTTPBasicAuth(jira_email, jira_token)
        
        # Test basic connection
        response = requests.get(
            f'{jira_url}/rest/api/3/myself',
            auth=auth,
            timeout=5
        )
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ Connected to Jira")
            print(f"   Account: {user_info.get('displayName', 'Unknown')}")
            
            # Get projects
            proj_response = requests.get(
                f'{jira_url}/rest/api/3/project',
                auth=auth,
                timeout=5
            )
            
            if proj_response.status_code == 200:
                projects = proj_response.json()
                print(f"✅ Found {len(projects)} project(s)")
                for p in projects[:3]:
                    print(f"   - {p['key']}: {p['name']}")
                if len(projects) > 3:
                    print(f"   ... and {len(projects) - 3} more")
            
            return True
        else:
            print(f"❌ Jira authentication failed: {response.status_code}")
            return False
    
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to {jira_url}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_claude_api():
    """Test Claude API"""
    print_step(5, "Testing Claude Haiku API")
    
    load_dotenv()
    
    api_key = os.getenv('CLAUDE_API_KEY')
    
    if not api_key:
        print("⚠️  Skipping (API key not set)")
        return False
    
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        
        # Test with a simple prompt
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=100,
            messages=[{"role": "user", "content": "Say 'Hello from AgentGuard'"}]
        )
        
        response_text = message.content[0].text if message.content else ""
        if response_text:
            print(f"✅ Claude Haiku API working")
            print(f"   Response: {response_text[:50]}...")
            return True
        else:
            print("❌ Claude API returned empty response")
            return False
    
    except Exception as e:
        print(f"❌ Claude API error: {str(e)}")
        return False

def check_file_structure():
    """Check required files"""
    print_step(6, "Checking File Structure")
    
    required_files = [
        'app.py',
        'requirements.txt',
        '.env',
        'agents/__init__.py',
        'agents/classifier_agent.py',
        'agents/monitor_agent.py',
        'agents/explainer_agent.py',
        'agents/report_agent.py',
        'utils/__init__.py',
        'utils/policy_engine.py',
        'utils/ai_detector.py',
        'utils/governance_client.py'
    ]
    
    all_exist = True
    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"✅ {filepath}")
        else:
            print(f"❌ {filepath}")
            all_exist = False
    
    return all_exist

def summary_and_start():
    """Summary and option to start app"""
    print_header("PRE-FLIGHT CHECK SUMMARY")
    
    checks = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'Configuration (.env)': check_env_file(),
        'File Structure': check_file_structure(),
        'Jira Connection': test_jira_connection(),
        'Claude Haiku API': test_claude_api()
    }
    
    print("\n" + "-"*70)
    for check, status in checks.items():
        emoji = "✅" if status else "⚠️ "
        print(f"{emoji} {check}")
    
    print("\n" + "="*70)
    
    critical_checks = [
        'Python Version',
        'Dependencies',
        'Configuration (.env)',
        'File Structure'
    ]
    
    all_critical_pass = all(checks.get(c) for c in critical_checks)
    
    if all_critical_pass:
        print("✅ All critical checks passed!")
        print("\n🚀 Ready to start AgentGuard")
        print("\nStarting application in 3 seconds...")
        
        import time
        for i in range(3, 0, -1):
            print(f"   {i}...", end='\r')
            time.sleep(1)
        
        print("\n" + "="*70)
        print("Starting Streamlit Application...")
        print("Open browser to: http://localhost:8501")
        print("="*70 + "\n")
        
        # Start Streamlit
        os.system('streamlit run app.py')
    
    else:
        print("❌ Some critical checks failed!")
        print("\nPlease fix the issues above before starting the application:")
        print("1. Check Python version >= 3.8")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Configure .env file with credentials")
        print("4. Ensure all required files exist")
        
        response = input("\nTry to start anyway? (y/n): ").lower().strip()
        if response == 'y':
            print("\nStarting application...")
            os.system('streamlit run app.py')
        else:
            print("Startup cancelled.")
            sys.exit(1)

if __name__ == "__main__":
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + "AGENTGUARD — ENTERPRISE STARTUP".center(68) + "║")
    print("║" + "AI Agent Governance Platform".center(68) + "║")
    print("╚" + "="*68 + "╝")
    
    try:
        summary_and_start()
    except KeyboardInterrupt:
        print("\n\nStartup cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Startup error: {str(e)}")
        sys.exit(1)
