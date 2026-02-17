### **Data Sources & API Integration**

Our application leverages a combination of historical racing databases, real-time telemetry, and meteorological services to power its machine learning models and interactive dashboard.

#### **1. Jolpica-F1 API (formerly Ergast API)**

* **Purpose:** Serves as the primary source for historical Formula 1 data.
* **Data Provided:** * Full race results from 1950 to the present.
* Driver and Constructor Championship standings.
* Qualifying results, lap times, and circuit information.


* **Usage in Project:** This data is used to populate our **PostgreSQL** database and provide the "ground truth" for training our machine learning models.

#### **2. OpenF1 API**

* **Purpose:** Provides real-time and low-latency data for live race scenarios.
* **Data Provided:**
* Live telemetry (speed, RPM, gear, throttle).
* Real-time car positions and track status (flags, safety cars).
* Official Race Control messages and team radio transcripts.


* **Usage in Project:** Powers the **Next Race Prediction** feature on the Dashboard and allows for real-time updates during a Grand Prix weekend.

#### **3. OpenWeather API**

* **Purpose:** Integrates critical environmental factors into the prediction engine.
* **Data Provided:**
* Current weather conditions at race track coordinates (temperature, humidity, precipitation).
* Short-term and long-term forecasts for upcoming Grand Prix weekends.


* **Usage in Project:** Weather data is a key feature in our **Race Prediction Simulator**, allowing users to see how changing track conditions (e.g., a sudden rainstorm) impact a driver's likelihood of winning.

#### **4. News Aggregation (RSS Feeds)**

* **Purpose:** Keeps users informed with the latest developments in the sport.
* **Sources:** Aggregated from reputable outlets including *Formula1.com*, *ESPN*, and *Motorsport.com*.
* **Data Provided:** Headlines, article summaries, images, and direct links to full stories.
* **Usage in Project:** Populates the dedicated **News Page**, which auto-refreshes every six hours to ensure content remains current.

#### **5. FastF1 (Python Library)**

* **Purpose:** Advanced data processing for high-fidelity strategy simulation.
* **Data Provided:** Detailed tire compound history, pit stop durations, and stint lengths.
* **Usage in Project:** Used by the Backend/ML team to perform feature engineering, specifically for calculating the impact of tire strategy on race outcomes.

---

### **Implementation Note**

To mitigate risks related to API rate limits and to optimize performance, our backend includes a **caching layer** and scheduled sync scripts that periodically fetch and store data in our local **PostgreSQL** database.