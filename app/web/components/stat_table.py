"""
A component for displaying statistics in a table format.
"""
from typing import Any

import streamlit as st


class StatTable:
    """A component for displaying statistics in a table format."""
    def __init__(self,
                 table_class: str = "stat-table",
                 label_class: str = "stat-label",
                 value_class: str = "stat-value"):
        """Initialize a StatTable component."""
        self.table_class = table_class
        self.label_class = label_class
        self.value_class = value_class
        self.stats: dict[str, str] = {}

    def add_stat(self, label: str, value: Any) -> "StatTable":
        """Add a stat to the table."""
        value_str = repr(value)
        self.stats[label] = value_str
        return self

    def add_stats(self, stats: dict[str, Any]) -> "StatTable":
        """Add stats to the table."""
        for label, value in stats.items():
            self.add_stat(label, value)
        return self

    def render(self) -> None:
        """Render the table."""
        table_html = f'<table class="{self.table_class}">'
        for label, value in self.stats.items():
            table_html += (f'<tr><td class="{self.label_class}">{label}</td>' +
                           f'<td class="{self.value_class}">{value}</td></tr>')
        table_html += "</table>"
        st.markdown(table_html, unsafe_allow_html=True)
