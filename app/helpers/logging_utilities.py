import logging
import streamlit as st


def setup_logging(debug: bool = False) -> None:
    # Ensure rich error details are logged (UI may still redact for external users)
    st.set_option("client.showErrorDetails", True)

    # Basic logging configuration so messages go to Streamlit Cloud logs
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
