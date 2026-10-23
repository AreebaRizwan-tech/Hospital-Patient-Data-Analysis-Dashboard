import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Hospital Patient Dashboard",
    page_icon="🏥",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background-color: white;
}

.dashboard-title {
    font-size: 40px;
    font-weight: 700;
    color: #16324f;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    font-size: 17px;
    color: #64748b;
    margin-bottom: 25px;
}

.section-heading {
    font-size: 24px;
    font-weight: 650;
    color: #16324f;
    margin-top: 25px;
    margin-bottom: 15px;
}

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #dbe4ee;
    padding: 10px;
    border-radius: 8px;
    box-shadow: 0px 4px 10px rgba(15, 23, 42, 0.06);
}

[data-testid="stMetricValue"] {
    font-size: 27px;
    font-weight: bold;
    color: #16324f;
}

[data-testid="stSidebar"] {
    background-color: #E8E8E8;
    border-right: 1px solid #F3C5BE;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 0rem;
}

[data-testid="stSidebar"] h2 {
    margin-bottom:bold;
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #16324f;
    font-weight: 700;
}

[data-testid="stSidebar"] label {
    color: #334155;
    font-weight: 600;
}

[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    border-radius: 8px;
    border: 1px solid #E58B7D;
    background-color: white;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
/* Plotly Chart Titles */
.js-plotly-plot .gtitle {
    font-size: 20px !important;
    font-weight: 600 !important;
}

/* Key Insight Cards */
.insight-card {
    background-color: #f8fafc;
    border-left: 5px solid #475569;
    border-radius: 10px;
    padding: 18px;
    min-height: 140px;
    box-shadow: 0px 3px 8px rgba(0, 0, 0, 0.05);
}

.insight-title {
    font-size: 16px;
    font-weight: 600;
    color: #334155;
    margin-bottom: 10px;
}

.insight-value {
    font-size: 22px;
    font-weight: 700;
    color: #1f77b4;
    margin-bottom: 5px;
}

.insight-detail {
    font-size: 14px;
    color: #64748b;
}

}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="dashboard-title">🏥 Hospital Patient Data Analysis Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">An interactive dashboard for analyzing hospital patient data</div>',
    unsafe_allow_html=True
)

df = pd.read_csv("healthcare_dataset.csv")

print(df.head())
print(df.columns)
print(df.info())
print(df.isnull().sum())
print(df.duplicated().sum())
df=df.drop_duplicates()
print("Remaining duplicates:", df.duplicated().sum())
print("Total records:", len(df))

print(df["Billing Amount"].dtype)
total_patients = len(df)
total_billing = df["Billing Amount"].sum()
average_billing = df["Billing Amount"].mean()
total_hospitals = df["Hospital"].nunique()

total_hospitals = df["Hospital"].nunique()

df["Admission Month"] = pd.to_datetime(df["Date of Admission"]).dt.to_period("M").astype(str)


with st.sidebar:
    st.header("🔍 Filter Data")
    gender_filter = st.selectbox(
        "Select Gender",
        ["All"] + sorted(df["Gender"].dropna().unique().tolist())
    )

    condition_filter = st.selectbox(
        "Select Medical Condition",
        ["All"] + sorted(df["Medical Condition"].dropna().unique().tolist())
    )

    admission_filter = st.selectbox(
        "Select Admission Type",
        ["All"] + sorted(df["Admission Type"].dropna().unique().tolist())
    )

filtered_df = df.copy()

if gender_filter != "All":
    filtered_df = filtered_df[filtered_df["Gender"] == gender_filter]

if condition_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Medical Condition"] == condition_filter
    ]

if admission_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Admission Type"] == admission_filter
    ]

 # Sidebar About
with st.sidebar:
    st.divider()
    st.sidebar.markdown(""" 
<style>

.category-heading {
    color: #16324F;
    font-size: 18px;
    font-weight: 700;
    margin-top: 20px;
    margin-bottom: 15px;
}

.category-box {
    background-color: #F0F4F8;
    padding: 12px;
    border-radius: 8px;
    border-left: 4px solid #1B4965;
    margin-bottom: 6px;
}

.category-box b {
    color: #16324F;
}

.category-box span {
    color: #666;
    font-size: 13px;
}

</style>

<div class="category-heading">
📊 Analysis Categories
</div>

<div class="category-box">
📈 <b>Admission Trends</b><br>
<span>Monthly Patient Admissions</span>
</div>

<div class="category-box">
👥 <b>Demographics</b><br>
<span>Gender & Blood Type</span>
</div>

<div class="category-box">
📋 <b>Clinical</b><br>
<span>Medical Condition & Admission Type</span>
</div>

<div class="category-box">
💊 <b>Medication</b><br>
<span>Top 5 Medications</span>
</div>
""", unsafe_allow_html=True)
    st.divider()

    st.subheader("ℹ️ About")

    st.caption(
        "This dashboard analyzes hospital patient records including "
        "demographics, billing, and admission trends. Use filters above "
        "to explore specific patient segments."
    )   

total_patients = len(filtered_df)
total_billing = filtered_df["Billing Amount"].sum()
average_billing = filtered_df["Billing Amount"].mean()
total_hospitals = filtered_df["Hospital"].nunique()

st.markdown('<div class="section-heading">📊 Key Performance Indicators</div>', unsafe_allow_html=True)

col1,col2,col3,col4=st.columns(4)

col1.metric("Total Patients", f"{total_patients/1000:.1f}K")
col2.metric("Total Billing", f"{total_billing/1000000:.1f}M")
col3.metric("Average Billing", f"{average_billing:,.2f}")
col4.metric("Total Hospitals", f"{total_hospitals:,}")

print("Total Patients:", total_patients)
print("Total Billing:", total_billing)
print("Average Billing:", average_billing)
print("Total Hospitals:", total_hospitals)

st.markdown('<div class="section-heading">📈 Patient Analysis</div>', unsafe_allow_html=True)

# Monthly Patient Admissions - Main Trend Chart
monthly_admissions = filtered_df["Admission Month"].value_counts().sort_index()

fig3 = px.line(
    x=monthly_admissions.index,
    y=monthly_admissions.values,
    title="Monthly Patient Admissions",
    labels={"x": "Month", "y": "Number of Patients"},
)

fig3.update_traces(
    line=dict(color="#186FE0", width=3),
)

st.plotly_chart(fig3, use_container_width=True)

tab1, tab2, tab3 = st.tabs([
    "📊 Demographics",
    "🏥 Clinical",
    "💊 Medication"
])
with tab1:

    # ==========================================
    # Gender Distribution
    # ==========================================

    gender_count = (
        filtered_df["Gender"]
        .value_counts()
        .reset_index()
    )

    gender_count.columns = ["Gender", "Count"]

    total_patients = gender_count["Count"].sum()

    fig4 = px.pie(
        gender_count,
        names="Gender",
        values="Count",
        color="Gender",
        color_discrete_map={
            "Male": "#3498DB",
            "Female": "#2E86C1"
        },
        hole=0.55
    )

    fig4.update_traces(
        textinfo="label+percent",
        textposition="inside"
    )

    fig4.add_annotation(
        text=f"<b>{total_patients:,}</b><br>Total Patients",
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(
            size=16,
            color="#16324F"
        )
    )

    fig4.update_layout(
        title="Gender Distribution",
        showlegend=True,
        height=450
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )


    # ==========================================
    # Blood Type Analysis
    # ==========================================

    blood_order = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]

    blood_count = (
        filtered_df["Blood Type"]
        .value_counts()
        .reindex(blood_order, fill_value=0)
    )

    fig5 = px.bar(
        x=blood_count.index,
        y=blood_count.values,
        color=blood_count.index,

        color_discrete_sequence=[
            "#1B4F72",
            "#21618C",
            "#2874A6",
            "#2E86C1",
            "#3498DB",
            "#5DADE2",
            "#85C1E9",
            "#AED6F1"
        ],

        labels={
            "x": "Blood Type",
            "y": "Number of Patients"
        },

        title="Patients by Blood Type"
    )

    fig5.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,

        title_font=dict(
            size=20,
            color="#16324F"
        ),

        height=450
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )


with tab2:

 col1, col2 = st.columns(2)

    # Medical Condition
with col1:

        condition_counts = filtered_df["Medical Condition"].value_counts()

        fig_condition = px.bar(
                   x=condition_counts.index,
            y=condition_counts.values,
            title="Patients by Medical Condition",
            labels={
                "x": "Medical Condition",
                "y": "Number of Patients"
            },
            color_discrete_sequence=["#2E86C1"]
        )

        fig_condition.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
            title_font=dict(
                size=20,
                color="#16324f"
            )
        )

        st.plotly_chart(
            fig_condition,
            use_container_width=True
        )


    # Admission Type
with col2:

        admission_counts = filtered_df["Admission Type"].value_counts()

        fig_admission = px.bar(
            x=admission_counts.index,
            y=admission_counts.values,
            title="Patients by Admission Type",
            labels={
                "x": "Admission Type",
                "y": "Number of Patients"
            },
            color=admission_counts.index,
            color_discrete_map={
                "Elective": "#5DADE2",
                "Urgent": "#3498DB",
                "Emergency":"#2874A6"
            }
        )
         
        fig_condition.update_traces(width=0.5)
        fig_admission.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            showlegend=False,
            title_font=dict(
                size=20,
                color="#16324f"
            )
        )

        st.plotly_chart(
            fig_admission,
            use_container_width=True
        )
      
  # Key Insights Section
st.markdown(
    '<div class="section-heading">💡 Key Insights</div>',
    unsafe_allow_html=True
)

if not filtered_df.empty:

    top_condition = filtered_df["Medical Condition"].value_counts().idxmax()
    top_condition_pct = round(
        filtered_df["Medical Condition"].value_counts(normalize=True).max() * 100,
        1
    )

    top_admission = filtered_df["Admission Type"].value_counts().idxmax()
    top_admission_pct = round(
        filtered_df["Admission Type"].value_counts(normalize=True).max() * 100,
        1
    )

    top_month = filtered_df["Admission Month"].value_counts().idxmax()
    top_month_count = filtered_df["Admission Month"].value_counts().max()

    insight_col1, insight_col2, insight_col3 = st.columns(3)

    with insight_col1:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">🏥 Most Common Condition</div>
                <div class="insight-value">{top_condition}</div>
                <div class="insight-detail">{top_condition_pct}% of patients</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with insight_col2:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">🚑 Most Common Admission Type</div>
                <div class="insight-value">{top_admission}</div>
                <div class="insight-detail">{top_admission_pct}% of patients</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with insight_col3:
        st.markdown(
            f"""
            <div class="insight-card">
                <div class="insight-title">📈 Busiest Admission Month</div>
                <div class="insight-value">{top_month}</div>
                <div class="insight-detail">{top_month_count:,} patients</div>
            </div>
            """,
            unsafe_allow_html=True
        )

monthly_admissions =filtered_df["Admission Month"].value_counts().sort_index()

print(monthly_admissions)

left_space, gender_col, right_space = st.columns([1, 3, 1])

with tab3:

    # Top 5 Medication Analysis
    medication_summary = filtered_df.groupby("Medication").agg(
        Total_Patients=("Medication", "count"),
        Avg_Billing=("Billing Amount", "mean")
    ).reset_index()

    medication_summary["Avg_Billing"] = medication_summary["Avg_Billing"].round(2)

    top_5_medications = medication_summary.sort_values(
        "Total_Patients",
        ascending=False
    ).head(5)

    st.markdown(
        '<div class="section-heading">💊 Top 5 Medication Analysis</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "A summary of medications based on total patients and average billing amount."
    )

    st.dataframe(
        top_5_medications,
        use_container_width=True,
        hide_index=True
    )


st.divider()
st.subheader("📋 Full Dataset")

st.dataframe(filtered_df, use_container_width=True, hide_index=True)

csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv,
    file_name='filtered_hospital_data.csv',
    mime='text/csv',
)



    

