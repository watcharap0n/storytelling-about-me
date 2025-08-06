"""Service layer for the GenAI & AI4ALL experience."""

from models.experience import GenAIProject, ThaicomGenAIExperience


def get_genai_experience() -> ThaicomGenAIExperience:
    """Return a populated ``ThaicomGenAIExperience`` instance.

    The values are derived from the project's ``Readme`` and
    describe the key achievements of the initiative.
    """

    projects = [
        GenAIProject(
            name="AI4ALL Platform",
            description=(
                "Organisation-wide GenAI platform using OpenWebUI "
                "integrated with OpenAI, Bedrock and Anthropic models."
            ),
        ),
        GenAIProject(
            name="HR Assistant",
            description=(
                "Retrieval-augmented generation agents answering policy "
                "queries for employees."
            ),
        ),
        GenAIProject(
            name="LibreChat Integration",
            description=(
                "MCP-based integration enabling access to RDS PostgreSQL "
                "for geospatial visualisations."
            ),
        ),
        GenAIProject(
            name="Unified Authentication",
            description=(
                "Single sign-on across tools through Microsoft Entra ID."
            ),
        ),
    ]

    return ThaicomGenAIExperience(
        role="AI Engineer & Data Engineer",
        projects=projects,
    )


