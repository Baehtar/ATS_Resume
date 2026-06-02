"""resume_generator.py

Generate ATS-friendly Data Engineering experience using an LLM API with a safe fallback.
"""
import os
import json
import random

def _get_openai_key():
    """Try Streamlit secrets first, then environment variables."""
    try:
        import streamlit as st
        try:
            key = st.secrets.get("openai", {}).get("key")
            if key:
                return key
        except Exception:
            pass
    except Exception:
        pass
    return os.environ.get("OPENAI_API_KEY")


def _get_openai_base():
    """Return an OpenAI-compatible base URL if specified."""
    try:
        import streamlit as st
        try:
            base = st.secrets.get("openai", {}).get("base_url") or st.secrets.get("openai", {}).get("api_base")
            if base:
                return base
        except Exception:
            pass
    except Exception:
        pass
    return os.environ.get("OPENAI_API_BASE")


def _get_openai_model():
    """Return the model name to use for ChatCompletion."""
    try:
        import streamlit as st
        try:
            model = st.secrets.get("openai", {}).get("model")
            if model:
                return model
        except Exception:
            pass
    except Exception:
        pass
    return os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")

BASE_PROMPT = '''You are a Senior Data Engineering Resume Writer and Hiring Manager with 15+ years of experience hiring Data Engineers for companies using Azure, Databricks, Spark, AWS, Snowflake, and modern cloud data platforms.
Your task is to transform my real work experience into highly professional, ATS-friendly, and believable Data Engineer resume bullet points.
Important Rules
NEVER fabricate impossible achievements.
You may intelligently reinterpret my experience from a Data Engineering perspective if it is logically connected.
Every bullet point must sound like actual work performed in a real company.
Use strong action verbs.
Quantify impact whenever possible.
Create a realistic business story behind the work.
Mention relevant stakeholders, business users, reporting teams, analytics teams, operations teams, etc.
If suitable, map my experience to real-world clients or industries.
Wherever possible, incorporate Data Engineering technologies naturally: Databricks, PySpark, Spark SQL, Delta Lake, Azure Data Factory, Azure Data Lake Storage Gen2, Medallion Architecture, Bronze / Silver / Gold Layers, Data Pipelines, ETL / ELT, Incremental Loading, CDC, Data Validation, Data Quality Checks, Data Modeling, Star Schema, Surrogate Keys, SCD Type 1, SCD Type 2, Workflow Automation, SQL, Git, CI/CD, Performance Optimization, Partitioning, Caching, Job Scheduling, Monitoring, Logging, Cloud Infrastructure.
If a domain is provided, create domain-specific business use cases.
If a client name is provided, weave it naturally into the project context (do NOT claim you worked for the client directly).

Create three outputs in JSON with keys: summary, bullets (array of 8-12 strings), project_story (string). Return ONLY valid JSON.
'''


def _call_openai(prompt_text):
    try:
        from openai import OpenAI
    except Exception:
        raise RuntimeError("openai package not installed")

    api_key = _get_openai_key()
    if not api_key:
        raise RuntimeError("API key not found. Set in .streamlit/secrets.toml")
    
    base_url = _get_openai_base()
    model = _get_openai_model()

    client = OpenAI(
        api_key=api_key,
        base_url=base_url or "https://api.openai.com/v1"
    )

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": BASE_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        max_tokens=1500,
        temperature=0.4
    )
    return resp.choices[0].message.content


def _fallback_generation(user_info):
    """A conservative fallback that turns user-provided activities and tools into bullets."""
    verbs = ["engineered","designed","implemented","optimized","automated","orchestrated","built","developed","streamlined","deployed"]
    domain = user_info.get("domain") or "" 
    tools = user_info.get("tools") or ""
    daily = user_info.get("daily_activities") or ""
    client = user_info.get("client") or ""

    bullets = []
    # Try to extract short actionable phrases from daily activities
    fragments = [f.strip() for f in daily.split(".") if f.strip()]
    for i, frag in enumerate(fragments[:8]):
        verb = random.choice(verbs)
        tech = tools.split(",")[0] if tools else "" 
        suffix = f" using {tech}" if tech else ""
        ctx = f" for {client}" if client else ""
        sentence = f"{verb.capitalize()} {frag.strip().rstrip('.')} {suffix}{ctx}."
        bullets.append(sentence)

    # If not enough bullets, add generic ones
    while len(bullets) < 8:
        verb = random.choice(verbs)
        tech = tools.split(",")[0] if tools else "PySpark"
        bullets.append(f"{verb.capitalize()} data pipelines and ETL jobs using {tech} to support {domain or 'business'} reporting.")

    summary = f"Data Engineer with {user_info.get('years','')} years of experience working on {domain or 'data'} projects. Skilled in {tools}."
    project_story = f"Generated project for {client or 'internal stakeholders'}: {summary}"
    return {"summary": summary, "bullets": bullets, "project_story": project_story}


def generate_experience(user_info):
    """Generate resume summary, bullets, and project story from user_info.

    user_info: dict with keys current_role, domain, daily_activities, tools, client, years, target_role
    Returns dict {summary, bullets (list), project_story}
    """
    # Build a compact prompt including the "My Information" block
    info_block = (
        "My Information:\n"
        f"Current Role: {user_info.get('current_role','')}\n"
        f"Industry / Domain: {user_info.get('domain','')}\n"
        f"Daily Activities: {user_info.get('daily_activities','')}\n"
        f"Tools I Actually Use: {user_info.get('tools','')}\n"
        f"Client Name (Optional): {user_info.get('client','')}\n"
        f"Years of Experience: {user_info.get('years','')}\n"
        f"Target Role: {user_info.get('target_role','data_engineer')}\n"
    )

    prompt_text = info_block + "\nPlease return a JSON object with keys: summary, bullets, project_story. bullets should be an array of 8-12 strings."

    api_error = None
    try:
        raw = _call_openai(prompt_text)
        # Try to extract JSON from response
        start = raw.find('{')
        end = raw.rfind('}')
        if start != -1 and end != -1 and end > start:
            js = raw[start:end+1]
            data = json.loads(js)
            bullets = data.get('bullets') or []
            bullets = [b.strip() for b in bullets if b and isinstance(b, str)]
            return {
                "summary": data.get('summary',''),
                "bullets": bullets,
                "project_story": data.get('project_story',''),
                "api_used": True,
                "api_error": None
            }
        api_error = "OpenAI response did not return valid JSON"
    except Exception as exc:
        api_error = str(exc)

    fallback = _fallback_generation(user_info)
    fallback["api_used"] = False
    fallback["api_error"] = api_error
    return fallback
