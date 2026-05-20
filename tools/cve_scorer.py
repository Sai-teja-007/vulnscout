import json
import re
from langchain_core.tools import tool


def extract_cvss_score(text: str) -> float:
    """Extract CVSS score from text using regex."""
    patterns = [
        r'CVSS[:\s]+([0-9]+\.?[0-9]*)',
        r'CVSS\s+v?3\.?\d*:\s+([0-9]+\.?[0-9]*)',
        r'Base\s+Score:\s+([0-9]+\.?[0-9]*)',
        r'([0-9]+\.?[0-9]*)\s*\/\s*10\.0',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                score = float(match.group(1))
                return min(10.0, max(0.0, score))
            except ValueError:
                continue
    
    return None


def score_to_severity(score: float) -> dict:
    """Convert CVSS score to severity level."""
    if score is None:
        return {
            "score": None,
            "severity": "UNKNOWN",
            "color": "#gray"
        }
    
    if score < 4.0:
        return {
            "score": score,
            "severity": "LOW",
            "color": "#28a745"
        }
    elif score < 7.0:
        return {
            "score": score,
            "severity": "MEDIUM",
            "color": "#ffc107"
        }
    elif score < 9.0:
        return {
            "score": score,
            "severity": "HIGH",
            "color": "#fd7e14"
        }
    else:
        return {
            "score": score,
            "severity": "CRITICAL",
            "color": "#dc3545"
        }


@tool
def cve_scorer(cve_data: str) -> str:
    """
    Analyze and score a CVE's severity level.
    Returns severity rating (LOW/MEDIUM/HIGH/CRITICAL) based on CVSS score.
    Input: CVE search results or CVE details text
    Returns: JSON with score, severity level, and color for UI display
    """
    try:
        cvss_score = extract_cvss_score(cve_data)
        severity_info = score_to_severity(cvss_score)
        
        result = {
            "cvss_score": severity_info["score"],
            "severity": severity_info["severity"],
            "display_color": severity_info["color"],
            "interpretation": get_severity_interpretation(severity_info["severity"])
        }
        
        return json.dumps(result, indent=2)
    
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "severity": "UNKNOWN"
        })


def get_severity_interpretation(severity: str) -> str:
    """Provide interpretation text for each severity level."""
    interpretations = {
        "CRITICAL": "This CVE poses an immediate and severe threat. Patch immediately.",
        "HIGH": "This CVE is serious and should be patched as soon as possible.",
        "MEDIUM": "This CVE should be addressed in the regular patching cycle.",
        "LOW": "This CVE is minor and can be addressed during routine maintenance.",
        "UNKNOWN": "Unable to determine severity. Manual review recommended."
    }
    return interpretations.get(severity, "Unknown severity level")
