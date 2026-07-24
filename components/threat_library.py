from pathlib import Path
import base64

import streamlit as st

ASSETS_DIR = Path("Assets")


def show_pdf(pdf_path: Path, height=1000):
    """Render PDF using an embedded iframe."""
    with open(pdf_path, "rb") as f:
        pdf_data = base64.b64encode(f.read()).decode("utf-8")

    pdf_display = f"""
    <iframe
        src="data:application/pdf;base64,{pdf_data}"
        width="100%"
        height="{height}"
        type="application/pdf"
        style="border:none;">
    </iframe>
    """

    st.markdown(pdf_display, unsafe_allow_html=True)


def render_threat_library():

    st.title("📚 Threat Library")
    st.caption("Technical reference library for Iranian UAV platforms.")

    if not ASSETS_DIR.exists():
        st.error("Assets folder not found.")
        return

    pdf_files = sorted(
        ASSETS_DIR.glob("*.pdf"),
        key=lambda p: p.stem.lower()
    )

    if not pdf_files:
        st.warning("No PDF handbooks found.")
        return

    col_search, col_mode, col_count = st.columns([5, 3, 2])

    with col_search:
        search = st.text_input(
            "Search",
            placeholder="Search handbooks..."
        )

    if search:
        pdf_files = [
            pdf
            for pdf in pdf_files
            if search.lower() in pdf.stem.lower()
        ]

    if not pdf_files:
        st.info("No matching handbooks found.")
        return

    with col_mode:
        mode = st.radio(
            "View",
            ["Single", "Compare"],
            horizontal=True
        )

    with col_count:
        st.metric("Platforms", len(pdf_files))

    st.divider()

    # ==================================================
    # SINGLE VIEW
    # ==================================================

    if mode == "Single":

        selected = st.selectbox(
            "Select Platform",
            pdf_files,
            format_func=lambda x: x.stem
        )

        c1, c2 = st.columns([6, 1])

        with c1:
            st.subheader(selected.stem)

        with c2:
            st.download_button(
                "⬇",
                data=selected.read_bytes(),
                file_name=selected.name,
                mime="application/pdf",
                use_container_width=True,
            )

        st.divider()

        show_pdf(selected, height=1100)

    # ==================================================
    # COMPARE VIEW
    # ==================================================

    else:

        left_col, right_col = st.columns(2)

        with left_col:

            left_pdf = st.selectbox(
                "Platform A",
                pdf_files,
                format_func=lambda x: x.stem,
                key="left_pdf"
            )

            st.download_button(
                "⬇ Download",
                data=left_pdf.read_bytes(),
                file_name=left_pdf.name,
                mime="application/pdf",
                key="download_left",
                use_container_width=True,
            )

            show_pdf(left_pdf, height=900)

        with right_col:

            available_right = [
                pdf for pdf in pdf_files
                if pdf != left_pdf
            ]

            if not available_right:
                st.warning("Only one handbook available.")
                return

            right_pdf = st.selectbox(
                "Platform B",
                available_right,
                format_func=lambda x: x.stem,
                key="right_pdf"
            )

            st.download_button(
                "⬇ Download",
                data=right_pdf.read_bytes(),
                file_name=right_pdf.name,
                mime="application/pdf",
                key="download_right",
                use_container_width=True,
            )

            show_pdf(right_pdf, height=900)
