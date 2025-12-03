# Bio-Adaptive Endurance Engine

**Start Date:** June 20, 2024
**Status:** In Development (Phase 1: Architecture & Data Ingestion)

## 1. Mission Statement
Most training apps rely on static, age-based formulas (e.g., "220 minus age") that fail to account for individual physiology. This project builds an **AI-driven coaching engine** that learns the specific user's physiological profile.

By analyzing historical training data, the system identifies the user's unique **Lactate Thresholds (LT1 & LT2)** and maps their daily training to proven physiological models (Seiler’s 3-Zone Model, Jack Daniels’ VDOT, and Friel Zones). The goal is to optimize **Metabolic Efficiency**—ensuring "Easy" runs maximize fat oxidation (below LT1) and "Quality" sessions hit the correct glycolytic demands (at or above LT2).

## 2. The Core Problem: The Unguided Solo Runner
Running has seen a massive surge in popularity, with countless individuals picking up the sport or returning to it with varying levels of experience. However, most of these athletes train in isolation.

* **The Knowledge Gap:** Without a professional coach, runners often rely on generic, static plans found online (e.g., "Couch to 5K") that do not adapt to their actual progress or daily fatigue.
* **The Feedback Void:** A runner might submit miles, but they rarely get *intelligent* feedback. They don't know if their "easy" run was actually easy, or if their "hard" run hit the right physiological systems.
* **The Solution:** An intelligent application that ingests the user's raw training telemetry. By processing this data through AI models grounded in exercise physiology, the system generates **personalized training zones** and **dynamic training plans** tailored specifically to *who the runner is right now*, not who a generic PDF says they should be.

## 3. Core Philosophy
* **Context over Raw Data:** Heart rate is a highly individual biometric. A reading of 150 bpm can represent a recovery effort for one runner and a threshold effort for another; raw numbers are meaningless without a personalized baseline.
* **The "Human" Element:** Algorithms often ignore subjective effort (RPE). This system prioritizes how the athlete *felt* alongside the biometric data.
* **Long-Term Consistency:** The goal is not just one fast workout, but optimizing the aggregate training load to improve VO2 Max and lactate threshold over time.

## 4. Project Roadmap

### Phase 1: The Physiological Profiler (Current Focus)
* **Objective:** Ingest raw data and build a "Runner Profile" JSON object.
* **Methodology:**
    * **Data Ingestion:** Automated ETL pipeline using Python (`garminconnect`) to pull daily Heart Rate, GPS, and Sleep data.
    * **Zone Estimation:** Using **K-Means Clustering** on Pace vs. HR data to identify the natural "inflection points" in the user's performance curve, effectively estimating:
        * **LT1 (Aerobic Threshold):** The top of "Zone 1" (Recovery/Base).
        * **LT2 (Lactate Threshold):** The transition from "Steady" to "Interval" intensity.
    * **Drift Analysis:** Calculating **Decoupling (Pw:HR)** to assess aerobic durability and readiness.

### Phase 2: The AI Coach (LLM Integration)
* **Objective:** Provide natural language feedback based on the Phase 1 profile.
* **Functionality:**
    * **Context-Aware Analysis:** Sending aggregated metrics to OpenAI to classify recent training blocks.
    * **Example Output:** *"Your HR was 155 on today's recovery run. Based on your LT1 of 148, you were training in the 'Grey Zone,' likely relying on carbohydrates rather than fat oxidation. Suggest slowing down 15 sec/mile tomorrow."*
    * **Adaptive Planning:** If Phase 1 detects "High Fatigue," the system suggests a specific recovery protocol. If it detects "Optimal Readiness," it suggests a quality workout.

## 5. Technical Architecture

* **Data Source:** Garmin Connect (via `garminconnect` Python library).
* **Ingestion:** Dockerized Python worker (Cron job).
* **Storage:** PostgreSQL (Time-series data for Heart Rate, Speed, Distance).
* **Logic:** Pandas & Scikit-Learn (K-Means Clustering for Zone Identification).
* **Intelligence:** OpenAI API (GPT-4o) for physiological reasoning and coaching feedback.
* **Frontend:** React/Streamlit (Visualizing the "Lactate Curve" and Training Zones).

## 6. Data Flow & Logic
1.  **Extract:** Python worker wakes up -> Fetches yesterday's activities from Garmin.
2.  **Transform:** Cleans data and calculates `Intensity Factor` and `Heart Rate Decoupling` (Efficiency).
3.  **Load:** Stores clean metrics in Postgres.
4.  **Profile:** K-Means algorithm runs on trailing 60 days of data to recalibrate LT1/LT2 zones.
5.  **Analyze:** System constructs a prompt injecting the user's **Dynamic Zones** and **Today's Metrics**.
6.  **Output:** AI generates a summary of training impact and suggests adjustments for tomorrow.

---

### Key Metrics Tracked
* **Heart Rate Reserve (HRR):** (Max HR - Resting HR).
* **Pa:HR (Pace to Heart Rate Ratio):** Efficiency metric.
* **RPE (Rate of Perceived Exertion):** Subjective feeling (1-10).
* **Training Impulse (TRIMP):** Cumulative load score.