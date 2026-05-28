# prep_db.py - Interview preparation question banks for Data Engineer and Data Analyst roles

INTERVIEW_QUESTIONS = {
    "data_engineer": {
        "title": "Data Engineer",
        "categories": {
            "SQL & Databases": [
                {
                    "question": "What is the difference between a Star Schema and a Snowflake Schema? When would you use each?",
                    "difficulty": "Medium",
                    "hint": "Think about normalization, query performance, and storage trade-offs.",
                    "sample_answer": "A Star Schema has a central fact table connected to denormalized dimension tables, making queries simpler and faster. A Snowflake Schema normalizes dimension tables into sub-dimensions, saving storage but requiring more joins. Star Schema is preferred for read-heavy analytics workloads (data warehouses), while Snowflake Schema suits scenarios where storage cost matters and data integrity is critical."
                },
                {
                    "question": "Explain window functions in SQL. Write a query to find the running total of sales by month.",
                    "difficulty": "Medium",
                    "hint": "Use SUM() OVER(ORDER BY ...) with PARTITION BY if needed.",
                    "sample_answer": "Window functions perform calculations across a set of rows related to the current row without collapsing them. Example:\n\nSELECT month, sales, SUM(sales) OVER(ORDER BY month) AS running_total FROM monthly_sales;"
                },
                {
                    "question": "What are Common Table Expressions (CTEs) and how do they differ from subqueries? When do you prefer one over the other?",
                    "difficulty": "Easy",
                    "hint": "Consider readability, recursion support, and query optimization.",
                    "sample_answer": "CTEs (WITH clauses) define temporary named result sets that improve readability and allow recursion. Unlike subqueries, CTEs can be referenced multiple times. Use CTEs for complex, multi-step transformations and subqueries for simple one-off filters."
                },
                {
                    "question": "How would you optimize a slow-running SQL query on a table with 500 million rows?",
                    "difficulty": "Hard",
                    "hint": "Think about indexing, partitioning, query execution plans, and materialized views.",
                    "sample_answer": "Steps: 1) Analyze the execution plan (EXPLAIN ANALYZE). 2) Add appropriate indexes (B-tree for equality, GIN for full-text). 3) Partition the table by date or region. 4) Use materialized views for pre-aggregated data. 5) Avoid SELECT *. 6) Consider denormalization if joins are the bottleneck."
                }
            ],
            "Python & Data Processing": [
                {
                    "question": "What is the difference between a list and a generator in Python? When would you use a generator for data processing?",
                    "difficulty": "Easy",
                    "hint": "Think about memory efficiency and lazy evaluation.",
                    "sample_answer": "Lists store all elements in memory. Generators produce elements one at a time using 'yield', consuming much less memory. Use generators when processing large files or streaming data where loading everything into memory is impractical."
                },
                {
                    "question": "How does PySpark differ from Pandas? When would you choose one over the other?",
                    "difficulty": "Medium",
                    "hint": "Consider data volume, distributed computing, and API similarities.",
                    "sample_answer": "Pandas runs on a single machine and is best for datasets that fit in memory (up to a few GB). PySpark distributes data across a cluster and handles terabytes. Choose Pandas for EDA and small datasets; PySpark for production ETL pipelines processing large-scale data."
                },
                {
                    "question": "Design a Python-based ETL pipeline that reads data from an API, transforms it, and loads it into a PostgreSQL database. What error handling would you include?",
                    "difficulty": "Hard",
                    "hint": "Cover idempotency, retry logic, logging, and schema validation.",
                    "sample_answer": "Architecture: 1) Extract: Use requests with retry/backoff. 2) Transform: Validate schema with Pydantic, clean nulls, deduplicate. 3) Load: Use SQLAlchemy with upsert (INSERT ON CONFLICT). Error handling: Exponential backoff for API failures, dead-letter queues for bad records, structured logging, alerting on failures."
                }
            ],
            "Data Pipeline & Architecture": [
                {
                    "question": "Explain the difference between batch processing and stream processing. Give real-world examples of each.",
                    "difficulty": "Easy",
                    "hint": "Think about latency requirements and use cases.",
                    "sample_answer": "Batch processing handles large volumes of data at scheduled intervals (e.g., nightly Spark jobs aggregating daily sales). Stream processing handles data in real-time as it arrives (e.g., Kafka consumers detecting fraud in payment transactions). Batch is simpler and cheaper; streaming provides lower latency."
                },
                {
                    "question": "What is Apache Airflow and how does it differ from a cron job? Design a DAG for a daily ETL pipeline.",
                    "difficulty": "Medium",
                    "hint": "Cover dependency management, retries, monitoring, and DAG structure.",
                    "sample_answer": "Airflow is a workflow orchestration platform with dependency management, retry logic, monitoring UI, and alerting. Unlike cron, it handles task dependencies (Task B waits for Task A), provides visibility into failures, and supports backfilling. DAG example: extract_api >> validate_data >> transform >> load_warehouse >> send_report."
                },
                {
                    "question": "How would you design a data pipeline that needs to handle exactly-once delivery semantics?",
                    "difficulty": "Hard",
                    "hint": "Consider idempotent consumers, transactional writes, and deduplication.",
                    "sample_answer": "Use Kafka with idempotent producers and transactional consumers. Assign unique message IDs and use deduplication at the consumer level. Write to the sink using upserts (idempotent writes). Use checkpointing in Spark Structured Streaming. For databases, use transactional outbox patterns."
                }
            ],
            "System Design": [
                {
                    "question": "Design a real-time analytics dashboard that shows live order metrics for an e-commerce platform.",
                    "difficulty": "Hard",
                    "hint": "Cover ingestion, processing, storage, and visualization layers.",
                    "sample_answer": "Architecture: 1) Ingestion: Kafka topics for order events. 2) Processing: Spark Structured Streaming or Flink for real-time aggregations. 3) Storage: Redis for real-time metrics, ClickHouse for historical analytics. 4) Serving: REST API layer. 5) Visualization: Grafana or custom React dashboard with WebSocket updates."
                }
            ]
        }
    },
    "data_analyst": {
        "title": "Data Analyst",
        "categories": {
            "SQL Proficiency": [
                {
                    "question": "Write a SQL query to find the second-highest salary in each department.",
                    "difficulty": "Medium",
                    "hint": "Use DENSE_RANK() or ROW_NUMBER() window functions with PARTITION BY.",
                    "sample_answer": "SELECT department, employee, salary FROM (\n  SELECT department, employee, salary,\n    DENSE_RANK() OVER(PARTITION BY department ORDER BY salary DESC) as rnk\n  FROM employees\n) ranked WHERE rnk = 2;"
                },
                {
                    "question": "What is the difference between WHERE and HAVING clauses in SQL?",
                    "difficulty": "Easy",
                    "hint": "Think about when filtering happens relative to GROUP BY.",
                    "sample_answer": "WHERE filters rows before grouping (operates on raw data). HAVING filters groups after aggregation. Example: WHERE salary > 50000 filters individual rows; HAVING COUNT(*) > 5 filters groups that have more than 5 members."
                },
                {
                    "question": "Explain different types of JOINs with examples. When would you use a LEFT JOIN vs INNER JOIN?",
                    "difficulty": "Easy",
                    "hint": "Cover INNER, LEFT, RIGHT, FULL OUTER, and CROSS joins.",
                    "sample_answer": "INNER JOIN returns only matching rows from both tables. LEFT JOIN returns all rows from the left table plus matching rows from the right (NULLs where no match). Use LEFT JOIN when you want to keep all records from the primary table (e.g., all customers, even those with no orders)."
                },
                {
                    "question": "Write a query to calculate Month-over-Month (MoM) growth rate in revenue.",
                    "difficulty": "Medium",
                    "hint": "Use LAG() window function to access previous month's value.",
                    "sample_answer": "SELECT month, revenue,\n  LAG(revenue) OVER(ORDER BY month) as prev_month_revenue,\n  ROUND((revenue - LAG(revenue) OVER(ORDER BY month)) * 100.0 / LAG(revenue) OVER(ORDER BY month), 2) as mom_growth_pct\nFROM monthly_revenue;"
                }
            ],
            "Statistics & Analytics": [
                {
                    "question": "Explain A/B testing. How do you determine sample size and statistical significance?",
                    "difficulty": "Medium",
                    "hint": "Cover null/alternative hypotheses, p-values, confidence intervals, and power analysis.",
                    "sample_answer": "A/B testing compares two variants to determine which performs better. Steps: 1) Define hypothesis (H0: no difference). 2) Calculate sample size using power analysis (based on desired significance level α=0.05, power=0.8, and minimum detectable effect). 3) Run test until sample size is reached. 4) Calculate p-value; reject H0 if p < α."
                },
                {
                    "question": "What is the difference between correlation and causation? Give a real-world example.",
                    "difficulty": "Easy",
                    "hint": "Think about confounding variables and experimental design.",
                    "sample_answer": "Correlation means two variables move together; causation means one directly causes the other. Example: Ice cream sales and drowning deaths are correlated (both increase in summer) but ice cream doesn't cause drowning. The confounding variable is hot weather. To establish causation, you need controlled experiments (A/B tests)."
                },
                {
                    "question": "A product manager asks: 'Our conversion rate dropped 15% this week. What happened?' How do you investigate?",
                    "difficulty": "Hard",
                    "hint": "Think about segmentation, funnel analysis, and external factors.",
                    "sample_answer": "Investigation steps: 1) Verify the data (check for logging issues). 2) Segment by dimensions: device, geography, traffic source, user cohort. 3) Analyze the conversion funnel step-by-step to find where drop-off increased. 4) Check for external factors (holidays, competitor launches, marketing changes). 5) Check for technical issues (page load time, broken flows). 6) Compare with historical patterns."
                }
            ],
            "Data Visualization & Storytelling": [
                {
                    "question": "You have data showing declining user engagement. How would you present this to non-technical stakeholders?",
                    "difficulty": "Medium",
                    "hint": "Focus on narrative structure, chart selection, and actionable recommendations.",
                    "sample_answer": "Structure: 1) Start with the headline insight ('Engagement dropped 20% in Q3'). 2) Show a clean time-series line chart of the trend. 3) Segment the data to show which user groups are most affected. 4) Provide root-cause analysis with supporting charts. 5) End with 3 specific, actionable recommendations. Keep it to 5-6 slides max. Avoid jargon."
                },
                {
                    "question": "When would you use a bar chart vs a line chart vs a scatter plot?",
                    "difficulty": "Easy",
                    "hint": "Think about data types: categorical vs continuous vs relationships.",
                    "sample_answer": "Bar charts: Comparing categories (revenue by region). Line charts: Showing trends over time (monthly sales). Scatter plots: Exploring relationships between two continuous variables (spend vs revenue). Avoid pie charts for more than 4-5 categories. Use heatmaps for correlation matrices."
                }
            ],
            "Python for Analysis": [
                {
                    "question": "How would you handle missing values in a dataset using Pandas? What strategies exist?",
                    "difficulty": "Medium",
                    "hint": "Cover detection, imputation methods, and when to drop vs fill.",
                    "sample_answer": "Detection: df.isnull().sum(). Strategies: 1) Drop rows/columns if missing rate is high (df.dropna()). 2) Fill with mean/median for numerical (df.fillna(df.mean())). 3) Forward/backward fill for time series. 4) Use domain knowledge (e.g., 0 for 'number of returns'). 5) Flag missingness as a feature. Choice depends on data type, missing mechanism (MCAR/MAR/MNAR), and analysis requirements."
                },
                {
                    "question": "Write Python code to perform EDA on a sales dataset. What steps would you follow?",
                    "difficulty": "Medium",
                    "hint": "Cover shape, dtypes, missing values, distributions, correlations, and outliers.",
                    "sample_answer": "Steps:\nimport pandas as pd\nimport matplotlib.pyplot as plt\n\ndf = pd.read_csv('sales.csv')\nprint(df.shape, df.dtypes)\nprint(df.describe())\nprint(df.isnull().sum())\ndf.hist(figsize=(12,8))\ndf.corr().style.background_gradient()\n# Check outliers with boxplots\ndf.boxplot(column='revenue', by='region')"
                }
            ],
            "Business Case Studies": [
                {
                    "question": "An e-commerce company wants to reduce cart abandonment from 70% to 50%. How would you approach this problem as a Data Analyst?",
                    "difficulty": "Hard",
                    "hint": "Think about funnel analysis, user segmentation, A/B testing, and benchmarking.",
                    "sample_answer": "Approach: 1) Analyze the checkout funnel to identify the biggest drop-off step. 2) Segment abandoners by device, payment method, cart value, and user type (new vs returning). 3) Benchmark against industry standards (~70% is typical). 4) Hypothesize interventions (e.g., simpler checkout, guest checkout, exit-intent popups). 5) Design A/B tests to validate. 6) Track impact on abandonment rate and revenue."
                }
            ]
        }
    }
}
