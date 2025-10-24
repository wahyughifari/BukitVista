# Bukit Vista: AI-Powered Property Search Engine

This project is a Streamlit web application that serves as a proof-of-concept for **GAIA**, Bukit Vista's AI assistant. It transforms a raw, messy property inventory dataset into a powerful, two-part business intelligence tool:

1.  **An Interactive EDA Dashboard** for the internal team to visualize and understand the property portfolio.
2.  **A "Semantic Search" Engine** that allows the sales team or GAIA to find properties based on natural language *intent* (e.g., "a quiet villa with a pool") rather than rigid filters.

---

## The Business Problem

Guests don't search for "3 beds, 2 baths." They search for *feelings* and *vibes*, like **"a romantic place with a great view"** or **"a quiet villa for working remotely."**

Our sales team and our AI assistant, GAIA, struggle to manually match these abstract desires with our property inventory. This manual process is slow and can lead to lost bookings.

This tool solves that problem by providing an "AI brain" that can understand and rank all 51 properties based on semantic meaning.

---

## Key Features

* **An Interactive EDA Dashboard (Tab 1):**
    * **Interactive Map:** Displays all geocoded properties on a map of Bali.
    * **Portfolio Analysis:** Interactive charts showing the distribution of property types, statuses, and guest capacity.
    * **Rating Distribution:** A histogram showing the spread of Airbnb ratings.

* **AI-Powered Semantic Search (Tab 2):**
    * **Natural Language Query:** Search using plain English (or Indonesian) phrases like "villa with a private pool and ocean view."
    * **Semantic Matching:** Uses a pre-trained AI model to find the best matches based on *meaning*, not just keywords.
    * **Relevance Scoring:** Ranks the top 5 properties by a "match score" to show the most relevant options first.
    * **Visual Results:** Displays property photos, ratings, guest capacity, and direct links to the Airbnb page.

---

## Strealit

**[HERE](https://bukitvista-interpro.streamlit.app/)**
---
