"""resume_generator.py

Generate ATS-friendly Data Engineering experience using an LLM API with a safe fallback.
"""
import os
import json
import re

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

BASE_PROMPT = '''You are an expert Data Engineering Resume Writer with experience hiring Data Engineers at product companies, consulting firms, and Fortune 500 organizations.

Your task is to transform my actual work experience into highly professional, ATS-friendly, interview-ready Data Engineer experience bullet points.

### Instructions

1. Generate ONLY the Experience Section.
2. Do not create a resume summary, skills section, certifications, or projects.
3. Convert my existing responsibilities into Data Engineering-focused responsibilities wherever logically possible.
4. Maintain realism. Do not invent impossible achievements.
5. Make the experience sound genuine and believable to an experienced interviewer.
6. Use strong action verbs and professional corporate language.
7. Write each bullet point as if it was performed in a production environment.
8. Include measurable business impact whenever reasonable.
9. Create a coherent business story behind the work instead of listing random technologies.
10. If a client name is provided, naturally incorporate it into the experience.
11. If a domain is provided, create domain-specific data engineering use cases.
12. Focus heavily on:

* Databricks
* PySpark
* Spark SQL
* Delta Lake
* Azure Data Factory
* Azure Data Lake Storage Gen2
* Medallion Architecture
* ETL / ELT Pipelines
* Incremental Loading
* CDC
* Data Quality Frameworks
* Workflow Orchestration
* Data Validation
* Data Modeling
* Star Schema
* SCD Type 1 / Type 2
* Partitioning
* Performance Optimization
* Monitoring & Logging
* SQL
* Cloud Data Platforms
* CI/CD
* Data Governance
* Reporting Enablement

### Writing Style

* Write 2–6 bullet points.
* Every bullet should sound like real production work.
* Avoid generic phrases like:

  * "Worked on Databricks"
  * "Used PySpark"
  * "Responsible for data engineering"

Instead write contextual business-focused statements such as:

"Designed and maintained PySpark-based transformation pipelines within Databricks to process high-volume retail transaction data, supporting downstream inventory and sales analytics."

### Important

If my current experience has no direct Data Engineering exposure, intelligently reinterpret transferable responsibilities from a Data Engineering perspective while staying believable.

For example:

Sales Analyst → Customer Analytics Data Pipelines

Operations Executive → Operational Reporting & Data Integration

MIS Executive → Data Warehousing & Reporting Automation

Business Analyst → Data Transformation & Reporting Pipelines

Excel Reporting → ETL Automation & Analytics Enablement

### Input

Company:
[PASTE]

Designation:
[PASTE]

Industry/Domain:
[PASTE]

Client (if any):
[PASTE]

Actual Responsibilities:
[PASTE]

Tools Used:
[PASTE]

Years of Experience:
[PASTE]

### Output Format

Company Name | Designation | Duration

• Bullet Point 1

• Bullet Point 2

• Bullet Point 3

...

Generate only the Experience Section in ATS-friendly resume format.'''

SUMMARY_PROMPT = '''You are an expert Data Engineering Resume Writer with experience hiring Data Engineers at product companies, consulting firms, and Fortune 500 organizations.

Your task is to write a strong, ATS-friendly professional resume summary based on the candidate profile and experience details.

Return only valid JSON with a key named summary.''' 


def _call_openai(prompt_text, system_prompt=None):
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
            {"role": "system", "content": system_prompt or BASE_PROMPT},
            {"role": "user", "content": prompt_text}
        ],
        max_tokens=1500,
        temperature=0.4
    )
    return resp.choices[0].message.content


def _parse_openai_json(raw_text):
    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start == -1 or end == -1 or start >= end:
        raise ValueError("OpenAI response did not return valid JSON")
    return json.loads(raw_text[start:end+1])


def _fallback_generation(user_info):
    """A conservative fallback that turns user-provided activities and tools into bullets."""
    verbs = ["Engineered","Designed","Implemented","Optimized","Automated","Orchestrated","Built","Developed","Streamlined","Deployed"]
    domain = user_info.get("domain") or ""
    tools = user_info.get("tools") or ""
    daily = user_info.get("daily_activities") or ""
    client = user_info.get("client") or ""

    primary_tool = tools.split(",")[0].strip() if tools else "PySpark"
    client_ctx = f" for {client.strip()}" if client.strip() else ""

    bullets = []
    # Split on periods or newlines, keep only non-trivial fragments
    fragments = [f.strip(" .\n") for f in re.split(r'[.\n]+', daily) if f.strip(" .\n")]
    for i, frag in enumerate(fragments[:4]):
        verb = verbs[i % len(verbs)]
        # Ensure the fragment doesn't start with a lowercase verb that duplicates our prefix
        clean_frag = frag[0].lower() + frag[1:] if frag else frag
        sentence = f"{verb} {clean_frag} using {primary_tool}{client_ctx}."
        bullets.append(sentence)

    # If not enough bullets, add generic data-focused ones
    generic = [
        f"Designed and maintained data pipelines using {primary_tool} to support {domain or 'business'} analytics.",
        f"Automated ETL workflows with {primary_tool}, reducing manual processing time significantly.",
        f"Validated data quality and implemented monitoring checks for {domain or 'production'} data flows.",
        f"Collaborated with stakeholders to translate {domain or 'business'} requirements into data solutions.",
    ]
    while len(bullets) < 4:
        bullets.append(generic[len(bullets)])

    summary = f"Data professional with {user_info.get('years','several')} years of experience in {domain or 'data'} projects. Skilled in {tools or primary_tool}."
    project_story = f"Built end-to-end data solutions{client_ctx} in the {domain or 'data'} domain: {summary}"
    return {"summary": summary, "bullets": bullets, "project_story": project_story}


def _fallback_summary(personal, experience, target_role):
    name = personal.get("fullName", "").strip()
    title = personal.get("headline", "").strip() or target_role.replace("_", " ").title()
    exp_count = len(experience)
    summary = (
        f"{title} with {exp_count} experience entries and a strong focus on {target_role.replace('_', ' ')}. "
        f"Skilled at translating technical work into business impact and building ATS-friendly resumes."
    )
    if name:
        summary = f"{name} is {summary}"
    return {"summary": summary}


def generate_entry_bullets(entry_info):
    """Generate 2-6 ATS-friendly bullet points for one experience entry."""
    prompt_text = (
        f"Company:\n{entry_info.get('company','')}\n"
        f"Designation:\n{entry_info.get('role','')}\n"
        f"Industry/Domain:\n{entry_info.get('domain','')}\n"
        f"Client (if any):\n{entry_info.get('client','')}\n"
        f"Actual Responsibilities:\n{entry_info.get('details','')}\n"
        f"Tools Used:\n{entry_info.get('tools','')}\n"
        f"Years of Experience:\n{entry_info.get('years','')}\n"
        f"Target Role:\n{entry_info.get('target_role','data_engineer')}\n\n"
        "Please generate 2-6 ATS-friendly experience bullet points for this role. "
        "Return valid JSON only with a key named bullets containing an array of strings."
    )

    api_error = None
    try:
        raw = _call_openai(prompt_text)
        data = _parse_openai_json(raw)
        bullets = data.get('bullets') or []
        bullets = [b.strip() for b in bullets if b and isinstance(b, str)]
        return {"bullets": bullets, "api_used": True, "api_error": None}
    except Exception as exc:
        api_error = str(exc)

    fallback = _fallback_generation({
        "daily_activities": entry_info.get('details', ''),
        "tools": entry_info.get('tools', ''),
        "client": entry_info.get('client', entry_info.get('company', '')),
        "domain": entry_info.get('domain', ''),
        "years": entry_info.get('years', '')
    })
    return {"bullets": fallback.get('bullets', []), "api_used": False, "api_error": api_error}


def generate_professional_summary(profile_statement, personal, experience, education, projects, skills, target_role):
    """Generate a professional summary from the full resume profile and content."""
    experience_summary = "\n".join(
        [f"{exp.get('role','')} at {exp.get('company','')}" for exp in experience if exp.get('role') or exp.get('company')]
    )
    
    education_summary = "\n".join(
        [f"{edu.get('degree','')} from {edu.get('school','')}" for edu in education if edu.get('degree') or edu.get('school')]
    )
    
    projects_summary = "\n".join(
        [f"{proj.get('name','')} ({proj.get('tech','')})" for proj in projects if proj.get('name')]
    )
    
    skills_summary = "\n".join(
        [f"{s.get('category','')} | {s.get('list','')}" for s in skills if s.get('list')]
    )
    
    prompt_text = (
        "You are an expert Data Engineering Resume Writer with experience hiring Data Engineers at product companies, consulting firms, and Fortune 500 organizations. "
        "Write a strong professional resume summary based on the complete candidate profile below. "
        "Use concise, ATS-friendly language and highlight transferable technical strengths, impact, and role fit. "
        "Return only valid JSON with a key named summary.\n\n"
        f"Profile Headline:\n{personal.get('headline','')}\n"
        f"Current Profile Statement:\n{profile_statement}\n"
        f"Experience:\n{experience_summary}\n"
        f"Education:\n{education_summary}\n"
        f"Projects:\n{projects_summary}\n"
        f"Skills:\n{skills_summary}\n"
        f"Target Role:\n{target_role}\n"
    )

    api_error = None
    try:
        raw = _call_openai(prompt_text, system_prompt=SUMMARY_PROMPT)
        data = _parse_openai_json(raw)
        return {"summary": data.get('summary', '').strip(), "api_used": True, "api_error": None}
    except Exception as exc:
        api_error = str(exc)

    fallback = _fallback_summary(personal, experience, target_role)
    fallback["api_used"] = False
    fallback["api_error"] = api_error
    return fallback


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
        data = _parse_openai_json(raw)
        bullets = data.get('bullets') or []
        bullets = [b.strip() for b in bullets if b and isinstance(b, str)]
        return {
            "summary": data.get('summary',''),
            "bullets": bullets,
            "project_story": data.get('project_story',''),
            "api_used": True,
            "api_error": None
        }
    except Exception as exc:
        api_error = str(exc)

    fallback = _fallback_generation(user_info)
    fallback["api_used"] = False
    fallback["api_error"] = api_error
    return fallback
