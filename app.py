from agents import planner_agent, moderator_agent, translation_agent

def generate_post(topic, mode, lang, length):
    """
    Generate a single post using multi-agent workflow
    Returns a dictionary with content, hinglish, status
    """
    # 1️⃣ Planner Agent
    plan = planner_agent(topic, mode)
    
    # Combine hook + points into text
    content_text = plan.get("hook", "") + "\n" + "\n".join(plan.get("points", []))
    
    # 2️⃣ Moderator Agent
    moderated_text = moderator_agent(content_text)
    
    # 3️⃣ Translation Agent
    hinglish_text = None
    if lang in ["hinglish", "both"]:
        hinglish_text = translation_agent(moderated_text)
    
    return {
        "content": moderated_text,
        "hinglish": hinglish_text,
        "status": "Approved"
    }

def generate_batch(topic, mode, lang, batch_size, length):
    """Generate multiple posts"""
    results = []
    for _ in range(batch_size):
        results.append(generate_post(topic, mode, lang, length))
    return results
