from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyChJyrEqhPDv_qqwK_MGsmpZT2XfCApc2w",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def analyze_and_optimize(content, product_info):
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {
                "role": "system",
                "content": "You are a marketing expert who improves content quality, engagement, and clarity."
            },
            {
                "role": "user",
                "content": f"""
Analyze and optimize this content:

CONTENT:
{content}

PRODUCT INFO:
{product_info}

Give:
1. Improved version
2. Engagement tips
3. Quality score out of 10
"""
            }
        ]
    )

    return {
        "optimization_report": response.choices[0].message.content
    }