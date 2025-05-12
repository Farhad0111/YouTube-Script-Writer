def build_prompt(data):
    return f"""
You are a professional YouTube script writer. Based on the inputs below, generate a full script.

Inputs:
Topic: {data.topic}
Tone: {data.tone}
Style: {data.style}
Duration: {data.duration} minutes
Target Audience: {data.audience}
Language: {data.language}
Additional Notes: {data.notes}

Output format:
1. Script Structure (with timestamps)
2. Hook
3. Chapters (3, each with a title and body)
4. Engagement Moment (question, twist, or CTA)
5. Scorecard (rate Clickability, SEO Strength, Clarity & Relevance from 0 to 10)

Write naturally, clearly, and engagingly. Do not include anything outside the specified format.
"""
