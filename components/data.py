from pathlib import Path

import pandas as pd
import streamlit as st

# =============================================================================
# Data Path
# =============================================================================

DATA_PATH = (
    Path(__file__).parent.parent
    / "data"
    / "Proliferation_Master Sheet_Sept 2024.xlsx"
)


# =============================================================================
# Load Data
# =============================================================================

@st.cache_data
def load_data():
    """Load the master proliferation dataset."""

    df = pd.read_excel(
        DATA_PATH,
        sheet_name="Full Data Set"
    )

    # Clean column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
    )

    return df


# =============================================================================
# Database Viewer
# =============================================================================

def render_database():

    st.title("📊 Database Explorer")

    st.markdown(
        """
Browse the complete Iranian Drone Proliferation Database or filter
records by recipient country.
"""
    )

    df = load_data()

    # -------------------------------------------------------------------------
    # Detect Country Column Automatically
    # -------------------------------------------------------------------------

    possible_columns = [
        "Country",
        "Recipient Country",
        "Operator Country",
        "Recipient",
        "Nation"
    ]

    country_column = None

    for col in possible_columns:
        if col in df.columns:
            country_column = col
            break

    if country_column is None:
        st.error(
            "No country column could be found.\n\n"
            f"Available columns:\n\n{list(df.columns)}"
        )
        return

    # -------------------------------------------------------------------------
    # Sidebar Filters
    # -------------------------------------------------------------------------

    st.sidebar.header("Filters")

    countries = sorted(
        df[country_column]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_countries = st.sidebar.multiselect(
        "Recipient Country",
        countries
    )

    # -------------------------------------------------------------------------
    # Filter Dataset
    # -------------------------------------------------------------------------

    filtered_df = df.copy()

    if selected_countries:
        filtered_df = filtered_df[
            filtered_df[country_column].isin(selected_countries)
        ]

    # -------------------------------------------------------------------------
    # Statistics
    # -------------------------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Original Records",
            len(df)
        )

    with col2:
        st.metric(
            "Filtered Records",
            len(filtered_df)
        )

    st.divider()

    # -------------------------------------------------------------------------
    # Display Tables
    # -------------------------------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.subheader("Original Database")

        st.dataframe(
            df,
            use_container_width=True,
            height=650
        )

    with right:

        st.subheader("Filtered Database")

        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=650
        )

    # -------------------------------------------------------------------------
    # Download Filtered Dataset
    # -------------------------------------------------------------------------

    st.divider()

    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Filtered Dataset",
        data=csv,
        file_name="filtered_proliferation_database.csv",
        mime="text/csv"
    )