"""Service layer providing career storytelling data."""

from app.models.experience import Experience


def get_mango_experience() -> Experience:
    """Return storytelling details for Mango Consultant."""
    return Experience(
        company="Mango Consultant",
        period="Jul 2020 – Jul 2022",
        role="AI Developer",
        highlights=[
            "Developed comprehensive AI solutions tailored to industry requirements",
            "Designed and deployed advanced machine learning and deep learning models",
            "Implemented end-to-end data processing pipelines",
            "Enhanced model interpretability and performance",
            "Collaborated on AI strategy and technical roadmaps",
        ],
    )


def get_thaicom_ai_experience() -> Experience:
    """Return storytelling details for Thaicom AI engineering."""
    return Experience(
        company="Thaicom Public Company Ltd",
        period="2022–2023",
        role="AI Engineer",
        highlights=[
            "Implemented machine learning deployment pipelines using SageMaker and MLflow",
            "Engineered real-time inference systems via Lambda and API Gateway",
            "Led geospatial AI projects including forestry analysis and carbon assessment",
        ],
    )


def get_thaicom_genai_experience() -> Experience:
    """Return storytelling details for the GenAI & AI4ALL initiative."""
    return Experience(
        company="Thaicom Public Company Ltd",
        period="2025",
        role="AI Engineer & Data Engineer",
        highlights=[
            "Launched AI4ALL, a GenAI platform for all employees",
            "Developed HR Assistant agents using RAG methodologies",
            "Integrated LibreChat with RDS PostgreSQL for geospatial visualizations",
            "Unified authentication using Microsoft Entra ID",
        ],
    )
