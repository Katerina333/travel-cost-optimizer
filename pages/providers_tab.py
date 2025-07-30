import streamlit as st
import folium
from streamlit_folium import folium_static
import json
import polyline as pl
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import io

from services.maps_service import MapsService
from services.uk_transport import UKTransportService
from services.excel_handler import ExcelHandler
from models.booking import OtherBooking

def render_providers_tab():
    """Render the provider cost calculation tab"""
    
    # Initialize services
    services = initialize_services()
    maps_service = services['maps_service']
    uk_transport = services['uk_transport']
    
    # Settings section
    settings = render_provider_settings()
    
    # Input method selection
    st.subheader("🚛 Provider Journey Calculation")
    
    input_method = st.radio(
        "Select Input Method",
        ["📝 Manual Entry", "📊 Excel Upload"],
        horizontal=True,
        key="provider_input_method"
    )
    
    st.divider()
    
    if input_method == "📝 Manual Entry":
        render_manual_entry(
            settings['provider_id'],
            settings['provider_start'],
            settings['travel_mode'],
            maps_service,
            uk_transport,
            settings['include_return']
        )
    else:  # Excel Upload
        render_excel_upload(
            settings['provider_id'],
            settings['provider_start'],
            settings['travel_mode'],
            maps_service,
            uk_transport,
            settings['include_return']
        )

@st.cache_resource
def initialize_services() -> Dict:
    """Initialize and cache services"""
    return {
        'maps_service': MapsService(),
        'uk_transport': UKTransportService(),
        'excel_handler': ExcelHandler()
    }

def render_provider_settings() -> Dict:
    """Render provider settings and return configuration"""
    with st.expander("⚙️ Provider Settings", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Provider Details**")
            provider_id = st.text_input("Provider ID", value="PROV001")
            provider_start = st.text_input("Start Location", value="Birmingham, B1 1AA")
            travel_mode = st.selectbox(
                "Travel Mode",
                ["Car", "Public Transport", "Mixed"],
                key="provider_travel_mode"
            )
        
        with col2:
            st.write("**Cost Rates**")
            if travel_mode in ["Car", "Mixed"]:
                mileage_rate = st.number_input(
                    "Mileage Rate (£/mile)", 
                    value=0.45, 
                    min_value=0.0,
                    max_value=1.0,
                    step=0.01,
                    key="mileage_rate"
                )
            else:
                mileage_rate = 0.45
                
            travel_time_rate = st.number_input(
                "Travel Time Rate (£/hour)", 
                value=15.00,
                min_value=0.0,
                max_value=100.0,
                step=1.00,
                key="travel_time_rate"
            )
            
            if travel_mode in ["Public Transport", "Mixed"]:
                include_receipts = st.checkbox("Include actual ticket costs")
            else:
                include_receipts = False
        
        with col3:
            st.write("**Calculation Options**")
            include_return = st.checkbox("Include return journey", value=True)
            include_parking = st.checkbox("Include parking costs", value=True, key="include_parking")
            include_congestion = st.checkbox("Include congestion charges", value=True)
    
    return {
        'provider_id': provider_id,
        'provider_start': provider_start,
        'travel_mode': travel_mode,
        'mileage_rate': mileage_rate,
        'travel_time_rate': travel_time_rate,
        'include_receipts': include_receipts,
        'include_return': include_return,
        'include_parking': include_parking,
        'include_congestion': include_congestion
    }

def render_manual_entry(provider_id: str, provider_start: str, travel_mode: str, 
                       maps_service, uk_transport, include_return: bool):
    """Render manual booking entry interface"""
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write("Enter booking details for journey calculation")
    
    with col2:
        num_bookings = st.number_input(
            "Number of bookings", 
            min_value=1, 
            max_value=10, 
            value=2
        )
    
    bookings = []
    
    # Create columns for bookings
    booking_cols = st.columns(min(num_bookings, 3))
    
    for i in range(num_bookings):
        col_idx = i % 3
        with booking_cols[col_idx]:
            with st.container():
                st.write(f"**Booking {i+1}**")
                
                booking_id = st.text_input(
                    f"ID", 
                    value=f"B{i+1:03d}", 
                    key=f"booking_id_{i}"
                )
                address = st.text_input(
                    f"Address", 
                    key=f"address_{i}",
                    placeholder="Full address with postcode"
                )
                
                col_a, col_b = st.columns(2)
                with col_a:
                    start_time = st.time_input(
                        f"Time", 
                        key=f"time_{i}",
                        value=datetime.strptime(f"{9+i*3}:00", "%H:%M").time()
                    )
                with col_b:
                    duration = st.number_input(
                        f"Hours", 
                        value=1.0, 
                        min_value=0.5, 
                        max_value=8.0, 
                        step=0.5, 
                        key=f"duration_{i}"
                    )
                
                if travel_mode in ["Public Transport", "Mixed"]:
                    ticket_cost = st.number_input(
                        f"Ticket £", 
                        value=0.0, 
                        step=0.50, 
                        key=f"ticket_{i}"
                    )
                else:
                    ticket_cost = 0
                
                if address:
                    bookings.append({
                        'booking_id': booking_id,
                        'address': address,
                        'start_time': start_time.strftime("%H:%M"),
                        'duration_hours': duration,
                        'ticket_cost': ticket_cost
                    })
    
    st.divider()
    
    # Calculate button
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col2:
        if st.button("🧮 Calculate Journey Costs", type="primary", use_container_width=True):
            if bookings:
                with st.spinner("Calculating optimal journey..."):
                    # Use the rates from settings for manual entry
                    travel_time_rate = st.session_state.get('travel_time_rate', 15.00)
                    mileage_rate = st.session_state.get('mileage_rate', 0.45)
                    parking_paid = st.session_state.get('include_parking', True)
                    
                    results = calculate_provider_journey_with_rates(
                        provider_start, 
                        bookings, 
                        travel_mode,
                        maps_service,
                        uk_transport,
                        include_return,
                        travel_time_rate,
                        mileage_rate,
                        not parking_paid  # Invert because setting is "include parking costs"
                    )
                    
                    # Store results in session state
                    st.session_state.journey_results = results
                    st.session_state.journey_bookings = bookings
            else:
                st.warning("Please enter at least one booking address")
    
    # Display results if available
    if 'journey_results' in st.session_state:
        st.divider()
        display_journey_results(
            st.session_state.journey_results, 
            travel_mode
        )
        show_journey_map(
            provider_start, 
            st.session_state.journey_bookings, 
            st.session_state.journey_results, 
            maps_service
        )

def render_excel_upload(provider_id: str, provider_start: str, travel_mode: str, 
                       maps_service, uk_transport, include_return: bool):
    """Render Excel file upload interface"""
    
    # Add clear instructions
    st.info("📋 **Important**: Use the Provider Journey Template (not the Planning template). The template should contain a 'Provider_Journey' worksheet with booking locations and times.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload completed provider journey Excel template",
            type=['xlsx'],
            help="Download and fill the Provider Journey Excel template, then upload here",
            key="provider_excel_upload"
        )
    
    with col2:
        # Download template
        excel_handler = ExcelHandler()
        template = excel_handler.create_provider_journey_template()
        
        st.download_button(
            label="📥 Download Provider Journey Template",
            data=template,
            file_name="provider_journey_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Download Excel template specifically for provider journey calculations"
        )
    
    if uploaded_file:
        try:
            # Check file size and name for debugging
            file_details = {"Filename": uploaded_file.name, "FileSize": f"{uploaded_file.size} bytes"}
            st.caption(f"Uploaded: {uploaded_file.name}")
            
            # Parse Excel file
            excel_handler = ExcelHandler()
            data = excel_handler.parse_provider_journey_excel(uploaded_file.read())
            
            # Extract provider details from Excel
            provider_id = data.get('provider_id', provider_id)
            provider_start = data.get('start_location', provider_start)
            travel_mode = data.get('travel_mode', 'Car')
            travel_time_rate = data.get('travel_time_cost_per_hour', 15.00)
            mileage_rate = data.get('mileage_cost_per_mile', 0.45)
            parking_paid = data.get('parking_paid', False)
            
            bookings = data.get('bookings', [])
            
            if bookings:
                st.success(f"✅ Loaded provider {provider_id} with {len(bookings)} bookings")
                
                # Display provider details
                with st.expander("Provider Details", expanded=True):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Provider ID:** {provider_id}")
                        st.write(f"**Start Location:** {provider_start}")
                    
                    with col2:
                        st.write(f"**Travel Mode:** {travel_mode}")
                        st.write(f"**Parking:** {'Paid' if parking_paid else 'Not Paid'}")
                    
                    with col3:
                        st.write(f"**Time Rate:** £{travel_time_rate}/hour")
                        if travel_mode == 'Car':
                            st.write(f"**Mileage Rate:** £{mileage_rate}/mile")
                
                # Show booking summary
                display_booking_summary(bookings)
                
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col2:
                    if st.button("🧮 Calculate Journey Costs", type="primary", use_container_width=True):
                        with st.spinner("Calculating journey costs..."):
                            # Pass the rates from Excel to calculation
                            results = calculate_provider_journey_with_rates(
                                provider_start,
                                bookings,
                                travel_mode,
                                maps_service,
                                uk_transport,
                                include_return,
                                travel_time_rate,
                                mileage_rate,
                                parking_paid
                            )
                            
                            st.session_state.journey_results = results
                            st.session_state.journey_bookings = bookings
                            st.session_state.provider_id = provider_id
                            st.session_state.provider_details = {
                                'travel_time_rate': travel_time_rate,
                                'mileage_rate': mileage_rate,
                                'parking_paid': parking_paid
                            }
                
                # Display results
                if 'journey_results' in st.session_state:
                    st.divider()
                    display_journey_results(
                        st.session_state.journey_results, 
                        travel_mode
                    )
                    show_journey_map(
                        provider_start, 
                        st.session_state.journey_bookings,
                        st.session_state.journey_results, 
                        maps_service
                    )
            else:
                st.warning("No bookings found in the Excel file. Please ensure you're using the Provider Journey template.")
            
        except ValueError as ve:
            if "Worksheet named 'Provider_Journey' not found" in str(ve):
                st.error("❌ Wrong template! This file doesn't contain a 'Provider_Journey' worksheet.")
                st.warning("Please download and use the 'Provider Journey Template' button above, not the planning templates.")
            else:
                st.error(f"Error processing Excel file: {str(ve)}")
        except Exception as e:
            st.error(f"Error processing Excel file: {str(e)}")
            st.write("Please ensure your Excel file matches the Provider Journey template format")

def display_booking_summary(bookings: List[Dict]):
    """Display summary of loaded bookings"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Bookings", len(bookings))
    
    with col2:
        total_duration = sum(b.get('duration_hours', 0) for b in bookings)
        st.metric("Total Service Hours", f"{total_duration}h")
    
    with col3:
        # Get time range
        if bookings:
            times = [b.get('start_time', '') for b in bookings if b.get('start_time')]
            if times:
                st.metric("Time Range", f"{min(times)} - {max(times)}")
    
    with col4:
        # Get date
        dates = [b.get('date', '') for b in bookings if b.get('date')]
        if dates:
            st.metric("Service Date", dates[0])
    
    # Show booking details in expander
    with st.expander("Booking Details", expanded=False):
        for i, booking in enumerate(bookings):
            st.write(f"**{booking.get('booking_id', f'Booking {i+1}')}**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"📍 {booking['address']}")
            with col2:
                st.write(f"🕐 {booking.get('start_time', 'N/A')}")
            with col3:
                st.write(f"⏱️ {booking.get('duration_hours', 0)}h")
            if i < len(bookings) - 1:
                st.divider()

def calculate_provider_journey_with_rates(start_location: str, bookings: List[Dict], 
                                         travel_mode: str, maps_service, uk_transport,
                                         include_return: bool, travel_time_rate: float,
                                         mileage_rate: float, parking_paid: bool) -> Dict:
    """Calculate costs for provider's journey using specific rates"""
    
    results = {
        'legs': [],
        'total_distance': 0,
        'total_duration': 0,
        'total_cost': 0,
        'breakdown': {}
    }
    
    # Sort bookings by time
    sorted_bookings = sorted(bookings, key=lambda x: x.get('start_time', '00:00'))
    
    # Calculate each leg
    current_location = start_location
    
    for i, booking in enumerate(sorted_bookings):
        # Calculate travel from current location to booking
        route_info = maps_service.get_route_with_directions(
            current_location,
            booking['address']
        )
        
        if route_info['success']:
            distance = route_info['distance_miles']
            duration = route_info['duration_minutes']
            
            # Calculate costs based on travel mode and provided rates
            cost_breakdown = {}
            leg_cost = 0
            
            if travel_mode == "Car":
                # Mileage cost using provided rate
                if mileage_rate > 0:
                    mileage_cost = round(distance * mileage_rate, 2)
                    cost_breakdown['mileage'] = mileage_cost
                    leg_cost += mileage_cost
                
                # Get parking cost if not paid
                if not parking_paid:
                    parking_costs = uk_transport.get_parking_costs(
                        booking['address'], 
                        booking.get('duration_hours', 1.0)
                    )
                    if parking_costs['success']:
                        parking_cost = parking_costs['total_cost']
                        cost_breakdown['parking'] = parking_cost
                        leg_cost += parking_cost
                
                # Check for congestion charges
                congestion = uk_transport.get_congestion_charge(booking['address'])
                if congestion['charge'] > 0:
                    cost_breakdown['congestion_charge'] = congestion['charge']
                    leg_cost += congestion['charge']
                
            else:  # Public Transport
                # Estimate public transport cost
                public_costs = uk_transport.estimate_public_transport_cost(
                    current_location,
                    booking['address'],
                    distance
                )
                
                if 'train' in public_costs:
                    transport_cost = public_costs['train']['cost']
                else:
                    transport_cost = distance * 0.20  # Default estimate
                
                cost_breakdown['public_transport'] = transport_cost
                leg_cost += transport_cost
            
            # Add travel time cost using provided rate
            travel_time_cost = round((duration / 60) * travel_time_rate, 2)
            cost_breakdown['travel_time'] = travel_time_cost
            leg_cost += travel_time_cost
            
            results['legs'].append({
                'from': current_location,
                'to': booking['address'],
                'booking_id': booking.get('booking_id', f'B{i+1}'),
                'distance': round(distance, 1),
                'duration': round(duration, 0),
                'cost': round(leg_cost, 2),
                'breakdown': cost_breakdown,
                'polyline': route_info.get('polyline')
            })
            
            results['total_distance'] += distance
            results['total_duration'] += duration
            results['total_cost'] += leg_cost
            
            current_location = booking['address']
    
    # Add return journey if requested
    if include_return and sorted_bookings:
        return_route = maps_service.get_route_with_directions(
            current_location,
            start_location
        )
        
        if return_route['success']:
            distance = return_route['distance_miles']
            duration = return_route['duration_minutes']
            
            cost_breakdown = {}
            leg_cost = 0
            
            if travel_mode == "Car":
                # Mileage cost
                if mileage_rate > 0:
                    mileage_cost = round(distance * mileage_rate, 2)
                    cost_breakdown['mileage'] = mileage_cost
                    leg_cost += mileage_cost
            else:
                transport_cost = distance * 0.20
                cost_breakdown['public_transport'] = transport_cost
                leg_cost += transport_cost
            
            # Travel time cost
            travel_time_cost = round((duration / 60) * travel_time_rate, 2)
            cost_breakdown['travel_time'] = travel_time_cost
            leg_cost += travel_time_cost
            
            results['legs'].append({
                'from': current_location,
                'to': start_location,
                'booking_id': 'RETURN',
                'distance': round(distance, 1),
                'duration': round(duration, 0),
                'cost': round(leg_cost, 2),
                'breakdown': cost_breakdown,
                'polyline': return_route.get('polyline')
            })
            
            results['total_distance'] += distance
            results['total_duration'] += duration
            results['total_cost'] += leg_cost
    
    # Round totals
    results['total_distance'] = round(results['total_distance'], 1)
    results['total_duration'] = round(results['total_duration'], 0)
    results['total_cost'] = round(results['total_cost'], 2)
    
    # Create breakdown summary
    breakdown_summary = {}
    for leg in results['legs']:
        for key, value in leg['breakdown'].items():
            if key not in breakdown_summary:
                breakdown_summary[key] = 0
            breakdown_summary[key] += value
    
    results['breakdown'] = {k: round(v, 2) for k, v in breakdown_summary.items()}
    
    # Add rate information to results
    results['rates_used'] = {
        'travel_time_rate': travel_time_rate,
        'mileage_rate': mileage_rate,
        'parking_paid': parking_paid
    }
    
    return results

def display_journey_results(results: Dict, travel_mode: str):
    """Display journey calculation results"""
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Distance", f"{results['total_distance']} miles")
    
    with col2:
        hours = int(results['total_duration'] // 60)
        mins = int(results['total_duration'] % 60)
        st.metric("Total Time", f"{hours}h {mins}m")
    
    with col3:
        st.metric("Total Cost", f"£{results['total_cost']}")
    
    with col4:
        st.metric("Journey Legs", len(results['legs']))
    
    # Journey timeline
    st.subheader("🛣️ Journey Timeline")
    
    # Create timeline visualization
    timeline_cols = st.columns(min(len(results['legs']), 5))
    
    for i, leg in enumerate(results['legs'][:5]):  # Show max 5 in timeline
        col_idx = i % len(timeline_cols)
        with timeline_cols[col_idx]:
            if leg['booking_id'] == 'RETURN':
                st.info(f"🏠 Return\n{leg['distance']}mi • £{leg['cost']}")
            else:
                st.success(f"📍 {leg['booking_id']}\n{leg['distance']}mi • £{leg['cost']}")
    
    if len(results['legs']) > 5:
        st.caption(f"... and {len(results['legs']) - 5} more stops")
    
    # Detailed breakdown
    with st.expander("📊 Detailed Cost Breakdown", expanded=False):
        for i, leg in enumerate(results['legs']):
            st.write(f"**Leg {i+1}: {leg['booking_id']}**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"Distance: {leg['distance']} miles")
            with col2:
                st.write(f"Duration: {leg['duration']} mins")
            with col3:
                st.write(f"Cost: £{leg['cost']}")
            
            # Cost breakdown
            breakdown_text = " • ".join([f"{k}: £{v:.2f}" for k, v in leg['breakdown'].items() if v > 0])
            st.caption(breakdown_text)
            
            if i < len(results['legs']) - 1:
                st.divider()
    
    # Total breakdown by category
    st.subheader("💰 Cost Summary by Category")
    
    breakdown_cols = st.columns(len(results['breakdown']))
    for i, (key, value) in enumerate(results['breakdown'].items()):
        with breakdown_cols[i]:
            st.metric(key.replace('_', ' ').title(), f"£{value}")
    
    # Export options
    st.divider()
    export_journey_results(results, travel_mode)

def export_journey_results(results: Dict, travel_mode: str):
    """Export journey results"""
    col1, col2 = st.columns(2)
    
    with col1:
        export_format = st.selectbox("Export Format", ["Excel", "JSON"], key="journey_export_format")
    
    with col2:
        excel_handler = ExcelHandler()
        
        if export_format == "Excel":
            # Create Excel report
            excel_data = excel_handler.create_results_excel({
                'total_distance_miles': results['total_distance'],
                'total_duration_minutes': results['total_duration'],
                'total_cost': results['total_cost'],
                'journey_legs': results['legs'],
                'cost_breakdown': results['breakdown']
            }, 'journey')
            
            st.download_button(
                label="📥 Download Excel Report",
                data=excel_data,
                file_name=f"journey_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            # JSON export
            report = {
                "provider_id": st.session_state.get('provider_id', 'PROV001'),
                "report_date": datetime.now().strftime("%Y-%m-%d"),
                "travel_mode": travel_mode,
                "summary": {
                    "total_distance_miles": results['total_distance'],
                    "total_duration_minutes": results['total_duration'],
                    "total_cost": results['total_cost']
                },
                "cost_breakdown": results['breakdown'],
                "journey_legs": results['legs']
            }
            
            st.download_button(
                label="📥 Download JSON Report",
                data=json.dumps(report, indent=2),
                file_name=f"journey_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

def show_journey_map(start_location: str, bookings: List[Dict], results: Dict, maps_service):
    """Display the complete journey on a map"""
    
    st.subheader("🗺️ Journey Visualization")
    
    coords = maps_service.geocode_address(start_location)
    
    if coords:
        m = folium.Map(location=[coords['lat'], coords['lng']], zoom_start=10)
        
        # Add start location
        folium.Marker(
            [coords['lat'], coords['lng']],
            popup="Start/End Location",
            icon=folium.Icon(color='green', icon='home')
        ).add_to(m)
        
        # Add booking locations
        for i, booking in enumerate(bookings):
            booking_coords = maps_service.geocode_address(booking['address'])
            if booking_coords:
                folium.Marker(
                    [booking_coords['lat'], booking_coords['lng']],
                    popup=f"{booking.get('booking_id', i+1)} - {booking.get('start_time', 'N/A')}",
                    icon=folium.Icon(color='blue', icon='info-sign')
                ).add_to(m)
        
        # Draw routes
        colors = ['blue', 'red', 'purple', 'orange', 'darkred', 'darkblue']
        
        for i, leg in enumerate(results['legs']):
            if leg.get('polyline'):
                try:
                    points = pl.decode(leg['polyline'])
                    color = 'green' if leg['booking_id'] == 'RETURN' else colors[i % len(colors)]
                    
                    folium.PolyLine(
                        points,
                        color=color,
                        weight=4,
                        opacity=0.8,
                        popup=f"{leg['booking_id']}: {leg['distance']} miles"
                    ).add_to(m)
                except Exception as e:
                    st.warning(f"Could not draw route for {leg['booking_id']}")
        
        folium_static(m)
        
        # Journey summary below map
        st.info(
            f"Total Journey: {results['total_distance']} miles | "
            f"{int(results['total_duration'] // 60)}h {int(results['total_duration'] % 60)}m | "
            f"£{results['total_cost']}"
        )
    else:
        st.error("Could not geocode start location. Please check the address.")