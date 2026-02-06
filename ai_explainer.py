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
Port {port} has severity level {severity}.
Issue: {description}

Explain why this is a security risk.
Provide short professional mitigation advice.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        explanations.append(response.choices[0].message["content"])

    return explanations
