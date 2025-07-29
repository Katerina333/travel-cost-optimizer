import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import polyline as pl
from typing import List, Dict
from datetime import datetime

from services.excel_handler import ExcelHandler
from services.cost_calculator import CostCalculator
from services.maps_service import MapsService
from models.booking import Booking

def render_planning_tab():
    """Simple planning tab for travel cost calculation"""
    
    # Initialize services
    excel_handler = ExcelHandler()
    cost_calculator = CostCalculator()
    maps_service = MapsService()
    
    st.title("🚗 Travel Cost Planning")
    
    # Step 1: Upload Files
    st.markdown("### 📁 Step 1: Upload Excel Files")
    
    col1, col2 = st.columns(2)
    
    with col1:
        bookings_file = st.file_uploader(
            "Upload Bookings File",
            type=['xlsx'],
            help="Excel file with customer bookings"
        )
        
        bookings_template, providers_template = excel_handler.create_planning_templates()
        st.download_button(
            "📥 Download Bookings Template",
            data=bookings_template,
            file_name="bookings_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col2:
        providers_file = st.file_uploader(
            "Upload Providers File",
            type=['xlsx'],
            help="Excel file with provider details"
        )
        
        st.download_button(
            "📥 Download Providers Template",
            data=providers_template,
            file_name="providers_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # Step 2: Planning
    if bookings_file and providers_file:
        st.markdown("### 🚀 Step 2: Run Planning")
        
        if st.button("Start Planning", type="primary", use_container_width=True):
            process_files(bookings_file, providers_file, excel_handler, cost_calculator, maps_service)

def process_files(bookings_file, providers_file, excel_handler, cost_calculator, maps_service):
    """Process uploaded files and calculate routes"""
    
    with st.spinner("Reading files..."):
        try:
            # Parse files
            bookings = excel_handler.parse_planning_files(
                bookings_file.read(),
                providers_file.read()
            )
            
            if not bookings:
                st.error("No valid bookings found")
                return
            
            st.success(f"✅ Found {len(bookings)} bookings")
            
            # Analyze bookings
            with st.spinner("Calculating routes and costs..."):
                results = cost_calculator.calculate_all_bookings(bookings)
            
            # Display results
            display_results(results, excel_handler, maps_service)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

def display_results(results: List[Dict], excel_handler, maps_service):
    """Display analysis results"""
    
    st.markdown("### 📊 Step 3: Results")
    
    # Summary table
    st.markdown("#### Summary Table")
    
    table_data = []
    total_cost = 0
    
    for result in results:
        booking = result['booking']
        best = result['best_provider']
        
        if best:
            total_cost += best['total_cost']
            table_data.append({
                'Booking': booking.booking_id,
                'Customer': booking.customer_address[:30] + '...',
                'Date': booking.service_date,
                'Time': booking.service_time,
                'Provider': best['provider'].name,
                'Distance': f"{best['distance']:.1f} mi",
                'Travel Time': f"{int(best['duration'])} min",
                'Total Cost': f"£{best['total_cost']:.2f}"
            })
        else:
            table_data.append({
                'Booking': booking.booking_id,
                'Customer': booking.customer_address[:30] + '...',
                'Date': booking.service_date,
                'Time': booking.service_time,
                'Provider': 'No Match',
                'Distance': '-',
                'Travel Time': '-',
                'Total Cost': '-'
            })
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Total cost
    st.info(f"**Total Cost: £{total_cost:.2f}**")
    
    # Map view
    st.markdown("#### 🗺️ Map View")
    
    # Create map centered on first booking
    if results and results[0]['best_provider']:
        first_route = results[0]['best_provider']['route_info']
        center_lat = (first_route['start_location']['lat'] + first_route['end_location']['lat']) / 2
        center_lng = (first_route['start_location']['lng'] + first_route['end_location']['lng']) / 2
        m = folium.Map(location=[center_lat, center_lng], zoom_start=10)
    else:
        m = folium.Map(location=[52.4862, -1.8904], zoom_start=10)  # UK center
    
    # Add all routes to map
    colors = ['blue', 'red', 'green', 'purple', 'orange']
    
    for idx, result in enumerate(results):
        if result['best_provider']:
            booking = result['booking']
            provider = result['best_provider']['provider']
            route_info = result['best_provider']['route_info']
            
            # Add markers
            if 'start_location' in route_info:
                # Provider marker
                folium.Marker(
                    [route_info['start_location']['lat'], route_info['start_location']['lng']],
                    popup=f"Provider: {provider.name}",
                    icon=folium.Icon(color='green', icon='user')
                ).add_to(m)
                
                # Customer marker
                folium.Marker(
                    [route_info['end_location']['lat'], route_info['end_location']['lng']],
                    popup=f"Customer: {booking.booking_id}",
                    icon=folium.Icon(color='red', icon='home')
                ).add_to(m)
                
                # Draw route
                if route_info.get('polyline'):
                    try:
                        points = pl.decode(route_info['polyline'])
                        folium.PolyLine(
                            points,
                            color=colors[idx % len(colors)],
                            weight=3,
                            opacity=0.8,
                            popup=f"{booking.booking_id}: {provider.name}"
                        ).add_to(m)
                    except:
                        pass
    
    folium_static(m, height=500)
    
    # Download report
    st.markdown("#### 📥 Download Report")
    
    excel_data = excel_handler.create_results_excel(results)
    st.download_button(
        "Download Excel Report",
        data=excel_data,
        file_name=f"travel_planning_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary"
    )