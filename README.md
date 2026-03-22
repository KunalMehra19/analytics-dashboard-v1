## Technical Report: Real-Time Activity Analytics Service

**Prepared by:** Kunal Mehra  
**Date:** March 23, 2026  
**Stack:** Python (Flask), PostgreSQL (Supabase), Chart.js, Tailwind CSS  

---

### 1. Project Overview
This project is a full-stack analytics engine designed to ingest, store, and visualize user behavioral data. Unlike simple logging tools, this service transforms raw event data into high-level business metrics, such as **Conversion Funnels** and **Time-Series Traffic Analysis**.

---

### 2. System Architecture & Data Flow
The system is built using a **Decoupled Cloud Architecture** to ensure high availability and data persistence.

1.  **Data Ingestion (API Layer):** The Flask backend provides a RESTful `POST /track` endpoint. It accepts JSON payloads containing a `user_id`, `event_type`, and flexible `metadata`.
2.  **Cloud Storage (Database Layer):** Data is persisted in a **Supabase PostgreSQL** instance. I utilized a `JSONB` column type for metadata to allow for "Schema-less" flexibility, enabling the tracking of different event types without database migrations.
3.  **Analytics Engine (Processing Layer):** The backend performs server-side aggregation. It filters raw noise into structured **KPIs** (Key Performance Indicators) before sending them to the frontend.
4.  **Data Visualization (Presentation Layer):** An interactive dashboard built with **Chart.js** fetches the processed data to render visual insights.

---

### 3. Key Concepts & Analytics Logic
The system focuses on **Behavioral Analytics** rather than just raw row counts:

#### **A. The Conversion Funnel**
I implemented a three-stage sales funnel logic to track the "User Journey":
* **Search:** The "Top of Funnel" (Initial interest).
* **Add to Cart:** The "Middle of Funnel" (High intent).
* **Checkout Success:** The "Bottom of Funnel" (Successful conversion).
* **Metric:** $$\text{Conversion Rate} = \left( \frac{\text{Total Purchases}}{\text{Total Searches}} \right) \times 100$$

#### **B. Hourly Traffic Pattern**
The system extracts the hour from the ISO timestamp of every event to create a distribution map. This allows stakeholders to identify "Peak Hours" for targeted marketing or server scaling.

#### **C. Loyalty Metrics**
By tracking event frequency per `user_id`, the system identifies "Power Users"—those who interact with the application more than three times in a single session.

---

### 4. Technical Assumptions
* **Statelessness:** I assumed the service must be stateless. By hosting the database on Supabase and the logic on Render, the API can scale horizontally without losing data.
* **CORS Protocols:** I assumed the frontend and backend might live on different domains. I implemented **Cross-Origin Resource Sharing** to allow secure communication between the dashboard and the API.
* **Generic Ingestion:** While the dashboard uses an E-commerce theme, the backend is built to be "Use-Case Agnostic," meaning it can track any event type (e.g., IoT data, social media likes) with zero code changes.

---

### 5. API Documentation

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/track` | `POST` | Ingests a new activity (requires `user_id`, `event_type`). |
| `/analytics/summary` | `GET` | Returns high-level system health and total counts. |
| `/analytics/detailed` | `GET` | Returns processed data for graphs (Funnel, Hourly Traffic). |

---

### 6. Conclusion
The "Activity Analytics Service" successfully bridges the gap between raw data collection and visual storytelling. It provides a robust foundation for any data-driven application requiring real-time monitoring of user behavior.

---

### 7. UI
<img width="1868" height="861" alt="Screenshot 2026-03-22 224033" src="https://github.com/user-attachments/assets/9be4039b-8697-4353-a083-5d55cc25eb17" />

<img width="1851" height="887" alt="image" src="https://github.com/user-attachments/assets/85b32a7f-5a7e-40c4-b2e2-0e35000b176b" />
