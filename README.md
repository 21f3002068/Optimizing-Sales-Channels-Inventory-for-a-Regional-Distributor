# Optimizing-Sales-Channels-Inventory-for-a-Regional-Distributor

![Project Status](https://img.shields.io/badge/Status-Completed-success)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Analysis](https://img.shields.io/badge/Analysis-Statistical%20%26%20Predictive-orange)
![Context](https://img.shields.io/badge/Context-IITM%20Capstone%20Project-red)

> **Business Data Management (BDM) Capstone Project**  
> **Author:** Vaibhav Satish (Roll No: 21f3002068)  
> **Client:** S.K. Timber, Aligarh

## 📖 Executive Summary
This project tackles structural inefficiencies in a regional plywood distributor operating on a hybrid sales model (Contractors + Direct Customers). Through primary data collection and advanced statistical modeling, I identified that the business faced a **strategic risk where ~54% of key revenue depended on just 20 individuals**, alongside a **hidden credit exposure of ₹16–18 Lakhs**.

This repository contains the full analysis pipeline: from digitizing physical invoices using OCR to running Monte Carlo simulations and Seasonal EOQ models.

---

## 🏗️ The Business Problems
The project focused on three core operational "leaks" identified during initial stakeholder interviews:

1.  **Contractor Over-Reliance (Fragility):** The business operates on a "100% Mediation" belief, assuming contractors are the only viable sales channel.
2.  **Latent Credit Risk (Cash Flow):** While books showed low credit, operational reality suggested massive liquidity strain due to informal credit in the unregistered segment.
3.  **Seasonal Blindness (Inventory):** Reactive procurement led to inventory bloating (peaking at **148.5% excess stock**) during low-demand months.

---

## 🛠️ Data Engineering (From Paper to Python)
**Unique Challenge:** The business had no formal database. Data existed only as physical invoices, logbooks, and "Estimate Memos."

**My Solution:**
*   **Digitization:** Utilized Windows 11 OCR ("Scan Text") to extract raw text from image files.
*   **Structuring:** Built custom **Python scripts** to parse unstructured text into clean CSV/Excel datasets.
*   **Feature Engineering:** Derived complex inventory metrics (Turnover Ratio, Holding Cost, Wastage %) which did not previously exist.

---

## 🧠 Analysis & Methodology
I employed a multi-suite analytical approach to diagnose risks and propose solutions:

### 1. Statistical Validation
*   **Welch’s ANOVA & Games-Howell Test:** Used to compare profitability across segments (B2B, Contractor, End Customer) while accounting for unequal variances ($p < 0.001$).
*   **Result:** Disproved the myth that contractors are value creators; they are high-volume enablers, but **End Customers (ECs)** are the true profit engine.

### 2. Risk Modeling
*   **Monte Carlo Simulation:** Simulated revenue outcomes under various channel-mix scenarios (80:20 vs 50:50).
*   **Binary Churn Simulation:** Stress-tested the network. **Finding:** Losing the top 20 contractors results in a **~54% revenue drop** for the A-list segment.
*   **Lorenz Curve & Gini Coefficient:** Calculated a Partial Gini of **0.329**, visualizing acute inequality and concentration risk.

### 3. Operational Optimization
*   **Seasonality-Aware EOQ:** Modeled Economic Order Quantity tailored to High, Mid, and Low demand months.
*   **Impact:** Proposed a model to reduce annual ordering frequency from **829 fragmented orders to ~68**, potentially saving **₹2.63 Lakhs/year**.
*   **FMEA (Failure Mode and Effects Analysis):** Prioritized risks, identifying "Loss of Top 20 Contractors" (RPN 315) as the most critical threat.

---

## 📂 Repository Structure

```text
├── data (NDA)/
│
├── scripts/                  # Python Analysis Notebooks
│   ├── Data_Extraction.py    # Custom script for parsing invoice text
│   ├── Attrition_Model.ipynb # Churn risk & Revenue Loss simulation
│   ├── Channel_Mix_Sim.ipynb # Monte Carlo simulation for channel strategy
│   ├── EOQ_Optimization.ipynb# Seasonality-aware inventory modeling
│   └── Statistical_Tests.ipynb # ANOVA, Welch's, Post-hoc tests
│
├── reports/
│   ├── Final_Report.pdf      # Comprehensive Capstone Report
│   ├── Mid_Term_Report.pdf   # Data exploration and metadata
│   └── Presentation.pptx     # Viva Voce Slide Deck
│
├── visualizations/          
│
└── README.md
```


--------------------------------------------------------------------------------
## Key Insights & Impact
<img width="1100" height="468" alt="image" src="https://github.com/user-attachments/assets/4e889d2d-e87f-4038-bbad-e3f3a2c4e381" />

--------------------------------------------------------------------------------
## 🚀 Tech Stack
- Language: Python 3.x
- Libraries: Pandas, NumPy, SciPy (Stats), Matplotlib/Seaborn (Visualization).
- Tools: Microsoft Excel (Advanced Modeling), Power BI (Dashboarding concepts).

--------------------------------------------------------------------------------
## 📜 Declaration
This project was conducted as part of the IIT Madras BS Degree Capstone. All primary data was collected with the consent of S.K. Timber. Some sensitive personal identifiable information (PII) has been anonymized in the public repository.

--------------------------------------------------------------------------------
## 📬 Contact
- Vaibhav Satish
- 📧 21f3002068@ds.study.iitm.ac.in

