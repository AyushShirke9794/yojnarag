import streamlit as st
from src.rag_engine import YojanaRAG
from src.scheme_database import load_schemes
from src.eligibility_engine import EligibilityEngine

st.set_page_config(
    page_title="YojanaRAG",
    page_icon="🇮🇳",
    layout="wide"
)

@st.cache_resource(show_spinner="Loading AI retrieval models...")
def load_rag():
    return YojanaRAG()

st.title("🇮🇳 YojanaRAG")
st.subheader("Multilingual Government Scheme Assistant")

st.info(
    "Explore five government schemes across agriculture, education, "
    "housing, employment, and women & children. "
    "Ask questions in English, Hindi, or Marathi. "
    "Answers use retrieved government documents."
)

language = st.selectbox(
    "Choose your preferred language",
    ["English", "Hindi", "Marathi"]
)

question = st.text_area(
    "Enter your question",
    placeholder="What financial benefits are provided under PM-KISAN?",
    height=120
)

if st.button("Get Answer", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            rag = load_rag()

            with st.spinner("Searching documents and generating answer..."):
                response = rag.answer(
                    question.strip(),
                    language=language
                )

            if response.startswith("OFFLINE EVIDENCE MODE"):
                st.warning(
                    "AI answer generation is currently unavailable. "
                    "Showing retrieved source excerpts instead."
                )

                with st.expander(
                    "View retrieved document evidence",
                    expanded=True
                ):
                    st.text(response)

            else:
                st.success("Answer generated successfully")

                st.markdown("### Answer")
                st.markdown(response)

        except Exception as error:
            st.error(
                "Unable to complete your request. "
                "Please try again."
            )
            st.caption(f"Technical details: {error}")

st.divider()
st.header("Government Scheme Eligibility Assistance")

schemes = load_schemes()

if schemes:
    scheme_names = {
        scheme.scheme_name: scheme for scheme in schemes
    }

    selected_name = st.selectbox(
        "Select a government scheme",
        list(scheme_names.keys())
    )

    selected_scheme = scheme_names[selected_name]

    st.write("**Category:**", selected_scheme.category)
    st.write("**Description:**", selected_scheme.description)
    st.write("**Benefits:**", selected_scheme.benefits)
    st.write("**Eligibility information:**", selected_scheme.eligibility_text)

    st.write(
        "**Verification status:**",
        selected_scheme.verification_status
    )

    if selected_scheme.required_documents:
        st.write(
            "**Required documents:**",
            ", ".join(selected_scheme.required_documents)
        )
    else:
        st.info("Required documents have not yet been verified.")

    st.markdown(
        f"**Official website:** {selected_scheme.official_source_url}"
    )

    if st.button("Check Eligibility Information"):
        engine = EligibilityEngine()
        result = engine.check(
            selected_scheme,
            applicant={}
        )

        if result.status == "rules_unverified":
            st.warning(result.explanation)
        elif result.status == "insufficient_information":
            st.info(result.explanation)
        else:
            st.write(result.explanation)

else:
    st.warning("No scheme records are available.")

st.divider()
st.caption(
    "YojanaRAG educational prototype | 5 government schemes | "
    "606 indexed document chunks. "
    "Source documents may be historical or superseded. "
    "Current eligibility and benefits have not been verified. "
    "Always confirm information on official government portals."
)
