import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Renewable Energy Analytics",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# CUSTOM CSS THEME
# =====================================================
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #F0FDF4, #E0F2F1); }
h1 { color: #087443; text-align: center; font-size: 40px; font-weight: bold; }
h2, h3 { color: #15803D; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #064E3B, #166534); }
[data-testid="stSidebar"] * { color: white; }
/* keep text readable inside white widgets in the sidebar */
[data-testid="stSidebar"] [data-testid="stFileUploader"] * { color: #064E3B; }
[data-testid="stSidebar"] [data-baseweb="select"] * { color: #064E3B; }
[data-testid="stMetric"] {
    background: white; padding: 18px; border-radius: 14px;
    border-left: 5px solid #16A34A; box-shadow: 0px 3px 10px rgba(0,0,0,0.08);
}
.stButton > button { background-color: #15803D; color: white; border-radius: 10px; border: none; }
.stButton > button:hover { background-color: #064E3B; color: white; }
[data-testid="stFileUploader"] { background: white; padding: 12px; border-radius: 12px; }
[data-testid="stDataFrame"] { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================
st.title("🌱 Renewable Energy Analytics Dashboard")
st.markdown(
    "<p style='text-align:center;color:#39745A;'>"
    "Explore renewable energy generation, plant performance, "
    "weather conditions and maintenance analytics."
    "</p>",
    unsafe_allow_html=True,
)
st.divider()

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("🌿 ENERGY ANALYTICS")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Dashboard",
        "⚡ Energy Analysis",
        "🌦 Weather Analysis",
        "🔧 Maintenance Analysis",
        "🏆 Plant Performance",
        "📋 Dataset Information",
        "📥 Download Report",
        "ℹ️ About Project",
    ],
)

st.sidebar.markdown("---")
st.sidebar.subheader("📂 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload renewable_energy_clean.csv", type=["csv"])
st.sidebar.info("Upload the exported raw_energy_data CSV file.")

# =====================================================
# NO FILE -> LANDING MESSAGE, THEN STOP
# =====================================================
if uploaded_file is None:
    st.warning("📂 Please upload renewable_energy_clean.csv using the sidebar to start the analysis.")
    st.info("Export the raw_energy_data table from MySQL as a CSV file.")
    st.markdown("""
    ### 🌍 Explore Renewable Energy

    This dashboard analyzes:

    - ☀️ Solar Energy
    - 🌬️ Wind Energy
    - 💧 Hydro Energy
    - 🌦 Weather Conditions
    - 🔧 Plant Maintenance
    - 🏆 Plant Performance
    """)
    st.stop()

# =====================================================
# LOAD DATASET
# =====================================================
NUMERIC_COLUMNS = [
    "Installed_Capacity_MW", "Energy_Generated_MWh", "Capacity_Utilization",
    "Efficiency_Percent", "Availability_Percent", "Operating_Cost",
    "Maintenance_Cost", "Revenue", "Cost_per_MWh", "Revenue_per_MWh",
    "Maintenance_Cost_per_MWh", "Downtime_Hours", "Maintenance_Hours",
    "Downtime_Rate", "Plant_Performance_Score", "Temperature_C",
    "Wind_Speed_kmh", "Solar_Irradiance", "Rainfall_mm",
]


@st.cache_data(show_spinner="Loading dataset...")
def load_data(file):
    data = pd.read_csv(file)
    data.columns = [str(c).strip() for c in data.columns]
    if "Date" in data.columns:
        data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    for col in NUMERIC_COLUMNS:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
    return data


try:
    df = load_data(uploaded_file)
except Exception as exc:
    st.error(f"Could not read the CSV file: {exc}")
    st.stop()

st.sidebar.success("Dataset uploaded successfully! ✅")

# =====================================================
# SIDEBAR FILTERS
# =====================================================
st.sidebar.markdown("---")
st.sidebar.subheader("🎛 Dataset Filters")

filtered_df = df.copy()

for col, label in [
    ("Energy_Type", "Select Energy Type"),
    ("Region", "Select Region"),
    ("Plant_Status", "Select Plant Status"),
]:
    if col in filtered_df.columns:
        options = sorted(filtered_df[col].dropna().unique())
        chosen = st.sidebar.multiselect(label, options, default=options)
        filtered_df = filtered_df[filtered_df[col].isin(chosen)]

if "Date" in filtered_df.columns:
    valid_dates = filtered_df["Date"].dropna()
    if not valid_dates.empty:
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(valid_dates.min().date(), valid_dates.max().date()),
        )
        if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
            start_date, end_date = date_range
            filtered_df = filtered_df[filtered_df["Date"].dt.date.between(start_date, end_date)]

if filtered_df.empty:
    st.warning("No records match the selected filters. Change or clear the filters.")
    st.stop()


def has(*cols):
    return all(c in filtered_df.columns for c in cols)



# =====================================================
# CHART HELPERS (matplotlib only)
# =====================================================
def show(fig):
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


def bar_chart(data, x, y, title, horizontal=False, rotate=0):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    if horizontal:
        ax.barh(data[x].astype(str), data[y], color="#16A34A")
        ax.invert_yaxis()
        ax.set_xlabel(y)
    else:
        ax.bar(data[x].astype(str), data[y], color="#16A34A")
        ax.set_ylabel(y)
        plt.setp(ax.get_xticklabels(), rotation=rotate, ha="right" if rotate else "center")
    ax.set_title(title)
    show(fig)


def pie_chart(data, names, values, title, donut=True):
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.pie(
        data[values], labels=data[names].astype(str), autopct="%1.1f%%", startangle=90,
        wedgeprops={"width": 0.45} if donut else None, textprops={"fontsize": 9},
    )
    ax.set_title(title)
    show(fig)


def box_chart(data, x, y, title):
    groups = [(k, g[y].dropna()) for k, g in data.groupby(x)]
    groups = [(k, v) for k, v in groups if not v.empty]
    if not groups:
        st.info("Not enough data for this chart.")
        return
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.boxplot([v for _, v in groups])
    ax.set_xticklabels([str(k) for k, _ in groups])
    ax.set_ylabel(y)
    ax.set_title(title)
    show(fig)


def scatter_chart(data, x, y, title, color=None):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    if color and color in data.columns:
        for key, grp in data.groupby(color):
            ax.scatter(grp[x], grp[y], alpha=0.6, s=18, label=str(key))
        ax.legend(title=color, fontsize=8)
    else:
        ax.scatter(data[x], data[y], alpha=0.6, s=18, color="#16A34A")
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(title)
    show(fig)


def line_chart(data, x, y, title):
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(data[x], data[y], marker="o", color="#16A34A")
    ax.set_ylabel(y)
    ax.set_title(title)
    step = max(1, len(data) // 12)
    ax.set_xticks(range(0, len(data), step))
    ax.set_xticklabels(data[x].iloc[::step], rotation=45, ha="right")
    show(fig)


# =====================================================
# HOME
# =====================================================
if menu == "🏠 Home":
    st.header("🌱 Welcome to Renewable Energy Analytics")
    st.markdown("""
    This project provides an interactive analysis of renewable energy data.

    **Main objectives:**

    - Analyze solar, wind and hydro energy generation.
    - Evaluate renewable energy plant performance.
    - Study weather conditions and energy generation.
    - Analyze operating and maintenance costs.
    - Identify high-performing energy plants.
    """)
    st.divider()

    st.subheader("📊 Dataset Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Records", f"{len(filtered_df):,}")
    if "Plant_ID" in filtered_df.columns:
        c2.metric("Total Plants", f"{filtered_df['Plant_ID'].nunique():,}")
    if "Energy_Type" in filtered_df.columns:
        c3.metric("Energy Types", f"{filtered_df['Energy_Type'].nunique():,}")
    c4.metric("Missing Values", f"{int(filtered_df.isnull().sum().sum()):,}")
    st.divider()

    st.subheader("📋 Dataset Preview")
    st.dataframe(filtered_df.head(10), use_container_width=True)

    st.subheader("🌍 Energy Sources")
    if has("Energy_Type", "Energy_Generated_MWh"):
        energy_by_source = (
            filtered_df.groupby("Energy_Type")["Energy_Generated_MWh"].sum().reset_index()
        )
        pie_chart(energy_by_source, "Energy_Type", "Energy_Generated_MWh",
                  "Renewable Energy Generation by Source")
    else:
        st.warning("Required columns (Energy_Type, Energy_Generated_MWh) are missing from the dataset.")

# =====================================================
# DASHBOARD
# =====================================================
elif menu == "📊 Dashboard":
    st.header("📊 Renewable Energy Dashboard")

    total_energy = filtered_df["Energy_Generated_MWh"].sum() if has("Energy_Generated_MWh") else 0
    total_revenue = filtered_df["Revenue"].sum() if has("Revenue") else 0
    avg_efficiency = filtered_df["Efficiency_Percent"].mean() if has("Efficiency_Percent") else 0
    total_capacity = (
        filtered_df.drop_duplicates("Plant_ID")["Installed_Capacity_MW"].sum()
        if has("Plant_ID", "Installed_Capacity_MW")
        else 0
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("⚡ Total Generation", f"{total_energy:,.2f} MWh")
    c2.metric("💰 Total Revenue", f"{total_revenue:,.2f}")
    c3.metric("📈 Avg Efficiency", f"{avg_efficiency:,.2f}%")
    c4.metric("🏭 Installed Capacity", f"{total_capacity:,.2f} MW")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if has("Energy_Type", "Energy_Generated_MWh"):
            energy_summary = (
                filtered_df.groupby("Energy_Type")["Energy_Generated_MWh"].sum().reset_index()
            )
            bar_chart(energy_summary, "Energy_Type", "Energy_Generated_MWh",
                      "Energy Generation by Type")

    with col2:
        if has("Region", "Energy_Generated_MWh"):
            region_summary = (
                filtered_df.groupby("Region")["Energy_Generated_MWh"].sum().reset_index()
            )
            pie_chart(region_summary, "Region", "Energy_Generated_MWh",
                      "Regional Energy Distribution")

    if has("Date", "Energy_Generated_MWh"):
        monthly = filtered_df.dropna(subset=["Date"]).copy()
        if not monthly.empty:
            monthly["Month"] = monthly["Date"].dt.to_period("M").astype(str)
            monthly = (
                monthly.groupby("Month")["Energy_Generated_MWh"].sum().reset_index().sort_values("Month")
            )
            line_chart(monthly.reset_index(drop=True), "Month", "Energy_Generated_MWh",
                       "Monthly Energy Generation")

# =====================================================
# ENERGY ANALYSIS
# =====================================================
elif menu == "⚡ Energy Analysis":
    st.header("⚡ Energy Generation Analysis")

    col1, col2 = st.columns(2)
    with col1:
        if has("Energy_Type", "Energy_Generated_MWh"):
            box_chart(filtered_df, "Energy_Type", "Energy_Generated_MWh",
                      "Generation Distribution by Energy Type")

    with col2:
        if has("Capacity_Utilization", "Energy_Type"):
            bar_chart(
                filtered_df.groupby("Energy_Type")["Capacity_Utilization"].mean().reset_index(),
                "Energy_Type", "Capacity_Utilization", "Average Capacity Utilization",
            )

    if has("Revenue", "Operating_Cost"):
        scatter_chart(filtered_df, "Operating_Cost", "Revenue", "Operating Cost vs Revenue",
                      color="Energy_Type" if has("Energy_Type") else None)

    if has("Cost_per_MWh", "Energy_Type"):
        cost_summary = filtered_df.groupby("Energy_Type")["Cost_per_MWh"].mean().reset_index()
        bar_chart(cost_summary, "Energy_Type", "Cost_per_MWh", "Average Cost per MWh")

# =====================================================
# WEATHER ANALYSIS
# =====================================================
elif menu == "🌦 Weather Analysis":
    st.header("🌦 Weather Impact on Energy Generation")

    weather_options = ["Temperature_C", "Wind_Speed_kmh", "Solar_Irradiance", "Rainfall_mm"]
    available_weather = [c for c in weather_options if c in filtered_df.columns]

    if available_weather and has("Energy_Generated_MWh"):
        selected_weather = st.selectbox("Select Weather Parameter", available_weather)
        scatter_chart(filtered_df, selected_weather, "Energy_Generated_MWh",
                      f"{selected_weather} vs Energy Generation",
                      color="Energy_Type" if has("Energy_Type") else None)
    else:
        st.warning("Weather or energy generation columns are missing.")

    if available_weather:
        st.subheader("Weather Summary")
        st.dataframe(filtered_df[available_weather].describe(), use_container_width=True)

# =====================================================
# MAINTENANCE ANALYSIS
# =====================================================
elif menu == "🔧 Maintenance Analysis":
    st.header("🔧 Plant Maintenance Analysis")

    downtime = filtered_df["Downtime_Hours"].sum() if has("Downtime_Hours") else 0
    maintenance_cost = filtered_df["Maintenance_Cost"].sum() if has("Maintenance_Cost") else 0
    maintenance_hours = filtered_df["Maintenance_Hours"].sum() if has("Maintenance_Hours") else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Downtime", f"{downtime:,.2f} Hours")
    col2.metric("Maintenance Cost", f"{maintenance_cost:,.2f}")
    col3.metric("Maintenance Hours", f"{maintenance_hours:,.2f}")

    if has("Plant_Name", "Downtime_Hours"):
        maintenance = filtered_df.groupby("Plant_Name")["Downtime_Hours"].sum().reset_index()
        maintenance = maintenance.nlargest(10, "Downtime_Hours")
        bar_chart(maintenance.sort_values("Downtime_Hours", ascending=False),
                  "Plant_Name", "Downtime_Hours", "Top 10 Plants by Downtime",
                  horizontal=True)

    if has("Maintenance_Cost", "Energy_Type"):
        box_chart(filtered_df, "Energy_Type", "Maintenance_Cost",
                  "Maintenance Cost by Energy Type")

# =====================================================
# PLANT PERFORMANCE
# =====================================================
elif menu == "🏆 Plant Performance":
    st.header("🏆 Plant Performance Analysis")

    if has("Plant_Name"):
        performance_columns = [
            "Efficiency_Percent", "Capacity_Utilization",
            "Availability_Percent", "Plant_Performance_Score",
        ]
        available = [c for c in performance_columns if c in filtered_df.columns]

        if available:
            performance = filtered_df.groupby("Plant_Name")[available].mean().reset_index()

            if "Plant_Performance_Score" in performance.columns:
                performance = performance.sort_values("Plant_Performance_Score", ascending=False)

                st.subheader("Top 10 Performing Plants")
                st.dataframe(performance.head(10), use_container_width=True)

                bar_chart(performance.head(10), "Plant_Name", "Plant_Performance_Score",
                          "Top 10 Plants by Performance Score", rotate=45)
            else:
                st.dataframe(
                    performance.sort_values(available[0], ascending=False).head(10),
                    use_container_width=True,
                )
        else:
            st.info("No performance columns are available in this dataset.")
    else:
        st.info("Plant_Name column is not available in this dataset.")

# =====================================================
# DATASET INFORMATION
# =====================================================
elif menu == "📋 Dataset Information":
    st.header("📋 Dataset Information")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Dataset Preview", "Shape & Columns", "Missing Values", "Statistics"]
    )

    with tab1:
        st.dataframe(filtered_df, use_container_width=True)

    with tab2:
        st.write("Rows:", filtered_df.shape[0])
        st.write("Columns:", filtered_df.shape[1])
        st.write("Column Names:")
        st.write(list(filtered_df.columns))
        st.write("Data Types:")
        st.write(filtered_df.dtypes.astype(str))

    with tab3:
        missing = filtered_df.isnull().sum().reset_index()
        missing.columns = ["Column", "Missing Values"]
        st.dataframe(missing, use_container_width=True)
        bar_chart(missing, "Column", "Missing Values", "Missing Values by Column", rotate=45)

    with tab4:
        # astype(str) avoids Arrow errors from mixed-type describe() output
        st.dataframe(
            filtered_df.describe(include="all").T.astype(str),
            use_container_width=True,
        )

    st.write("Duplicate Records:", int(filtered_df.duplicated().sum()))

# =====================================================
# DOWNLOAD REPORT
# =====================================================
elif menu == "📥 Download Report":
    st.header("📥 Download Analytics Report")
    st.subheader("🤖 Automatic Insights")

    if has("Energy_Generated_MWh"):
        st.info(f"Total Energy Generated: {filtered_df['Energy_Generated_MWh'].sum():,.2f} MWh")
        st.info(f"Average Energy Generated: {filtered_df['Energy_Generated_MWh'].mean():,.2f} MWh")

    if has("Energy_Type", "Energy_Generated_MWh"):
        energy_ranking = filtered_df.groupby("Energy_Type")["Energy_Generated_MWh"].sum()
        if not energy_ranking.empty:
            st.success(f"Highest Generation Energy Type: {energy_ranking.idxmax()}")

    if has("Plant_Name", "Energy_Generated_MWh"):
        plant_ranking = filtered_df.groupby("Plant_Name")["Energy_Generated_MWh"].sum()
        if not plant_ranking.empty:
            st.success(f"Highest Generating Plant: {plant_ranking.idxmax()}")

    if has("Efficiency_Percent"):
        st.info(f"Average Efficiency: {filtered_df['Efficiency_Percent'].mean():.2f}%")

    if has("Downtime_Hours"):
        st.warning(f"Total Plant Downtime: {filtered_df['Downtime_Hours'].sum():,.2f} hours")

    st.divider()

    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Filtered Dataset",
        data=csv,
        file_name="renewable_energy_report.csv",
        mime="text/csv",
    )

# =====================================================
# ABOUT PROJECT
# =====================================================
elif menu == "ℹ️ About Project":
    st.header("ℹ️ About Renewable Energy Analytics")
    st.markdown("""
    ### 🌱 Project Overview

    **Project Name:** Renewable Energy Analytics

    **Project Type:** Data Analytics and Visualization

    ### 🎯 Objectives

    1. Analyze renewable energy generation.
    2. Compare Solar, Wind and Hydro energy.
    3. Study the impact of weather on generation.
    4. Monitor plant efficiency and availability.
    5. Analyze maintenance costs and downtime.
    6. Identify top-performing renewable energy plants.

    ### 🛠 Technologies Used

    - Python
    - SQL / MySQL
    - Streamlit
    - Pandas
    - Matplotlib

    ### 📊 Database Tables

    1. Plants
    2. Energy_Generation
    3. Weather_Data
    4. Maintenance_Records

    ### 📌 Project Outcome

    An interactive analytics dashboard that helps explore renewable energy
    generation, operational performance, weather conditions and maintenance data.
    """)

# =====================================================
# FOOTER (shown on every page)
# =====================================================
st.divider()
st.markdown(
    "<h4 style='text-align:center;color:#15803D;'>🌱 Renewable Energy Analytics Dashboard</h4>",
    unsafe_allow_html=True,
)
st.caption("Developed using Python, Streamlit, Pandas and Matplotlib")