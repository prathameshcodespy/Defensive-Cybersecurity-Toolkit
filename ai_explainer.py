def explain_risks(risks):
    explanations = []
    for port, service, reason in risks:
        explanation = f"""
Port {port} running {service} may pose security risks.
Reason: {reason}
Recommendation: Ensure secure configuration or disable if unnecessary.
"""
        explanations.append(explanation)
    return explanations
