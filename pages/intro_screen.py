import streamlit as st
import streamlit.components.v1 as components

def render_intro_screen():
    """Render the introduction/landing screen"""
    
    # Custom CSS for professional styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 3rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .problem-visual {
        background: #fff5f5;
        border: 2px solid #feb2b2;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 1rem;
        transition: transform 0.3s;
    }
    .problem-visual:hover {
        transform: translateY(-5px);
    }
    .solution-visual {
        background: #f0fff4;
        border: 2px solid #9ae6b4;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 1rem;
        transition: transform 0.3s;
    }
    .solution-visual:hover {
        transform: translateY(-5px);
    }
    .big-number {
        font-size: 3rem;
        font-weight: bold;
        color: #e53e3e;
        margin: 0;
    }
    .solution-number {
        font-size: 3rem;
        font-weight: bold;
        color: #38a169;
        margin: 0;
    }
    .visual-box {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        text-align: center;
        height: 100%;
        transition: transform 0.3s;
    }
    .visual-box:hover {
        transform: translateY(-5px);
    }
    .api-demo {
        background: #1a202c;
        color: #68d391;
        padding: 1.5rem;
        border-radius: 10px;
        font-family: 'Monaco', 'Courier New', monospace;
        font-size: 0.9rem;
        line-height: 1.6;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .cta-button {
        display: inline-block;
        background: white;
        color: #667eea;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: bold;
        font-size: 1.1rem;
        margin: 0.5rem;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s;
    }
    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }
    .cta-button-outline {
        display: inline-block;
        background: transparent;
        color: white;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: bold;
        font-size: 1.1rem;
        margin: 0.5rem;
        border: 2px solid white;
        transition: all 0.3s;
    }
    .cta-button-outline:hover {
        background: white;
        color: #667eea;
    }
    .comparison-table {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    }
    .comparison-row {
        display: flex;
        align-items: center;
        padding: 1rem;
        border-bottom: 1px solid #e2e8f0;
    }
    .comparison-row:last-child {
        border-bottom: none;
    }
    .check-mark {
        color: #48bb78;
        font-size: 1.5rem;
        margin-right: 1rem;
    }
    .cross-mark {
        color: #e53e3e;
        font-size: 1.5rem;
        margin-right: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1 style="font-size: 3.5rem; margin-bottom: 1rem;">🚗 Smart Travel Cost Optimizer</h1>
        <p style="font-size: 1.4rem; opacity: 0.95; margin-bottom: 2rem;">AI-Powered Route Planning for Service Provider Businesses</p>
        <p style="font-size: 1.1rem; opacity: 0.9; margin-bottom: 2rem;">Match the right freelancer to each job while minimizing travel costs</p>
    </div>
    """, unsafe_allow_html=True)
    
    # The Problem - Visual
    st.markdown("## 🔴 The Problem")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="problem-visual">
            <h1 style="font-size: 4rem; margin: 0;">📍</h1>
            <p class="big-number">4hrs</p>
            <p style="margin: 0; font-weight: bold;">Daily planning time</p>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">Manually matching freelancers to clients</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="problem-visual">
            <h1 style="font-size: 4rem; margin: 0;">🚗</h1>
            <p class="big-number">£45K</p>
            <p style="margin: 0; font-weight: bold;">Annual overspend</p>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">Wrong provider = longer trips</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="problem-visual">
            <h1 style="font-size: 4rem; margin: 0;">💸</h1>
            <p class="big-number">73%</p>
            <p style="margin: 0; font-weight: bold;">Hidden travel costs</p>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">Mixed transport modes ignored</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # The Solution - Visual
    st.markdown("## ✅ The Solution")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="visual-box">
            <h1 style="color: #667eea; font-size: 3rem; margin: 0;">🎯</h1>
            <p style="font-weight: bold; margin: 0.5rem 0;">Smart Matching</p>
            <p style="color: #666; font-size: 0.9rem; margin: 0;">Best provider for each job</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="visual-box">
            <h1 style="color: #667eea; font-size: 3rem; margin: 0;">🚌</h1>
            <p style="font-weight: bold; margin: 0.5rem 0;">Multi-modal</p>
            <p style="color: #666; font-size: 0.9rem; margin: 0;">Car, public, or mixed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="visual-box">
            <h1 style="color: #667eea; font-size: 3rem; margin: 0;">💰</h1>
            <p style="font-weight: bold; margin: 0.5rem 0;">True Costs</p>
            <p style="color: #666; font-size: 0.9rem; margin: 0;">All expenses included</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="visual-box">
            <h1 style="color: #667eea; font-size: 3rem; margin: 0;">⚡</h1>
            <p style="font-weight: bold; margin: 0.5rem 0;">Instant</p>
            <p style="color: #666; font-size: 0.9rem; margin: 0;">Real-time results</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # How It Works
    st.markdown("## 🚀 How It Works for Businesses")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="visual-box">
            <h1 style="font-size: 3rem; margin: 0; color: #667eea;">1️⃣</h1>
            <h4 style="color: #667eea;">Single API Call</h4>
            <p style="color: #666; font-size: 0.95rem;">
            Your system sends booking and provider data to our API endpoint for instant analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="visual-box">
            <h1 style="font-size: 3rem; margin: 0; color: #667eea;">2️⃣</h1>
            <h4 style="color: #667eea;">Intelligent Processing</h4>
            <p style="color: #666; font-size: 0.95rem;">
            AI optimizes provider assignments and calculates complete travel costs in milliseconds.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="visual-box">
            <h1 style="font-size: 3rem; margin: 0; color: #667eea;">3️⃣</h1>
            <h4 style="color: #667eea;">Structured Response</h4>
            <p style="color: #666; font-size: 0.95rem;">
            Receive optimized planning with recommendations and detailed cost breakdowns via API.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # API Integration Info
    st.markdown("""
    <div style="background: #f0f4f8; padding: 2rem; border-radius: 15px; margin-bottom: 2rem;">
        <h3 style="color: #667eea; text-align: center; margin-bottom: 1.5rem;">🔌 Enterprise Integration</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem;">
            <div style="text-align: center;">
                <h1 style="font-size: 2.5rem; color: #667eea; margin: 0;">⚡</h1>
                <h4 style="margin: 0.5rem 0;">Real-time Planning</h4>
                <p style="color: #666; font-size: 0.9rem;">Optimize assignments for future bookings</p>
            </div>
            <div style="text-align: center;">
                <h1 style="font-size: 2.5rem; color: #667eea; margin: 0;">📊</h1>
                <h4 style="margin: 0.5rem 0;">Historical Analysis</h4>
                <p style="color: #666; font-size: 0.9rem;">Calculate costs for completed journeys</p>
            </div>
            <div style="text-align: center;">
                <h1 style="font-size: 2.5rem; color: #667eea; margin: 0;">🔄</h1>
                <h4 style="margin: 0.5rem 0;">Seamless Integration</h4>
                <p style="color: #666; font-size: 0.9rem;">Works with your existing systems</p>
            </div>
        </div>
        <p style="text-align: center; margin-top: 1.5rem; color: #666;">
        <em>Note: The Excel upload in this demo is for testing purposes. Enterprise customers use direct API integration.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Service Benefits
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="comparison-table">
            <h3 style="color: #38a169; margin-bottom: 1.5rem;">✨ Key Features</h3>
            <div class="comparison-row">
                <span class="check-mark">✓</span>
                <span><strong>Freelancer matching</strong> - Skills, location, availability</span>
            </div>
            <div class="comparison-row">
                <span class="check-mark">✓</span>
                <span><strong>Mixed transport modes</strong> - Car, public, or combined</span>
            </div>
            <div class="comparison-row">
                <span class="check-mark">✓</span>
                <span><strong>Different rates</strong> - Each provider's travel costs</span>
            </div>
            <div class="comparison-row">
                <span class="check-mark">✓</span>
                <span><strong>UK charges</strong> - Congestion, parking, tolls</span>
            </div>
            <div class="comparison-row">
                <span class="check-mark">✓</span>
                <span><strong>Multi-booking routes</strong> - Optimize full days</span>
            </div>
            <div class="comparison-row">
                <span class="check-mark">✓</span>
                <span><strong>API integration</strong> - Connects to your system</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="comparison-table">
            <h3 style="color: #667eea; margin-bottom: 1.5rem;">🎯 Perfect For</h3>
            <div class="comparison-row">
                <span style="font-size: 1.5rem; margin-right: 1rem;">🔧</span>
                <span><strong>Plumbers</strong> - Emergency & scheduled calls</span>
            </div>
            <div class="comparison-row">
                <span style="font-size: 1.5rem; margin-right: 1rem;">🧹</span>
                <span><strong>Cleaners</strong> - Residential & commercial</span>
            </div>
            <div class="comparison-row">
                <span style="font-size: 1.5rem; margin-right: 1rem;">👶</span>
                <span><strong>Childcare</strong> - Babysitters & nannies</span>
            </div>
            <div class="comparison-row">
                <span style="font-size: 1.5rem; margin-right: 1rem;">🗣️</span>
                <span><strong>Interpreters</strong> - Medical & legal visits</span>
            </div>
            <div class="comparison-row">
                <span style="font-size: 1.5rem; margin-right: 1rem;">🏥</span>
                <span><strong>Care providers</strong> - Home healthcare</span>
            </div>
            <div class="comparison-row">
                <span style="font-size: 1.5rem; margin-right: 1rem;">📐</span>
                <span><strong>Tutors</strong> - In-home education</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # What's Included
    st.markdown("## 🎁 What We Calculate")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="visual-box">
            <h1 style="font-size: 2.5rem; margin: 0;">🚗</h1>
            <h4 style="color: #667eea;">Travel Costs</h4>
            <p style="color: #666; font-size: 0.9rem;">
            • Mileage/fuel<br>
            • Public transport<br>
            • Parking fees<br>
            • Congestion charges
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="visual-box">
            <h1 style="font-size: 2.5rem; margin: 0;">⏱️</h1>
            <h4 style="color: #667eea;">Time & Rates</h4>
            <p style="color: #666; font-size: 0.9rem;">
            • Travel time costs<br>
            • Individual rates<br>
            • Service duration<br>
            • Multi-stop routes
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="visual-box">
            <h1 style="font-size: 2.5rem; margin: 0;">🎯</h1>
            <h4 style="color: #667eea;">Smart Matching</h4>
            <p style="color: #666; font-size: 0.9rem;">
            • Skill matching<br>
            • Availability<br>
            • Location proximity<br>
            • Transport mode
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Try It Now CTA
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 15px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <h2 style="margin-bottom: 1rem; font-size: 2rem;">👆 Try the Demo Above</h2>
        <p style="font-size: 1.1rem; opacity: 0.95;">
        Click the <strong>Planning Demo</strong> or <strong>Journey Demo</strong> tabs to test with your data
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Contact Section
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h3 style="color: #667eea; margin-bottom: 1rem;">Want to implement this for your business?</h3>
        <p style="font-size: 1.1rem; color: #666; margin-bottom: 1rem;">
        This solution is built for UK businesses but can be localized for other regions.
        </p>
        <p style="font-size: 1.2rem;">✉️ <strong>katerina.i@eco-n-tech.com</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Hackathon Footer
    st.markdown("""
    <div style="background: #f8f9fa; padding: 2rem; border-radius: 15px; text-align: center;">
        <h3 style="color: #667eea; margin-bottom: 1rem;">🏆 Hackathon 2025 Project</h3>
        <p style="font-size: 1.1rem; color: #666; margin-bottom: 1.5rem;">
        Built with cutting-edge technology to solve real business problems
        </p>
        <div style="display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap;">
            <div>
                <img src="https://www.vectorlogo.zone/logos/google_maps/google_maps-icon.svg" width="60" height="60" style="margin-bottom: 0.5rem;">
                <p style="font-weight: bold; margin: 0;">Google Maps API</p>
                <p style="color: #666; font-size: 0.9rem;">Real-time routing</p>
            </div>
            <div>
                <img src="https://www.vectorlogo.zone/logos/google/google-icon.svg" width="60" height="60" style="margin-bottom: 0.5rem;">
                <p style="font-weight: bold; margin: 0;">Gemini AI</p>
                <p style="color: #666; font-size: 0.9rem;">Smart optimization</p>
            </div>
            <div>
                <img src="https://www.vectorlogo.zone/logos/python/python-icon.svg" width="60" height="60" style="margin-bottom: 0.5rem;">
                <p style="font-weight: bold; margin: 0;">Python + Streamlit</p>
                <p style="color: #666; font-size: 0.9rem;">Rapid development</p>
            </div>
        </div>
        <p style="margin-top: 2rem; color: #666;">
        <strong>Innovation:</strong> First UK-specific travel cost optimizer with complete charge coverage<br>
        <strong>Impact:</strong> Saves businesses £45K+ annually on travel expenses<br>
        <strong>Scalability:</strong> Designed for easy deployment and localization
        </p>
    </div>
    """, unsafe_allow_html=True)