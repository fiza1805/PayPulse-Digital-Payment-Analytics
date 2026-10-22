
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="PayPulse Dashboard",
    page_icon="💳",
    layout="wide"
)

# Dashboard title
st.markdown(
    """
    <h1 style="font-size:46px; font-weight:800;">
    💳 PayPulse
    </h1>
    <p style="font-size:20px; color:#64748b;">
    India's Digital Payment Intelligence Dashboard
    </p>
    """,
    unsafe_allow_html=True
)
st.caption("Data Source: PhonePe Pulse")

# Load real transaction data
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "processed_data" / "state_transactions.csv"

df = pd.read_csv(CSV_PATH)

# Select year
selected_year = st.selectbox(
    "Select Year",
    sorted(df["year"].unique(), reverse=True)
)

# State / UT filter
state_options = ["All India"] + sorted(df["state"].unique().tolist())

selected_state = st.selectbox(
    "Select State / UT",
    state_options
)

filtered_df = df[df["year"] == selected_year].copy()

if selected_state != "All India":
    filtered_df = filtered_df[
        filtered_df["state"] == selected_state
    ]

# Key metrics
total_transactions = filtered_df["transaction_count"].sum()
total_amount = filtered_df["transaction_amount"].sum()
states = filtered_df["state"].nunique()
# Average Transaction Value
average_transaction_value = (
    total_amount / total_transactions
    if total_transactions > 0 else 0
)

# Professional KPI cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.metric(
            "💳 Total Transactions",
            f"{total_transactions / 1e9:,.2f} Billion"
        )

with col2:
    with st.container(border=True):
        st.metric(
            "💰 Transaction Value",
            f"₹{total_amount / 1e12:,.2f} Trillion"
        )

with col3:
    with st.container(border=True):
        st.metric(
            "📍 States / UTs",
            states
        )
with col4:
    with st.container(border=True):
        st.metric(
            "📈 Avg. Transaction Value",
            f"₹{average_transaction_value:,.2f}"
        )
if selected_year == 2026:
    st.info(
        "2026 data currently covers Q1–Q2 only. "
        "These totals are year-to-date, not full-year figures."
    )


st.divider()

# Quarterly transaction trend
st.header("Quarterly Transaction Trends")

quarterly = (
    filtered_df.groupby("quarter", as_index=False)
    ["transaction_count"].sum()
)

fig = px.line(
    quarterly,
    x="quarter",
    y="transaction_count",
    markers=True,
    title="Quarterly Transaction Volume",
    labels={
        "quarter": "Quarter",
        "transaction_count": "Transactions"
    }
)

fig.update_xaxes(
    tickmode="array",
    tickvals=[1, 2, 3, 4],
    ticktext=["Q1", "Q2", "Q3", "Q4"]
)

st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Figures represent aggregated PhonePe Pulse "
    "transaction statistics."
)

# Top 10 states by transaction volume
st.divider()
st.header("Top 10 States by Transaction Volume")

# State rankings always compare all states
state_data = (
    df[df["year"] == selected_year]
    .groupby("state", as_index=False)["transaction_count"]
    .sum()
)

top_states = state_data.nlargest(
    10, "transaction_count"
).sort_values("transaction_count")

fig_states = px.bar(
    top_states,
    x="transaction_count",
    y="state",
    orientation="h",
    title=f"Top 10 States - {selected_year}",
    labels={
        "transaction_count": "Total Transactions",
        "state": "State / UT"
    },
    color="transaction_count",
    color_continuous_scale="Blues"
)

fig_states.update_layout(
    showlegend=False,
    coloraxis_showscale=False,
    height=500
)

st.plotly_chart(fig_states, use_container_width=True)
# STEP 16: Quarterly Transaction Growth

st.divider()
st.header("Quarterly Transaction Growth")

# Use the full dataset so Q1 can be compared
# with Q4 of the previous year.
# Calculate growth for the selected geography
growth_source = df.copy()

if selected_state != "All India":
    growth_source = growth_source[
        growth_source["state"] == selected_state
    ]

all_quarters = (
    growth_source
    .groupby(["year", "quarter"], as_index=False)["transaction_count"]
    .sum()
    .sort_values(["year", "quarter"])
)

all_quarters["growth_percentage"] = (
    all_quarters["transaction_count"].pct_change() * 100
)

# Filter for the selected year
growth_data = all_quarters[
    all_quarters["year"] == selected_year
].copy()

growth_data["quarter_label"] = (
    "Q" + growth_data["quarter"].astype(str)
)

# Create interactive bar chart
fig_growth = px.bar(
    growth_data,
    x="quarter_label",
    y="growth_percentage",
    title=f"Quarterly Growth Rate - {selected_year}",
    labels={
        "quarter_label": "Quarter",
        "growth_percentage": "Growth (%)"
    },
    color="growth_percentage",
    color_continuous_scale="Blues",
    text="growth_percentage"
)

fig_growth.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_growth.update_layout(
    coloraxis_showscale=False,
    yaxis_title="Quarter-over-Quarter Growth (%)"
)

st.plotly_chart(fig_growth, use_container_width=True)

# STEP 21: Automated Business Insights

st.divider()
st.header("📊 Business Insights")

yearly_states = (
    df[df["year"] == selected_year]
    .groupby("state", as_index=False)["transaction_count"]
    .sum()
)

top_state = yearly_states.loc[
    yearly_states["transaction_count"].idxmax()
]

top_state_name = top_state["state"].title()

top_state_share = (
    top_state["transaction_count"]
    / yearly_states["transaction_count"].sum()
) * 100

st.success(
    f"🏆 {top_state_name} recorded the highest transaction "
    f"volume in {selected_year}, accounting for "
    f"{top_state_share:.2f}% of the total."
)


# STEP 23: Historical State Leaders

st.divider()
st.header("🏆 Historical Transaction Leaders")

yearly_leaders = (
    df.groupby(["year", "state"], as_index=False)
    ["transaction_count"].sum()
)

leader_indices = (
    yearly_leaders.groupby("year")
    ["transaction_count"].idxmax()
)

leaders = (
    yearly_leaders.loc[
        leader_indices,
        ["year", "state", "transaction_count"]
    ]
    .sort_values("year",ascending=False)
    .copy()
)

leaders["state"] = leaders["state"].str.title()

leaders["transactions_billion"] = (
    leaders["transaction_count"] / 1e9
).round(2)

leaders = leaders.rename(columns={
    "year": "Year",
    "state": "Leading State",
    "transactions_billion": "Transactions (Billion)"
})

st.dataframe(
    leaders[
        ["Year", "Leading State", "Transactions (Billion)"]
    ],
    hide_index=True,
    use_container_width=True
)

st.caption(
    "2026 rankings use available Q1–Q2 data only."
)
