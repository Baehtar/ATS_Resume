# projects_db.py - Preset project templates for the Resume Builder
#
# Each entry has:
#   name        — display name shown in the dropdown and on the resume
#   tech        — comma-separated tech stack (pre-fills the Tech Stack field)
#   link        — optional GitHub / portfolio link
#   description — full project description pre-filled into the Description field
#
# To add a new project, append a new dict to PROJECT_TEMPLATES.

PROJECT_TEMPLATES = [
    {
        "name": "Scalable Cloud Data Lakehouse Pipeline with Medallion Architecture for Retail",
        "tech": "Azure Data Factory, Azure SQL, ADLS Gen2, Databricks, PySpark, Delta Lake",
        "link": "",
        "description": (
            "Built an end-to-end ETL/ELT pipeline using ADF, Azure SQL, and ADLS to ingest and manage client data. "
            "Implemented incremental loading using Lookups, dynamic parameters, and stored procedures for automated "
            "date tracking decisions. "
            "Performed Bronze-to-Silver transformations in Databricks (PySpark) including schema enforcement, null "
            "handling, and deduplication. "
            "Designed Gold-layer Dim & Fact tables using Delta Lake with SCD Type-1 merge logic for accurate record "
            "updates. "
            "Delivered a scalable, production-ready pipeline supporting reporting and analytics."
        ),
    },
]

# Quick lookup by project name
_PROJECT_MAP = {p["name"]: p for p in PROJECT_TEMPLATES}


def get_project_names():
    """Return a list of all project names for use in a dropdown."""
    return [p["name"] for p in PROJECT_TEMPLATES]


def get_project_by_name(name):
    """Return the full project dict for the given name, or None if not found."""
    return _PROJECT_MAP.get(name)
