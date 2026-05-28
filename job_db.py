# job_db.py - Mock job listings data for the Job Board scraper UI

MOCK_JOB_LISTINGS = [
    {
        "id": 1,
        "title": "Senior Data Engineer",
        "company": "Flipkart",
        "location": "Bengaluru, India",
        "experience": "3-5 years",
        "role_type": "data_engineer",
        "posted": "2 days ago",
        "salary_range": "₹18L - ₹30L / year",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs",
        "description": """We are looking for a Senior Data Engineer to build and maintain scalable data pipelines. 
You will work with Apache Spark, Airflow, and AWS to process terabytes of e-commerce data daily.

Responsibilities:
• Design and implement ETL/ELT pipelines using Apache Spark and Airflow
• Build and maintain data warehouse solutions on AWS Redshift and Snowflake
• Optimize SQL queries and data models for analytical workloads
• Collaborate with Data Scientists and Analysts to deliver clean, reliable datasets
• Implement data quality checks and monitoring dashboards

Requirements:
• 3+ years of experience in Data Engineering
• Strong proficiency in Python and SQL
• Hands-on experience with Apache Spark, Kafka, or similar big data tools
• Experience with cloud platforms (AWS/GCP/Azure)
• Knowledge of Docker and CI/CD pipelines""",
        "tags": ["Python", "SQL", "Spark", "AWS", "Airflow", "ETL", "Snowflake"]
    },
    {
        "id": 2,
        "title": "Data Analyst - Product Analytics",
        "company": "Razorpay",
        "location": "Bengaluru, India",
        "experience": "1-3 years",
        "role_type": "data_analyst",
        "posted": "1 day ago",
        "salary_range": "₹10L - ₹18L / year",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs",
        "description": """Join our Product Analytics team and help drive data-informed decisions across Razorpay's payment products.

Responsibilities:
• Analyze user behavior and product metrics using SQL and Python
• Build interactive dashboards in Tableau and Looker for stakeholders
• Conduct A/B testing and statistical analysis to measure feature impact
• Create weekly and monthly KPI reports for leadership
• Collaborate with Product Managers to define success metrics

Requirements:
• 1+ years of experience in Data Analytics or Business Intelligence
• Strong SQL skills (complex joins, window functions, CTEs)
• Proficiency in Python (Pandas, NumPy) for data manipulation
• Experience with Tableau, Power BI, or Looker
• Understanding of statistical concepts (hypothesis testing, regression)""",
        "tags": ["SQL", "Python", "Tableau", "A/B Testing", "KPI", "Looker"]
    },
    {
        "id": 3,
        "title": "Data Engineer - Real-Time Systems",
        "company": "Swiggy",
        "location": "Bengaluru, India (Hybrid)",
        "experience": "2-4 years",
        "role_type": "data_engineer",
        "posted": "3 days ago",
        "salary_range": "₹15L - ₹25L / year",
        "source": "Indeed",
        "apply_url": "https://indeed.com/jobs",
        "description": """Swiggy is hiring a Data Engineer to work on real-time streaming data infrastructure powering delivery logistics.

Responsibilities:
• Build and scale real-time data pipelines using Apache Kafka and Spark Streaming
• Design data models for event-driven architecture
• Maintain and optimize data lake on AWS S3 with Delta Lake
• Implement data governance and lineage tracking
• Write unit tests and integration tests for pipeline reliability

Requirements:
• 2+ years in data engineering roles
• Experience with stream processing (Kafka, Flink, or Spark Streaming)
• Proficiency in Python and/or Scala
• Familiarity with Docker, Kubernetes, and Terraform
• Experience with dbt for data transformation""",
        "tags": ["Kafka", "Spark", "Python", "AWS", "Docker", "Delta Lake", "dbt"]
    },
    {
        "id": 4,
        "title": "Business Data Analyst",
        "company": "Meesho",
        "location": "Delhi NCR, India",
        "experience": "0-2 years",
        "role_type": "data_analyst",
        "posted": "5 days ago",
        "salary_range": "₹6L - ₹12L / year",
        "source": "Naukri",
        "apply_url": "https://naukri.com/jobs",
        "description": """Meesho is looking for a Business Data Analyst to support growth and marketing teams with actionable insights.

Responsibilities:
• Write complex SQL queries to extract insights from large datasets
• Build dashboards in Power BI for marketing campaign tracking
• Perform cohort analysis and customer segmentation
• Conduct funnel analysis to identify drop-off points
• Present data stories and recommendations to non-technical stakeholders

Requirements:
• Bachelor's degree in Statistics, Mathematics, or related field
• Strong SQL and Excel skills
• Experience with Power BI or Tableau
• Knowledge of statistical analysis and EDA
• Excellent communication and data storytelling skills""",
        "tags": ["SQL", "Power BI", "Excel", "Cohort Analysis", "EDA", "Segmentation"]
    },
    {
        "id": 5,
        "title": "Lead Data Engineer",
        "company": "Paytm",
        "location": "Noida, India",
        "experience": "5-8 years",
        "role_type": "data_engineer",
        "posted": "1 week ago",
        "salary_range": "₹28L - ₹45L / year",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs",
        "description": """Lead the data platform team at Paytm and architect next-generation data infrastructure.

Responsibilities:
• Architect and lead development of enterprise-scale data pipelines
• Manage a team of 4-6 data engineers
• Design data warehouse and data lake strategy on GCP BigQuery
• Implement data governance, security, and compliance frameworks
• Drive adoption of modern data stack (dbt, Airflow, Databricks)

Requirements:
• 5+ years of data engineering experience with 2+ years in a lead role
• Expert-level SQL and Python
• Deep experience with GCP (BigQuery, Dataflow, Pub/Sub)
• Experience with Databricks and Apache Spark
• Strong data modeling and schema design skills""",
        "tags": ["GCP", "BigQuery", "Databricks", "Spark", "Airflow", "dbt", "Leadership"]
    },
    {
        "id": 6,
        "title": "Data Analyst - Growth & Marketing",
        "company": "CRED",
        "location": "Bengaluru, India",
        "experience": "2-4 years",
        "role_type": "data_analyst",
        "posted": "4 days ago",
        "salary_range": "₹14L - ₹22L / year",
        "source": "LinkedIn",
        "apply_url": "https://linkedin.com/jobs",
        "description": """CRED is hiring a Growth Data Analyst to optimize user acquisition, engagement, and retention strategies.

Responsibilities:
• Analyze marketing campaigns and user funnels to drive growth
• Build automated reporting dashboards using Looker
• Design and evaluate A/B tests for product experiments
• Perform statistical modeling including regression and time series forecasting
• Partner with engineering to implement event tracking and data pipelines

Requirements:
• 2+ years of analytics experience, preferably in fintech or consumer tech
• Advanced SQL (CTEs, window functions, optimization)
• Python proficiency (Pandas, Matplotlib, Seaborn)
• Experience with Google Analytics and product analytics tools
• Strong data visualization and storytelling ability""",
        "tags": ["SQL", "Python", "Looker", "A/B Testing", "Google Analytics", "Forecasting"]
    },
    {
        "id": 7,
        "title": "Junior Data Engineer",
        "company": "Zomato",
        "location": "Gurugram, India",
        "experience": "0-2 years",
        "role_type": "data_engineer",
        "posted": "6 days ago",
        "salary_range": "₹8L - ₹14L / year",
        "source": "Indeed",
        "apply_url": "https://indeed.com/jobs",
        "description": """Start your data engineering career at Zomato! Work on real-world food-tech data systems.

Responsibilities:
• Assist in building and maintaining ETL pipelines using Python and Airflow
• Write and optimize SQL queries on PostgreSQL and Redshift
• Help migrate batch jobs to streaming architecture
• Write data quality validation scripts
• Document data models and pipeline architectures

Requirements:
• Bachelor's degree in CS, IT, or related field
• Fundamentals of Python and SQL
• Basic understanding of databases (PostgreSQL, MongoDB)
• Familiarity with Linux command line
• Eagerness to learn cloud platforms (AWS preferred)""",
        "tags": ["Python", "SQL", "PostgreSQL", "Airflow", "ETL", "AWS"]
    },
    {
        "id": 8,
        "title": "Senior Data Analyst",
        "company": "PhonePe",
        "location": "Bengaluru, India",
        "experience": "3-5 years",
        "role_type": "data_analyst",
        "posted": "2 days ago",
        "salary_range": "₹18L - ₹28L / year",
        "source": "Naukri",
        "apply_url": "https://naukri.com/jobs",
        "description": """PhonePe seeks a Senior Data Analyst to own analytics for our lending and insurance verticals.

Responsibilities:
• Own end-to-end analytics for financial product lines
• Build predictive models using Python and Scikit-learn
• Create executive dashboards in Tableau with real-time data
• Conduct deep-dive analyses on user behavior and financial metrics
• Mentor junior analysts and establish analytics best practices

Requirements:
• 3+ years in a data analyst or business intelligence role
• Expert SQL and Python skills
• Experience with Machine Learning basics (Scikit-learn)
• Proficiency in Tableau or Power BI
• Experience in fintech, banking, or payments domain preferred""",
        "tags": ["SQL", "Python", "Tableau", "Scikit-learn", "Machine Learning", "KPI"]
    }
]
