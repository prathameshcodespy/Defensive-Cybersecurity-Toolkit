import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")


def explain_risks(risks):
    if not risks:
        return ["No risks detected."]

    explanations = []

    for risk in risks:
        port = risk["port"]
        severity = risk["severity"]
        description = risk["description"]

        prompt = f"""
Port {port} has severity {severity}.
Issue: {description}

1. Explain the security risk.
2. Provide professional mitigation steps.
3. Suggest best practices to secure this service.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        explanations.append(response.choices[0].message["content"])

    return explanations
