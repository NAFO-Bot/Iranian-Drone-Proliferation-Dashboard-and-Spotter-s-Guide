import streamlit as st
import pandas as pd


def render_analysis(df: pd.DataFrame):

    st.header("📊 Analysis")

    if df.empty:
        st.warning("No records found.")
        return

    # -----------------------------
    # Top Metrics
    # -----------------------------

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Export Events",
        len(df)
    )

    c2.metric(
        "Recipient States",
        df["Seeker"].nunique()
    )

    c3.metric(
        "Platforms",
        df["Paltform Model"].nunique()
    )

    st.divider()

    # -----------------------------
    # Charts
    # -----------------------------

    left, right = st.columns(2)

    with left:

        st.subheader("Top Recipients")

        recipients = (
            df["Seeker"]
            .value_counts()
        )

        st.bar_chart(recipients)

    with right:

        st.subheader("Most Exported Platforms")

        platforms = (
            df["Paltform Model"]
            .value_counts()
        )

        st.bar_chart(platforms)

    st.divider()

    # -----------------------------
    # Region Distribution
    # -----------------------------

    region_col = None

    if "Region" in df.columns:
        region_col = "Region"

    elif "Region " in df.columns:
        region_col = "Region "

    if region_col:

        st.subheader("Regional Distribution")

        st.bar_chart(
            df[region_col].value_counts()
        )

    st.divider()

    # -----------------------------
    # Executive Summary
    # -----------------------------

    st.subheader("Executive Summary")

    top_recipient = df["Seeker"].value_counts().idxmax()

    top_platform = df["Paltform Model"].value_counts().idxmax()

    delivery_years = pd.to_numeric(
        df["Year of First Delivery"],
        errors="coerce"
    ).dropna()

    first_year = int(delivery_years.min())

    latest_year = int(delivery_years.max())

    st.info(
        f"""
**Key Findings**

• Total export events: **{len(df)}**

• Recipient entities: **{df['Seeker'].nunique()}**

• Platforms identified: **{df['Paltform Model'].nunique()}**

• Most frequent recipient: **{top_recipient}**

• Most exported platform: **{top_platform}**

• Recorded deliveries span **{first_year}–{latest_year}**.
"""
    )