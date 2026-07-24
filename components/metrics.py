import streamlit as st
import pandas as pd


def render_sidebar(df: pd.DataFrame):

    st.sidebar.title("🇮🇷 Iran Dashboard")

    transfers = len(df)

    recipients = df["Seeker"].nunique()

    platforms = df["Paltform Model"].nunique()

    regions = (
        df["Region"].nunique()
        if "Region" in df.columns
        else (
            df["Region "].nunique()
            if "Region " in df.columns
            else 0
        )
    )

    years = pd.to_numeric(
        df["Year of First Delivery"],
        errors="coerce"
    )

    st.sidebar.metric(
        "Export Events",
        transfers
    )

    st.sidebar.metric(
        "Recipients",
        recipients
    )

    st.sidebar.metric(
        "Platforms",
        platforms
    )

    st.sidebar.metric(
        "Regions",
        regions
    )

    st.sidebar.metric(
        "First Export",
        int(years.min())
    )

    st.sidebar.metric(
        "Latest Export",
        int(years.max())
    )

    st.sidebar.divider()

    st.sidebar.caption("Dataset")

    st.sidebar.write(f"Rows: **{len(df)}**")

    st.sidebar.write(f"Columns: **{len(df.columns)}**")


def render_dashboard_metrics(df: pd.DataFrame):

    transfers = len(df)

    recipients = df["Seeker"].nunique()

    platforms = df["Paltform Model"].nunique()

    years = pd.to_numeric(
        df["Year of First Delivery"],
        errors="coerce"
    )

    first_export = int(years.min())

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Export Events",
        transfers
    )

    c2.metric(
        "Recipients",
        recipients
    )

    c3.metric(
        "Platforms",
        platforms
    )

    c4.metric(
        "First Export",
        first_export
    )