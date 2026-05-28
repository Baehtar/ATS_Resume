# resume_templates.py - HTML layout templates and print stylesheet configurations

def get_default_sample():
    return {
        "personal": {
            "fullName": "Alex Mercer",
            "email": "alex.mercer@email.com",
            "phone": "(555) 019-2834",
            "location": "San Francisco, CA",
            "linkedin": "linkedin.com/in/alexmercer",
            "github": "github.com/alexmercer",
            "website": "alexmercer.dev"
        },
        "summary": "Results-driven Software Engineer with 4+ years of experience designing, developing, and deploying scalable full-stack web applications. Expert in React, Node.js, and cloud architectures. Proven track record of spearheading cross-functional teams to automate workflows, optimize API response times by 40%, and deliver secure, high-performance customer portals.",
        "experience": [
            {
                "company": "InnovateTech Solutions",
                "role": "Senior Full Stack Engineer",
                "location": "San Francisco, CA",
                "startDate": "2023-03",
                "endDate": "Present",
                "bullets": [
                    "Spearheaded development of a high-traffic B2B SaaS platform using React, TypeScript, and Node.js, increasing active monthly users by 35%.",
                    "Orchestrated migration of legacy services to AWS ECS microservices, reducing infrastructure costs by 22% and improving system uptime to 99.99%.",
                    "Optimized SQL database query execution plans and implemented Redis caching, lowering average API latency from 450ms to 120ms.",
                    "Mentored 4 junior engineers on clean code practices, Git workflows, and CI/CD pipelines, increasing team velocity by 18%."
                ]
            },
            {
                "company": "Nexus Digital Group",
                "role": "Software Engineer II",
                "location": "Austin, TX",
                "startDate": "2021-06",
                "endDate": "2023-02",
                "bullets": [
                    "Designed and implemented interactive dashboards and charts using React and D3.js, boosting customer engagement metrics by 25%.",
                    "Automated unit and integration testing suites utilizing Jest and Cypress, raising overall test coverage from 60% to 92% and preventing regression bugs.",
                    "Collaborated closely with product managers and UX designers to build responsive, accessible web pages conforming to WCAG 2.1 compliance."
                ]
            }
        ],
        "education": [
            {
                "school": "University of California, Berkeley",
                "degree": "Bachelor of Science in Computer Science",
                "location": "Berkeley, CA",
                "date": "2017-09 to 2021-05",
                "details": "GPA: 3.82/4.0. Relevant coursework: Data Structures, Algorithms, Databases."
            }
        ],
        "projects": [
            {
                "name": "CloudScale Task Manager",
                "tech": "React, Node.js, PostgreSQL, Docker",
                "link": "github.com/alexmercer/cloudscale",
                "description": "A secure, dockerized collaborative project workspace tool. Built real-time notifications via WebSockets and integrated OAuth2 authentication."
            },
            {
                "name": "NeuroText NLP Tool",
                "tech": "Python, Flask, TensorFlow, JavaScript",
                "link": "github.com/alexmercer/neurotext",
                "description": "An AI-powered client text analyzer that extracts semantic keywords and summarizes text. Processed over 10,000 requests monthly."
            }
        ],
        "skills": [
            {"category": "Languages & Frameworks", "list": "JavaScript, TypeScript, Python, HTML5, SQL, React, Node.js, Express.js"},
            {"category": "Cloud & Dev Tools", "list": "AWS, Docker, PostgreSQL, Redis, Git, GitHub, REST APIs, GraphQL, CI/CD"},
            {"category": "Methodologies", "list": "Agile, Scrum, Test-Driven Development (TDD), Responsive Web Design"}
        ],
        "certifications": [
            {"name": "AWS Certified Solutions Architect – Associate", "issuer": "Amazon Web Services", "date": "2024-04"},
            {"name": "Certified ScrumMaster (CSM)", "issuer": "Scrum Alliance", "date": "2022-11"}
        ]
    }

def get_empty_schema():
    return {
        "personal": {
            "fullName": "",
            "email": "",
            "phone": "",
            "location": "",
            "linkedin": "",
            "github": "",
            "website": ""
        },
        "summary": "",
        "experience": [],
        "education": [],
        "projects": [],
        "skills": [
            {"category": "Technical Skills", "list": ""},
            {"category": "Tools & Methodologies", "list": ""}
        ],
        "certifications": []
    }

def generate_resume_html(data, template_id, is_print=False):
    personal = data.get("personal", {})
    summary = data.get("summary", "")
    experience = data.get("experience", [])
    education = data.get("education", [])
    projects = data.get("projects", [])
    skills = data.get("skills", [])
    certifications = data.get("certifications", [])

    # Format contact items
    contact_parts = []
    if personal.get("phone"):
        contact_parts.append(personal["phone"])
    if personal.get("email"):
        contact_parts.append(f'<a href="mailto:{personal["email"]}">{personal["email"]}</a>')
    if personal.get("location"):
        contact_parts.append(personal["location"])
    if personal.get("linkedin"):
        contact_parts.append(personal["linkedin"])
    if personal.get("github"):
        contact_parts.append(personal["github"])
    if personal.get("website"):
        contact_parts.append(personal["website"])
        
    contact_html = " | ".join(contact_parts)

    # 1. Experience HTML
    experience_html = ""
    if experience:
        exp_items = []
        for exp in experience:
            bullets = exp.get("bullets", [])
            bullets_html = "".join([f"<li>{bullet}</li>" for bullet in bullets if bullet.strip()])
            bullets_list = f'<ul class="resume-bullets">{bullets_html}</ul>' if bullets_html else ""
            
            exp_items.append(f"""
                <div class="resume-item">
                    <table class="item-table">
                        <tr>
                            <td class="company-name"><strong>{exp.get('company', '')}</strong></td>
                            <td class="item-date" align="right">{exp.get('startDate', '')} – {exp.get('endDate', '')}</td>
                        </tr>
                        <tr>
                            <td class="role-title"><em>{exp.get('role', '')}</em></td>
                            <td class="item-location" align="right">{exp.get('location', '')}</td>
                        </tr>
                    </table>
                    {bullets_list}
                </div>
            """)
        
        experience_html = f"""
            <div class="resume-section">
                <h2 class="section-title">WORK EXPERIENCE</h2>
                {"".join(exp_items)}
            </div>
        """

    # 2. Education HTML
    education_html = ""
    if education:
        edu_items = []
        for edu in education:
            details_html = f'<p class="edu-details">{edu.get("details", "")}</p>' if edu.get("details") else ""
            edu_items.append(f"""
                <div class="resume-item">
                    <table class="item-table">
                        <tr>
                            <td class="school-name"><strong>{edu.get('school', '')}</strong></td>
                            <td class="item-date" align="right">{edu.get('date', '')}</td>
                        </tr>
                        <tr>
                            <td class="degree-title"><em>{edu.get('degree', '')}</em></td>
                            <td class="item-location" align="right">{edu.get('location', '')}</td>
                        </tr>
                    </table>
                    {details_html}
                </div>
            """)
        education_html = f"""
            <div class="resume-section">
                <h2 class="section-title">EDUCATION</h2>
                {"".join(edu_items)}
            </div>
        """

    # 3. Projects HTML
    projects_html = ""
    if projects:
        proj_items = []
        for proj in projects:
            tech_span = f'<span class="project-tech">[{proj.get("tech", "")}]</span>' if proj.get("tech") else ""
            proj_items.append(f"""
                <div class="resume-item">
                    <table class="item-table">
                        <tr>
                            <td class="project-name"><strong>{proj.get('name', '')}</strong> {tech_span}</td>
                            <td class="project-link" align="right">{f"<a href='https://{proj.get('link')}' target='_blank'>{proj.get('link')}</a>" if proj.get('link') else ""}</td>
                        </tr>
                    </table>
                    <p class="project-desc">{proj.get('description', '')}</p>
                </div>
            """)
        projects_html = f"""
            <div class="resume-section">
                <h2 class="section-title">PROJECTS</h2>
                {"".join(proj_items)}
            </div>
        """

    # 4. Skills HTML
    skills_html = ""
    active_skills = [s for s in skills if s.get("category", "").strip() and s.get("list", "").strip()]
    if active_skills:
        skill_rows = []
        for s in active_skills:
            skill_rows.append(f"""
                <div class="skill-category-row">
                    <strong>{s.get('category')}:</strong> {s.get('list')}
                </div>
            """)
        skills_html = f"""
            <div class="resume-section">
                <h2 class="section-title">SKILLS</h2>
                <div class="skills-block">
                    {"".join(skill_rows)}
                </div>
            </div>
        """

    # 5. Certifications HTML
    certifications_html = ""
    if certifications:
        cert_rows = []
        for cert in certifications:
            cert_rows.append(f"""
                <div class="cert-row">
                    <table class="item-table">
                        <tr>
                            <td><strong>{cert.get('name', '')}</strong> – {cert.get('issuer', '')}</td>
                            <td align="right" class="cert-date">{cert.get('date', '')}</td>
                        </tr>
                    </table>
                </div>
            """)
        certifications_html = f"""
            <div class="resume-section">
                <h2 class="section-title">CERTIFICATIONS</h2>
                <div class="certifications-block">
                    {"".join(cert_rows)}
                </div>
            </div>
        """

    # 6. Summary HTML
    summary_html = ""
    if summary.strip():
        summary_html = f"""
            <div class="resume-section">
                <h2 class="section-title">PROFESSIONAL SUMMARY</h2>
                <p class="summary-text">{summary}</p>
            </div>
        """

    # Font definitions for PDF renderer compatibility (ReportLab standard fonts)
    # Standard PDF fonts include Helvetica, Times-Roman, Courier
    font_family = "Helvetica"
    font_title = "Helvetica-Bold"
    
    if template_id == "classic":
        font_family = "Times-Roman"
        font_title = "Times-Bold"
    elif template_id == "executive":
        font_family = "Times-Roman"
        font_title = "Times-Bold"

    # Base styling variables
    primary_color = "#111111"
    border_color = "#222222"
    accent_color = "#111111"
    
    if template_id == "modern":
        accent_color = "#1a365d" # Dark blue
        border_color = "#cbd5e1" # Slate light

    # Combine layout HTML
    html_out = f"""
    <html>
    <head>
        <style>
            @page {{
                size: a4;
                margin: 15mm 15mm 15mm 15mm;
            }}
            body {{
                font-family: {font_family};
                color: {primary_color};
                line-height: 1.4;
                font-size: 9.5pt;
                background-color: #ffffff;
            }}
            .resume-header {{
                text-align: center;
                margin-bottom: 12pt;
            }}
            .user-name {{
                font-family: {font_title};
                font-size: 22pt;
                margin: 0 0 4pt 0;
                color: {accent_color};
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            .contact-info {{
                font-size: 9pt;
                color: #333333;
            }}
            .contact-info a {{
                color: #111111;
                text-decoration: none;
            }}
            .resume-section {{
                margin-top: 10pt;
            }}
            .section-title {{
                font-family: {font_title};
                font-size: 10.5pt;
                border-bottom: 1px solid {border_color};
                padding-bottom: 2pt;
                margin: 0 0 6pt 0;
                letter-spacing: 0.8px;
                color: {accent_color};
            }}
            .resume-item {{
                margin-bottom: 6pt;
            }}
            .item-table {{
                width: 100%;
                margin-bottom: 2pt;
            }}
            .item-table td {{
                padding: 0;
                font-size: 9.5pt;
            }}
            .company-name, .school-name, .project-name {{
                font-family: {font_title};
            }}
            .item-date, .cert-date {{
                color: #333333;
            }}
            .item-location, .role-title, .degree-title {{
                font-size: 9pt;
            }}
            .summary-text, .edu-details, .project-desc {{
                font-size: 9.2pt;
                margin: 0 0 3pt 0;
                text-align: justify;
            }}
            .resume-bullets {{
                margin: 0;
                padding-left: 12pt;
            }}
            .resume-bullets li {{
                font-size: 9.2pt;
                margin-bottom: 2pt;
                list-style-type: disc;
            }}
            .skills-block, .certifications-block {{
                font-size: 9.2pt;
            }}
            .skill-category-row {{
                margin-bottom: 2pt;
            }}
            .project-tech {{
                font-size: 8.5pt;
                color: #555555;
                font-weight: normal;
            }}
        </style>
    </head>
    <body>
        <div class="resume-header">
            <h1 class="user-name">{personal.get("fullName") or "Your Name"}</h1>
            <div class="contact-info">
                {contact_html}
            </div>
        </div>
        {summary_html}
        {experience_html}
        {education_html}
        {projects_html}
        {skills_html}
        {certifications_html}
    </body>
    </html>
    """
    return html_out
