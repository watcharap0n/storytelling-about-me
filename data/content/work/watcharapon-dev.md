# Project: watcharapon.dev — Technical Implementation

## Overview
**watcharapon.dev** is my personal portfolio webapp designed as a **Next.js 14 (App Router)** project showcasing my AI and cloud engineering work.  
It serves as the **central hub for my AI ecosystem**, integrating with my assistant service, n8n automation, and booking calendar.  
The goal: create an interactive, cinematic, and intelligent portfolio that feels alive — not static.

---

## 🧱 Architecture Summary
| Layer | Stack / Tools | Description |
|-------|----------------|-------------|
| **Frontend Framework** | **Next.js 14** (App Router) | Fully static + ISR ready architecture. Built with React Server Components for performance and SEO. |
| **Styling** | **Tailwind CSS** + CSS Variables + `next/font` | Dark, minimal, Apple-inspired UI with motion-driven transitions. |
| **3D / Visual Layer** | **react-three-fiber** + `@react-three/drei` + Framer Motion | Custom 3D scenes (Data Constellation, timeline orrery). Controlled via hooks to sync scroll position and lighting animations. |
| **Type System** | TypeScript (strict mode) | Typed content modules and component props across all sections. |
| **Content System** | Local `content/*.ts` modules | Static typed data sources for biography, skills, pillars, and projects. Auto-generates pages from these modules. |
| **Deployment / Hosting** | **Vercel** + Docker (multi-stage)** | Runs as containerized build for local dev / on-prem deployment; production on Vercel Edge. |
| **Assistant Integration** | Custom **/api/assistant** proxy | Next.js API route forwards requests to external Assistant API (my AI backend). |
| **Automation Layer** | **n8n + Webhook Triggers** | Automations for form submissions, scheduling, analytics aggregation. |
| **Booking Integration** | **Cal.com / Google Calendar** slots via assistant action | AI assistant can expose real-time availability and booking links. |
| **Analytics** | **Vercel Analytics** (opt-in) | Lightweight telemetry for user interaction. |
| **Monitoring** | CloudWatch + n8n notifications | Error logs and uptime alerts forwarded to my n8n workflow. |

---

## ⚙️ Assistant Integration (MCP-ready)
The site acts as a **frontend shell for my AI assistant**, accessible 24/7.

**Flow:**
1. Client sends user message → `/api/assistant`  
2. Next.js route handler signs JWT (if `ASSISTANT_JWT_SECRET` set)  
3. Request forwarded to external Assistant API (`ASSISTANT_API_BASE + ASSISTANT_API_PATH`)  
4. Assistant API (FastAPI-based) routes request through **MCP bridge** → can access:
   - my personal data (`about`, `skills`, `projects`, etc.)
   - n8n automations (calendar, message routing)
   - contextual knowledge for answering about me  
5. Response returned as JSON to client widget.

**Environment Variables (Server-side):**

| Variable | Purpose |
|-----------|----------|
| `ASSISTANT_API_BASE` | Base URL of backend assistant service |
| `ASSISTANT_API_PATH` | Endpoint path (default `/api/chat`) |
| `ASSISTANT_API_TOKEN` | Optional static Bearer token |
| `ASSISTANT_JWT_SECRET` | Secret used to sign per-request JWT |
| `ASSISTANT_JWT_TTL` | Lifetime in seconds (default 120) |
| `NEXT_PUBLIC_ASSISTANT_ENABLED` | Toggle assistant widget (true / false) |

**Assistant Contract (for MCP context):**
```jsonc
{
  "sessionId": "uuid",
  "message": "User query",
  "context": {
    "page": "/work/carbon-watch",
    "preferredLanguage": "en"
  }
}
```
→ The assistant replies with text, suggestion buttons, or booking actions.

---

## 🧩 3D Scene and Performance Notes
- 3D models loaded lazily via GLTF / DRACO compression.  
- Motion orchestrated using Framer Motion + React hooks to sync with scroll positions.  
- Custom WebGL shaders for particles and data constellations.  
- Server components used for initial HTML render → minimal hydration.  
- Lighthouse score > 95 on desktop / mobile.

---

## 🔐 Deployment & Security
- Multi-stage Dockerfile (build → runtime stages).  
- `node:20-alpine` image with non-root user.  
- Environment variables injected at build-time via Vercel / GitHub Actions.  
- HTTPS enforced via Vercel Edge Network (ACME cert).  
- All outbound assistant requests signed with HMAC JWT token (HS256).  

---

## 🔄 Automation Workflows (via n8n)
1. **Contact Form** → Webhook → n8n → Slack DM + Email Notification.  
2. **Booking Event** → Sync with Google Calendar + confirmation email.  
3. **Portfolio Metrics** → Daily scrape (Vercel Analytics API) → summary to Notion.  
4. **Assistant Feedback** → User ratings → n8n → store in MongoDB + Dashboard.  

---

## 🧠 MCP Integration Intent
The `watcharapon.dev` project functions as the **front-door for my MCP ecosystem**.  
It lets MCP access structured metadata (about me, projects, availability) while keeping the frontend static and secure.  
The MCP agent uses this site as a context source when users ask questions like “Who is Kane?”, “What projects has he built?”, or “How can I book a meeting with him?”.

---

## 🧾 Summary
- **Goal:** Interactive, intelligent portfolio for personal AI ecosystem.  
- **Built with:** Next.js 14 · Tailwind CSS · react-three-fiber · Framer Motion · TypeScript.  
- **Integrated with:** Assistant API (MCP), n8n Automation, Cal.com / Google Calendar.  
- **Hosted on:** Vercel (Edge Runtime + Docker).  
- **Outcome:** A cinematic portfolio that acts as a 24/7 AI assistant hub for Watcharapon Weeraborirak.

---

© 2025 Watcharapon “Kane” Weeraborirak · All Rights Reserved
