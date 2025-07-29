import streamlit as st
from pages.planning_tab import render_planning_tab
from pages.providers_tab import render_providers_tab

# Page config
st.set_page_config(
    page_title="Travel Cost Calculator",
    page_icon="🚗",
    layout="wide"
)

# Title
st.title("🚗 Travel Cost Calculator")
st.caption("Calculate travel costs and optimize routes")

# Create tabs
tab1, tab2 = st.tabs(["📋 Planning Travel & Cost", "🚛 Provider Journey"])

with tab1:
    render_planning_tab()

with tab2:
    render_providers_tab()

# Footer
st.divider()
st.caption("Travel Cost Calculator v1.0")