# My Career Storytelling

An API service narrating my professional journey, achievements, and transformative projects at Thaicom, built using FastAPI and structured with the MVC pattern.

## My Story

From foundational development roles to advanced AI engineering and innovative GenAI initiatives, my career spans significant growth, contributions, and impactful projects.

### Mango Consultant (Jul 2020 – Jul 2022)

* **Role:** AI Developer
* **Responsibilities:**

  * Developed comprehensive AI solutions tailored to specific industry requirements.
  * Designed and deployed advanced machine learning and deep learning models.
  * Implemented end-to-end data processing pipelines to streamline data ingestion and preparation.
  * Enhanced model interpretability and performance through rigorous experimentation and optimization.
  * Collaborated with stakeholders to define AI strategy and technical roadmaps, ensuring alignment with business objectives.

### Thaicom Public Company Ltd (Jul 2022 – Present)

#### AI Engineering (2022–2023)

* **Role:** AI Engineer
* **Achievements:**

  * Implemented robust machine learning deployment pipelines using SageMaker and MLflow.
  * Engineered real-time inference systems via Lambda and API Gateway, significantly reducing response times.
  * Led technical efforts in geospatial AI projects such as forestry analysis and carbon assessment.

#### GenAI & AI4ALL Initiative (2025)

* **Role:** AI Engineer & Data Engineer
* **Key Projects:**

  * Launched AI4ALL, a cost-effective and powerful GenAI platform accessible to all Thaicom employees, leveraging OpenWebUI with integrations from OpenAI, Bedrock, and Anthropic.
  * Developed HR Assistant agents using RAG methodologies to efficiently answer policy-related queries.
  * Integrated LibreChat using the MCP protocol to effectively utilize RDS PostgreSQL for geospatial data visualizations.
  * Unified authentication processes with Microsoft Entra ID for seamless integration across organizational tools and systems.

## API Overview

Expose your career milestones via these clear, storytelling endpoints:

* **GET /experience/mango**: AI-focused projects and roles at Mango Consultant (2020–2022)
* **GET /experience/thaicom/ai**: Evolution into AI engineering and model deployment (2022–2023)
* **GET /experience/thaicom/genai**: Comprehensive details on GenAI projects including AI4ALL (2025)

## Architecture & Design

* **Framework:** FastAPI
* **Pattern:** MVC (models, services, controllers)
* **Authentication:** OAuth2 / JWT (planned)

## Authentication Flow (Planned)

1. The client submits login credentials to an authentication endpoint and receives a signed token upon success.
2. Each subsequent request includes the token in the `Authorization` header.
3. Middleware or route dependencies verify the token's integrity and extract user information.
4. Authorized requests proceed to the intended endpoint, while invalid or missing tokens result in an authentication error.

## Getting Started

1. **Clone Repository**

```bash
git clone https://github.com/watcharap0n/storytelling-about-me.git
cd storytelling-about-me
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

3. **Run the Server**

```bash
uvicorn app.main:app --reload
```

## Next Steps

* Develop endpoint-specific controllers
* Define data models using Pydantic schemas
* Enhance readability with detailed code comments and documentation
* Finalize scripts for streamlined deployment
