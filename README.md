
# 🌱 Renewable Energy Performance Analytics

### Data Analyst Project | Python • MySQL • Power BI • Streamlit

## 📌 Project Overview

Renewable Energy Performance Analytics is a data analytics project designed to analyze the performance of renewable energy plants using **Solar, Wind, and Hydro energy data**.

The project focuses on understanding energy generation, plant efficiency, capacity utilization, weather impact, downtime, maintenance costs, and revenue.

Using Python, MySQL, Power BI, and Streamlit, the project transforms raw renewable energy data into meaningful business insights that can support better operational and business decisions.

## 🎯 Business Objectives

- Analyze total renewable energy generation.
- Compare Solar, Wind, and Hydro energy performance.
- Identify high-performing and low-performing power plants.
- Analyze plant efficiency and capacity utilization.
- Understand the relationship between weather conditions and energy generation.
- Analyze downtime and maintenance performance.
- Evaluate operating costs, maintenance costs, and revenue.
- Build an interactive Power BI dashboard.
- Develop a simple Streamlit application for exploring energy records.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data cleaning, EDA, and performance analysis |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| MySQL | Database management and SQL analysis |
| Power BI | Interactive dashboard and business visualization |
| Streamlit | Interactive energy data explorer |

## 📂 Dataset Description

The project uses a renewable energy dataset concept containing **50,000+ energy generation and operational records**.

The dataset includes information about:

| Category | Description |
|---|---|
| Energy Plant | Plant ID, plant name, energy type, region, and city |
| Generation | Date, hour, and energy generated in MWh |
| Capacity | Installed capacity and capacity utilization |
| Weather | Temperature, wind speed, solar irradiance, and rainfall |
| Operations | Downtime, maintenance hours, and plant status |
| Cost | Operating cost, maintenance cost, and revenue |
| Performance | Efficiency and availability percentage |

## 🔍 Project Workflow

1. Load the raw renewable energy dataset.
2. Perform data cleaning and preprocessing using Python.
3. Handle missing values and duplicate records.
4. Validate data types and standardize categorical values.
5. Perform Exploratory Data Analysis (EDA).
6. Calculate important business and performance metrics.
7. Store cleaned data in a MySQL database.
8. Perform analytical SQL queries using joins, CTEs, and window functions.
9. Connect the data to Power BI.
10. Develop an interactive Power BI dashboard.
11. Build a simple Streamlit data explorer.
12. Validate results and prepare business insights.

## 🐍 Python Analysis

Python is used for data cleaning, exploratory data analysis, and performance analysis.

### Data Cleaning
- Handling missing values
- Removing duplicate records
- Converting date and time columns
- Validating numeric values
- Standardizing categorical data
- Identifying invalid or unrealistic values

### Exploratory Data Analysis (EDA)
- Energy generation trends
- Energy generation by type
- Plant-wise and region-wise analysis
- Capacity utilization analysis
- Plant efficiency comparison
- Weather impact analysis
- Downtime and maintenance analysis
- Operating cost and revenue analysis

## 📊 Key Performance Indicators (KPIs)

The following business metrics are analyzed:

- Total Energy Generated (MWh)
- Average Daily Generation
- Capacity Utilization Rate
- Plant Efficiency Rate
- Plant Availability Rate
- Downtime Rate
- Cost per MWh
- Revenue per MWh
- Maintenance Cost per MWh
- Plant Performance Score

## 🗄️ MySQL Analysis

The MySQL database is named:

`renewable_energy_analytics`

### Database Tables

- Plants
- Energy_Generation
- Weather_Data
- Maintenance_Records

### SQL Concepts Used

- CREATE DATABASE and CREATE TABLE
- INSERT and SELECT
- WHERE, GROUP BY, HAVING, ORDER BY
- INNER JOIN and LEFT JOIN
- CASE statements
- Common Table Expressions (CTEs)
- Window Functions
- RANK() and DENSE_RANK()
- Aggregate Functions
- SQL Views

### Business Questions

- Which plants generate the highest amount of energy?
- Which renewable energy type has the highest generation?
- Which plants have the highest capacity utilization?
- Which regions generate the most energy?
- Which plants have the highest downtime?
- How do weather conditions relate to energy generation?
- Which plants have the lowest cost per MWh?
- What are the top-performing plants?
- Which months have the highest energy generation?
- Which plants have high installed capacity but relatively low generation?

## 📈 Power BI Dashboard

Power BI is the **main dashboard and visualization tool** used in this project.

The dashboard is organized into five analytical pages:

### 1. Executive Overview
- Total energy generated
- Installed capacity
- Average efficiency
- Capacity utilization
- Total revenue
- Total operating cost
- Energy generation trends
- Generation by energy type

### 2. Plant Performance
- Plant-wise energy generation
- Average efficiency
- Capacity utilization
- Plant availability
- High-performing and low-performing plants
- Cost per MWh

### 3. Renewable Energy Type Analytics
- Solar vs Wind vs Hydro comparison
- Average efficiency by energy type
- Installed capacity comparison
- Revenue comparison
- Cost per MWh
- Monthly generation trends

### 4. Weather & Operations
- Solar irradiance vs Solar generation
- Wind speed vs Wind generation
- Rainfall vs Hydro generation
- Downtime vs energy generation
- Maintenance hours vs efficiency
- Plant availability

### 5. Cost & Revenue Analytics
- Operating cost by plant
- Maintenance cost by plant
- Cost per MWh
- Revenue by energy type
- Revenue vs energy generation
- Monthly cost and revenue trends

## 🌐 Streamlit Data Explorer

A simple Streamlit application is developed to provide interactive access to renewable energy records.

### Features

- View energy generation records
- Filter data by energy type
- Filter by plant and region
- Select a date range
- Filter by plant status
- View basic summary statistics
- Explore individual plant details
- Download filtered data as CSV

**Note:** Power BI is used for the main dashboard. Streamlit is only used as a simple interactive data explorer.

## 📁 Project Structure

```text
Renewable_Energy_Performance_Analytics/
│
├── data/
│   ├── raw_energy_data.csv
│   └── cleaned_energy_data.csv
│
├── python/
│   ├── Data_Cleaning.ipynb
│   ├── EDA.ipynb
│   └── Performance_Analysis.ipynb
│
├── mysql/
│   ├── schema.sql
│   ├── queries.sql
│   └── views.sql
│
├── powerbi/
│   └── Renewable_Energy_Performance_Analytics.pbix
│
├── streamlit_app/
│   └── app.py
│
├── requirements.txt
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Renewable-Energy-Performance-Analytics.git
```

### 2. Navigate to the Project Folder

```bash
cd Renewable-Energy-Performance-Analytics
```

### 3. Install Required Libraries

```bash
pip install pandas numpy matplotlib seaborn streamlit
```

### 4. Run the Streamlit Application

```bash
streamlit run streamlit_app/app.py
```

## 💡 Expected Business Insights

This project aims to identify:

- Differences in energy generation across renewable energy types.
- High-performing and low-performing power plants.
- Capacity utilization and efficiency patterns.
- Relationships between weather conditions and energy generation.
- Plants with higher downtime or maintenance requirements.
- Operating and maintenance cost patterns.
- Revenue trends across energy types.
- Unusual energy generation patterns.

## 🚀 Project Outcome

The project demonstrates an end-to-end Data Analyst workflow, from raw data cleaning and exploratory analysis to SQL-based analysis, interactive dashboard development, and business insight generation.

It showcases practical skills in **Python, SQL, data visualization, dashboard development, and business analytics** within the renewable energy domain.

## 👩‍💻 Project Contributors

- Riya
- Kunika

---

⭐ If you find this project interesting, feel free to explore the repository!
