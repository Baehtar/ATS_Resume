# ats_analyzer.py - Role-based keyword scoring and resume compliance engine
import re
import json
import os

def load_role_keywords():
    """Load keywords from role_keywords.json. Falls back to defaults if file is missing."""
    json_path = os.path.join(os.path.dirname(__file__), "role_keywords.json")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback defaults
        return {
            "data_engineer": {
                "title": "Data Engineer",
                "must_have": ["SQL", "Python", "ETL", "Data Pipeline", "Apache Spark", "AWS"],
                "good_to_have": ["Scala", "Docker", "Kubernetes"],
                "action_verbs": ["engineered", "optimized", "automated", "designed", "built"]
            },
            "data_analyst": {
                "title": "Data Analyst",
                "must_have": ["SQL", "Python", "Excel", "Tableau", "Power BI", "A/B Testing"],
                "good_to_have": ["R", "Scikit-learn", "Looker"],
                "action_verbs": ["analyzed", "identified", "visualized", "reported", "quantified"]
            }
        }

# Common English stopwords
STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
    "between", "both", "but", "by", "can", "could", "did", "do", "does", "doing",
    "down", "during", "each", "few", "for", "from", "further", "get", "had", "has",
    "have", "having", "he", "her", "here", "hers", "herself", "him", "himself", "his",
    "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just", "me",
    "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on",
    "once", "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own",
    "same", "she", "should", "so", "some", "such", "than", "that", "the", "their",
    "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those",
    "through", "to", "too", "under", "until", "up", "very", "was", "we", "were",
    "what", "when", "where", "which", "while", "who", "whom", "why", "will", "with",
    "would", "you", "your", "yours", "yourself", "yourselves"
}

def tokenize(text):
    """Tokenize text into lowercase words, preserving tech terms."""
    if not text:
        return []
    tokens = re.findall(r'\b[\w\-\#\+\.\/]+\b', text.lower())
    return [t for t in tokens if len(t) > 1]

def get_resume_full_text(resume_data):
    """Compile all resume content into a single text block for matching."""
    personal = resume_data.get("personal", {})
    parts = [
        personal.get("fullName", ""),
        personal.get("email", ""),
        resume_data.get("summary", "")
    ]

    for exp in resume_data.get("experience", []):
        parts.extend([exp.get("company", ""), exp.get("role", ""), exp.get("location", "")])
        parts.extend(exp.get("bullets", []))

    for edu in resume_data.get("education", []):
        parts.extend([edu.get("school", ""), edu.get("degree", ""), edu.get("details", "")])

    for proj in resume_data.get("projects", []):
        parts.extend([proj.get("name", ""), proj.get("tech", ""), proj.get("description", "")])

    for s in resume_data.get("skills", []):
        parts.extend([s.get("category", ""), s.get("list", "")])

    for cert in resume_data.get("certifications", []):
        parts.extend([cert.get("name", ""), cert.get("issuer", "")])

    return " ".join([t for t in parts if t])

def analyze_resume(resume_data, selected_role):
    """
    Analyze resume against the selected role's keyword requirements.
    Returns a detailed report with score breakdown, matched/missing keywords, and warnings.
    """
    role_keywords = load_role_keywords()
    role_config = role_keywords.get(selected_role, {})

    must_have = role_config.get("must_have", [])
    good_to_have = role_config.get("good_to_have", [])
    action_verbs = role_config.get("action_verbs", [])

    analysis = {
        "score": 0,
        "breakdown": {
            "must_have_keywords": 0,   # Max 40
            "good_to_have_keywords": 0, # Max 15
            "sections": 0,             # Max 25
            "formatting": 0            # Max 20
        },
        "must_have_matched": [],
        "must_have_missing": [],
        "good_to_have_matched": [],
        "good_to_have_missing": [],
        "formatting_warnings": [],
        "verb_suggestions": [],
        "word_count": 0
    }

    # Compile resume text
    resume_text = get_resume_full_text(resume_data)
    resume_text_lower = resume_text.lower()
    resume_tokens = tokenize(resume_text)
    analysis["word_count"] = len(resume_tokens)

    # 1. Must-Have Keywords (40 points max)
    for kw in must_have:
        pattern = r'\b' + re.escape(kw.lower()) + r'\b'
        if re.search(pattern, resume_text_lower) or kw.lower() in resume_text_lower:
            analysis["must_have_matched"].append(kw)
        else:
            analysis["must_have_missing"].append(kw)

    if must_have:
        match_ratio = len(analysis["must_have_matched"]) / len(must_have)
        analysis["breakdown"]["must_have_keywords"] = round(match_ratio * 40)

    # 2. Good-to-Have Keywords (15 points max)
    for kw in good_to_have:
        pattern = r'\b' + re.escape(kw.lower()) + r'\b'
        if re.search(pattern, resume_text_lower) or kw.lower() in resume_text_lower:
            analysis["good_to_have_matched"].append(kw)
        else:
            analysis["good_to_have_missing"].append(kw)

    if good_to_have:
        match_ratio = len(analysis["good_to_have_matched"]) / len(good_to_have)
        analysis["breakdown"]["good_to_have_keywords"] = round(match_ratio * 15)

    # 3. Section Completeness (25 points max)
    personal = resume_data.get("personal", {})
    section_points = 0

    if personal.get("fullName") and (personal.get("email") or personal.get("phone")):
        section_points += 5
    else:
        analysis["formatting_warnings"].append({
            "type": "error",
            "message": "Missing contact details (Name + Email or Phone required)."
        })

    summary = resume_data.get("summary", "")
    if summary and len(summary.strip()) > 30:
        section_points += 5
    else:
        analysis["formatting_warnings"].append({
            "type": "warning",
            "message": "Professional summary is missing or too short. Write a 2-3 sentence pitch."
        })

    if resume_data.get("experience"):
        section_points += 5
    else:
        analysis["formatting_warnings"].append({
            "type": "error",
            "message": "Work/Internship Experience section is empty."
        })

    if resume_data.get("education"):
        section_points += 5
    else:
        analysis["formatting_warnings"].append({
            "type": "warning",
            "message": "Education section is empty."
        })

    active_skills = [s for s in resume_data.get("skills", []) if s.get("list", "").strip()]
    if active_skills:
        section_points += 5
    else:
        analysis["formatting_warnings"].append({
            "type": "error",
            "message": "Skills section is empty. ATS systems heavily index technical skills."
        })

    analysis["breakdown"]["sections"] = section_points

    # 4. Formatting Checks (20 points max)
    fmt_points = 20

    # Word count check
    if 0 < analysis["word_count"] < 150:
        fmt_points -= 5
        analysis["formatting_warnings"].append({
            "type": "warning",
            "message": f"Resume is too brief ({analysis['word_count']} words). Add more detail to experience and projects."
        })
    elif analysis["word_count"] > 1000:
        fmt_points -= 5
        analysis["formatting_warnings"].append({
            "type": "warning",
            "message": f"Resume is very long ({analysis['word_count']} words). Condense to 1-2 pages."
        })

    # Action verb usage in bullets
    bullet_count = 0
    verb_matches = 0
    action_verbs_lower = [v.lower() for v in action_verbs]

    for exp in resume_data.get("experience", []):
        for bullet in exp.get("bullets", []):
            if bullet.strip():
                bullet_count += 1
                words = tokenize(bullet)
                if any(w in action_verbs_lower for w in words):
                    verb_matches += 1

    if bullet_count > 0:
        verb_ratio = verb_matches / bullet_count
        if verb_ratio < 0.5:
            fmt_points -= 5
            analysis["formatting_warnings"].append({
                "type": "warning",
                "message": f"Only {round(verb_ratio * 100)}% of experience bullets use strong action verbs. Start bullets with verbs like: {', '.join(action_verbs[:5])}."
            })

    # Emoji check
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff\u2600-\u27bf]', flags=re.UNICODE)
    if emoji_pattern.search(resume_text):
        fmt_points -= 5
        analysis["formatting_warnings"].append({
            "type": "warning",
            "message": "Avoid emojis or special icons. They can break ATS parsing."
        })

    analysis["breakdown"]["formatting"] = max(0, fmt_points)

    # Total score
    analysis["score"] = (
        analysis["breakdown"]["must_have_keywords"] +
        analysis["breakdown"]["good_to_have_keywords"] +
        analysis["breakdown"]["sections"] +
        analysis["breakdown"]["formatting"]
    )

    # Suggest unused action verbs
    resume_tokens_set = set(resume_tokens)
    for verb in action_verbs:
        if verb.lower() not in resume_tokens_set and len(analysis["verb_suggestions"]) < 6:
            analysis["verb_suggestions"].append(verb)

    return analysis
