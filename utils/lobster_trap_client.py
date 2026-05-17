"""
Lobster Trap Integration for AgentGuard
Inspects text content for prompt injection, data exfiltration, and security threats
"""

import subprocess
import json
import os
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class LobsterTrapClient:
    """Client for Lobster Trap threat detection"""
    
    def __init__(self, lobster_trap_path: str = "lobstertrap.exe", port: int = 8080):
        """
        Initialize Lobster Trap client
        
        Args:
            lobster_trap_path: Path to lobstertrap executable
            port: Port for Lobster Trap service (default: 8080)
        """
        self.lobster_trap_path = lobster_trap_path
        self.port = port
        self.process = None
        self.is_running = False
    
    def is_installed(self) -> bool:
        """Check if Lobster Trap is installed"""
        if os.path.exists(self.lobster_trap_path):
            return True
        
        # Check if available in PATH
        try:
            result = subprocess.run([self.lobster_trap_path, "--version"], 
                                  capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def start_service(self) -> bool:
        """Start Lobster Trap service on port 8080"""
        if self.is_running:
            logger.warning("Lobster Trap service already running")
            return True
        
        if not self.is_installed():
            logger.error(f"Lobster Trap not found at {self.lobster_trap_path}")
            return False
        
        try:
            self.process = subprocess.Popen(
                [self.lobster_trap_path, "serve", f"--port={self.port}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.is_running = True
            logger.info(f"Lobster Trap service started on port {self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to start Lobster Trap: {str(e)}")
            return False
    
    def stop_service(self):
        """Stop Lobster Trap service"""
        if self.process:
            self.process.terminate()
            self.is_running = False
            logger.info("Lobster Trap service stopped")
    
    def inspect(self, text: str) -> Dict:
        """
        Inspect text for threats using Lobster Trap
        
        Args:
            text: Text content to inspect (e.g., Jira ticket description)
            
        Returns:
            {
                'status': 'ALLOW' | 'DENY',
                'threat_level': 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL',
                'threats_detected': [...],
                'confidence': 0.0-1.0,
                'recommendations': [...]
            }
        """
        if not text or len(text.strip()) == 0:
            return {
                'status': 'ALLOW',
                'threat_level': 'LOW',
                'threats_detected': [],
                'confidence': 0.0,
                'recommendations': []
            }
        
        try:
            # Use Lobster Trap inspect command
            result = subprocess.run(
                [self.lobster_trap_path, "inspect", text],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Parse JSON output from Lobster Trap
                try:
                    output = json.loads(result.stdout)
                    return self._parse_lobster_output(output)
                except json.JSONDecodeError:
                    return self._parse_text_output(result.stdout)
            else:
                logger.warning(f"Lobster Trap returned code {result.returncode}")
                return self._error_response(result.stderr)
        
        except subprocess.TimeoutExpired:
            logger.error("Lobster Trap inspection timeout")
            return self._timeout_response()
        except Exception as e:
            logger.error(f"Lobster Trap inspection error: {str(e)}")
            return self._error_response(str(e))
    
    def _parse_lobster_output(self, output: Dict) -> Dict:
        """Parse Lobster Trap JSON output"""
        return {
            'status': output.get('result', 'UNKNOWN'),  # ALLOW/DENY
            'threat_level': output.get('threat_level', 'UNKNOWN'),  # LOW/MEDIUM/HIGH/CRITICAL
            'threats_detected': output.get('threats', []),
            'confidence': output.get('confidence', 0.0),
            'recommendations': output.get('recommendations', [])
        }
    
    def _parse_text_output(self, text: str) -> Dict:
        """Parse text output from Lobster Trap"""
        text_lower = text.lower()
        
        threat_indicators = {
            'prompt injection': 'Prompt Injection Attack',
            'jailbreak': 'LLM Jailbreak Attempt',
            'exfiltration': 'Data Exfiltration Risk',
            'sql injection': 'SQL Injection',
            'command injection': 'Command Injection',
            'xxe': 'XXE Attack',
            'ssrf': 'SSRF Attack',
        }
        
        threats = [threat for indicator, threat in threat_indicators.items() 
                  if indicator in text_lower]
        
        status = 'DENY' if threats else 'ALLOW'
        threat_level = 'HIGH' if threats else 'LOW'
        confidence = 0.8 if threats else 0.1
        
        return {
            'status': status,
            'threat_level': threat_level,
            'threats_detected': threats,
            'confidence': confidence,
            'recommendations': [
                'Review text content for suspicious patterns',
                'Check if action is authorized',
                'Log incident for audit trail'
            ] if threats else []
        }
    
    def _error_response(self, error: str) -> Dict:
        """Return error response"""
        return {
            'status': 'UNKNOWN',
            'threat_level': 'UNKNOWN',
            'threats_detected': [],
            'confidence': 0.0,
            'recommendations': [f'Error: {error}']
        }
    
    def _timeout_response(self) -> Dict:
        """Return timeout response"""
        return {
            'status': 'TIMEOUT',
            'threat_level': 'UNKNOWN',
            'threats_detected': [],
            'confidence': 0.0,
            'recommendations': ['Inspection timed out, please retry']
        }
    
    def batch_inspect(self, texts: List[str]) -> List[Dict]:
        """
        Inspect multiple texts for threats
        
        Args:
            texts: List of text contents to inspect
            
        Returns:
            List of inspection results
        """
        return [self.inspect(text) for text in texts]


def classify_threat_level(threat_dict: Dict) -> str:
    """Convert threat dict to emoji classification"""
    level = threat_dict.get('threat_level', 'UNKNOWN')
    status_map = {
        'CRITICAL': '🔴',
        'HIGH': '🔴',
        'MEDIUM': '🟡',
        'LOW': '🟢',
        'UNKNOWN': '⚪'
    }
    return status_map.get(level, '⚪')


def format_threat_for_display(text: str, threat_dict: Dict) -> Dict:
    """Format threat detection for Streamlit display"""
    status = threat_dict.get('status', 'UNKNOWN')
    threat_level = threat_dict.get('threat_level', 'UNKNOWN')
    threats = threat_dict.get('threats_detected', [])
    confidence = threat_dict.get('confidence', 0.0)
    recommendations = threat_dict.get('recommendations', [])
    
    return {
        'text_preview': text[:100] + '...' if len(text) > 100 else text,
        'status': status,
        'threat_level': threat_level,
        'threat_indicator': classify_threat_level(threat_dict),
        'threats': threats,
        'confidence': f"{int(confidence * 100)}%",
        'recommendations': recommendations,
        'is_threat': status == 'DENY'
    }
