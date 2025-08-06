"""Business logic for Mango Consultant experience."""
from models.experience import Experience


def get_mango_experience() -> Experience:
    """Return the Mango Consultant role details."""
    return Experience(
        role="AI Developer",
        responsibilities=[
            "Developed comprehensive AI solutions tailored to industry requirements.",
            "Designed and deployed advanced machine learning and deep learning models.",
            "Implemented end-to-end data processing pipelines for data ingestion and preparation.",
            "Enhanced model interpretability and performance through experimentation and optimization.",
            "Collaborated with stakeholders to define AI strategy and technical roadmaps.",
        ],
        start_date="Jul 2020",
        end_date="Jul 2022",
    )
