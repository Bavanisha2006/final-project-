import os
import json
import random
import requests

# Standard Group Discussion topics
PRESET_TOPICS = {
    "AI vs. Human Programmers: Will generative AI completely replace software engineers?": {
        "context": "Discussion around the rapid development of LLMs in coding, automated code generation, and the changing role of software developers.",
        "ideal_concepts": ["productivity boost", "boiler-plate automation", "system design", "security vulnerability", "mentorship gap"]
    },
    "Work from Home vs. Office: What is the future of corporate work culture?": {
        "context": "Exploring the balance between productivity, work-life balance, collaboration, and company culture in hybrid, remote, and fully in-office setups.",
        "ideal_concepts": ["collaboration", "work-life balance", "overhead cost", "isolation", "hybrid structure"]
    },
    "Cryptocurrency & Blockchain: A revolutionary financial system or a speculative bubble?": {
        "context": "Analyzing the decentralized nature, security, and utility of blockchain versus the extreme volatility, speculation, and environmental impact of crypto.",
        "ideal_concepts": ["decentralization", "smart contracts", "speculation", "volatility", "regulation"]
    },
    "Universal Basic Income: Is UBI a viable solution to automation-induced job loss?": {
        "context": "Examining whether giving unconditional monthly cash payments to all citizens can resolve economic displacement caused by AI and robotics.",
        "ideal_concepts": ["automation displacement", "economic safety net", "taxation structure", "inflation risk", "motivation to work"]
    },
    "Social Media: Connecting people or creating echo chambers and mental health crises?": {
        "context": "Analyzing the double-edged sword of global connectivity versus algorithmic polarization, misinformation, and developmental mental health effects.",
        "ideal_concepts": ["algorithmic bias", "connectivity", "mental health", "misinformation", "echo chambers"]
    }
}

# AI Character Personas
CHARACTERS = {
    "Rohan": {
        "name": "Rohan",
        "role": "Participant",
        "avatar": "👨‍💻",
        "color": "#3B82F6",
        "style": "Analytical & Data-Driven",
        "description": "Bases arguments on statistics, facts, and logical frameworks. Speaks concisely, looking for metrics.",
        "offline_responses": {
            "AI vs. Human Programmers: Will generative AI completely replace software engineers?": [
                "If we look at the data, developers using AI coding tools see an average productivity increase of 55%. This indicates that generative AI is not a replacement, but an accelerator. The actual risk lies in software engineers refusing to adapt to these toolsets.",
                "To add some structure, we must distinguish between syntax creation and system architecture. Writing code is only 30% of a software developer's job. AI is excellent at syntax, but it fails at complex, multi-service system design and deep business logic mapping.",
                "In conclusion, the data points towards a hybrid future. Software engineering roles will evolve from purely writing code to reviewing, prompting, and orchestrating large systems. The demand for engineers who understand optimization and domain logic will actually rise."
            ],
            "Work from Home vs. Office: What is the future of corporate work culture?": [
                "From a cost-efficiency standpoint, companies save an average of $11,000 per remote worker annually, while employees save on commuting. However, data from McKinsey shows a 15% drop in cross-functional collaboration. We need to measure output, not presence.",
                "Let's look at the metrics for employee retention. Surveys show that 74% of professionals would choose hybrid work over in-office. This makes flexible arrangements a major factor in hiring talent, directly affecting a company's recruitment budget.",
                "My final takeaway is that a data-driven approach supports a structured hybrid model. Requiring 2 days in office for collaborative sprints, and 3 days remote for focused coding, achieves the optimal balance of productivity and cost savings."
            ],
            "Cryptocurrency & Blockchain: A revolutionary financial system or a speculative bubble?": [
                "Statistically, cryptocurrency has high volatility, with Bitcoin experiencing multiple 80% drawdowns. However, blockchain technology itself handles millions of decentralized transactions globally. We must separate the speculation of coins from the ledger technology.",
                "Let's look at the transactional efficiency. Cross-border bank transfers take 3-5 days and charge up to 5% fees. Ripple or stablecoins can settle transactions in seconds for pennies. That is a concrete utility metric that financial systems cannot ignore.",
                "To summarize, while 95% of altcoins are speculative bubbles, the underlying blockchain technology is a fundamental shift in ledger management. Decentralization is highly efficient for trustless global transactions."
            ],
            "Universal Basic Income: Is UBI a viable solution to automation-induced job loss?": [
                "Data from UBI trials in Finland and Stockton show improved mental health and high housing security, with no significant decline in employment. In fact, participants were more likely to start businesses due to the safety net mitigating risk.",
                "We must look at the fiscal math. Providing a $1,000 monthly check to 250 million adult Americans costs $3 trillion annually. This is roughly 75% of the entire federal tax revenue. We would need a massive Value Added Tax or automation tax to fund this.",
                "In short, UBI is mathematically challenging but socially viable. To offset automation displacement, a targeted basic income funded by automation taxes is a more sustainable fiscal model than a blanket unconditional payout."
            ],
            "Social Media: Connecting people or creating echo chambers and mental health crises?": [
                "The core issue is the algorithm. Engagement metrics drive recommendation engines, meaning polarizing content is amplified because it triggers strong emotional responses. Data shows extreme content gets 7 times more engagement than neutral facts.",
                "Looking at the mental health stats, the rise of adolescent depression correlates directly with the widespread adoption of smartphones and algorithm-driven feeds post-2012. It is not just about connectivity; it's about dopamine loop exploitation.",
                "In conclusion, the connectivity value of social media is overshadowed by the business model of attention extraction. We need data regulations that penalize algorithmic outrage-loops to fix this."
            ]
        }
    },
    "Priya": {
        "name": "Priya",
        "role": "Participant",
        "avatar": "👩‍💼",
        "color": "#10B981",
        "style": "Cooperative & Synthesizer",
        "description": "Synthesizes arguments, builds consensus, highlights common ground, and maintains discussion flow.",
        "offline_responses": {
            "AI vs. Human Programmers: Will generative AI completely replace software engineers?": [
                "I agree with Rohan's point about productivity. AI is definitely a powerful tool. However, we should also think about entry-level developers. If we rely on AI for basic code, how will junior developers learn the logic needed to become senior engineers?",
                "That's a very fair counterpoint, Kabir. The security risks and copy-paste culture are real concerns. But as Rohan mentioned, the role is shifting. Maybe our focus should be on teaching juniors code review and debugging rather than pure writing.",
                "To synthesize what everyone is saying: AI increases efficiency but introduces risks like a lack of deep code comprehension and security. The solution seems to be modifying engineering curriculum to emphasize design, testing, and security checks."
            ],
            "Work from Home vs. Office: What is the future of corporate work culture?": [
                "Rohan's comparison of cost savings vs. collaboration is very accurate. Remote work gives great flexibility, but we shouldn't lose the human touch. Face-to-face mentorship for new graduates is extremely hard to replicate over video calls.",
                "I think Kabir's point about hybrid model friction is very real. If some people are in office and others remote, it creates communication gaps. We need clear, team-wide agreements so that on in-office days, the whole team is actually present to connect.",
                "Looking at the discussion, it seems we all agree that flexibility is necessary, but collaboration and mentorship must be preserved. A well-organized hybrid structure with dedicated sync days seems to be the consensus here."
            ],
            "Cryptocurrency & Blockchain: A revolutionary financial system or a speculative bubble?": [
                "Rohan makes an excellent distinction between volatile coins and the underlying ledger utility. Cryptocurrencies might feel like a bubble to many, but the technology solves real trust issues. How do we ensure regulatory compliance, though?",
                "I see Kabir's concern about illegal transactions, but as Rohan highlighted, stablecoins can offer massive cross-border payment efficiency. Perhaps if we combine government-backed digital currencies with blockchain, we get the best of both worlds.",
                "So, to summarize our points: the speculation is a major risk, but blockchain utility is undeniable. The consensus path forward seems to be smart regulation and central bank digital currencies, rather than a completely unregulated system."
            ],
            "Universal Basic Income: Is UBI a viable solution to automation-induced job loss?": [
                "I think Rohan's point about fiscal cost is critical, but the security UBI provides can't be ignored. As automation speeds up, people will need support to transition. UBI could give workers the breathing room to retrain without falling into poverty.",
                "Kabir's point about inflation is very valid—if everyone gets $1,000, landlords might raise rent. Perhaps instead of UBI, we should focus on 'Universal Basic Services' like free healthcare, education, and subsidized housing to lower living costs.",
                "Synthesizing the views: while a direct financial payout (UBI) is expensive and risks inflation, the underlying need to support workers during automation is crucial. Combining targeted safety nets with subsidized retraining could be a practical compromise."
            ],
            "Social Media: Connecting people or creating echo chambers and mental health crises?": [
                "Rohan's analysis of algorithm-driven outrage is very true. Social media was built to connect us, but the profit model drove us apart. I think we need to emphasize digital literacy in schools so users understand how algorithms manipulate their attention.",
                "That's a very practical observation, Kabir. Regulating the tech giants is difficult, but as Rohan and I suggested, user empowerment and ethical design are places we can start. Platforms should offer an 'algorithm-free' chronological feed by default.",
                "To wrap up our views: social media's connectivity is valuable, but the current engagement-maximizing algorithms are harmful. We agree that a combination of government regulations, ethical design defaults, and digital literacy is required."
            ]
        }
    },
    "Kabir": {
        "name": "Kabir",
        "role": "Participant",
        "avatar": "🙋‍♂️",
        "color": "#F59E0B",
        "style": "Skeptical & Practical",
        "description": "Focuses on execution, operational bottlenecks, real-world limitations, and questions optimistic views.",
        "offline_responses": {
            "AI vs. Human Programmers: Will generative AI completely replace software engineers?": [
                "While the productivity stats Rohan quoted sound impressive, in practice, relying too much on AI tools creates a 'copy-paste' culture. Developers might accept AI-generated code they don't understand, leading to technical debt and massive security vulnerabilities.",
                "I appreciate Priya's suggestion about training, but let's be realistic: companies want quick delivery. If developers just prompt AI without understanding runtime complexities, database indexes, or memory management, debugging critical outages will become a nightmare.",
                "Let's look at the liability: if an AI model generates code that leads to a data breach, who is legally responsible? The developer? The AI provider? Until legal and security frameworks catch up, human oversight remains non-negotiable."
            ],
            "Work from Home vs. Office: What is the future of corporate work culture?": [
                "Rohan talks about hybrid work, but the practical reality of hybrid schedules is often chaotic. If I go to the office and spend my entire day on video calls because half my team is remote, that is a waste of a commute and frustrates employees.",
                "Priya mentioned mentorship, but juniors can't learn from seniors who are constantly on mute or busy. In-office work forces spontaneous knowledge sharing. You can't schedule a 'watercooler chat' on Google Meet; it has to happen naturally.",
                "My view is that hybrid systems fail unless companies are strict about in-office alignment. Otherwise, fully remote or fully in-office are the only clean operational models. Half-and-half solutions usually create friction for both sides."
            ],
            "Cryptocurrency & Blockchain: A revolutionary financial system or a speculative bubble?": [
                "The 'ledger efficiency' Rohan talks about ignores the massive regulatory and illicit finance problems. Cryptocurrencies are widely used for ransomware payouts, tax evasion, and money laundering. A financial system without accountability is a recipe for chaos.",
                "Priya suggests digital currencies, but governments will never hand over control of monetary policy. The value of a currency relies on state backing and tax collection. Without that, crypto is just digital gold at best, and a Ponzi scheme at worst.",
                "To be practical, blockchain has been looking for a real mainstream use case for over a decade. Apart from speculation and quick international transfers, standard centralized databases are still faster, cheaper, and easier to manage for 99% of businesses."
            ],
            "Universal Basic Income: Is UBI a viable solution to automation-induced job loss?": [
                "The Stockton and Finland trials were temporary and funded by grants. If you inject $3 trillion of newly printed money into the economy permanently, inflation will rise, erasing the purchasing power of that $1,000. Landlords and grocery stores will adjust prices.",
                "Priya mentioned retraining, but the practical track record of government retraining programs is extremely poor. You can't easily turn a 50-year-old factory worker into a software engineer. UBI doesn't solve the psychological loss of purpose that work provides.",
                "Ultimately, UBI is a band-aid. Instead of giving out cash, we should focus on infrastructure projects, subsidizing green energy jobs, and local manufacturing. Work gives people dignity; unconditional cash transfers do not solve structural unemployment."
            ],
            "Social Media: Connecting people or creating echo chambers and mental health crises?": [
                "Rohan blames the algorithm, but let's be realistic: humans have always sought out echo chambers. We naturally associate with people who agree with us. Social media just accelerated this human bias at a global scale. Regulation won't change human psychology.",
                "Priya's digital literacy idea is good, but platforms are designed to bypass cognitive filters using variable reward schedules, just like slot machines. Expecting a teenager to self-regulate against a multi-billion dollar supercomputer algorithm is highly unrealistic.",
                "The practical solution is treating social media like tobacco or gambling. We need age restrictions, strict bans on tracking minors, and liability for platforms when their algorithms recommend self-harm content. Voluntary ethics don't work."
            ]
        }
    },
    "Ananya": {
        "name": "Ananya",
        "role": "Participant",
        "avatar": "👩‍🎨",
        "color": "#EC4899",
        "style": "Empathetic & Creative",
        "description": "Focuses on human element, social equity, ethics, mental wellbeing, and creative solutions.",
        "offline_responses": {
            "AI vs. Human Programmers: Will generative AI completely replace software engineers?": [
                "We must look at the human side. Tech is not just about writing lines of code; it's about solving real human problems. AI lacks empathy and ethical judgment. An AI might write code efficiently, but it won't understand how that code impacts diversity or access.",
                "I agree with Priya's focus on juniors. If we automate entry-level roles, we shut the door on developers from underrepresented backgrounds who rely on junior roles to enter the industry. The tech community needs to protect these opportunities.",
                "In short, we should build cooperative AI systems that assist rather than automate. Our focus must be on human-centric engineering where AI handles repetitive tasks, enabling humans to focus on ethical system design and accessibility."
            ],
            "Work from Home vs. Office: What is the future of corporate work culture?": [
                "Remote work has been a blessing for accessibility. Working mothers, caregivers, and disabled professionals have finally found a way to participate fully in the workforce. Going back to a rigid 5-day office week would be a massive step backward.",
                "Kabir's point about spontaneous connection is valid, but the mental health benefits of remote work—like spending time with family, cooking healthy food, and avoiding stressful commutes—outweigh the watercooler chat. We must value wellbeing.",
                "Ultimately, the future of work must be human-centric. Work should fit around our lives, not the other way around. Giving employees the autonomy to choose their workspace shows trust and fosters a healthier, more creative culture."
            ],
            "Cryptocurrency & Blockchain: A revolutionary financial system or a speculative bubble?": [
                "We are ignoring the unbanked population. Millions of people in developing countries have no access to banks but have mobile phones. Cryptocurrency allows them to receive remittances directly without predatory middleman fees. This is about financial inclusion.",
                "While Kabir focuses on crime, the current banking system has also facilitated massive corruption. Blockchain offers a transparent, public record of transactions. Imagine tracking government spending or charity donations on a public ledger—that is revolutionary.",
                "My perspective is that cryptocurrency has the potential to democratize wealth. If we focus on carbon-neutral blockchain protocols and micro-transactions, we can create a fairer financial system that supports community-led economies."
            ],
            "Universal Basic Income: Is UBI a viable solution to automation-induced job loss?": [
                "UBI is a matter of human dignity. In an automated world, we must decouple survival from labor. A person's value shouldn't be defined solely by their economic productivity. UBI would allow people to pursue arts, caregiving, and community service.",
                "Kabir mentioned dignity in work, but many jobs today are exploitative and offer no dignity. UBI gives workers the 'power to say no' to bad bosses and unsafe working conditions. It balances the power dynamic between labor and capital.",
                "In conclusion, UBI is a moral necessity for a civilized society facing automation. It ensures that the wealth generated by machines is shared by all of humanity, freeing us to engage in meaningful work rather than just survival jobs."
            ],
            "Social Media: Connecting people or creating echo chambers and mental health crises?": [
                "We must talk about the loneliness epidemic. For marginalized youth, LGBTQ+ individuals, or people in isolated areas, social media is a vital lifeline to find community and support. We cannot ignore this emotional and social rescue.",
                "I agree with Kabir about platform liability, but let's also support cooperative, user-owned platforms. Imagine ad-free networks run as digital commons, where the goal is human connection rather than selling ads. The internet can be beautiful again.",
                "To summarize, social media's core value is human solidarity. While commercial algorithms have turned it toxic, we can reclaim the digital space by investing in public, ad-free platforms designed to nurture connection and community."
            ]
        }
    }
}

def fetch_available_groq_models(groq_key):
    """Queries Groq API for available model IDs."""
    try:
        url = "https://api.groq.com/openai/v1/models"
        headers = {
            "Authorization": f"Bearer {groq_key.strip()}"
        }
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            models_data = res.json().get("data", [])
            return [m["id"] for m in models_data]
    except Exception:
        pass
    return []

def resolve_groq_model(groq_key, preferred_model=None):
    """
    Resolves the model name to use. Checks if preferred_model is in the list
    of available models. If not (or if preferred_model is deprecated/404),
    finds the best available text generation model.
    """
    env_model = os.environ.get("GROQ_MODEL") or os.environ.get("GROK_MODEL")
    target_model = preferred_model or env_model or "openai/gpt-oss-20b"
    
    available = fetch_available_groq_models(groq_key)
    if not available:
        return target_model
        
    if target_model in available:
        return target_model
        
    # Find active text-generation models
    text_models = []
    for m in available:
        m_lower = m.lower()
        if "whisper" not in m_lower and "guard" not in m_lower:
            text_models.append(m)
            
    # Prefer standard available text models
    for pref in ["openai/gpt-oss-20b", "groq/compound", "openai/gpt-oss-120b", "qwen/qwen3.6-27b"]:
        if pref in text_models:
            return pref
            
    if text_models:
        return text_models[0]
        
    return target_model

def call_llm_api(messages, api_key=None, model=None):
    """
    Calls the Groq Cloud API directly using the Groq key stored in GROK_API_KEY.
    With robust fallback if the configured model is unavailable.
    """
    groq_key = api_key or os.environ.get("GROK_API_KEY") or os.environ.get("GROQ_API_KEY")
    if not groq_key:
        raise ValueError(
            "Groq API key is required but not configured. "
            "Please provide a valid GROK_API_KEY or GROQ_API_KEY in your environment or .env file."
        )
        
    resolved_model = resolve_groq_model(groq_key, model)
        
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {groq_key.strip()}"
    }
    payload = {
        "model": resolved_model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1000
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=35)
        
        # If we get a 404 or 400 indicating model not found, try to resolve fallback dynamically
        if response.status_code in (404, 400):
            try:
                err_msg = response.json().get("error", {}).get("message", "")
            except Exception:
                err_msg = response.text
            if "model" in err_msg.lower() or "not exist" in err_msg.lower() or response.status_code == 404:
                # Dynamically resolve a new model and retry
                fallback_model = resolve_groq_model(groq_key, None)
                if fallback_model != resolved_model:
                    payload["model"] = fallback_model
                    response = requests.post(url, headers=headers, json=payload, timeout=35)
                    
        response.raise_for_status()
        res_json = response.json()
        return res_json["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        try:
            err_json = response.json()
            err_msg = err_json.get("error", {}).get("message", response.text)
        except Exception:
            err_msg = response.text
        raise RuntimeError(f"Groq API request failed ({response.status_code}): {err_msg}")
    except Exception as e:
        raise RuntimeError(f"Groq API request failed: {str(e)}")

def generate_participant_response(character_name, topic, track, history, api_key=None, model=None):
    """
    Generates the next statement for an AI character.
    Always uses the Grok API to ensure dynamic, AI-generated content.
    """
    char = CHARACTERS.get(character_name)
    if not char:
        return {"speaker": "System", "text": "Invalid speaker", "avatar": "⚠️"}

    # Format the discussion history for the model context
    formatted_history = []
    for msg in history:
        role_label = "User (Candidate)" if msg.get("is_user") else msg.get("speaker")
        formatted_history.append(f"{role_label}: {msg.get('text')}")
    
    history_str = "\n".join(formatted_history[-8:])

    system_prompt = f"""You are participating in a Group Discussion (GD) for a job placement process. 
Your character name is **{char['name']}**.
Your character profile:
- Style: {char['style']}
- Personality: {char['description']}

The Topic of the GD is: "{topic}"
The candidate's target career track is: "{track}"

Your role is to act as **{char['name']}** and contribute the next turn in the discussion.
Rules:
1. Stay strictly in character. Do not explain your response, do not say "Here is my response" or include any intros/meta-text. Just state the speech directly.
2. Be concise: write exactly 2-4 sentences (about 50-80 words).
3. React directly, agree, or constructiveness-disagree with what the previous speakers (including the User/Candidate or other AI participants) said. Refer to them by name (e.g. "Rohan", "Priya", "Kabir", "Ananya" or "Candidate").
4. Keep the discussion professional and intellectually engaging.
"""

    user_prompt = f"""Here is the recent discussion history:
{history_str}

It is now your turn. Write your next response as **{char['name']}**."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        content = call_llm_api(messages, api_key, model=model)
        content_stripped = content.strip().strip('"').strip("'")
        return {
            "speaker": char["name"],
            "role": char["role"],
            "avatar": char["avatar"],
            "color": char["color"],
            "style": char["style"],
            "text": content_stripped
        }
    except Exception as e:
        return {
            "speaker": char["name"],
            "role": char["role"],
            "avatar": char["avatar"],
            "color": char["color"],
            "style": char["style"],
            "text": f"Roundtable error: AI generation failed. Details: {str(e)}"
        }

def generate_offline_participant_response(character_name, topic, history):
    """
    Retrieves the next pre-defined statement for a character based on the current round.
    If the topic is custom or we exceed preloaded statements, we generate a generic fallback statement.
    """
    char = CHARACTERS.get(character_name)
    char_turns = [msg for msg in history if msg.get("speaker") == character_name]
    turn_idx = len(char_turns)
    
    responses = char["offline_responses"].get(topic)
    
    if responses and turn_idx < len(responses):
        text = responses[turn_idx]
    else:
        if character_name == "Rohan":
            text = f"Analyzing the metrics of '{topic}', we see that efficiency gains are paramount. A structured data-driven approach shows that we can optimize results. Let's examine the primary metrics of this issue."
        elif character_name == "Priya":
            text = f"To bridge Rohan and Kabir's perspectives on '{topic}', we must recognize the common thread. We all want viable outcomes. I propose we outline a cooperative guideline to move forward."
        elif character_name == "Kabir":
            text = f"The ideas mentioned sound good on paper, but the real-world operational challenges of '{topic}' are massive. How do we tackle structural budgets, legal compliance, and initial friction?"
        else: # Ananya
            text = f"I want to bring our focus back to the social impact of '{topic}'. Systems are only as good as the lives they improve. We need a creative, human-centric viewpoint to guide this discussion."
            
        text += f" (Round {turn_idx + 1} analysis)"
        
    return {
        "speaker": char["name"],
        "role": char["role"],
        "avatar": char["avatar"],
        "color": char["color"],
        "style": char["style"],
        "text": text
    }

def generate_moderator_message(topic, history, action="introduce", api_key=None, model=None):
    """
    Generates moderator text. Action can be 'introduce', 'intervene', or 'conclude'.
    Always uses the Grok API to ensure dynamic, AI-generated content.
    """
    formatted_history = []
    for msg in history:
        role_label = "User (Candidate)" if msg.get("is_user") else msg.get("speaker")
        formatted_history.append(f"{role_label}: {msg.get('text')}")
    history_str = "\n".join(formatted_history[-8:])

    if action == "introduce":
        system_prompt = "You are the professional Moderator of a corporate Group Discussion. Introduce the topic, lay out brief guidelines, and invite Rohan to start the discussion. Keep your intro highly professional and under 60 words."
        user_prompt = f"Introduce the GD. Topic: '{topic}'"
    elif action == "intervene":
        system_prompt = "You are the professional Moderator of a corporate Group Discussion. Intervene briefly based on the discussion transcript. Highlight a point that needs more debate or ask the participants to focus. Keep it under 60 words."
        user_prompt = f"Based on this history, intervene to guide the group:\n{history_str}"
    else: # conclude
        system_prompt = "You are the professional Moderator. Summarize and officially conclude the Group Discussion. Provide a brief wrapping statement under 60 words."
        user_prompt = f"Conclude this discussion:\n{history_str}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        content = call_llm_api(messages, api_key, model=model)
        return {
            "speaker": "Moderator",
            "role": "Moderator",
            "avatar": "🎙️",
            "color": "#6B7280",
            "style": "Official Moderator",
            "text": content.strip().strip('"').strip("'")
        }
    except Exception as e:
        return {
            "speaker": "Moderator",
            "role": "Moderator",
            "avatar": "🎙️",
            "color": "#6B7280",
            "style": "Official Moderator",
            "text": f"Moderator error: AI generation failed. Details: {str(e)}"
        }

def generate_offline_moderator_message(topic, history, action="introduce"):
    if action == "introduce":
        text = f"Welcome everyone to today's Group Discussion. The topic is '{topic}'. We have 4 participants ready. We will run this discussion for a few rounds, after which I will evaluate your contributions. Rohan, please start us off."
    elif action == "intervene":
        text = f"Moderator Interjection: We have heard some interesting arguments regarding efficiency and implementation details. Let's make sure we also explore the social implications and how the end-users are affected by this topic. Please continue."
    else: # conclude
        text = f"Thank you everyone. We've had a highly productive session exploring multiple dimensions of '{topic}'. The discussion is now concluded. I will generate your performance evaluation reports shortly. Excellent effort by all."
        
    return {
        "speaker": "Moderator",
        "role": "Moderator",
        "avatar": "🎙️",
        "color": "#6B7280",
        "style": "Official Moderator",
        "text": text
    }

def evaluate_gd_performance(topic, track, history, api_key=None, model=None):
    """
    Evaluates the candidate's performance in the Group Discussion.
    Generates a detailed JSON evaluation report.
    """
    user_msgs = [msg for msg in history if msg.get("is_user")]
    user_inputs = [f"- {msg['text']}" for msg in user_msgs]
    user_inputs_str = "\n".join(user_inputs)
    
    word_count = sum(len(msg["text"].split()) for msg in user_msgs)
    
    if not user_msgs:
        return generate_offline_gd_evaluation(topic, track, history, user_msgs, word_count)

    full_transcript = []
    for msg in history:
        speaker_name = "Candidate (User)" if msg.get("is_user") else msg.get("speaker")
        full_transcript.append(f"{speaker_name}: {msg.get('text')}")
    transcript_str = "\n".join(full_transcript)

    system_prompt = """You are an elite corporate Recruiter, HR Assessor, and Moderator evaluating a job candidate's performance in a Group Discussion (GD).
Analyze the candidate's contributions in the provided GD transcript. Evaluate them strictly and provide critical, constructive corporate feedback.

Rubric Parameters (out of 5.0):
1. Communication Skills (Vocabulary, clarity, professional tone)
2. Content & Domain Knowledge (Depth of ideas, technical accuracy, relevance to target track)
3. Leadership & Teamwork (Initiating, building on others' points, respect, facilitation)
4. Listening & Synthesizing (Active listening, referencing others, summarizing arguments)

Respond strictly in JSON format matching the schema below:
{
  "score": 82.5,
  "rating": "Strong Contributor",
  "rating_color": "green", // green for score >= 80, orange for score 50-79, red for score < 50
  "ratings": {
    "communication": 4.2,
    "content": 4.0,
    "leadership": 3.8,
    "listening": 4.5
  },
  "strengths": [
    "Specific positive point 1",
    "Specific positive point 2"
  ],
  "weaknesses": [
    "Constructive improvement point 1",
    "Constructive improvement point 2"
  ],
  "summary": "Detailed summary paragraph of overall candidate alignment, speaking frequency, and behavior in the discussion.",
  "transcript_analysis": [
    {
      "statement": "The user's statement snippet",
      "analysis": "Quick sentence evaluating this specific entry's technical depth, relevance, or style."
    }
  ]
}

Provide raw JSON. Do not include markdown formatting or ```json block fences.
"""

    user_prompt = f"""Target Career Track: "{track}"
GD Topic: "{topic}"

Full GD Transcript:
{transcript_str}

Evaluate the Candidate's responses:
{user_inputs_str}
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        content = call_llm_api(messages, api_key, model=model)
        text = content.strip()
        
        if text.startswith("```"):
            lines = text.split("\n")
            if lines[0].startswith("```json") or lines[0].startswith("```"):
                lines = lines[1:-1]
            text = "\n".join(lines).strip()
            
        data = json.loads(text)
        data['word_count'] = word_count
        data['total_turns'] = len(user_msgs)
        return data
    except Exception as e:
        return generate_offline_gd_evaluation(topic, track, history, user_msgs, word_count, error_msg=str(e))

def generate_offline_gd_evaluation(topic, track, history, user_msgs, word_count, error_msg=None):
    """
    Performs a deterministic, keyword-based evaluation of the user's input.
    """
    total_turns = len(user_msgs)
    
    if total_turns == 0:
        return {
            "score": 10.0,
            "rating": "Passive Observer",
            "rating_color": "red",
            "ratings": {"communication": 1.0, "content": 1.0, "leadership": 1.0, "listening": 1.0},
            "strengths": ["Attended the discussion session."],
            "weaknesses": ["Did not contribute any statements. Group discussions require active verbal participation."],
            "summary": "The candidate was silent throughout the Group Discussion. To improve, prepare key concepts beforehand and interject early in the conversation.",
            "transcript_analysis": [],
            "word_count": 0,
            "total_turns": 0,
            "offline_mode": True
        }

    preset = PRESET_TOPICS.get(topic, {"ideal_concepts": ["implementation", "collaboration", "strategy"]})
    concepts = preset["ideal_concepts"]
    
    matched_concepts = []
    all_user_text = " ".join([m["text"].lower() for m in user_msgs])
    
    for c in concepts:
        if c.lower() in all_user_text or any(part in all_user_text for part in c.lower().split() if len(part) > 3):
            matched_concepts.append(c)

    turn_score = min(5.0, total_turns * 1.5)
    
    avg_words = word_count / total_turns
    word_score = 3.0
    if avg_words > 40:
        word_score = 5.0
    elif avg_words > 20:
        word_score = 4.0
    elif avg_words < 10:
        word_score = 1.5
        
    concept_ratio = len(matched_concepts) / len(concepts) if concepts else 0.5
    content_rating = round(1.0 + (concept_ratio * 4.0), 1)
    
    referencing = 2.0
    for name in ["rohan", "priya", "kabir", "ananya"]:
        if name in all_user_text:
            referencing += 0.75
    referencing = min(5.0, referencing)

    comm_score = round(min(5.0, word_score * 0.9 + turn_score * 0.1), 1)
    cont_score = content_rating
    lead_score = round(min(5.0, turn_score * 0.8 + referencing * 0.2), 1)
    list_score = round(referencing, 1)
    
    overall_score = round(((comm_score + cont_score + lead_score + list_score) / 20.0) * 100.0, 1)

    if overall_score >= 80:
        rating = "Leader (Strong Placement Fit)"
        rating_color = "green"
    elif overall_score >= 60:
        rating = "Strong Contributor (Good Potential)"
        rating_color = "orange"
    else:
        rating = "Needs Practice (Passive/Flipped)"
        rating_color = "red"

    strengths = []
    weaknesses = []
    
    if comm_score >= 4.0:
        strengths.append("Demonstrated good vocabulary and clear professional phrasing.")
    else:
        weaknesses.append("Statements were brief or lacked structured definitions. Elaborate more on technical components.")
        
    if cont_score >= 3.5:
        strengths.append(f"Addressed relevant domain concepts such as: {', '.join(matched_concepts[:2])}.")
    else:
        weaknesses.append("Contributions were general. Incorporate specific industry examples or technical metrics.")
        
    if lead_score >= 3.8:
        strengths.append("Proactively built upon or responded to other participants' ideas.")
    else:
        weaknesses.append("Spoke in isolation. Actively reference previous participants' inputs to synthesize points.")

    if not strengths:
        strengths.append("Participated in the discussion and shared opinions on the topic.")
    if not weaknesses:
        weaknesses.append("Try to take the lead in summarizing the discussion towards the end.")

    summary = f"The candidate participated with {total_turns} turn(s). "
    if overall_score >= 80:
        summary += "They displayed excellent placement readiness, balancing active argumentation with synthesis. They frequently referenced peers to build consensus."
    elif overall_score >= 60:
        summary += "They displayed solid foundation but can improve by adding more data/metrics to support their arguments and actively engaging in consensus building."
    else:
        summary += "The candidate was relatively passive. They should focus on interjecting earlier, raising structured points, and directly referencing other speakers."

    if error_msg:
        summary += f" (Note: Evaluated in Offline Mode due to API error: {error_msg})"
    else:
        summary += " (Evaluated in Offline Mode)"

    transcript_analysis = []
    for msg in user_msgs:
        words = len(msg["text"].split())
        ref_count = sum(1 for name in ["rohan", "priya", "kabir", "ananya"] if name in msg["text"].lower())
        analysis_text = f"Length: {words} words. "
        if ref_count > 0:
            analysis_text += "Good active listening by acknowledging others by name. "
        else:
            analysis_text += "Spoke independently without referencing the team. "
            
        if words < 15:
            analysis_text += "Too concise to demonstrate technical or domain depth."
        else:
            analysis_text += "Contributed solid context to the flow."
            
        transcript_analysis.append({
            "statement": msg["text"][:60] + "..." if len(msg["text"]) > 60 else msg["text"],
            "analysis": analysis_text
        })

    return {
        "score": overall_score,
        "rating": rating,
        "rating_color": rating_color,
        "ratings": {
            "communication": comm_score,
            "content": cont_score,
            "leadership": lead_score,
            "listening": list_score
        },
        "strengths": strengths,
        "weaknesses": weaknesses,
        "summary": summary,
        "transcript_analysis": transcript_analysis,
        "word_count": word_count,
        "total_turns": total_turns,
        "offline_mode": True
    }
