# 🏨 EasyStay Asia --- Project Technical Overview

## 1. Project Overview

**EasyStay Asia** is a hospitality platform designed to connect
travelers with hotels and empower hotel owners to manage their
operations through an intuitive backend dashboard.\
It provides a seamless booking experience for customers and a powerful
management suite for hotel owners.

### Objectives

-   Simplify hotel booking and payment processes.
-   Offer full management control for hotel owners (rooms, rates,
    availability, and reports).
-   Automate booking validation and payment verification through
    integrated services.

------------------------------------------------------------------------

## 2. System Architecture

### Frontend

-   **Framework:** Nuxt.js 2\
-   **Authentication:** Auth-Next (supports owner/officer/viewer roles)\
-   **UI Library:** TailwindCSS + custom admin theme\
-   **Visualization:** ApexCharts (for dashboard analytics)

### Backend

-   **Framework:** FastAPI (Python)\
-   **Database:** MongoDB (NoSQL, camelCase schema)\
-   **ORM/Models:** Pydantic models (snake_case → camelCase conversion
    for DB)\
-   **Payment Integration:** OPN (Omise)\
-   **Automation & Workflow:** n8n used for payment verification and
    email automation\
-   **Storage:** AWS S3 for image uploads and email templates\
-   **Deployment:** Docker-based services running on EC2

------------------------------------------------------------------------

## 3. Core Modules

### 🏨 Hotel Owner Features

-   Manage **hotel settings**: name, address, description, cover image,
    etc.\
-   Configure **room types**, prices, quantity, and images.\
-   Access **calendar view** for room availability management.\
-   View **booking history** and reservation details.\
-   Manage **user roles** (owner, officer, viewer).\
-   Configure **bank account settings** for receiving payments.\
-   Analyze performance through **dashboard reports** (ApexCharts).

### 👤 Customer Features

-   Search and browse hotels by destination or keyword.\
-   View hotel and room details (with images, description, and price).\
-   Book rooms by selecting check-in and check-out dates.\
-   Complete payments through the OPN gateway (credit card, mobile
    banking, PromptPay).\
-   Receive automatic confirmation via email after successful payment.

------------------------------------------------------------------------

## 4. Booking Logic

-   **Check-in/out Policy:**

    -   Guests can check in after **12:00 PM**.\
    -   Check-out must be done **before 12:00 PM**.\
    -   If a room is checked out before noon, it can be booked again on
        the same day from noon onward.

-   **Booking ID Format:**

        ES[YYYYMMDD]-[##]

    Example: `ES20250628-02` → booking on June 28, 2025 (second booking
    of the day).

-   **Price Calculation Example:**

        3 nights × 1,000 THB/night = 3,000 THB

------------------------------------------------------------------------

## 5. Payment Verification Flow (Simplified)

> 🔒 *Sensitive business logic and identifiers are omitted for
> security.*

1.  **Customer Payment:**\
    Customer completes payment through OPN gateway.

2.  **Webhook Processing:**\
    OPN sends charge status to EasyStay API (via FastAPI endpoint).

3.  **n8n Verification Workflow:**\
    n8n compares data between **EasyStay bookings** and **OPN charges**
    to ensure:

    -   Matching booking ID\
    -   Correct amount and currency\
    -   Proper payment status\
    -   Valid customer identity

4.  **Result Handling:**

    -   If matched → booking marked as **confirmed**\
    -   If mismatched → system triggers **email alert** (HTML bilingual
        message in TH/EN)

------------------------------------------------------------------------

## 6. Authentication and Access Control

-   **Auth Provider:** `auth-next`\
-   **Roles:**
    -   **Owner:** Full access to hotel and financial settings.\
    -   **Officer:** Limited access to room and booking management.\
    -   **Viewer:** Read-only dashboard and report view.

------------------------------------------------------------------------

## 7. Future Modules (In Progress)

  -----------------------------------------------------------------------
  Module                    Description
  ------------------------- ---------------------------------------------
  🧾 Purchase Order         Manage procurement contracts with vendors
  Management                

  📑 Contract Management    Track contracts between hotels and service
                            partners

  🚀 Feature Limitation     Tiered access system defining feature
  Packages                  availability

  🛍️ Purchase History       Records of upgrades and plan changes
  -----------------------------------------------------------------------

> These new modules appear under an orange-themed **"Feature
> Management"** menu group in the admin interface.

------------------------------------------------------------------------

## 8. Technical Highlights

-   **Cloud Infrastructure:** AWS EC2, S3, CloudFront, Lambda, API
    Gateway\
-   **CI/CD:** GitHub Actions (Docker build + deploy)\
-   **Email System:** HTML templates stored in S3 and rendered via
    Jinja2\
-   **Monitoring:** Basic CloudWatch metrics for booking and email
    delivery logs\
-   **Security:**
    -   HTTPS enforced across all endpoints\
    -   Booking and payment verification abstracted from user layer\
    -   No sensitive keys or webhook secrets exposed in frontend

------------------------------------------------------------------------

## 9. Summary

**EasyStay Asia** bridges hotel management and customer booking into a
single streamlined platform.\
Its modular design supports future expansion (e.g., tiered hotel
features, contract management) while maintaining a secure and scalable
architecture leveraging AWS and Python-based automation.

------------------------------------------------------------------------
