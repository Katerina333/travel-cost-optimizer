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
        <p style="font-size: 1.4rem; opacity: 0.95; margin-bottom: 2rem;">AI-Powered Route Planning for Service Businesses</p>
        <p style="font-size: 1.1rem; opacity: 0.9; margin-bottom: 2rem;">Automatically assign the right provider to each job while minimizing travel costs</p>
    </div>
    """, unsafe_allow_html=True)
    
    # The Problem - Visual
    st.markdown("## 🔴 The Problem: Service Businesses Waste Money on Travel")
    st.markdown("""
    <p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">
    When you have 50 service providers and 100 jobs across the city, who goes where? 
    Current planning methods are broken.
    </p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="problem-visual">
            <h1 style="font-size: 4rem; margin: 0;">📍</h1>
            <p class="big-number">4hrs</p>
            <p style="margin: 0; font-weight: bold;">Daily planning time</p>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">Manually matching providers to jobs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="problem-visual">
            <h1 style="font-size: 4rem; margin: 0;">🚗</h1>
            <p class="big-number">£45K</p>
            <p style="margin: 0; font-weight: bold;">Annual overspend</p>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">Sending wrong provider = longer trips</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="problem-visual">
            <h1 style="font-size: 4rem; margin: 0;">💸</h1>
            <p class="big-number">73%</p>
            <p style="margin: 0; font-weight: bold;">Hidden travel costs</p>
            <p style="margin: 0; color: #666; font-size: 0.9rem;">Parking, congestion, tolls forgotten</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # The Solution - Visual
    st.markdown("## ✅ The Solution")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="visual-box">
            <h2 style="color: #667eea; margin-bottom: 1.5rem;">One API Call = Complete Solution</h2>
            <div class="api-demo">
            POST /api/v1/optimize<br>
            {<br>
            &nbsp;&nbsp;"booking_id": "B2025-001",<br>
            &nbsp;&nbsp;"customer": "10 Downing St, London",<br>
            &nbsp;&nbsp;"service": "emergency_repair"<br>
            }<br><br>
            // Returns in 200ms ⚡<br>
            {<br>
            &nbsp;&nbsp;"provider": "John Smith",<br>
            &nbsp;&nbsp;"total_cost": 73.45,<br>
            &nbsp;&nbsp;"eta": "14:45",<br>
            &nbsp;&nbsp;"route": "optimized_path"<br>
            }
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="solution-visual" style="height: 100%;">
            <h1 style="font-size: 4rem; margin: 0;">🎯</h1>
            <p class="solution-number">200ms</p>
            <p style="margin: 0; font-weight: bold;">Response time</p>
            <p style="margin-top: 1rem; color: #666;">✓ Best provider<br>✓ All costs included<br>✓ Optimized route</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Visual Benefits
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="visual-box">
            <h1 style="color: #667eea; font-size: 3rem; margin: 0;">30%</h1>
            <p style="font-weight: bold; margin: 0.5rem 0;">Cost Reduction</p>
            <p style="color: #666; font-size: 0.9rem; margin: 0;">Guaranteed savings</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="visual-box">
            <h1 style="color: #667eea; font-size: 3rem; margin: 0;">5min</h1>
            <p style="font-weight: bold; margin: 0.5rem 0;">Integration</p>
            <p style="color: #666; font-size: 0.9rem; margin: 0;">Quick setup</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="visual-box">
            <h1 style="color: #667eea; font-size: 3rem; margin: 0;">100%</h1>
            <p style="font-weight: bold; margin: 0.5rem 0;">UK Coverage</p>
            <p style="color: #666; font-size: 0.9rem; margin: 0;">All zones & charges</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="visual-box">
            <h1 style="color: #667eea; font-size: 3rem; margin: 0;">24/7</h1>
            <p style="font-weight: bold; margin: 0.5rem 0;">Availability</p>
            <p style="color: #666; font-size: 0.9rem; margin: 0;">Always online</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Why Choose Our Service
    st.markdown("## 🚀 Why Businesses Choose Us")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="visual-box">
            <h1 style="font-size: 3rem; margin: 0; color: #667eea;">⚡</h1>
            <h4 style="color: #667eea;">Instant Setup</h4>
            <p style="color: #666; font-size: 0.95rem;">
            Go live in 5 minutes with our simple API. No complex installations, no training needed. Just send a request and get optimized results.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="visual-box">
            <h1 style="font-size: 3rem; margin: 0; color: #667eea;">🎯</h1>
            <h4 style="color: #667eea;">Tailored to Your Business</h4>
            <p style="color: #666; font-size: 0.95rem;">
            Every business is unique. Configure your own rates, service types, and constraints. Our AI adapts to your specific needs.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="visual-box">
            <h1 style="font-size: 3rem; margin: 0; color: #667eea;">📈</h1>
            <h4 style="color: #667eea;">Scale Without Limits</h4>
            <p style="color: #666; font-size: 0.95rem;">
            From 10 to 10,000 bookings daily. Our infrastructure grows with you. Pay only for what you use, no upfront costs.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Service Benefits
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="comparison-table">
            <h3 style="color: #38a169; margin-bottom: 1.5rem;">✨ Complete Service Package</h3>
            <div class="comparison-row">
                <span class="check-mark">✓</span>
                <span><strong>Real-time optimization</strong> - Always get the best match</span>
            </div>
            <div class="comparison-row">
                <span class="check-mark">✓</span>
                <span><strong>All UK charges included</strong> - Congestion, parking, tolls</span>
            </div>
            <div class="comparison-row">
                <span class="check-mark">✓</span>
                <span><strong>Multi-stop journeys</strong> - Complex routes simplified</span>
            </div>
            <div class="comparison-row">
                <span class="check-mark">✓</span>
                <span><strong>Provider availability</strong> - Never double-book</span>
            </div>
            <div class="comparison-row">
                <span class="check-mark">✓</span>
                <span><strong>Automatic updates</strong> - Always current with regulations</span>
            </div>
            <div class="comparison-row">
                <span class="check-mark">✓</span>
                <span><strong>24/7 support</strong> - We're here when you need us</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="comparison-table">
            <h3 style="color: #667eea; margin-bottom: 1.5rem;">🎯 Perfect For</h3>
            <div class="comparison-row">
                <span style="font-size: 1.5rem; margin-right: 1rem;">🏥</span>
                <span><strong>Healthcare</strong> - Home visits, mobile clinics</span>
            </div>
            <div class="comparison-row">
                <span style="font-size: 1.5rem; margin-right: 1rem;">🔧</span>
                <span><strong>Field Services</strong> - Repairs, maintenance, installations</span>
            </div>
            <div class="comparison-row">
                <span style="font-size: 1.5rem; margin-right: 1rem;">📦</span>
                <span><strong>Delivery</strong> - Last-mile optimization</span>
            </div>
            <div class="comparison-row">
                <span style="font-size: 1.5rem; margin-right: 1rem;">🏗️</span>
                <span><strong>Construction</strong> - Site visits, inspections</span>
            </div>
            <div class="comparison-row">
                <span style="font-size: 1.5rem; margin-right: 1rem;">💼</span>
                <span><strong>Consulting</strong> - Client meetings, interpreting </span>
            </div>
            <div class="comparison-row">
                <span style="font-size: 1.5rem; margin-right: 1rem;">🚨</span>
                <span><strong>Emergency Services</strong> - Rapid response</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # What's Included
    st.markdown("## 🎁 Everything You Need")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="visual-box">
            <h1 style="font-size: 3rem; margin: 0;">🧠</h1>
            <h4 style="color: #667eea;">Smart Matching</h4>
            <p style="color: #666; font-size: 0.9rem;">
            • AI provider selection<br>
            • Skill matching<br>
            • Availability checking<br>
            • Cost optimization
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="visual-box">
            <h1 style="font-size: 3rem; margin: 0;">💰</h1>
            <h4 style="color: #667eea;">Complete Costs</h4>
            <p style="color: #666; font-size: 0.9rem;">
            • Mileage & fuel<br>
            • Parking fees<br>
            • Congestion charges<br>
            • Travel time
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="visual-box">
            <h1 style="font-size: 3rem; margin: 0;">📊</h1>
            <h4 style="color: #667eea;">Real Intelligence</h4>
            <p style="color: #666; font-size: 0.9rem;">
            • Traffic prediction<br>
            • Route optimization<br>
            • Historical learning<br>
            • Cost forecasting
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Final CTA
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 3rem; border-radius: 15px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.2);">
        <h2 style="margin-bottom: 1rem; font-size: 2.5rem;">Start Saving Today</h2>
        <div>
            <a href="mailto:katerina.i@eco-n-tech.com?subject=Travel Cost Optimizer API Access Request&body=Hi,%0D%0A%0D%0AI'm interested in getting API access to the Travel Cost Optimizer.%0D%0A%0D%0ACompany:%0D%0AUse Case:%0D%0AMonthly Volume:%0D%0A%0D%0AThanks!" class="cta-button" style="font-size: 1.2rem; padding: 1rem 3rem;">Get API Access</a>
        </div>
        <p style="margin-top: 2rem; font-size: 0.9rem; opacity: 0.8;">✉️ katerina.i@eco-n-tech.com</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
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
        <strong>Scalability:</strong> API-first design ready for enterprise deployment
        </p>
    </div>
    """, unsafe_allow_html=True)