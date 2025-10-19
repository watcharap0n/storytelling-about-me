# 🌳 CarbonWatch Project

**Organization:** Thaicom PLC  
**Role:** AI Engineer — Geospatial AI & Cloud System Deployment  
**Tech Stack:** AWS Lambda • SageMaker • API Gateway • Aurora (PostGIS) • S3 • GeoPandas • GDAL • FastAPI  

---

## 🧠 Overview

**CarbonWatch** is an end-to-end geospatial AI platform that automates **forest carbon baseline assessment**, **forest type classification**, and **canopy density analysis** for carbon credit projects.  
It focuses on transforming customer-submitted **shapefile-based area polygons** into scientifically validated datasets for national-scale forest monitoring.

---

## 🔁 Data Flow Pipeline

```mermaid
flowchart TD
  A[Customer Uploads Project to S3 /input/] -->|Event Trigger| B[AWS Lambda]
  B --> C{Check Selected Package}
  C -->|Package 1| D[Trigger Baseline Model (SageMaker)]
  C -->|Package 2 or 3| E[Wait for Manual Forest Type Assignment]
  E --> F[Lambda Validates Data]
  F --> G[Run SageMaker Model]
  G --> H[Store Output in S3 /output/]
  H --> I[Update Metadata in Aurora (PostGIS)]
```

---

## 🧩 Project Data Structure (S3)

```
S3 Bucket/
│
└── input/
    ├── Project_1/
    │   ├── Area_1/
    │   │   ├── Polygon_1.shp
    │   │   ├── Polygon_2.shp
    │   ├── Area_2/
    │   │   ├── Polygon_1.shp
    │   │   ├── Polygon_2.shp
    ├── Project_2/
        ├── Area_1/
        ├── Area_2/
```

**After processing:**

```
S3 Bucket/
└── output/
    ├── Project_1/
    │   ├── BaseLine/
    │   ├── Forest Type/
    │   ├── Forest Canopy Density/
```

---

## ⚙️ Technical Architecture

| Layer | Component | Description |
|-------|------------|--------------|
| **Storage Layer** | Amazon S3 | Stores project data (input/output) organized by project/area/polygon. |
| **Event Layer** | Lambda Trigger | Detects new uploads in `/input/` and triggers the processing workflow. |
| **Compute Layer** | SageMaker Processing | Runs geospatial model for baseline & canopy analysis. |
| **Database Layer** | Aurora PostgreSQL + PostGIS | Manages spatial metadata, polygon indexing, and result tracking. |
| **API Layer** | API Gateway + FastAPI | Provides endpoints for project creation, package selection, and result retrieval. |
| **Orchestration** | Lambda (Python + Boto3) | Controls model flow, S3 event parsing, and data validation logic. |

---

## 🧠 AI Deployment Thinking

| Stage | Approach | Why |
|--------|-----------|-----|
| **1. Input Validation** | Lambda ensures `.shp` structure and attribute completeness before any model run | Prevents model crash and saves processing cost |
| **2. Model Triggering** | Lambda → SageMaker event | Enables on-demand compute for each project |
| **3. Processing Isolation** | Each SageMaker job runs per project | Ensures reproducibility and fault isolation |
| **4. Output Management** | Lambda renames and stores outputs in structured S3 folders | Supports long-term project traceability |
| **5. Post-Processing** | GeoPandas + GDAL for projection handling and shapefile cleanup | Guarantees spatial accuracy |
| **6. Metadata Storage** | PostGIS records with geometry + project ID | Enables future querying and spatial join operations |
| **7. Staff Notification** | Lambda notifies via internal service when results are ready | Keeps workflow asynchronous and event-driven |

---

## 🌲 Packages Logic

| Package | Description | Workflow Type |
|----------|--------------|----------------|
| **1 — Baseline Assessment** | Run AI model automatically after project submission | Fully automated |
| **2 — Forest Type + Canopy Density** | Staff classification required | Semi-automated |
| **3 — Baseline + Type + Canopy** | Multi-step model chain | Hybrid manual/auto |
| **4 — Hotspot & Burn Scar Tracking** | Detect forest damage from fire/satellite data | Event-triggered |

---

## 📈 Benefits

### 🎯 Organizational Impact
- Reduced manual GIS processing time by **>70%** through serverless automation.  
- Standardized data pipeline between **customer uploads**, **AI models**, and **storage layers**.  
- Enabled internal teams to generate **carbon baseline maps within minutes**.  
- Lowered operation costs with **SageMaker spot instances** and Lambda concurrency tuning.  

### 👨‍💻 Kane’s Technical Growth
- Designed **modular Lambda architecture** with versioned deployments (dev/prod).  
- Integrated **PostGIS spatial operations** into AI data pipelines.  
- Learned to apply **AI orchestration patterns** across heterogeneous geospatial models.  
- Built a **fully event-driven architecture** without manual intervention.  
- Strengthened understanding of **data lineage, model reproducibility, and traceability** in production.  

---

## 🧰 Core Technologies

- **Python:** FastAPI, Boto3, GeoPandas, GDAL, Rasterio  
- **AWS Services:** Lambda, SageMaker, S3, Aurora PostgreSQL, API Gateway, CloudWatch  
- **Spatial Database:** PostGIS  
- **Pipeline Design:** Event-driven serverless workflow  

---

## 📦 Example Lambda Event

```json
{
  "Records": [
    {
      "s3": {
        "bucket": { "name": "carbonwatch-input" },
        "object": { "key": "input/Project_2/Area_1/Polygon_1.shp" }
      }
    }
  ]
}
```

Lambda parses this event, validates the path, identifies the package, and either triggers SageMaker or flags the project for staff review.

---

## 🧭 Reflection

> “CarbonWatch taught me to design AI not just as models, but as **ecosystems** — where automation, geospatial accuracy, and scalable infrastructure all merge.”  
> — *Watcharapon “Kane” Weeraborirak*

---

**© 2025 Watcharapon “Kane” Weeraborirak**  
_AI Engineer @ Thaicom | Geospatial AI Deployment Specialist_
