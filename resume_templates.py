# resume_templates.py - HTML layout templates and print stylesheet configurations

def get_default_sample():
    return {
        "personal": {
            "fullName": "Alex Mercer",
            "headline": "Software Engineer | Full Stack Development | Cloud Architecture",
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


def get_ideal_template(target_role):
    """Return a complete ATS-friendly example for the selected target role."""
    common = {
        "personal": {
            "fullName": "Your Name",
            "headline": "Data Analyst | Business Intelligence | Data Visualization",
            "email": "your.email@example.com",
            "phone": "+91 98765 43210",
            "location": "Bengaluru, India",
            "linkedin": "linkedin.com/in/yourname",
            "github": "github.com/yourname",
            "website": "yourname.dev"
        },
        "education": [
            {
                "school": "Your University",
                "degree": "Bachelor of Technology in Computer Science",
                "location": "Bengaluru, India",
                "date": "2018-08 to 2022-05",
                "details": "GPA: 8.7/10. Relevant coursework: Databases, Statistics, Data Structures, Cloud Computing."
            }
        ],
        "certifications": [
            {"name": "AWS Certified Cloud Practitioner", "issuer": "Amazon Web Services", "date": "2024-03"},
            {"name": "SQL for Data Science", "issuer": "Coursera", "date": "2023-11"}
        ]
    }

    if target_role == "data_analyst":
        common.update({
            "summary": "Data Analyst with 3+ years of experience translating complex datasets into actionable business insights. Proficient in SQL, Python, Excel, Tableau, and Power BI, with hands-on expertise in data cleaning, statistical analysis, A/B testing, KPI reporting, and stakeholder communication. Automated reporting workflows and built dashboards that improved decision-making speed by 35%.",
            "experience": [
                {
                    "company": "Example Analytics Pvt. Ltd.",
                    "role": "Data Analyst",
                    "location": "Bengaluru, India",
                    "startDate": "2023-01",
                    "endDate": "Present",
                    "bullets": [
                        "Analyzed customer behavior using SQL, Python, Pandas, and NumPy, identifying retention opportunities that increased repeat purchases by 14%.",
                        "Built Tableau and Power BI dashboards for 20+ KPIs, reducing weekly reporting time by 65% and improving stakeholder visibility.",
                        "Evaluated A/B tests with hypothesis testing and regression analysis, enabling product teams to improve onboarding conversion by 11%.",
                        "Automated Excel and Python reporting workflows, saving 18 analyst hours per month and improving data accuracy."
                    ]
                },
                {
                    "company": "Example Retail Technologies",
                    "role": "Junior Data Analyst",
                    "location": "Pune, India",
                    "startDate": "2022-06",
                    "endDate": "2022-12",
                    "bullets": [
                        "Cleaned and validated 500K+ transaction records for exploratory data analysis and monthly business intelligence reporting.",
                        "Presented funnel analysis, cohort analysis, and customer segmentation findings to marketing stakeholders, supporting a 9% increase in campaign ROI."
                    ]
                }
            ],
            "projects": [
                {
                    "name": "E-commerce Sales Intelligence Dashboard",
                    "tech": "SQL, Python, Pandas, Tableau",
                    "link": "github.com/yourname/sales-dashboard",
                    "description": "Built an interactive dashboard for revenue, customer segmentation, cohort analysis, and KPI tracking. Cleaned 100K+ records and delivered data storytelling insights for product and marketing teams."
                },
                {
                    "name": "Customer Churn Analysis",
                    "tech": "Python, NumPy, Seaborn, Scikit-learn",
                    "link": "github.com/yourname/churn-analysis",
                    "description": "Performed EDA, correlation analysis, and regression modeling to identify churn drivers and recommend targeted retention strategies."
                }
            ],
            "skills": [
                {"category": "Analytics", "list": "SQL, Python, Excel, Pandas, NumPy, Statistical Analysis, A/B Testing, Hypothesis Testing, Regression Analysis, EDA"},
                {"category": "Visualization & BI", "list": "Tableau, Power BI, Looker, Data Visualization, Dashboard Design, KPI Reporting, Data Storytelling"},
                {"category": "Business Analysis", "list": "Business Intelligence, Product Analytics, Funnel Analysis, Cohort Analysis, Segmentation, Stakeholder Communication, Google Analytics"}
            ]
        })
        return common

    common["personal"]["headline"] = "Data Engineer | Data Pipelines | ETL and Cloud Platforms"
    common.update({
        "summary": "Data Engineer with 3+ years of experience designing scalable ETL and ELT data pipelines, data warehouses, and cloud-based analytics platforms. Proficient in Python, SQL, Apache Spark, Apache Kafka, Airflow, AWS, Snowflake, and dbt. Engineered reliable batch and stream processing systems that reduced pipeline latency by 45% while improving data quality and observability.",
        "experience": [
            {
                "company": "Example Data Platforms Pvt. Ltd.",
                "role": "Data Engineer",
                "location": "Bengaluru, India",
                "startDate": "2023-01",
                "endDate": "Present",
                "bullets": [
                    "Engineered ETL and ELT data pipelines using Python, SQL, Apache Spark, and Airflow to process 15M+ records daily with 99.9% reliability.",
                    "Designed a Snowflake data warehouse and dbt transformation models, reducing analytics query time by 42% and improving schema consistency.",
                    "Built Apache Kafka stream processing workflows on AWS, cutting data availability latency from 60 minutes to under 10 minutes.",
                    "Implemented automated data quality checks, monitoring, and CI/CD with Docker and GitHub Actions, reducing production incidents by 30%."
                ]
            },
            {
                "company": "Example Cloud Solutions",
                "role": "Junior Data Engineer",
                "location": "Hyderabad, India",
                "startDate": "2022-06",
                "endDate": "2022-12",
                "bullets": [
                    "Developed Python and SQL ingestion jobs for PostgreSQL, REST API, and S3 data sources, automating daily batch processing workflows.",
                    "Optimized data models and Spark jobs for a cloud data lake, lowering processing costs by 18% while maintaining data governance standards."
                ]
            }
        ],
        "projects": [
            {
                "name": "Real-Time Analytics Pipeline",
                "tech": "Python, Kafka, Spark, Airflow, AWS, Docker",
                "link": "github.com/yourname/realtime-data-pipeline",
                "description": "Architected an event-driven data pipeline that ingests, validates, and transforms streaming events into an analytics-ready data lake with monitoring and data quality checks."
            },
            {
                "name": "Cloud Data Warehouse",
                "tech": "SQL, Snowflake, dbt, PostgreSQL, Terraform",
                "link": "github.com/yourname/cloud-data-warehouse",
                "description": "Designed dimensional data models and reusable dbt transformations for a Snowflake warehouse. Added CI/CD validation, lineage documentation, and automated tests."
            }
        ],
        "skills": [
            {"category": "Data Engineering", "list": "Python, SQL, ETL, ELT, Data Pipeline, Data Modeling, Schema Design, Batch Processing, Stream Processing, Data Quality"},
            {"category": "Platforms & Tools", "list": "Apache Spark, Apache Kafka, Airflow, Snowflake, dbt, PostgreSQL, MongoDB, Redis, Docker, Kubernetes, Terraform"},
            {"category": "Cloud & DevOps", "list": "AWS, Azure, GCP, Data Warehouse, Data Lake, Databricks, CI/CD, GitHub Actions, Data Governance, Data Lineage"}
        ]
    })
    return common


def get_empty_schema():
    return {
        "personal": {
            "fullName": "",
            "headline": "",
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

    layouts = {
        "modern": {
            "font_family": "Helvetica",
            "font_title": "Helvetica-Bold",
            "accent_color": "#1a365d",
            "border_color": "#cbd5e1",
            "header_alignment": "center",
            "sections": (summary_html, experience_html, education_html, projects_html, skills_html, certifications_html),
        },
        "professional": {
            "font_family": "Helvetica",
            "font_title": "Helvetica-Bold",
            "accent_color": "#111827",
            "border_color": "#111827",
            "header_alignment": "left",
            "sections": (summary_html, skills_html, experience_html, projects_html, education_html, certifications_html),
        },
        "graduate": {
            "font_family": "Helvetica",
            "font_title": "Helvetica-Bold",
            "accent_color": "#1d4ed8",
            "border_color": "#93c5fd",
            "header_alignment": "left",
            "sections": (summary_html, education_html, projects_html, skills_html, experience_html, certifications_html),
        },
        "executive": {
            "font_family": "Times-Roman",
            "font_title": "Times-Bold",
            "accent_color": "#111111",
            "border_color": "#222222",
            "header_alignment": "left",
            "sections": (summary_html, experience_html, skills_html, education_html, projects_html, certifications_html),
        },
    }
    layout = layouts.get(template_id, layouts["modern"])
    font_family = layout["font_family"]
    font_title = layout["font_title"]
    accent_color = layout["accent_color"]
    border_color = layout["border_color"]
    header_alignment = layout["header_alignment"]
    sections_html = "".join(layout["sections"])
    headline_html = (
        f'<div class="professional-headline">{personal.get("headline", "")}</div>'
        if personal.get("headline")
        else ""
    )
    primary_color = "#111111"

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
                text-align: {header_alignment};
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
            .professional-headline {{
                color: {accent_color};
                font-size: 10pt;
                font-weight: bold;
                margin: -1pt 0 3pt 0;
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
            body.layout-professional .resume-header {{
                border-bottom: 2px solid {border_color};
                padding-bottom: 6pt;
            }}
            body.layout-professional .section-title {{
                border-bottom-width: 2px;
            }}
            body.layout-graduate .user-name {{
                font-size: 20pt;
                text-transform: none;
            }}
            body.layout-graduate .section-title {{
                font-size: 10pt;
            }}
            body.layout-executive .user-name {{
                font-size: 24pt;
                letter-spacing: 0;
            }}
        </style>
    </head>
    <body class="layout-{template_id}">
        <div class="resume-header">
            <h1 class="user-name">{personal.get("fullName") or "Your Name"}</h1>
            {headline_html}
            <div class="contact-info">
                {contact_html}
            </div>
        </div>
        {sections_html}
    </body>
    </html>
    """
    return html_out
