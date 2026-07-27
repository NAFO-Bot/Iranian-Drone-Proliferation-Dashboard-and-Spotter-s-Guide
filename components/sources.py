import streamlit as st


def render_sources():

    st.title(" Sources & Methodology")

    st.markdown("""
This dashboard visualizes historical transfers of Iranian unmanned aerial systems. Furthermore, this platform attempts to map Iran's UAS fleet using publicly available information.No Classified material was used to create this dashboard. Likewise, Radar Reflection and Detection in the IR and Visual Spectrum  ranges collected from CMANO-DB are placeholders and should be treated as such. My own models of radar reflection will clearly be labelled as such.

The objective of this application is to support exploratory analysis of historical proliferation patterns. It is intended for research, education, and open-source intelligence (OSINT) visualization.

---

## Secondary Data Sources

- United Nations Blast Damage Estimator
- SIPRI Arms Transfers Database
- Military Balance (IISS)
- Open-source reporting
- Government publications
- Defence journalism and investigative reporting
- CNAS 
- CSIS
- AEI
- OSMP
- CMANO-DB as Placeholders where found till the models are made. 
- Spas Consulting
- Janes

---

## Dataset

The dataset records historical export events and includes attributes such as:

- Supplier
- Recipient
- Platform Model
- Year of First Delivery
- Region
- Platform

The proliferation data in this dashboard is based on a dataset published by CNAS. Inspiration for this dashboard came from recent work by CSIS and Janes 

---

## Visualizations

-  Interactive Globe
-  Network Graph
-  Statistical Analysis
-  Dataset Explorer
-  Threat Library

---

## Methodology

1. Collect open-source records.
2. Validate recipient and platform information.
3. Standardize country names.
4. Assign geographic coordinates.
5. Build an interactive analytical dashboard using Streamlit and Plotly.
6. Collate data from many sources, including military equipment databases and open-source material

---

## Limitations

This dashboard reflects publicly reported historical transfer events.

Open-source reporting may be incomplete, delayed, or revised over time. The absence of a transfer record should not be interpreted as evidence that no transfer occurred.

This application does not model operational capability, battlefield effectiveness, inventory levels, or current force posture.

---

## Author's Note

Hello and welcome to my Iranian Drone Proliferation Dataset and Handbook. I hope you liked it. Firstly, I would like to thank my teachers at the Institute of Management Study for their invaluable guidance and support. Teaching me how to do research must not have been very easy, and I am extremely thankful that they did. Secondly, there is my family whose love and support have powered every keystroke behind this project. Didi, if you are reading this, I want to thank you for all you do. Lastly, there was the effort behind it all: sleepless nights and coffee-fueled sprints that all led up to this forever semi-finished library of Iranian Drones.

On a serious note, CMANO-DB simulations are just that, simulations. Not that it should matter, but real values might differ significantly. My own radar models will clearly be labelled as such.

Learn from it, play with it, don't harm with it. 

Should you wish to cite my work, please do so as such: Nath.S(2026)-Independent Researcher 
""")
