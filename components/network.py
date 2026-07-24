import os
import tempfile

import networkx as nx
from pyvis.network import Network

import streamlit as st
from streamlit.components.v1 import html


REGION_COLORS = {
    "Africa": "#2ECC71",
    "Europe": "#3498DB",
    "Middle East": "#9B59B6",
    "Asia": "#F39C12",
    "Americas": "#1ABC9C",
}


def render_network(df):
    """
    Iranian Drone Proliferation Network

    Iran
        ↓
    Platform
        ↓
    Recipient
    """

    st.subheader(" Proliferation Network")

    if df.empty:
        st.warning("No records found.")
        return

    # ------------------------------------------------
    # Region Filter
    # ------------------------------------------------

    if "Region " in df.columns:

        regions = sorted(df["Region "].dropna().unique())

        selected_regions = st.multiselect(
            "Filter by Region",
            regions,
            default=regions,
        )

        df = df[df["Region "].isin(selected_regions)]

    if df.empty:
        st.warning("No records match the selected filters.")
        return

    # ------------------------------------------------
    # Count recipient platforms
    # ------------------------------------------------

    recipient_counts = (
        df.groupby("Seeker")
        .size()
        .to_dict()
    )

    # ------------------------------------------------
    # Build Graph
    # ------------------------------------------------

    G = nx.DiGraph()

    supplier = "Iran"

    G.add_node(
        supplier,
        color="#E74C3C",
        size=65,
        shape="dot",
        title="<b>Iran</b><br>Supplier",
    )

    # ------------------------------------------------
    # Build Network
    # ------------------------------------------------

    for _, row in df.iterrows():

        platform = str(row["Paltform Model"]).strip()

        recipient = str(row["Seeker"]).strip()

        region = str(
            row.get("Region ", "")
        ).strip()

        year = row.get(
            "Year of First Delivery",
            "Unknown"
        )

        node_color = REGION_COLORS.get(
            region,
            "#95A5A6"
        )

        # Platform

        if platform not in G:

            G.add_node(
                platform,
                color="#F39C12",
                shape="box",
                title=f"""
                <b>{platform}</b><br>
                Iranian UAV Platform
                """
            )

        # Recipient

        if recipient not in G:

            G.add_node(
                recipient,
                color=node_color,
                shape="dot",
                title=f"""
                <b>{recipient}</b><br>
                Region: {region}<br>
                Platforms Received:
                {recipient_counts.get(recipient,1)}
                """
            )

        # Supplier → Platform

        if not G.has_edge(supplier, platform):

            G.add_edge(
                supplier,
                platform,
                color="#AAAAAA",
                arrows="to"
            )

        # Platform → Recipient

        if not G.has_edge(platform, recipient):

            G.add_edge(
                platform,
                recipient,
                arrows="to",
                color=node_color,
                title=f"""
                <b>{platform}</b><br>
                Recipient: {recipient}<br>
                Region: {region}<br>
                First Delivery: {year}
                """
            )

    # ------------------------------------------------
    # Node Sizes
    # ------------------------------------------------
# ------------------------------------------------
# Node Sizes
# ------------------------------------------------
    # ------------------------------------------------
    # Node Sizes
    # ------------------------------------------------

    for node in G.nodes():

        if node == supplier:

            G.nodes[node]["size"] = 65

        elif G.nodes[node]["shape"] == "box":

            G.nodes[node]["size"] = 35

        else:

            count = recipient_counts.get(node, 1)
            G.nodes[node]["size"] = 18 + count * 4    # ------------------------------------------------
    # Build PyVis Network
    # ------------------------------------------------

    net = Network(
        height="900px",
        width="100%",
        bgcolor="#FFFFFF",
        font_color="black",
        directed=True,
    )

    net.from_nx(G)

    for edge in net.edges:

        edge["smooth"] = {
            "enabled": True,
            "type": "dynamic"
        }
 
net.repulsion(
    node_distance=260,
    spring_length=220,
    spring_strength=0.03,
    central_gravity=0.35,
    damping=0.18,
)

net.set_options("""
var options = {
  "physics": {
    "enabled": true,
    "solver": "forceAtlas2Based",
    "forceAtlas2Based": {
      "gravitationalConstant": -80,
      "centralGravity": 0.08,
      "springLength": 220,
      "springConstant": 0.05,
      "damping": 0.4,
      "avoidOverlap": 0.8
    },
    "stabilization": {
      "enabled": true,
      "iterations": 1200,
      "fit": true
    }
  },

  "layout": {
    "improvedLayout": true
  },

  "interaction": {
    "hover": true,
    "navigationButtons": true,
    "keyboard": true,
    "zoomView": true,
    "dragView": true
  }
}
""")
    net.toggle_physics(False)

   # ------------------------------------------------
    # Render
    # ------------------------------------------------

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
<script type="text/javascript">

network.once("stabilizationIterationsDone", function () {

    network.fit({
        animation: {
            duration: 800,
            easingFunction: "easeInOutQuad"
        }
    });

    network.setOptions({
        physics: false
    });

});

</script>
</body>
"""
)


    # ------------------------------------------------
    # Dashboard Metrics
    # ------------------------------------------------

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

