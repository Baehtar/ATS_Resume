# app.py -(Streamlit Frontend)
import streamlit as st
import base64
import json
from html import escape
from io import BytesIO
from weasyprint import HTML

import resume_templates
import ats_analyzer
import resume_generator
from job_db import MOCK_JOB_LISTINGS
from prep_db import INTERVIEW_QUESTIONS
import portal_db_client as db_client

TEMPLATE_OPTIONS = {
    "modern": "Modern",
    "professional": "Professional",
    "graduate": "Graduate / Fresher",
    "executive": "Executive",
}


# ─────────────────────────────────────────────────
# 1. PAGE CONFIG & GLOBAL STYLING
# ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Console Flare — ATS Resume Builder & Interview Prep",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Hide Streamlit toolbar */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Custom badge styles */
    .kw-must-matched {
        display:inline-block; background:rgba(16,185,129,0.12); color:#10b981;
        padding:4px 12px; margin:3px; border-radius:20px; font-size:0.82rem;
        border:1px solid rgba(16,185,129,0.25); font-weight:500;
    }
    .kw-must-missing {
        display:inline-block; background:rgba(239,68,68,0.12); color:#ef4444;
        padding:4px 12px; margin:3px; border-radius:20px; font-size:0.82rem;
        border:1px solid rgba(239,68,68,0.25); font-weight:500;
    }
    .kw-good-matched {
        display:inline-block; background:rgba(59,130,246,0.12); color:#3b82f6;
        padding:4px 12px; margin:3px; border-radius:20px; font-size:0.82rem;
        border:1px solid rgba(59,130,246,0.25); font-weight:500;
    }
    .kw-good-missing {
        display:inline-block; background:rgba(251,191,36,0.12); color:#d97706;
        padding:4px 12px; margin:3px; border-radius:20px; font-size:0.82rem;
        border:1px solid rgba(251,191,36,0.25); font-weight:500;
    }
    .verb-badge {
        display:inline-block; background:rgba(139,92,246,0.12); color:#8b5cf6;
        padding:4px 12px; margin:3px; border-radius:20px; font-size:0.82rem;
        border:1px solid rgba(139,92,246,0.25); font-weight:500;
    }
    .warn-box {
        padding:10px 16px; border-radius:8px; margin-bottom:8px; font-size:0.88rem;
    }
    .warn-error {
        background:rgba(239,68,68,0.08); border-left:4px solid #ef4444; color:#f87171;
    }
    .warn-warning {
        background:rgba(245,158,11,0.08); border-left:4px solid #f59e0b; color:#fbbf24;
    }
    .job-card {
        background:rgba(30,41,59,0.05); border:1px solid rgba(148,163,184,0.2);
        border-radius:12px; padding:20px; margin-bottom:16px;
    }
    .job-tag {
        display:inline-block; background:rgba(99,102,241,0.1); color:#6366f1;
        padding:3px 10px; margin:2px; border-radius:12px; font-size:0.78rem;
        font-weight:500;
    }
    .difficulty-easy { color:#10b981; font-weight:600; }
    .difficulty-medium { color:#f59e0b; font-weight:600; }
    .difficulty-hard { color:#ef4444; font-weight:600; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# 2. SESSION STATE & AUTHENTICATION
# ─────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None
if "resume_loaded_from_db" not in st.session_state:
    st.session_state.resume_loaded_from_db = False
if "resume" not in st.session_state:
    st.session_state.resume = resume_templates.get_empty_schema()
if "target_role" not in st.session_state:
    st.session_state.target_role = "data_engineer"

# List of batches for selection
BATCH_OPTIONS = [
    "Select your batch...",
    "Data Science Fellowship - Jan 2026",
    "Data Science Fellowship - Mar 2026",
    "Data Engineering Bootcamp - Jan 2026",
    "Data Engineering Bootcamp - Mar 2026",
    "Generative AI Specialist - Feb 2026"
]
COURSE_OPTIONS = ["Select your course...", "Data Engineer", "Data Analyst"]

# Check if user is logged in
if st.session_state.user is None:
    supabase_ready = db_client.is_configured()
    
    st.markdown("<h2 style='text-align: center; margin-top: 30px; color: #3b82f6;'>🚀 Console Flare Portal</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Sign in to access your ATS Resume Builder & Career Tools</p>", unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 1.8, 1])
    
    with col_b:
        if not supabase_ready:
            st.warning("⚠️ **Supabase Connection Pending**")
            st.markdown(
                "Please configure your Supabase URL and Key in `.streamlit/secrets.toml` to activate user authentication. "
                "You can copy `.streamlit/secrets.toml.example` to get started."
            )
            if st.button("🔓 Enter Demo Mode (Skip Auth)", type="primary", use_container_width=True):
                st.session_state.user = {
                    "id": "demo-user",
                    "email": "student@demo.com",
                    "user_metadata": {
                        "name": "Demo Student",
                        "batch": "Data Science Fellowship - Jan 2026",
                        "course": "Data Engineer"
                    }
                }
                st.toast("Entered Demo Mode!", icon="🔓")
                st.rerun()
            st.stop()
            
        auth_tab_in, auth_tab_up = st.tabs(["🔒 Sign In", "📝 Sign Up"])
        
        with auth_tab_in:
            st.markdown("#### Student Login")
            login_email = st.text_input("Email Address", placeholder="student@email.com", key="login_email")
            login_pass = st.text_input("Password", type="password", placeholder="••••••••", key="login_pass")
            
            # Forgot password flow
            if st.button("Forgot Password", type="secondary", use_container_width=True):
                if not login_email:
                    st.warning("Please enter your email to reset password.")
                else:
                    fp_res = db_client.reset_password_student(login_email)
                    if fp_res.get("error"):
                        st.error(fp_res["error"])
                    else:
                        st.success("Password reset email sent. Check your inbox.")
            
            if st.button("Log In", type="primary", use_container_width=True):
                if not login_email or not login_pass:
                    st.error("Please enter both email and password.")
                else:
                    res = db_client.sign_in_student(login_email, login_pass)
                    if res["error"]:
                        st.error(res["error"])
                    else:
                        st.session_state.user = res["user"]
                        st.session_state.resume_loaded_from_db = False
                        st.toast("Logged in successfully!", icon="👋")
                        st.rerun()
                        
        with auth_tab_up:
            st.markdown("#### Register Student Account")
            reg_name = st.text_input("Full Name", placeholder="Alex Mercer", key="reg_name")
            reg_email = st.text_input("Email Address", placeholder="student@email.com", key="reg_email")
            reg_batch = st.selectbox("Batch Name/Number", options=BATCH_OPTIONS, key="reg_batch")
            reg_course = st.selectbox("Course Name", options=COURSE_OPTIONS, key="reg_course")
            reg_pass = st.text_input("Password (min 6 characters)", type="password", placeholder="••••••••", key="reg_pass")
            reg_pass_conf = st.text_input("Confirm Password", type="password", placeholder="••••••••", key="reg_pass_conf")
            
            if st.button("Create Account", type="primary", use_container_width=True):
                if not reg_name or not reg_email or reg_batch == BATCH_OPTIONS[0] or reg_course == COURSE_OPTIONS[0] or not reg_pass or not reg_pass_conf:
                    st.error("Please fill in all fields and select a batch and course.")
                elif reg_pass != reg_pass_conf:
                    st.error("Passwords do not match.")
                elif len(reg_pass) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    res = db_client.sign_up_student(reg_email, reg_pass, reg_name, reg_batch, reg_course)
                    if res["error"]:
                        st.error(res["error"])
                    else:
                        st.success("Registration successful! Please sign in using the 'Sign In' tab.")
                        st.balloons()
    st.stop()
# Helper: Convert HTML to PDF bytes
def compile_pdf(html_content):
    try:
        return HTML(string=html_content).write_pdf()
    except Exception:
        return None


def show_pdf_preview(pdf_bytes, width=620):
    height = round(width * 1.414)
    encoded_pdf = base64.b64encode(pdf_bytes).decode("ascii")
    st.components.v1.html(
        f"""
        <div style="display:flex; justify-content:center; background:#eef2f7; padding:16px;">
            <object
                data="data:application/pdf;base64,{encoded_pdf}"
                type="application/pdf"
                width="{width}"
                height="{height}"
                style="max-width:100%; background:white; box-shadow:0 2px 10px rgba(0,0,0,0.15);"
            >
                <p>PDF preview is unavailable in this browser. Use the download button below.</p>
            </object>
        </div>
        """,
        height=height + 40,
        scrolling=True,
    )


def show_resume_preview(html_content, width=620):
    height = round(width * 1.414)
    encoded_html = base64.b64encode(html_content.encode("utf-8")).decode("ascii")
    st.components.v1.html(
        f"""
        <div style="display:flex; justify-content:center; background:#eef2f7; padding:16px;">
            <iframe
                src="data:text/html;base64,{encoded_html}"
                width="{width}"
                height="{height}"
                style="max-width:100%; border:0; background:white; box-shadow:0 2px 10px rgba(0,0,0,0.15);"
            ></iframe>
        </div>
        """,
        height=height + 40,
        scrolling=True,
    )


# ─────────────────────────────────────────────────
# ADMIN DASHBOARD
# ─────────────────────────────────────────────────
def show_admin_dashboard():
    st.markdown("<h2 style='color:#3b82f6;'>🛡️ Admin Dashboard</h2>", unsafe_allow_html=True)
    
    client = db_client.get_supabase_client()
    
    # Fetch all profiles
    try:
        profiles = client.table("profiles").select("*").execute()
        students = [p for p in profiles.data if p.get("role") == "student"]
    except Exception as e:
        st.error(f"Could not fetch students: {e}")
        return

    st.markdown(f"### 👥 Registered Students ({len(students)})")
    course_filter = st.selectbox("Filter by Course", ["All", "Data Engineer", "Data Analyst"], key="admin_course_filter")
    if course_filter != "All":
        students = [student for student in students if student.get("course") == course_filter]
    st.caption(f"Showing {len(students)} students")
    st.markdown("---")

    for student in students:
        col1, col2, col3, col4 = st.columns([2, 2, 1.5, 1])
        with col1:
            st.markdown(f"**{student.get('name', 'N/A')}**")
        with col2:
            st.markdown(f"{student.get('batch', 'N/A')}")
        with col3:
            st.markdown(f"{student.get('course', 'N/A')}")
        with col4:
            if st.button("View Resume", key=f"view_{student['id']}"):
                st.session_state["viewing_student"] = student["id"]
                st.session_state["viewing_name"] = student.get("name", "Student")

    # Show selected student's resume
    if "viewing_student" in st.session_state:
        st.markdown("---")
        st.markdown(f"### 📄 Resume — {st.session_state['viewing_name']}")
        resume = db_client.load_resume(st.session_state["viewing_student"])
        if resume:
            template_id = st.selectbox(
                "Template",
                options=list(TEMPLATE_OPTIONS),
                format_func=lambda template: TEMPLATE_OPTIONS[template],
                key="admin_tmpl",
            )
            html = resume_templates.generate_resume_html(resume, template_id)
            pdf_data = compile_pdf(html)
            if pdf_data:
                safe_name = st.session_state["viewing_name"].lower().replace(" ", "_")
                st.download_button(
                    "🖨 Download Student Resume PDF",
                    data=pdf_data,
                    file_name=f"{safe_name}_resume.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            else:
                st.warning("PDF download unavailable.")
            show_resume_preview(html)
        else:
            st.info("This student hasn't saved a resume yet.")

    st.markdown("---")
    if st.button("🚪 Sign Out", use_container_width=True):
        db_client.sign_out_student()
        st.session_state.user = None
        st.session_state.resume_loaded_from_db = False
        st.rerun()
# Greeting display
if st.session_state.user:
    # Support both dict and Supabase User object
    if isinstance(st.session_state.user, dict):
        metadata = st.session_state.user.get("user_metadata", {})
    else:
        metadata = getattr(st.session_state.user, "user_metadata", {})
    user_name = metadata.get("name", "Student")
    col_left, col_right = st.columns([0.8, 0.2])
    with col_right:
        st.markdown(
            f"<div style='text-align: right; font-size:1.2rem; color:#3b82f6;'>👋 Hello {user_name}</div>",
            unsafe_allow_html=True,
        )
# Auto load user resume from database once logged in
if st.session_state.user and not st.session_state.resume_loaded_from_db:
    user_id = st.session_state.user.get("id") if isinstance(st.session_state.user, dict) else getattr(st.session_state.user, "id", None)
    if user_id and user_id != "demo-user":
        db_resume = db_client.load_resume(user_id)
        if db_resume:
            st.session_state.resume = db_resume
            st.toast("CV loaded from Supabase!", icon="☁️")
    st.session_state.resume_loaded_from_db = True

# Route admin vs student
user_id = st.session_state.user.get("id") if isinstance(st.session_state.user, dict) else getattr(st.session_state.user, "id", None)
role = db_client.get_user_role(user_id)
if role == "admin":
    show_admin_dashboard()
    st.stop()

# ─────────────────────────────────────────────────
# 3. SIDEBAR — BRANDING & GLOBAL CONTROLS
# ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚀 Console Flare")
    st.caption("Your launchpad to data science careers")
    st.markdown("---")

    st.markdown("### 🎯 Target Role")
    role_keywords = ats_analyzer.load_role_keywords()
    role_options = {k: v.get("title", k) for k, v in role_keywords.items()}
    st.session_state.target_role = st.selectbox(
        "I am applying for:",
        options=list(role_options.keys()),
        format_func=lambda x: role_options[x],
        index=list(role_options.keys()).index(st.session_state.target_role)
            if st.session_state.target_role in role_options else 0
    )

    st.markdown("---")
    st.markdown("### 📂 Resume Data")

    def reset_resume_editor_widgets():
        editor_prefixes = (
            "cv_", "ec_", "el_", "er_", "es_", "ee_", "eb_", "edsc_", "eddg_",
            "edlo_", "eddt_", "edde_", "pn_", "pt_", "pl_", "pd_", "sc_", "sl_",
            "cn_", "ci_", "cd_",
        )
        for key in list(st.session_state):
            if key.startswith(editor_prefixes):
                del st.session_state[key]

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Load Sample", use_container_width=True):
            reset_resume_editor_widgets()
            st.session_state.resume = resume_templates.get_default_sample()
            st.toast("Sample resume loaded!", icon="📂")
            st.rerun()
    with col2:
        if st.button("Clear All", use_container_width=True, type="primary"):
            reset_resume_editor_widgets()
            st.session_state.resume = resume_templates.get_empty_schema()
            st.toast("Resume cleared!", icon="🗑")
            st.rerun()
    if st.button("✨ Create Ideal Resume Template", use_container_width=True):
        reset_resume_editor_widgets()
        st.session_state.resume = resume_templates.get_ideal_template(st.session_state.target_role)
        st.toast("Ideal resume template created!", icon="✨")
        st.rerun()

    # JSON backup
    st.markdown("---")
    json_str = json.dumps(st.session_state.resume, indent=2)
    st.download_button(
        "💾 Download JSON Backup", data=json_str,
        file_name="resume_backup.json", mime="application/json",
        use_container_width=True
    )
    uploaded = st.file_uploader("📥 Import JSON Backup", type=["json"])
    if uploaded:
        try:
            data = json.load(uploaded)
            if "personal" in data:
                st.session_state.resume = data
                st.success("Imported successfully!")
                st.rerun()
            else:
                st.error("Invalid resume JSON format.")
        except Exception:
            st.error("Could not parse JSON file.")

    # Cloud Save section
    st.markdown("---")
    st.markdown("### ☁️ Cloud Storage")
    user_id = st.session_state.user.get("id") if isinstance(st.session_state.user, dict) else getattr(st.session_state.user, "id", None)
    if user_id == "demo-user":
        st.warning("Running in Demo Mode. Cloud saving is disabled.")
    else:
        if st.button("💾 Save Resume to Cloud", type="primary", use_container_width=True):
            with st.spinner("Saving to Supabase..."):
                save_result = db_client.save_resume(user_id, st.session_state.resume)
                if save_result["ok"]:
                    st.success("Resume saved successfully!")
                else:
                    st.error(f"Failed to save resume: {save_result['error']}")

    # Student Profile section
    st.markdown("---")
    st.markdown("### 👤 Student Profile")
    metadata = st.session_state.user.get("user_metadata", {}) if isinstance(st.session_state.user, dict) else getattr(st.session_state.user, "user_metadata", {})
    user_email = st.session_state.user.get("email") if isinstance(st.session_state.user, dict) else getattr(st.session_state.user, "email", "")
    
    st.markdown(f"**Name:** {metadata.get('name', 'Student')}")
    st.markdown(f"**Email:** {user_email}")
    st.markdown(f"**Batch:** {metadata.get('batch', 'N/A')}")
    st.markdown(f"**Course:** {metadata.get('course', 'N/A')}")
    
    st.markdown("---")
    if st.button("🚪 Sign Out", use_container_width=True):
        db_client.sign_out_student()
        st.session_state.user = None
        st.session_state.resume_loaded_from_db = False
        st.rerun()

    

# ─────────────────────────────────────────────────
# 4. MAIN CONTENT — THREE TABS
# ─────────────────────────────────────────────────
tab_cv, tab_jobs, tab_prep = st.tabs([
    "📝 My CV",
    "🔍 Job Openings",
    "🎓 Interview Prep"
])

# ═══════════════════════════════════════════════════
# TAB 1: MY CV — Resume Builder + ATS Optimizer
# ═══════════════════════════════════════════════════
with tab_cv:
    col_form, col_right = st.columns([1.1, 0.9])

    # ── LEFT: Form Editor ──
    with col_form:
        st.subheader(f"Resume Editor — {role_options.get(st.session_state.target_role, 'Role')}")

        # Personal Details
        with st.expander("👤 Personal Details", expanded=True):
            st.session_state.resume["personal"]["fullName"] = st.text_input(
                "Full Name", value=st.session_state.resume["personal"].get("fullName", ""), key="cv_name")
            st.session_state.resume["personal"]["headline"] = st.text_input(
                "Professional Headline", value=st.session_state.resume["personal"].get("headline", ""), key="cv_headline",
                placeholder="Data Engineer | Data Pipelines | ETL Processes")
            c1, c2 = st.columns(2)
            with c1:
                st.session_state.resume["personal"]["email"] = st.text_input(
                    "Email", value=st.session_state.resume["personal"].get("email", ""), key="cv_email")
            with c2:
                st.session_state.resume["personal"]["phone"] = st.text_input(
                    "Phone", value=st.session_state.resume["personal"].get("phone", ""), key="cv_phone")
            st.session_state.resume["personal"]["location"] = st.text_input(
                "Location", value=st.session_state.resume["personal"].get("location", ""), key="cv_loc")
            c3, c4 = st.columns(2)
            with c3:
                st.session_state.resume["personal"]["linkedin"] = st.text_input(
                    "LinkedIn", value=st.session_state.resume["personal"].get("linkedin", ""), key="cv_li")
            with c4:
                st.session_state.resume["personal"]["github"] = st.text_input(
                    "GitHub", value=st.session_state.resume["personal"].get("github", ""), key="cv_gh")
            st.session_state.resume["personal"]["website"] = st.text_input(
                "Portfolio / Website", value=st.session_state.resume["personal"].get("website", ""), key="cv_web")

        # Summary
        with st.expander("✍ Professional Summary", expanded=False):
            st.session_state.resume["summary"] = st.text_area(
                "Profile Statement", value=st.session_state.resume.get("summary", ""),
                height=100, key="cv_sum",
                placeholder="Highlight your data science expertise, tools you use, and quantified achievements...")
            if st.button("Generate Professional Summary (AI)", key="gen_summary"):
                with st.spinner("Generating professional summary..."):
                    gen_summary = resume_generator.generate_professional_summary(
                        st.session_state.resume["personal"],
                        st.session_state.resume.get("experience", []),
                        st.session_state.target_role
                    )
                    if gen_summary.get("summary"):
                        st.session_state.resume["summary"] = gen_summary["summary"]
                        if gen_summary.get("api_used"):
                            st.success("Professional summary generated by OpenAI.")
                        else:
                            st.warning("Fallback summary generated; OpenAI API unavailable.")
                    else:
                        st.error("Could not generate a professional summary.")
                st.rerun()

        # Work Experience
        with st.expander("💼 Work / Internship Experience", expanded=False):
            st.markdown("#### ✨ AI Experience Generator")
            st.markdown("Provide concise details and click 'Generate Entry' to create ATS-friendly bullets for one experience entry.")
            ai_col1, ai_col2 = st.columns(2)
            with ai_col1:
                ai_current_role = st.text_input("Current Role:", value="", key="ai_current_role")
                ai_domain = st.text_input("Industry / Domain:", value="", key="ai_domain",
                                          placeholder="e.g. Retail, Healthcare, Banking")
                ai_years = st.text_input("Years of Experience:", value="", key="ai_years")
            with ai_col2:
                ai_daily = st.text_area("Daily Activities (short):", value="", key="ai_daily", height=80,
                                        placeholder="What you do day-to-day (brief)")
                ai_tools = st.text_input("Tools I Actually Use:", value="", key="ai_tools",
                                         placeholder="e.g. PySpark, Databricks, Azure Data Factory")
                ai_client = st.text_input("Client Name (optional):", value="", key="ai_client",
                                          placeholder="Optional client or project name")

            if st.button("Generate Entry", key="gen_ai_exp"):
                entry_info = {
                    "company": ai_client or "Generated Project",
                    "role": ai_current_role or st.session_state.resume["personal"].get("headline", ""),
                    "domain": ai_domain,
                    "client": ai_client,
                    "details": ai_daily,
                    "tools": ai_tools,
                    "years": ai_years or "",
                    "target_role": "data_engineer"
                }
                with st.spinner("Generating entry bullets via AI..."):
                    try:
                        gen = resume_generator.generate_entry_bullets(entry_info)
                    except Exception as e:
                        st.error(f"AI generation failed: {e}")
                        gen = None

                if gen:
                    bullets = gen.get("bullets") or []
                    exp_entry = {"company": entry_info["company"],
                                 "role": entry_info.get("role", ""),
                                 "location": "",
                                 "startDate": "",
                                 "endDate": "",
                                 "bullets": bullets}
                    st.session_state.resume["experience"] = [exp_entry]
                    if gen.get("api_used"):
                        st.success("Entry bullets generated by OpenAI.")
                    else:
                        st.warning("Fallback bullets generated; OpenAI API unavailable.")
                    st.rerun()

            exp_list = st.session_state.resume.get("experience", [])
            if st.button("+ Add Experience Entry", use_container_width=True, key="add_exp"):
                exp_list.append({"company":"","role":"","location":"","startDate":"","endDate":"","bullets":[""]})
                st.session_state.resume["experience"] = exp_list
                st.rerun()
            for i, exp in enumerate(exp_list):
                st.markdown(f"**Entry {i+1}**")
                c1, c2 = st.columns(2)
                with c1:
                    exp["company"] = st.text_input("Company", value=exp.get("company",""), key=f"ec_{i}")
                with c2:
                    exp["location"] = st.text_input("Location", value=exp.get("location",""), key=f"el_{i}")
                c3, c4 = st.columns(2)
                with c3:
                    exp["role"] = st.text_input("Role/Title", value=exp.get("role",""), key=f"er_{i}")
                with c4:
                    d1, d2 = st.columns(2)
                    with d1:
                        exp["startDate"] = st.text_input("Start", value=exp.get("startDate",""), key=f"es_{i}", placeholder="YYYY-MM")
                    with d2:
                        exp["endDate"] = st.text_input("End", value=exp.get("endDate",""), key=f"ee_{i}", placeholder="Present")
                st.markdown("*Bullet points (use action verbs + metrics)*")
                bullets = exp.get("bullets", [])
                for bi, b in enumerate(bullets):
                    bc1, bc2 = st.columns([0.92, 0.08])
                    with bc1:
                        bullets[bi] = st.text_input(f"Bullet", value=b, key=f"eb_{i}_{bi}", label_visibility="collapsed",
                                                    placeholder="Engineered a data pipeline that reduced latency by 40%...")
                    with bc2:
                        if st.button("✖", key=f"rb_{i}_{bi}"):
                            bullets.pop(bi); st.rerun()
                cb1, cb2 = st.columns(2)
                with cb1:
                    if st.button("+ Bullet", key=f"ab_{i}"):
                        bullets.append(""); st.rerun()
                with cb2:
                    if st.button("🗑 Delete Entry", key=f"de_{i}"):
                        exp_list.pop(i); st.rerun()
                st.markdown("---")

        # Education
        with st.expander("🎓 Education", expanded=False):
            edu_list = st.session_state.resume.get("education", [])
            if st.button("+ Add Education", use_container_width=True, key="add_edu"):
                edu_list.append({"school":"","degree":"","location":"","date":"","details":""})
                st.session_state.resume["education"] = edu_list
                st.rerun()
            for i, edu in enumerate(edu_list):
                c1, c2 = st.columns(2)
                with c1:
                    edu["school"] = st.text_input("School", value=edu.get("school",""), key=f"edsc_{i}")
                with c2:
                    edu["degree"] = st.text_input("Degree", value=edu.get("degree",""), key=f"eddg_{i}")
                c3, c4 = st.columns(2)
                with c3:
                    edu["location"] = st.text_input("Location", value=edu.get("location",""), key=f"edlo_{i}")
                with c4:
                    edu["date"] = st.text_input("Dates", value=edu.get("date",""), key=f"eddt_{i}")
                edu["details"] = st.text_input("Details (GPA, Honors)", value=edu.get("details",""), key=f"edde_{i}")
                if st.button("🗑 Delete", key=f"deled_{i}"):
                    edu_list.pop(i); st.rerun()
                st.markdown("---")

        # Projects
        with st.expander("💻 Projects", expanded=False):
            proj_list = st.session_state.resume.get("projects", [])
            if st.button("+ Add Project", use_container_width=True, key="add_proj"):
                proj_list.append({"name":"","tech":"","link":"","description":""})
                st.session_state.resume["projects"] = proj_list
                st.rerun()
            for i, proj in enumerate(proj_list):
                c1, c2 = st.columns(2)
                with c1:
                    proj["name"] = st.text_input("Project Name", value=proj.get("name",""), key=f"pn_{i}")
                with c2:
                    proj["tech"] = st.text_input("Tech Stack", value=proj.get("tech",""), key=f"pt_{i}")
                proj["link"] = st.text_input("Link", value=proj.get("link",""), key=f"pl_{i}")
                proj["description"] = st.text_area("Description", value=proj.get("description",""), key=f"pd_{i}", height=70)
                if st.button("🗑 Delete", key=f"delpr_{i}"):
                    proj_list.pop(i); st.rerun()
                st.markdown("---")

        # Skills
        with st.expander("🛠 Skills", expanded=False):
            skills_list = st.session_state.resume.get("skills", [])
            if st.button("+ Add Skill Group", use_container_width=True, key="add_sk"):
                skills_list.append({"category":"","list":""})
                st.session_state.resume["skills"] = skills_list
                st.rerun()
            for i, s in enumerate(skills_list):
                s["category"] = st.text_input("Group Name", value=s.get("category",""), key=f"sc_{i}")
                s["list"] = st.text_input("Skills (comma separated)", value=s.get("list",""), key=f"sl_{i}")
                if st.button("🗑 Delete", key=f"delsk_{i}"):
                    skills_list.pop(i); st.rerun()
                st.markdown("---")

        # Certifications
        with st.expander("📜 Certifications", expanded=False):
            cert_list = st.session_state.resume.get("certifications", [])
            if st.button("+ Add Certification", use_container_width=True, key="add_cert"):
                cert_list.append({"name":"","issuer":"","date":""})
                st.session_state.resume["certifications"] = cert_list
                st.rerun()
            for i, c in enumerate(cert_list):
                c["name"] = st.text_input("Title", value=c.get("name",""), key=f"cn_{i}")
                cc1, cc2 = st.columns(2)
                with cc1:
                    c["issuer"] = st.text_input("Issuer", value=c.get("issuer",""), key=f"ci_{i}")
                with cc2:
                    c["date"] = st.text_input("Date", value=c.get("date",""), key=f"cd_{i}")
                if st.button("🗑 Delete", key=f"delce_{i}"):
                    cert_list.pop(i); st.rerun()
                st.markdown("---")

    # ── RIGHT: ATS Score + Preview ──
    with col_right:
        sub_score, sub_preview = st.tabs(["🎯 ATS Keyword Audit", "📄 Preview & Download"])

        with sub_score:
            report = ats_analyzer.analyze_resume(st.session_state.resume, st.session_state.target_role)
            score = report["score"]

            # Score display
            st.markdown(f"### ATS Optimization Score")
            cs1, cs2 = st.columns([0.35, 0.65])
            with cs1:
                st.metric("Score", f"{score} / 100")
                if score >= 75:
                    st.success("Strong Match! 🎉")
                elif score >= 50:
                    st.warning("Moderate — needs refinement")
                else:
                    st.error("Weak — add more keywords")
            with cs2:
                st.markdown(f"""
                | Component | Score |
                |---|---|
                | Must-Have Keywords | **{report['breakdown']['must_have_keywords']}** / 40 |
                | Good-to-Have Keywords | **{report['breakdown']['good_to_have_keywords']}** / 15 |
                | Section Completeness | **{report['breakdown']['sections']}** / 25 |
                | Formatting Quality | **{report['breakdown']['formatting']}** / 20 |
                """)
            st.markdown("---")

            # Must-Have Keywords
            st.markdown("##### 🔴 Must-Have Keywords")
            if report["must_have_matched"]:
                badges = "".join([f'<span class="kw-must-matched">✓ {kw}</span>' for kw in report["must_have_matched"]])
                st.markdown(badges, unsafe_allow_html=True)
            if report["must_have_missing"]:
                st.markdown("**Missing (add these!):**")
                badges = "".join([f'<span class="kw-must-missing">✗ {kw}</span>' for kw in report["must_have_missing"]])
                st.markdown(badges, unsafe_allow_html=True)
            elif report["must_have_matched"]:
                st.markdown("<small style='color:#10b981'>✅ All must-have keywords present!</small>", unsafe_allow_html=True)

            st.markdown("")

            # Good-to-Have Keywords
            st.markdown("##### 🔵 Good-to-Have Keywords")
            if report["good_to_have_matched"]:
                badges = "".join([f'<span class="kw-good-matched">✓ {kw}</span>' for kw in report["good_to_have_matched"]])
                st.markdown(badges, unsafe_allow_html=True)
            if report["good_to_have_missing"]:
                st.markdown("**Could add:**")
                badges = "".join([f'<span class="kw-good-missing">○ {kw}</span>' for kw in report["good_to_have_missing"]])
                st.markdown(badges, unsafe_allow_html=True)

            st.markdown("---")

            # Action Verbs
            st.markdown("##### 💡 Suggested Action Verbs")
            if report["verb_suggestions"]:
                badges = "".join([f'<span class="verb-badge">{v}</span>' for v in report["verb_suggestions"]])
                st.markdown(badges, unsafe_allow_html=True)
            else:
                st.markdown("<small style='color:#10b981'>Great verb usage!</small>", unsafe_allow_html=True)

            st.markdown("---")

            # Warnings
            st.markdown("##### 📋 Formatting & Structure Audit")
            if not report["formatting_warnings"]:
                st.markdown("<small style='color:#10b981'>✅ No formatting issues found!</small>", unsafe_allow_html=True)
            else:
                for w in report["formatting_warnings"]:
                    cls = "warn-error" if w["type"] == "error" else "warn-warning"
                    icon = "✖" if w["type"] == "error" else "⚠"
                    st.markdown(f'<div class="warn-box {cls}"><strong>{icon}</strong> {w["message"]}</div>', unsafe_allow_html=True)

        with sub_preview:
            template_id = st.selectbox(
                "Template Style",
                options=list(TEMPLATE_OPTIONS),
                format_func=lambda template: TEMPLATE_OPTIONS[template],
                key="tmpl_select",
            )

            html = resume_templates.generate_resume_html(st.session_state.resume, template_id)
            pdf_data = compile_pdf(html)

            if pdf_data:
                safe_name = (st.session_state.resume["personal"].get("fullName", "resume") or "resume").lower().replace(" ","_")
                st.download_button("🖨 Download ATS-Optimized PDF", data=pdf_data,
                    file_name=f"{safe_name}_resume.pdf", mime="application/pdf",
                    type="primary", use_container_width=True)
            else:
                st.error("Error generating PDF.")

            show_resume_preview(html)


# ═══════════════════════════════════════════════════
# TAB 2: JOB OPENINGS — Live Job Board
# ═══════════════════════════════════════════════════
with tab_jobs:
    st.header("🔍 Latest Data Science Job Openings")
    st.caption("Curated openings for Data Engineers and Data Analysts")
    job_listings = MOCK_JOB_LISTINGS

    # Filters
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        filter_role = st.selectbox("Filter by Role", ["All", "Data Engineer", "Data Analyst"], key="job_role_filter")
    with fc2:
        experience_order = ["0-2 years", "1-3 years", "2-4 years", "3-5 years", "3+ years", "5-8 years", "5+ years", "Not specified"]
        experience_options = [level for level in experience_order if any(j["experience"] == level for j in job_listings)]
        filter_exp = st.selectbox("Experience Level", ["All", *experience_options], key="job_exp_filter")
    with fc3:
        source_options = sorted({j["source"] for j in job_listings})
        filter_source = st.selectbox("Source", ["All", *source_options], key="job_src_filter")

    st.markdown("---")

    # Filter jobs
    filtered = job_listings
    if filter_role != "All":
        role_key = "data_engineer" if filter_role == "Data Engineer" else "data_analyst"
        filtered = [j for j in filtered if j["role_type"] == role_key]
    if filter_exp != "All":
        filtered = [j for j in filtered if j["experience"] == filter_exp]
    if filter_source != "All":
        filtered = [j for j in filtered if j["source"] == filter_source]

    if not filtered:
        st.info("No jobs match your filters. Try broadening your search.")
    else:
        st.markdown(f"**Showing {len(filtered)} openings**")

    for job in filtered:
        safe_title = escape(job["title"])
        safe_company = escape(job["company"])
        safe_location = escape(job["location"])
        safe_salary = escape(job["salary_range"])
        safe_posted = escape(job["posted"])
        safe_source = escape(job["source"])
        safe_tags = "".join([f'<span class="job-tag">{escape(tag)}</span>' for tag in job["tags"]])
        with st.container():
            st.markdown(f"""
            <div class="job-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <h3 style="margin:0 0 4px 0;">{safe_title}</h3>
                        <p style="margin:0; color:gray;">🏢 {safe_company} &nbsp; | &nbsp; 📍 {safe_location} &nbsp; | &nbsp; 💰 {safe_salary}</p>
                    </div>
                    <div style="text-align:right;">
                        <small style="color:gray;">📅 {safe_posted}</small><br>
                        <small style="color:gray;">via {safe_source}</small>
                    </div>
                </div>
                <div style="margin-top:8px;">
                    {safe_tags}
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander(f"📖 View Full Description — {job['title']} at {job['company']}"):
                st.markdown(job["description"])
                st.markdown("---")
                st.markdown(f"**Experience Required:** {job['experience']}")
                st.link_button(f"🔗 Apply on {job['source']}", url=job["apply_url"], use_container_width=True)


# ═══════════════════════════════════════════════════
# TAB 3: INTERVIEW PREP — Question Banks
# ═══════════════════════════════════════════════════
with tab_prep:
    st.header("🎓 Interview Preparation")
    st.caption("Practice role-specific technical and behavioral questions")

    prep_role = st.selectbox(
        "Select Role to Practice",
        options=list(INTERVIEW_QUESTIONS.keys()),
        format_func=lambda x: INTERVIEW_QUESTIONS[x]["title"],
        key="prep_role"
    )

    role_data = INTERVIEW_QUESTIONS[prep_role]

    for category_name, questions in role_data["categories"].items():
        st.markdown(f"### 📂 {category_name}")

        for qi, q in enumerate(questions):
            diff_cls = f"difficulty-{q['difficulty'].lower()}"

            with st.expander(f"Q{qi+1}: {q['question']}"):
                st.markdown(f'<span class="{diff_cls}">Difficulty: {q["difficulty"]}</span>', unsafe_allow_html=True)
                st.markdown("")

                # Hint toggle
                if st.checkbox(f"💡 Show Hint", key=f"hint_{prep_role}_{category_name}_{qi}"):
                    st.info(f"**Hint:** {q['hint']}")

                # Practice area
                st.text_area(
                    "✍ Write your answer here:",
                    key=f"ans_{prep_role}_{category_name}_{qi}",
                    height=120,
                    placeholder="Type your answer to practice..."
                )

                # Reveal sample answer
                if st.checkbox(f"📝 Show Sample Answer", key=f"sa_{prep_role}_{category_name}_{qi}"):
                    st.success(f"**Sample Answer:**\n\n{q['sample_answer']}")

        st.markdown("---")
