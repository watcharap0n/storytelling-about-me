# 🧠 Pasa Education

**Subtitle:** Building a Modern Bilingual E-Learning Platform  
**Role:** Full-Stack Developer (Freelance Project)  
**Developer:** [Watcharapon “Kane” Weeraborirak](https://watcharapon.dev)

---

## 🎯 Overview
**Pasa Education** was my very first freelance project — the foundation that shaped how I design, structure, and build modern educational platforms.  
The goal was to create a **flexible e-learning system** supporting multiple learning experiences:
- **Meetups:** In-person sessions  
- **Workshops:** Practical, hands-on training  
- **Out-of-the-box Courses:** Creative and specialized learning paths  
- **Online Courses:** Self-paced video and audio-based lessons  

**Website:** [pasaeducation.com](https://pasaeducation.com)

---

## ⚙️ Architecture & Stack

| Layer | Technology | Description |
|-------|-------------|-------------|
| **Frontend** | Nuxt.js 2 | Responsive and bilingual (EN/TH) interface |
| **Backend** | FastAPI (Python) | RESTful API with JWT-based authentication |
| **Database** | MongoDB | Collections for `courses`, `students`, and `enrollments` |
| **Storage** | AWS S3 + CloudFront | For media, static assets, and course files |
| **Notification** | AWS Lambda + SES | Email notifications for new enrollments and updates |
| **CI/CD** | GitHub → AWS CodePipeline | Automated deployment pipeline |
| **Hosting** | AWS (API Gateway + Lambda + S3) | Fully serverless setup for scalability and cost efficiency |

---

## 🧩 Key Features

### 👨‍🏫 Course Management
- Admin can create, edit, and categorize courses dynamically  
- Tagging system for topic classification  
- Dedicated UI sections for each course category  

### 👩‍🎓 Student Enrollment
- Frontend enrollment with auto-tracking  
- Students can enroll in multiple courses simultaneously  
- Progress tracking stored in MongoDB  

### 📺 Learning Experience
- Responsive video/audio player  
- Resume progress feature (continue where you left off)  
- Lesson completion tracking in real-time  

### 🧭 Dashboard
- Dual dashboard: Instructor and Student views  
- Instructors can monitor course participants  
- Students can manage enrolled courses and learning status  

---

## 🧠 Technical Highlights

- Modular **FastAPI architecture** with service and schema separation  
- **JWT Authentication** + role-based access control (Admin, Instructor, Student)  
- **Reusable UI Components** for course display and media player  
- **Bilingual support** via JSON-based translation management  
- **AWS Lambda** automations for background jobs (email, progress updates)  
- **Serverless-first approach** with stateless API design for scaling  

---

## 📊 Impact & Learning Outcomes

| Metric | Description |
|---------|--------------|
| ⏱️ Development Duration | ~2 months including design & implementation |
| 🧩 Code Reusability | Core API and components reused in later projects (e.g., new e-learning system) |
| ☁️ Cloud Mastery | Deepened understanding of AWS Lambda, SES, and CloudFront integration |
| 🧠 Growth | Gained practical experience in designing full-stack learning architectures |

---

## 🪶 Summary
**Pasa Education** marked my first milestone as a full-stack freelance developer.  
It taught me to think beyond code — focusing on **learning experience design**, **system scalability**, and **user engagement**.  
Concepts born from this project later influenced my other works like **EasyStay** and **Carbon Watch**, shaping my end-to-end thinking about data, users, and automation.

---

**Project by:** [Watcharapon “Kane” Weeraborirak](https://watcharapon.dev)  
**Stack:** FastAPI · MongoDB · Nuxt.js · AWS Lambda · CloudFront · SES  
**Timeline:** 2023  