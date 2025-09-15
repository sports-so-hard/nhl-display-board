"""
Represents a CSS file utility for including CSS resources within a Streamlit app.

This module provides functionality to resolve the path of a CSS resource file
and include it seamlessly into a Streamlit application using Streamlit's HTML
rendering capabilities. It simplifies the process of styling a Streamlit app
through custom CSS.
"""
import streamlit as st

from app.helpers.file_utilities import resolve_resource_path


class CSS:
    """
    Represents a CSS file that can be included in a Streamlit app.
    """
    def __init__(self, resource_path_str: str):
        self.resource_path = resolve_resource_path(resource_path_str)

    def include(self):
        """Include the CSS file in the Streamlit app."""
        st.html(self.resource_path)  # leverages the fact that Streamlit will wrap CSS in <style> tags
