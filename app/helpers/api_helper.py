import logging

# I had an issue once while running in Streamlit Cloud, and I wanted more info, so adding this
# defensive logging
try:
    from nhlpy import NHLClient
except Exception as e:
    # Log enough context to debug missing/incorrect dependency on Streamlit Cloud
    logging.exception(
        "Failed to import NHLClient from 'nhlpy'. "
        "This typically means the required pip package isn't installed or the version is incompatible."
    )
    # Re-raise so the app still fails visibly (details will be in logs)
    raise

# Define the NHL client once and reuse it throughout the application
client = NHLClient()
