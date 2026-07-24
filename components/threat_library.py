from pathlib import Path

import fitz  # PyMuPDF
import streamlit as st

ASSETS_DIR = Path("Assets")


# ==========================================================
# PDF RENDERING
# ==========================================================

@st.cache_data(show_spinner=False)
def render_pdf_pages(pdf_path: str):
    """
    Convert every page of a PDF into PNG images.
    Cached so PDFs are only rendered once.
    """
    doc = fitz.open(pdf_path)
    pages = []

    zoom = 2.0  # Higher = sharper pages

    for page in doc:
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        pages.append(pix.tobytes("png"))

    doc.close()
    return pages


def show_pdf(pdf_path: Path):
    pages = render_pdf_pages(str(pdf_path))

    for page in pages:
        st.image(page, use_container_width=True)


# ==========================================================
# MAIN COMPONENT
# ==========================================================

def render_threat_library():

    st.title(" Threat Library")
    st.caption("Technical reference library for Iranian UAV platforms.")

    # ------------------------------------------------------
    # Verify Assets folder
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # Toolbar
    # ------------------------------------------------------

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

    # ======================================================
    # SINGLE VIEW
    # ======================================================

    if mode == "Single":

        selected = st.selectbox(
            "Select Platform",
            pdf_files,
            format_func=lambda x: x.stem
        )

        title_col, button_col = st.columns([6, 1])

        with title_col:
            st.subheader(selected.stem)

        with button_col:
            st.download_button(
                "⬇",
                data=selected.read_bytes(),
                file_name=selected.name,
                mime="application/pdf",
                use_container_width=True
            )

        st.divider()

        show_pdf(selected)

    # ======================================================
    # COMPARE VIEW
    # ======================================================

    else:

        left_col, right_col = st.columns(2)

        # ---------------- LEFT ----------------

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
                use_container_width=True
            )

            st.divider()

            show_pdf(left_pdf)

        # ---------------- RIGHT ----------------

        with right_col:

            available_right = [
                pdf
                for pdf in pdf_files
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
                use_container_width=True
            )

            st.divider()

            show_pdf(right_pdf)
