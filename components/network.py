import os
import math
import tempfile

import networkx as nx
from pyvis.network import Network

import streamlit as st
from streamlit.components.v1 import html


# ============================================================
# Region Colours
# ============================================================

REGION_COLORS = {
    "Africa": "#2ECC71",
    "Europe": "#3498DB",
    "Middle East": "#9B59B6",
    "Asia": "#F39C12",
    "Americas": "#1ABC9C",
}


# ============================================================
# Helper Functions
# ============================================================

def get_region_colour(region):
    return REGION_COLORS.get(region, "#95A5A6")


def build_recipient_tooltip(name, region, platforms, year):
    platform_text = "<br>".join(sorted(platforms))

    return f"""
    <b>{name}</b><br><br>

    <b>Region:</b> {region}<br>

    <b>Platforms:</b><br>
    {platform_text}

    <br>

    <b>First Delivery:</b> {year}
    """


# ============================================================
# Main Renderer
# ============================================================

def render_network(df):

    st.subheader("🛰 Iranian Drone Proliferation Network")

    if df.empty:
        st.warning("Dataset is empty.")
        return

    # --------------------------------------------------------
    # Region Filter
    # --------------------------------------------------------

    if "Region " in df.columns:

        regions = sorted(df["Region "].dropna().unique())

        selected_regions = st.multiselect(
            "Filter by Region",
            regions,
            default=regions
        )

        df = df[df["Region "].isin(selected_regions)]

    if df.empty:
        st.warning("No records match the selected filters.")
        return

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    recipient_counts = (
        df.groupby("Seeker")
        .size()
        .to_dict()
    )

    recipient_platforms = (
        df.groupby("Seeker")["Paltform Model"]
        .apply(lambda x: sorted(set(x)))
        .to_dict()
    )

    # --------------------------------------------------------
    # Graph
    # --------------------------------------------------------

    G = nx.DiGraph()

    supplier = "Iran"

    G.add_node(
        supplier,
        label="Iran",
        shape="dot",
        color="#E74C3C",
        size=70,
        physics=False,
        x=0,
        y=0,
        fixed=True,
        title="""
        <b>Islamic Republic of Iran</b><br><br>

        Primary exporter of Iranian UAV systems.
        """
    )

    # --------------------------------------------------------
    # Platform Ring
    # --------------------------------------------------------

    platforms = sorted(df["Paltform Model"].dropna().unique())

    radius = 350

    platform_positions = {}

    for i, platform in enumerate(platforms):

        angle = (2 * math.pi * i) / len(platforms)

        x = radius * math.cos(angle)
        y = radius * math.sin(angle)

        platform_positions[platform] = (x, y)

        G.add_node(
            platform,
            shape="box",
            color="#F39C12",
            size=36,
            physics=False,
            x=x,
            y=y,
            fixed=True,
            title=f"""
            <b>{platform}</b><br>
            Iranian UAV Platform
            """
        )

        G.add_edge(
            supplier,
            platform,
            color="#BBBBBB",
            arrows="to"
        )

    # --------------------------------------------------------
    # Recipient Nodes
    # --------------------------------------------------------
    recipient_added = set()

    for _, row in df.iterrows():

        platform = str(row["Paltform Model"]).strip()
        recipient = str(row["Seeker"]).strip()
        region = str(row.get("Region ", "")).strip()

        year = row.get(
            "Year of First Delivery",
            "Unknown"
        )

        if recipient not in recipient_added:

            recipient_added.add(recipient)

            connected_platforms = recipient_platforms.get(
                recipient,
                []
            )

            # Average the coordinates of every platform the
            # recipient operates.

            xs = []
            ys = []

            for p in connected_platforms:

                if p in platform_positions:

                    px, py = platform_positions[p]

                    xs.append(px)
                    ys.append(py)

            if xs:

                cx = sum(xs) / len(xs)
                cy = sum(ys) / len(ys)

            else:

                cx = 0
                cy = 0

            # Push recipients outward from the platform ring

            angle = math.atan2(cy, cx)

            x = cx + 240 * math.cos(angle)
            y = cy + 240 * math.sin(angle)

            G.add_node(
                recipient,
                shape="dot",
                color=get_region_colour(region),
                size=18 + 4 * len(connected_platforms),
                physics=False,
                fixed=True,
                x=x,
                y=y,
                title=build_recipient_tooltip(
                    recipient,
                    region,
                    connected_platforms,
                    year
                )
            )

        G.add_edge(
            platform,
            recipient,
            arrows="to",
            color=get_region_colour(region),
            title=f"""
            <b>{platform}</b><br>
            Recipient: {recipient}<br>
            Region: {region}<br>
            First Delivery: {year}
            """
        )

# ============================================================
# Build PyVis Network
# ============================================================

    net = Network(
        height="900px",
        width="100%",
        bgcolor="#FFFFFF",
        font_color="black",
        directed=True,
    )

    net.from_nx(G)

    # Smooth curved edges

    for edge in net.edges:

        edge["smooth"] = {
            "enabled": True,
            "type": "dynamic"
        }

    # --------------------------------------------------------
    # Layout Options
    # --------------------------------------------------------

    net.set_options("""
    var options = {

      "layout": {
        "improvedLayout": true
      },

      "physics": {
        "enabled": false
      },

      "interaction": {

        "hover": true,
        "multiselect": true,
        "dragNodes": false,
        "dragView": true,
        "zoomView": true,
        "navigationButtons": true,
        "keyboard": true
      },

      "nodes": {

        "borderWidth": 1,
        "borderWidthSelected": 3,

        "font": {
          "size": 18
        }

      },

      "edges": {

        "smooth": {
          "enabled": true,
          "type": "dynamic"
        }

      }

    }
    """)

# ============================================================
# Render HTML
# ============================================================

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".html"
    ) as tmp:

        html_path = tmp.name

    net.save_graph(html_path)

    with open(
        html_path,
        "r",
        encoding="utf-8"
    ) as f:

        source = f.read()

    source = source.replace(
        "</body>",
        """
<script>

network.once("afterDrawing", function () {

    network.fit({

        animation: {

            duration: 700

        }

    });

});

</script>

</body>
"""
    )

    html(
        source,
        height=920,
        scrolling=True,
    )

    os.remove(html_path)
# ============================================================
# Dashboard Metrics
# ============================================================

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Platforms",
        df["Paltform Model"].nunique()
    )

    col2.metric(
        "Recipients",
        df["Seeker"].nunique()
    )

    col3.metric(
        "Transfers",
        len(df)
    )

    col4.metric(
        "Network Nodes",
        G.number_of_nodes()
    )

# ============================================================
# Network Summary
# ============================================================

    st.markdown("### 📊 Network Summary")

    summary1, summary2 = st.columns(2)

    summary1.markdown(
        f"""
**Supplier**

- 🇮🇷 Iran

**Platforms**

- {df["Paltform Model"].nunique()}

**Recipients**

- {df["Seeker"].nunique()}

**Transfers**

- {len(df)}
"""
    )

    top_recipients = (
        df.groupby("Seeker")
        .size()
        .sort_values(ascending=False)
        .head(10)
    )

    summary2.markdown("**Top Recipient States**")

    for recipient, count in top_recipients.items():

        st.write(f"• **{recipient}** — {count} transfer(s)")

# ============================================================
# Region Legend
# ============================================================

    st.divider()

    st.markdown("### 🌍 Region Legend")

    legend_cols = st.columns(len(REGION_COLORS))

    for (region, colour), col in zip(REGION_COLORS.items(), legend_cols):

        col.markdown(
            f"""
<div style="display:flex;align-items:center;gap:8px;">
<div style="
width:18px;
height:18px;
border-radius:50%;
background:{colour};
border:1px solid #444;">
</div>

<span>{region}</span>

</div>
""",
            unsafe_allow_html=True,
        )

# ============================================================
# Network Statistics
# ============================================================

    st.divider()

    degrees = dict(G.degree())

    busiest = sorted(
        degrees.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    st.markdown("### 🔗 Highest Connectivity")

    stats = []

    for node, degree in busiest:

        if node == supplier:
            continue

        stats.append(
            {
                "Node": node,
                "Connections": degree
            }
        )

    if stats:

        st.dataframe(
            stats,
            use_container_width=True,
            hide_index=True
        )

# ============================================================
# Download HTML
# ============================================================

    with open(
        html_path,
        "rb"
    ) as f:

        st.download_button(
            "⬇ Download Interactive Network",
            f,
            file_name="Iranian_Drone_Network.html",
            mime="text/html",
            use_container_width=True
        )
