import streamlit as st
from pages.intro_screen import render_intro_screen
from pages.planning_tab import render_planning_tab
from pages.providers_tab import render_providers_tab

# Page config
st.set_page_config(
    page_title="Smart Travel Cost Optimizer - B2B API Platform",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        background-color: #f0f2f6;
        border-radius: 5px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(["🏠 Home", "📋 Planning Demo", "🚛 Provider Journey Demo"])

with tab1:
    render_intro_screen()

with tab2:
    st.markdown("### 📋 Planning & Cost Calculation Demo")
    st.info("Try our planning module - upload Excel files with bookings and providers to see optimal assignments and cost calculations")
    render_planning_tab()

with tab3:
    st.markdown("### 🚛 Provider Journey Calculation Demo")
    st.info("Calculate costs for multi-stop provider journeys with detailed travel breakdowns")
    render_providers_tab()

# Sidebar with API info
with st.sidebar:
    st.markdown("## 🔌 Smart Travel Cost Optimizer")
    st.markdown("""
    ### Features
    - ⚡ Real-time calculation
    - 🚗 Multi-modal transport
    - 📊 Batch processing
    - 💰 Complete cost breakdown
    - 🗺️ Route optimization
    
    ### Use Cases
    - Healthcare providers
    - Field service teams
    - Delivery services
    - Emergency responders
    - Mobile consultants
    
    ### Contact
    📧 katerina.i@eco-n-tech.com
    """)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🏆 Hackathon Project 2025")
with col2:
    st.caption("💼 Built for UK B2B Services")
with col3:
    st.caption("🚀 API-First Platform")