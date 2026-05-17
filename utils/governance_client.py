"""
AgentGuard Enterprise Governance Module
Centralized AI Agent Activity Tracking & Compliance
"""
import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import json

load_dotenv()

class JiraGovernanceClient:
    """Enterprise-grade Jira governance client for AI agent tracking"""
    
    def __init__(self):
        self.jira_url = os.getenv('JIRA_URL')
        self.jira_email = os.getenv('JIRA_EMAIL')
        self.jira_token = os.getenv('JIRA_API_TOKEN')
        self.auth = HTTPBasicAuth(self.jira_email, self.jira_token)
        self.headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    
    def create_ai_tracked_issue(self, summary, description, agent_name, risk_level="Medium", 
                                issue_type="Task", priority="High"):
        """
        Create a Jira issue with AI governance tracking
        
        Args:
            summary: Issue title
            description: Issue description
            agent_name: Name of AI agent creating issue
            risk_level: Risk level (Low, Medium, High)
            issue_type: Jira issue type
            priority: Issue priority
            
        Returns:
            Ticket key or None
        """
        
        # Get project
        projects_url = f'{self.jira_url}/rest/api/3/project'
        proj_response = requests.get(projects_url, auth=self.auth, headers=self.headers)
        
        if proj_response.status_code != 200:
            return None
        
        projects = proj_response.json()
        if not projects:
            return None
        
        project_key = projects[0]['key']
        
        # Build issue with AI metadata
        issue_data = {
            'fields': {
                'project': {'key': project_key},
                'summary': f'[AI-GENERATED] {summary}',
                'description': {
                    'type': 'doc',
                    'version': 1,
                    'content': [
                        {
                            'type': 'paragraph',
                            'content': [
                                {'type': 'text', 'text': '🤖 AI AGENT GENERATED TICKET\n\n'},
                                {'type': 'text', 'text': 'Agent: ', 'marks': [{'type': 'strong'}]},
                                {'type': 'text', 'text': f'{agent_name}\n'},
                                {'type': 'text', 'text': 'Risk Level: ', 'marks': [{'type': 'strong'}]},
                                {'type': 'text', 'text': f'{risk_level}\n'},
                                {'type': 'text', 'text': 'Governance: ', 'marks': [{'type': 'strong'}]},
                                {'type': 'text', 'text': 'Review Required\n\n'},
                                {'type': 'text', 'text': description}
                            ]
                        }
                    ]
                },
                'issuetype': {'name': issue_type},
                'priority': {'name': priority},
                'labels': [
                    'ai-generated',
                    f'agent:{agent_name}',
                    f'risk:{risk_level.lower()}',
                    'governance-review'
                ]
            }
        }
        
        # Create issue
        issue_url = f'{self.jira_url}/rest/api/3/issue'
        response = requests.post(issue_url, json=issue_data, auth=self.auth, headers=self.headers)
        
        if response.status_code == 201:
            ticket = response.json()
            return ticket['key']
        
        return None
    
    def get_ai_generated_issues(self, max_results=50):
        """Get all AI-generated issues"""
        
        r = requests.get(
            f'{self.jira_url}/rest/api/3/search/jql',
            headers=self.headers,
            auth=self.auth,
            params={
                'jql': 'labels in (ai-generated) ORDER BY created DESC',
                'maxResults': max_results,
                'fields': 'summary,labels,created,updated,creator,priority,status'
            }
        )
        
        if r.status_code != 200:
            return []
        
        return r.json().get('issues', [])
    
    def get_high_risk_actions(self, max_results=50):
        """Get high-risk AI actions"""
        
        r = requests.get(
            f'{self.jira_url}/rest/api/3/search/jql',
            headers=self.headers,
            auth=self.auth,
            params={
                'jql': 'labels in (ai-generated) AND labels in (risk:high) ORDER BY created DESC',
                'maxResults': max_results,
                'fields': 'summary,labels,created,priority'
            }
        )
        
        if r.status_code != 200:
            return []
        
        return r.json().get('issues', [])
    
    def get_issues_by_agent(self, agent_name, max_results=50):
        """Get all issues created by specific agent"""
        
        r = requests.get(
            f'{self.jira_url}/rest/api/3/search/jql',
            headers=self.headers,
            auth=self.auth,
            params={
                'jql': f'labels in (agent:{agent_name}) ORDER BY created DESC',
                'maxResults': max_results,
                'fields': 'summary,labels,created,updated'
            }
        )
        
        if r.status_code != 200:
            return []
        
        return r.json().get('issues', [])
    
    def get_governance_metrics(self):
        """Get AI governance metrics"""
        
        # Total AI actions
        r_ai = requests.get(
            f'{self.jira_url}/rest/api/3/search/jql',
            headers=self.headers,
            auth=self.auth,
            params={'jql': 'labels in (ai-generated)', 'maxResults': 1}
        )
        
        # High-risk actions
        r_high = requests.get(
            f'{self.jira_url}/rest/api/3/search/jql',
            headers=self.headers,
            auth=self.auth,
            params={'jql': 'labels in (ai-generated) AND labels in (risk:high)', 'maxResults': 1}
        )
        
        # Pending review
        r_review = requests.get(
            f'{self.jira_url}/rest/api/3/search/jql',
            headers=self.headers,
            auth=self.auth,
            params={'jql': 'labels in (governance-review)', 'maxResults': 1}
        )
        
        return {
            'total_ai_actions': r_ai.json().get('total', 0) if r_ai.status_code == 200 else 0,
            'high_risk_actions': r_high.json().get('total', 0) if r_high.status_code == 200 else 0,
            'pending_review': r_review.json().get('total', 0) if r_review.status_code == 200 else 0,
            'timestamp': datetime.now().isoformat()
        }


def format_issue_for_display(issue):
    """Format issue for Streamlit display"""
    key = issue.get('key', 'N/A')
    summary = issue['fields'].get('summary', 'N/A')
    labels = issue['fields'].get('labels', [])
    created = issue['fields'].get('created', 'N/A')
    priority = issue['fields']['priority'].get('name', 'N/A') if issue['fields'].get('priority') else 'N/A'
    
    # Extract agent name
    agent = 'Unknown'
    for label in labels:
        if label.startswith('agent:'):
            agent = label.replace('agent:', '')
            break
    
    # Extract risk
    risk = 'Unknown'
    for label in labels:
        if label.startswith('risk:'):
            risk = label.replace('risk:', '').upper()
            break
    
    return {
        'key': key,
        'summary': summary,
        'agent': agent,
        'risk': risk,
        'created': created[:10],
        'priority': priority
    }


def get_risk_color(risk_level):
    """Get color for risk level"""
    risk_map = {
        'HIGH': '🔴',
        'MEDIUM': '🟡',
        'LOW': '🟢'
    }
    return risk_map.get(risk_level, '⚪')
