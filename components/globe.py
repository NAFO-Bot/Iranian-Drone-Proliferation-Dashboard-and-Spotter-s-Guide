import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from coords import country_coords
from components.metrics import render_dashboard_metrics


RECIPIENT_TYPE = {
    "Russia": "State",
    "Belarus": "State",
    "Syria": "State",
    "Sudan": "State",
    "Venezuela": "State",
    "Ethiopia": "State",
    "Algeria": "State",
    "Bolivia": "State",
    "Serbia": "State",
    "Tajikistan": "State",
    "Iraq": "State",
    "Lebanon (Hezbollah)": "Proxy",
    "Yemen (Houthi)": "Proxy",
    "Palestine (Hamas)": "Proxy",
    "Palestine (Palestinian Islamic Jihad)": "Proxy",
    "Iraq (PMF)": "Militia",
    "Libya (LNA)": "Militia"
}


LINE_COLOURS = {
    "State": "#3FA9F5",
    "Proxy": "#FF4B4B",
    "Militia": "#F7B731",
    "Unknown": "#A55EEA"
}


def render_globe(df: pd.DataFrame):

    st.subheader("🌍 Global Iranian Drone Proliferation")

    render_dashboard_metrics(df)

    if df.empty:
        st.warning("No records found.")
        return

    arc_data = []

    for _, row in df.iterrows():

        recipient = str(row["Seeker"]).strip()

        if recipient not in country_coords:
            continue

        actor = RECIPIENT_TYPE.get(
            recipient,
            "Unknown"
        )

        arc_data.append({

            "from_lon": country_coords["Iran"][0],
            "from_lat": country_coords["Iran"][1],

            "to_lon": country_coords[recipient][0],
            "to_lat": country_coords[recipient][1],

            "recipient": recipient,
            "platform": row["Paltform Model"],
            "year": row["Year of First Delivery"],
            "actor": actor

        })

    if len(arc_data) == 0:
        st.warning("No valid coordinates found.")
        return

    arc_df = pd.DataFrame(arc_data)

    fig = go.Figure()

    # --------------------------------------------------
    # Transfer Arcs
    # --------------------------------------------------

    for _, row in arc_df.iterrows():

        fig.add_trace(

            go.Scattergeo(

                lon=[
                    row["from_lon"],
                    row["to_lon"]
                ],

                lat=[
                    row["from_lat"],
                    row["to_lat"]
                ],

                mode="lines",

                line=dict(
                    width=2,
                    color=LINE_COLOURS.get(
                        row["actor"],
                        "#999999"
                    )
                ),

                hoverinfo="text",

                text=(
                    f"<b>{row['recipient']}</b><br>"
                    f"Platform: {row['platform']}<br>"
                    f"Year: {row['year']}<br>"
                    f"Actor: {row['actor']}"
                ),

                showlegend=False

            )

        )

    # --------------------------------------------------
    # Recipient markers
    # --------------------------------------------------

    fig.add_trace(

        go.Scattergeo(

            lon=arc_df["to_lon"],

            lat=arc_df["to_lat"],

            mode="markers",

            marker=dict(

                size=8,

                color="gold",

                line=dict(
                    color="black",
                    width=1
                )

            ),

            text=arc_df["recipient"],

            hovertemplate="<b>%{text}</b><extra></extra>",

            showlegend=False

        )

    )

    # --------------------------------------------------
    # Iran marker
    # --------------------------------------------------

    fig.add_trace(

        go.Scattergeo(

            lon=[country_coords["Iran"][0]],

            lat=[country_coords["Iran"][1]],

            mode="markers+text",

            marker=dict(
                size=12,
                color="red"
            ),

            text=["Iran"],

            textposition="top center",

            showlegend=False

        )

    )

    # --------------------------------------------------
    # Globe
    # --------------------------------------------------

    fig.update_geos(

        projection_type="orthographic",

        projection_rotation=dict(
            lon=45,
            lat=25
        ),

        showland=True,
        landcolor="#4a4a4a",

        showocean=True,
        oceancolor="#061A40",

        showcountries=True,
        countrycolor="gray",

        showcoastlines=True,
        coastlinecolor="white",

        bgcolor="black"

    )

    fig.update_layout(

        height=800,

        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        ),

        paper_bgcolor="black",
        plot_bgcolor="black"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Top Recipients")

        st.bar_chart(
            df["Seeker"].value_counts()
        )

    with col2:

        st.subheader("Top Platforms")

        st.bar_chart(
            df["Paltform Model"].value_counts()
        )
