import json
import re
from langchain_core.tools import tool

MITRE_MAPPING = {
    "phishing": {"id": "T1566", "name": "Phishing", "category": "Initial Access"},
    "spear phishing": {"id": "T1566.002", "name": "Spear Phishing", "category": "Initial Access"},
    "malware": {"id": "T1204", "name": "User Execution", "category": "Execution"},
    "ransomware": {"id": "T1486", "name": "Data Encrypted for Impact", "category": "Impact"},
    "injection": {"id": "T1190", "name": "Exploit Public-Facing Application", "category": "Initial Access"},
    "sql injection": {"id": "T1190", "name": "Exploit Public-Facing Application", "category": "Initial Access"},
    "xss": {"id": "T1598", "name": "Phishing for Information", "category": "Reconnaissance"},
    "privilege escalation": {"id": "T1548", "name": "Abuse Elevation Control Mechanism", "category": "Privilege Escalation"},
    "lateral movement": {"id": "T1570", "name": "Lateral Tool Transfer", "category": "Lateral Movement"},
    "credential dumping": {"id": "T1110", "name": "Brute Force", "category": "Credential Access"},
    "exfiltration": {"id": "T1041", "name": "Exfiltration Over C2 Channel", "category": "Exfiltration"},
    "data theft": {"id": "T1557", "name": "Man-in-the-Middle", "category": "Credential Access"},
    "dos": {"id": "T1498", "name": "Network Denial of Service", "category": "Impact"},
    "ddos": {"id": "T1498", "name": "Network Denial of Service", "category": "Impact"},
    "command and control": {"id": "T1071", "name": "Application Layer Protocol", "category": "Command and Control"},
    "persistence": {"id": "T1547", "name": "Boot or Logon Autostart Execution", "category": "Persistence"},
    "remote access": {"id": "T1021", "name": "Remote Services", "category": "Lateral Movement"},
    "backdoor": {"id": "T1547", "name": "Boot or Logon Autostart Execution", "category": "Persistence"},
    "privilege escalation": {"id": "T1548", "name": "Abuse Elevation Control Mechanism", "category": "Privilege Escalation"},
    "authentication bypass": {"id": "T1110", "name": "Brute Force", "category": "Credential Access"},
    "weak encryption": {"id": "T1621", "name": "Multi-Factor Authentication Interception", "category": "Credential Access"},
    "information disclosure": {"id": "T1526", "name": "Gather Victim Identity Information", "category": "Reconnaissance"},
    "buffer overflow": {"id": "T1190", "name": "Exploit Public-Facing Application", "category": "Initial Access"},
    "zero day": {"id": "T1190", "name": "Exploit Public-Facing Application", "category": "Initial Access"},
}


@tool
def mitre_mapper(threat_description: str) -> str:
    """
    Map security threats or CVEs to MITRE ATT&CK framework technique IDs.
    Use this when you want to connect threats to MITRE tactics and techniques.
    Input: Description of threat, CVE details, or attack method
    Returns: JSON with matched MITRE technique IDs, names, and categories
    """
    try:
        threat_lower = threat_description.lower()
        matched_techniques = []
        
        for keyword, technique in MITRE_MAPPING.items():
            if keyword in threat_lower:
                matched_techniques.append(technique)
        
        if not matched_techniques:
            matched_techniques = find_fuzzy_matches(threat_lower)
        
        if not matched_techniques:
            return json.dumps({
                "matches": [],
                "message": "No MITRE ATT&CK techniques matched. Try providing more specific threat details.",
                "techniques_found": 0
            })
        
        unique_techniques = []
        seen_ids = set()
        for tech in matched_techniques:
            if tech["id"] not in seen_ids:
                unique_techniques.append(tech)
                seen_ids.add(tech["id"])
        
        result = {
            "matches": unique_techniques,
            "techniques_found": len(unique_techniques),
            "message": f"Found {len(unique_techniques)} MITRE ATT&CK technique(s) related to this threat."
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "matches": [],
            "techniques_found": 0
        })


def find_fuzzy_matches(threat_lower: str) -> list:
    """Find techniques using fuzzy keyword matching."""
    matched = []
    keywords_to_check = ["attack", "threat", "vulnerability", "exploit", "breach"]
    
    for keyword in keywords_to_check:
        if keyword in threat_lower:
            for map_keyword, technique in MITRE_MAPPING.items():
                if len(map_keyword.split()) == 1 and map_keyword in threat_lower:
                    matched.append(technique)
    
    return matched
