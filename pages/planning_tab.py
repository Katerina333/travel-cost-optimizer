import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import polyline as pl
from typing import List, Dict
from datetime import datetime
from folium import plugins

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
            help="Excel file with customer bookings",
            key="bookings_upload"
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
            help="Excel file with provider details",
            key="providers_upload"
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
    
    # Step 3: Display results if available in session state
    if 'planning_results' in st.session_state and st.session_state.planning_results:
        display_results(
            st.session_state.planning_results, 
            st.session_state.excel_handler,
            st.session_state.maps_service
        )

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
            
            # Store results in session state
            st.session_state.planning_results = results
            st.session_state.excel_handler = excel_handler
            st.session_state.maps_service = maps_service
            
            # Force rerun to display results
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

def display_results(results: List[Dict], excel_handler, maps_service):
    """Display analysis results with improved visualization"""
    
    st.markdown("### 📊 Step 3: Results")
    
    # Cost summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_cost = sum(r['best_provider']['total_cost'] if r['best_provider'] else 0 for r in results)
    total_distance = sum(r['best_provider']['distance'] * 2 if r['best_provider'] else 0 for r in results)
    total_duration = sum(r['best_provider']['duration'] * 2 if r['best_provider'] else 0 for r in results)
    matched_bookings = sum(1 for r in results if r['best_provider'])
    
    with col1:
        st.metric("Total Cost", f"£{total_cost:.2f}")
    with col2:
        st.metric("Total Distance", f"{total_distance:.1f} miles")
    with col3:
        # Convert minutes to hours and minutes
        hours = int(total_duration // 60)
        minutes = int(total_duration % 60)
        st.metric("Total Travel Time", f"{hours}h {minutes}m")
    with col4:
        st.metric("Matched Bookings", f"{matched_bookings}/{len(results)}")
    
    # View options with tabs
    st.markdown("#### View Options")
    tab1, tab2, tab3 = st.tabs(["📋 Summary Table", "💰 Detailed Costs", "🛣️ Individual Routes"])
    
    with tab1:
        display_summary_table(results)
    
    with tab2:
        display_detailed_costs(results)
    
    with tab3:
        display_individual_routes(results, maps_service)
    
    # Download report section
    st.divider()
    st.markdown("#### 📥 Download Report")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info("Download a comprehensive Excel report with all booking details, provider assignments, and cost breakdowns.")
    
    with col2:
        excel_data = excel_handler.create_results_excel(results)
        st.download_button(
            "📥 Download Excel Report",
            data=excel_data,
            file_name=f"travel_planning_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True
        )
    
    # Clear results button
    if st.button("🔄 Clear Results and Start New", type="secondary"):
        del st.session_state.planning_results
        st.rerun()

def display_summary_table(results: List[Dict]):
    """Display summary table"""
    table_data = []
    
    for result in results:
        booking = result['booking']
        best = result['best_provider']
        
        if best:
            # Get provider service types for debugging
            provider_services = getattr(best['provider'], 'service_types', 'Unknown')
            
            table_data.append({
                'Booking': booking.booking_id,
                'Customer': booking.customer_address[:30] + '...',
                'Date': booking.service_date,
                'Time': booking.service_time,
                'Service Type': getattr(booking, 'service_type', 'General'),
                'Provider': best['provider'].name,
                'Provider Services': provider_services,
                'Distance': f"{best['distance']:.1f} mi",
                'Travel Time': f"{int(best['duration'])} min",
                'Travel Cost': f"£{best['travel_cost']:.2f}",
                'Service Cost': f"£{best['service_cost']:.2f}",
                'Total Cost': f"£{best['total_cost']:.2f}"
            })
        else:
            table_data.append({
                'Booking': booking.booking_id,
                'Customer': booking.customer_address[:30] + '...',
                'Date': booking.service_date,
                'Time': booking.service_time,
                'Service Type': getattr(booking, 'service_type', 'General'),
                'Provider': 'No Match',
                'Provider Services': '-',
                'Distance': '-',
                'Travel Time': '-',
                'Travel Cost': '-',
                'Service Cost': '-',
                'Total Cost': '-'
            })
    
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Summary statistics
    matched_bookings = sum(1 for r in results if r['best_provider'])
    if matched_bookings > 0:
        total_cost = sum(r['best_provider']['total_cost'] for r in results if r['best_provider'])
        avg_cost = total_cost / matched_bookings
        st.caption(f"Average cost per booking: £{avg_cost:.2f}")
    
    # Debug info - show how many providers were considered
    with st.expander("📊 Provider Selection Analysis"):
        for i, result in enumerate(results):
            booking = result['booking']
            best = result.get('best_provider')
            
            st.write(f"**Booking {booking.booking_id} - {getattr(booking, 'service_type', 'Unknown')}**")
            st.write(f"Customer Location: {booking.customer_address[:50]}...")
            
            if best and 'all_providers' in best:
                # Create a detailed comparison table
                comparison_data = []
                for p_info in best['all_providers']:
                    # Find the full provider data
                    provider = next((p for p in booking.providers if p.name == p_info['provider_name']), None)
                    if provider:
                        comparison_data.append({
                            'Provider': p_info['provider_name'],
                            'Location': provider.address[:30] + '...',
                            'Services': getattr(provider, 'service_types', 'Unknown'),
                            'Distance': f"{p_info['distance']:.1f} mi",
                            'Travel Cost': f"£{p_info.get('travel_cost', 0):.2f}",
                            'Service Cost': f"£{p_info.get('service_cost', 0):.2f}",
                            'Total Cost': f"£{p_info['total_cost']:.2f}",
                            'Selected': '✅' if p_info['provider_name'] == best['provider'].name else ''
                        })
                
                if comparison_data:
                    comparison_df = pd.DataFrame(comparison_data)
                    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
                    
                    # Explain why this provider was selected
                    st.info(f"✅ {best['provider'].name} was selected with the lowest total cost of £{best['total_cost']:.2f}")
            else:
                st.write(f"Matched providers: {len(booking.providers)}")
                if booking.providers:
                    for p in booking.providers[:5]:
                        st.write(f"- {p.name} ({getattr(p, 'service_types', 'Unknown')})")
            
            if i < len(results) - 1:
                st.divider()

def display_detailed_costs(results: List[Dict]):
    """Display detailed cost breakdown WITHOUT nested expanders"""
    
    # Filter options
    col1, col2 = st.columns([2, 1])
    with col1:
        show_only_matched = st.checkbox("Show only matched bookings", value=True)
    
    # Show all providers comparison first
    st.markdown("### 📊 Provider Cost Comparison")
    
    # Collect all unique providers and their average costs
    provider_stats = {}
    for result in results:
        if result['best_provider'] and 'all_providers' in result['best_provider']:
            for p in result['best_provider']['all_providers']:
                if p['provider_name'] not in provider_stats:
                    provider_stats[p['provider_name']] = {
                        'total_cost': 0,
                        'count': 0,
                        'selected': 0
                    }
                provider_stats[p['provider_name']]['total_cost'] += p['total_cost']
                provider_stats[p['provider_name']]['count'] += 1
            
            # Mark selected provider
            selected_name = result['best_provider']['provider'].name
            if selected_name in provider_stats:
                provider_stats[selected_name]['selected'] += 1
    
    if provider_stats:
        stats_data = []
        for name, stats in provider_stats.items():
            stats_data.append({
                'Provider': name,
                'Times Selected': stats['selected'],
                'Avg Cost When Available': f"£{stats['total_cost'] / stats['count']:.2f}",
                'Total Evaluations': stats['count']
            })
        
        stats_df = pd.DataFrame(stats_data)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)
    
    st.markdown("### 📋 Booking Details")
    
    for i, result in enumerate(results):
        booking = result['booking']
        best = result['best_provider']
        
        if show_only_matched and not best:
            continue
        
        # Use container instead of expander for better layout
        with st.container():
            st.markdown(f"#### 📍 {booking.booking_id} - {booking.customer_address[:50]}...")
            
            if best:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write("**📅 Booking Details**")
                    st.write(f"Date: {booking.service_date}")
                    st.write(f"Time: {booking.service_time}")
                    st.write(f"Duration: {getattr(booking, 'duration', 2.0)}h")
                    st.write(f"Service Type: {getattr(booking, 'service_type', 'General')}")
                
                with col2:
                    st.write("**👤 Selected Provider**")
                    st.write(f"Name: {best['provider'].name}")
                    st.write(f"Location: {best['provider'].address}")
                    st.write(f"Travel Mode: {best['cost_details']['travel_mode']}")
                    st.write(f"Service Cost: £{best['cost_details']['service_cost']:.2f} (flat)")
                    st.write(f"Travel Time Rate: £{best['cost_details'].get('travel_time_rate', 15.00):.2f}/hr")
                
                with col3:
                    st.write("**💰 Cost Breakdown**")
                    st.write("*Travel Costs:*")
                    for cost_type, amount in best['travel_breakdown'].items():
                        if isinstance(amount, (int, float)) and amount > 0:
                            label = cost_type.replace('_', ' ').title()
                            st.write(f"{label}: £{amount:.2f}")
                    st.write("---")
                    st.write(f"**Total Travel: £{best['travel_cost']:.2f}**")
                    st.write(f"**Service: £{best['service_cost']:.2f}**")
                    st.write(f"**Grand Total: £{best['total_cost']:.2f}**")
                
                # Show optimization status
                if best.get('optimized'):
                    st.success("✨ Optimized route - Provider already in area")
                
                # Show route details
                st.write("**🛣️ Route Details**")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"One-way distance: {best['distance']:.1f} miles")
                    st.write(f"Round-trip distance: {best['cost_details']['round_trip_distance']:.1f} miles")
                with col2:
                    one_way_hours = int(best['duration'] // 60)
                    one_way_mins = int(best['duration'] % 60)
                    round_trip_hours = int(best['cost_details']['round_trip_duration'] // 60)
                    round_trip_mins = int(best['cost_details']['round_trip_duration'] % 60)
                    st.write(f"One-way time: {one_way_hours}h {one_way_mins}m")
                    st.write(f"Round-trip time: {round_trip_hours}h {round_trip_mins}m")
                
                # Show all providers evaluated (not in expander)
                if 'all_providers' in best and len(best['all_providers']) > 1:
                    st.write("**🔍 All Providers Evaluated for this Booking:**")
                    providers_df = pd.DataFrame(best['all_providers'])
                    providers_df = providers_df.sort_values('total_cost')
                    providers_df['total_cost'] = providers_df['total_cost'].apply(lambda x: f"£{x:.2f}")
                    providers_df['distance'] = providers_df['distance'].apply(lambda x: f"{x:.1f} mi")
                    providers_df['selected'] = providers_df['provider_name'] == best['provider'].name
                    providers_df['selected'] = providers_df['selected'].apply(lambda x: '✅' if x else '')
                    st.dataframe(providers_df, use_container_width=True, hide_index=True)
            else:
                st.error("❌ No suitable provider found for this booking")
                st.write(f"Service required: {getattr(booking, 'service_type', 'Unknown')}")
            
            st.divider()

def display_individual_routes(results: List[Dict], maps_service):
    """Display individual route maps for each booking"""
    
    # Filter to only bookings with matches
    matched_results = [(i, r) for i, r in enumerate(results) if r['best_provider']]
    
    if not matched_results:
        st.warning("No routes to display")
        return
    
    # Create booking selector
    booking_options = []
    for idx, (original_idx, result) in enumerate(matched_results):
        booking = result['booking']
        provider = result['best_provider']['provider']
        service_type = getattr(booking, 'service_type', 'General')
        booking_options.append(
            f"{booking.booking_id} - {service_type} → {provider.name} "
            f"(£{result['best_provider']['total_cost']:.2f})"
        )
    
    selected_idx = st.selectbox(
        "Select booking to view route:",
        range(len(booking_options)),
        format_func=lambda x: booking_options[x],
        key="individual_route_selector"
    )
    
    # Display selected route
    _, selected_result = matched_results[selected_idx]
    booking = selected_result['booking']
    best = selected_result['best_provider']
    route_info = best['route_info']
    
    # Route details
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Distance", f"{best['distance']:.1f} miles", help="One-way distance")
    with col2:
        # Format travel time properly
        travel_hours = int(best['duration'] // 60)
        travel_mins = int(best['duration'] % 60)
        if travel_hours > 0:
            travel_time_str = f"{travel_hours}h {travel_mins}m"
        else:
            travel_time_str = f"{travel_mins} min"
        st.metric("Travel Time", travel_time_str, help="One-way duration")
    with col3:
        st.metric("Travel Cost", f"£{best['travel_cost']:.2f}", help="Round-trip travel cost")
    with col4:
        st.metric("Total Cost", f"£{best['total_cost']:.2f}", help="Travel + Service cost")
    
    # Create map for individual route
    if 'start_location' in route_info and 'end_location' in route_info:
        # Center map on route
        center_lat = (route_info['start_location']['lat'] + route_info['end_location']['lat']) / 2
        center_lng = (route_info['start_location']['lng'] + route_info['end_location']['lng']) / 2
        
        m = folium.Map(location=[center_lat, center_lng], zoom_start=10)
        
        # Provider marker
        folium.Marker(
            [route_info['start_location']['lat'], route_info['start_location']['lng']],
            popup=f"<b>Provider: {best['provider'].name}</b><br>"
                  f"Address: {best['provider'].address}<br>"
                  f"Travel Mode: {best['cost_details']['travel_mode']}",
            icon=folium.Icon(color='green', icon='user', prefix='fa'),
            tooltip="Provider Location"
        ).add_to(m)
        
        # Customer marker
        folium.Marker(
            [route_info['end_location']['lat'], route_info['end_location']['lng']],
            popup=f"<b>Customer Location</b><br>"
                  f"Address: {booking.customer_address}<br>"
                  f"Service: {booking.service_date} {booking.service_time}<br>"
                  f"Service Type: {getattr(booking, 'service_type', 'General')}",
            icon=folium.Icon(color='red', icon='home', prefix='fa'),
            tooltip="Customer Location"
        ).add_to(m)
        
        # Draw route
        if route_info.get('polyline'):
            try:
                points = pl.decode(route_info['polyline'])
                folium.PolyLine(
                    points,
                    color='blue',
                    weight=4,
                    opacity=0.8,
                    tooltip=f"Distance: {best['distance']:.1f} miles"
                ).add_to(m)
            except:
                # Draw straight line if polyline fails
                folium.PolyLine(
                    [
                        [route_info['start_location']['lat'], route_info['start_location']['lng']],
                        [route_info['end_location']['lat'], route_info['end_location']['lng']]
                    ],
                    color='blue',
                    weight=4,
                    opacity=0.8,
                    dash_array='10',
                    tooltip="Direct line (route not available)"
                ).add_to(m)
        
        # Fit bounds
        bounds = [
            [route_info['start_location']['lat'], route_info['start_location']['lng']],
            [route_info['end_location']['lat'], route_info['end_location']['lng']]
        ]
        m.fit_bounds(bounds, padding=[50, 50])
        
        folium_static(m, height=500)
        
        # Cost breakdown
        st.markdown("### 💰 Detailed Cost Breakdown")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Travel Costs (Round Trip):**")
            for cost_type, amount in best['travel_breakdown'].items():
                if isinstance(amount, (int, float)) and amount > 0:
                    label = cost_type.replace('_', ' ').title()
                    st.write(f"• {label}: £{amount:.2f}")
            
            # Show additional route details if available
            if 'route_details' in best:
                details = best['route_details']
                st.write("\n**Route Information:**")
                st.write(f"• Distance: {details['distance_miles']:.1f} miles (one way)")
                st.write(f"• Duration: {details['duration_minutes']:.0f} minutes (one way)")
                if 'traffic_conditions' in details:
                    st.write(f"• Traffic: {details['traffic_conditions']}")
            
            st.write(f"\n**Total Travel: £{best['travel_cost']:.2f}**")
        
        with col2:
            st.write("**Service Details:**")
            st.write(f"• Service Type: {getattr(booking, 'service_type', 'General')}")
            st.write(f"• Service Duration: {best['cost_details']['service_duration']} hours")
            st.write(f"• Service Cost: £{best['cost_details']['service_cost']:.2f} (flat rate)")
            st.write(f"• Travel Time Rate: £{best['cost_details'].get('travel_time_rate', 15.00):.2f}/hr")
            
            travel_hours = best['cost_details']['round_trip_duration'] / 60
            st.write(f"\n**Travel Time Compensation:**")
            st.write(f"• {travel_hours:.1f} hours × £{best['cost_details'].get('travel_time_rate', 15.00):.2f}/hr")
            st.write(f"• = £{best['travel_breakdown'].get('travel_time', 0):.2f}")
        
        st.write("---")
        st.write(f"### Total Cost: £{best['total_cost']:.2f}")