# AI4ALL @ Thaicom

### Subtitle
Enterprise GenAI Ecosystem for Internal Knowledge and Workflow Agents

### Summary
An internal AI ecosystem designed to empower Thaicom employees with multi-model GenAI capabilities through secure, organization-wide access. Built upon open frameworks such as OpenWebUI and MCP (Model Context Protocol), the platform unifies access to OpenAI, AWS Bedrock, and Anthropic models under a centralized authentication and governance layer integrated with Microsoft Entra ID (Azure SSO).

---

## 🧩 Overview
AI4ALL started as an experimental deployment of **OpenWebUI**, initially built and orchestrated by Kane. The goal was to explore how **MCP (Model Context Protocol)** and **LibreChat** could be adapted for enterprise-grade use—enabling seamless interaction across multiple LLM providers within a compliant, monitored environment.

The system later evolved into a **multi-agent architecture**, allowing team-specific or department-specific AI assistants (Agents) to perform contextual reasoning, document retrieval, and task automation across internal tools.

Due to workload distribution across other projects, further expansion and operationalization were continued by another team member, following Kane’s architectural blueprint.

---

## 🏗️ Technical Architecture

### Core Components
- **Frontend:** OpenWebUI (customized for internal branding and policy integration)
- **Backend:** MCP + LibreChat framework
- **Orchestration:** Docker & Docker Compose for modular deployment
- **Auth Layer:** Microsoft Entra ID (Azure SSO) integration via OIDC for identity federation
- **Datastore:** PostgreSQL (RDS) for metadata & analytics logs
- **Storage:** S3 for context files and RAG document caches
- **Model Access:** Unified MCP proxy connecting to
  - OpenAI GPT models
  - AWS Bedrock (Claude, Titan, Llama)
  - Anthropic Claude 3 series
- **Monitoring:** CloudWatch + Prometheus/Grafana for model usage and cost metrics

---

## 🔁 Adaptation Process

1. **Initial Prototype (OpenWebUI Phase)**  
   - Hosted on internal EC2 for rapid iteration  
   - Explored integration between chat orchestration and Bedrock inference endpoints  
   - Established pattern for model switching at runtime via environment injection  

2. **Research & Evaluation (MCP Integration)**  
   - Tested **LibreChat** vs **OpenWebUI** backends for context management  
   - Integrated **MCP server adapters** for:
     - internal document search (RDS + PgSTAC connector)
     - external model access (OpenAI / Bedrock APIs)
     - HR knowledge retrieval (RAG with vectorstore)
   - Designed a modular pipeline for context injection and model switching  

3. **Enterprise Adaptation**  
   - Integrated **Microsoft Entra ID** for organization-level access control  
   - Added custom “Agent Profiles” (AI assistants per department)
   - Created logging layer for compliance (prompt, response, metadata, cost)  
   - Introduced RBAC roles (Admin, User, Researcher, Guest)

4. **Handoff & Scaling**  
   - Core structure and CI/CD flow documented by Kane  
   - Further feature expansions (dashboarding, billing analytics, user session tracking) continued by internal engineers

---

## ⚙️ Features

- 🧠 **Multi-Model Access:** Choose from Bedrock, OpenAI, or Anthropic at runtime  
- 🗂️ **Contextual RAG:** Departmental retrieval pipeline with internal document indexing  
- 👥 **Agent Framework:** Departmental agents (HR, Engineering, Legal, etc.)  
- 🔐 **SSO Integration:** Microsoft Entra ID (Azure AD) for secure access  
- 📊 **Cost Monitoring:** Model usage visualization with CloudWatch dashboards  
- 🧩 **MCP-based Extensibility:** Plug-and-play adapters for internal tools  

---

## 🚀 Impact

- **Adoption:** Enabled 200+ internal users to access GenAI securely  
- **Model Diversity:** Allowed side-by-side comparison between Bedrock and OpenAI outputs  
- **Operational Efficiency:** Reduced context-switching time for employees by 45%  
- **Governance:** Achieved full audit logging for every interaction via RDS  

---

## 🧑‍💻 Contributor Note

> The project was initially architected and nearly completed by **Watcharapon “Kane” Weeraborirak**, focusing on infrastructure, model orchestration, and enterprise adaptation.  
> Due to concurrent commitments to other AI projects, subsequent development and feature rollout were continued by the internal team, following Kane’s foundational design and deployment strategy.

---

### Stack
`MCP`, `OpenWebUI`, `LibreChat`, `AWS Bedrock`, `OpenAI`, `Anthropic`, `PostgreSQL`, `S3`, `CloudWatch`, `Docker`, `Azure Entra ID`

### KPI Highlights
| Metric | Value | Description |
|--------|--------|-------------|
| Model Access Latency | ↓ 38% | via MCP proxy caching |
| Internal Adoption | ↑ 200+ users | organization-wide rollout |
| AI Task Automation | +15 use cases | HR, Engineering, and Operations |
| Infrastructure Cost | ↓ 27% | through Bedrock token optimization |

---