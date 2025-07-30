import pandas as pd
import io
from typing import List, Tuple, Dict
from datetime import datetime
from models.booking import Booking, Provider

class ExcelHandler:
    """Simple Excel handler for any service type"""
    
    @staticmethod
    def create_planning_templates() -> Tuple[bytes, bytes]:
        """Create simple Excel templates"""
        
        # Bookings template
        bookings_output = io.BytesIO()
        with pd.ExcelWriter(bookings_output, engine='xlsxwriter') as writer:
            bookings_df = pd.DataFrame({
                'BookingID': ['B001', 'B002', 'B003', 'B004', 'B005'],
                'CustomerAddress': [
                    '123 High Street, Birmingham, B1 1AA',
                    '456 Park Road, Solihull, B91 2BC',
                    '789 Queen Street, Coventry, CV1 3DE',
                    '321 King Avenue, Birmingham, B2 2EF',
                    '654 Main Street, Wolverhampton, WV1 4GH'
                ],
                'ServiceDate': ['2024-03-25', '2024-03-25', '2024-03-26', '2024-03-26', '2024-03-27'],
                'ServiceTime': ['09:00', '14:00', '10:00', '15:00', '11:00'],
                'ServiceType': ['Emergency', 'Installation', 'Repair', 'Maintenance', 'Emergency'],
                'Duration': [2.0, 3.0, 1.5, 2.0, 2.5]
            })
            bookings_df.to_excel(writer, sheet_name='Bookings', index=False)
            
            workbook = writer.book
            worksheet = writer.sheets['Bookings']
            header_format = workbook.add_format({'bold': True, 'bg_color': '#4472C4', 'font_color': 'white'})
            worksheet.set_row(0, 20, header_format)
            worksheet.set_column('A:F', 20)
        
        # Providers template  
        providers_output = io.BytesIO()
        with pd.ExcelWriter(providers_output, engine='xlsxwriter') as writer:
            providers_df = pd.DataFrame({
                'ProviderID': ['P001', 'P002', 'P003', 'P004', 'P005'],
                'ProviderName': ['John Smith', 'Sarah Jones', 'Mike Wilson', 'Emma Brown', 'David Lee'],
                'ProviderAddress': [
                    'Birmingham, B3 3AA',
                    'Solihull, B90 4BB',
                    'Coventry, CV2 5CC',
                    'Birmingham, B4 6DD',
                    'Wolverhampton, WV2 7EE'
                ],
                'ServiceTypes': ['Emergency,Repair', 'Installation,Maintenance', 'All', 'Repair,Emergency', 'Emergency,Installation'],
                'TravelMode': ['Car', 'Public Transport', 'Van', 'Car and Public Transport', 'Van'],
                'ServiceCost': [50.00, 45.00, 60.00, 48.00, 55.00],  # Flat service cost
                'TravelTimeRate': [15.00, 15.00, 18.00, 15.00, 18.00],  # Per hour for travel
                'MileageRate': [0.45, 0.00, 0.60, 0.30, 0.60]  # Per mile (reduced for Car+Public)
            })
            providers_df.to_excel(writer, sheet_name='Providers', index=False)
            
            workbook = writer.book
            worksheet = writer.sheets['Providers']
            header_format = workbook.add_format({'bold': True, 'bg_color': '#4472C4', 'font_color': 'white'})
            worksheet.set_row(0, 20, header_format)
            worksheet.set_column('A:H', 20)
        
        return bookings_output.getvalue(), providers_output.getvalue()
    
    @staticmethod
    def create_provider_journey_template() -> bytes:
        """Create Excel template for provider journey with detailed columns"""
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Main Journey Sheet with all details in one row
            journey_df = pd.DataFrame({
                'Provider_ID': ['PROV001', 'PROV002'],
                'Provider_Start_Location': ['Birmingham, B1 1AA', 'Manchester, M1 1AA'],
                'Provider_Travel_Type': ['Car', 'Public Transport'],
                'Provider_Travel_Time_Cost_Per_Hour': [15.00, 15.00],
                'Provider_Mileage_Cost_Per_Mile': [0.45, 0.00],
                'Parking_Paid': ['YES', 'NO'],
                
                # Booking 1
                'Booking_Location_1': ['123 High Street, Solihull, B91 1AA', '456 Market St, Salford, M3 1AA'],
                'Booking_Appointment_Time_1': ['09:00', '10:00'],
                'Booking_Duration_1': [2.0, 1.5],
                
                # Booking 2
                'Booking_Location_2': ['456 Park Lane, Coventry, CV1 2AB', '789 King St, Bolton, BL1 1AA'],
                'Booking_Appointment_Time_2': ['14:00', '13:00'],
                'Booking_Duration_2': [1.5, 2.0],
                
                # Booking 3
                'Booking_Location_3': ['789 Queen Street, Birmingham, B2 4QZ', ''],
                'Booking_Appointment_Time_3': ['16:30', ''],
                'Booking_Duration_3': [1.0, ''],
            })
            
            journey_df.to_excel(writer, sheet_name='Provider_Journey', index=False)
            
            # Instructions Sheet
            instructions = pd.DataFrame({
                'Instructions': [
                    'PROVIDER JOURNEY TEMPLATE INSTRUCTIONS',
                    '',
                    '1. PROVIDER DETAILS:',
                    '   - Provider_ID: Unique identifier for the provider',
                    '   - Provider_Start_Location: Where the provider starts their journey',
                    '   - Provider_Travel_Type: Car, Van, Public Transport, or Car and Public Transport',
                    '   - Provider_Travel_Time_Cost_Per_Hour: Hourly rate for travel time (number only, no £ symbol)',
                    '   - Provider_Mileage_Cost_Per_Mile: Cost per mile (number only, no £ symbol) - use 0 for public transport',
                    '   - Parking_Paid: YES if parking costs are covered, NO if not',
                    '',
                    '2. BOOKING DETAILS:',
                    '   - Each booking needs 3 columns: Location, Appointment Time, and Duration',
                    '   - Add bookings in chronological order',
                    '   - Location: Full address including postcode',
                    '   - Appointment Time: 24-hour format (HH:MM)',
                    '   - Duration: Service duration in hours (number only, e.g., 1.5 for 1 hour 30 minutes)',
                    '   - Leave cells empty if fewer bookings than columns',
                    '',
                    '3. ADDING MORE BOOKINGS:',
                    '   - Add new columns following the pattern:',
                    '   - Booking_Location_4, Booking_Appointment_Time_4, Booking_Duration_4',
                    '   - Booking_Location_5, Booking_Appointment_Time_5, Booking_Duration_5',
                    '   - And so on...',
                    '',
                    '4. IMPORTANT FORMATTING NOTES:',
                    '   ⚠️ DO NOT use currency symbols (£, $) in cost fields - numbers only',
                    '   ⚠️ Use decimal numbers for costs (15.00 not £15.00)',
                    '   ⚠️ Duration should be decimal hours (1.5 not 1h 30m)',
                    '   - One row per provider journey',
                    '   - Times in 24-hour format (09:00, 14:30, etc.)',
                    '   - Full addresses with postcodes for accurate routing',
                    '   - Save as .xlsx format before uploading',
                ]
            })
            instructions.to_excel(writer, sheet_name='Instructions', index=False)
            
            # Format the workbook
            workbook = writer.book
            
            # Add formats
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1,
                'text_wrap': True,
                'valign': 'vcenter'
            })
            
            # Format the journey sheet
            journey_sheet = writer.sheets['Provider_Journey']
            
            # Set header row height and format
            journey_sheet.set_row(0, 30, header_format)
            
            # Set column widths
            journey_sheet.set_column('A:A', 12)  # Provider ID
            journey_sheet.set_column('B:B', 25)  # Start Location
            journey_sheet.set_column('C:C', 15)  # Travel Type
            journey_sheet.set_column('D:E', 12)  # Cost columns
            journey_sheet.set_column('F:F', 10)  # Parking Paid
            
            # Booking columns (3 per booking)
            for i in range(10):  # Support up to 10 bookings
                location_col = 6 + (i * 3)
                time_col = 7 + (i * 3)
                duration_col = 8 + (i * 3)
                
                journey_sheet.set_column(location_col, location_col, 30)  # Location
                journey_sheet.set_column(time_col, time_col, 12)  # Time
                journey_sheet.set_column(duration_col, duration_col, 10)  # Duration
        
        return output.getvalue()
    
    @staticmethod
    def parse_provider_journey_excel(file_content: bytes) -> Dict:
        """Parse provider journey Excel file with new format"""
        try:
            excel_file = pd.ExcelFile(io.BytesIO(file_content))
            
            # Read the main journey sheet
            journey_df = pd.read_excel(excel_file, sheet_name='Provider_Journey')
            
            # Process each row as a separate provider journey
            all_journeys = []
            
            for _, row in journey_df.iterrows():
                # Helper function to parse currency values
                def parse_currency(value):
                    """Parse currency string to float"""
                    if pd.isna(value):
                        return 0.0
                    if isinstance(value, (int, float)):
                        return float(value)
                    # Remove currency symbols and convert to float
                    value_str = str(value).replace('£', '').replace(',', '').strip()
                    try:
                        return float(value_str)
                    except:
                        return 0.0
                
                # Extract provider details
                provider_data = {
                    'provider_id': str(row['Provider_ID']),
                    'start_location': str(row['Provider_Start_Location']),
                    'travel_mode': str(row['Provider_Travel_Type']),
                    'travel_time_cost_per_hour': parse_currency(row.get('Provider_Travel_Time_Cost_Per_Hour', 15.00)),
                    'mileage_cost_per_mile': parse_currency(row.get('Provider_Mileage_Cost_Per_Mile', 0.45)),
                    'parking_paid': str(row.get('Parking_Paid', 'NO')).upper() == 'YES'
                }
                
                # Extract bookings
                bookings = []
                booking_num = 1
                
                while True:
                    # Check if booking columns exist
                    location_col = f'Booking_Location_{booking_num}'
                    time_col = f'Booking_Appointment_Time_{booking_num}'
                    duration_col = f'Booking_Duration_{booking_num}'
                    
                    if location_col not in row or pd.isna(row[location_col]) or str(row[location_col]).strip() == '':
                        break
                    
                    # Parse duration - handle both numeric and string formats
                    duration_value = row.get(duration_col, 1.0)
                    if isinstance(duration_value, str):
                        # Remove any non-numeric characters except decimal point
                        duration_str = ''.join(c for c in duration_value if c.isdigit() or c == '.')
                        try:
                            duration = float(duration_str) if duration_str else 1.0
                        except:
                            duration = 1.0
                    else:
                        duration = float(duration_value) if not pd.isna(duration_value) else 1.0
                    
                    booking = {
                        'booking_id': f'B{booking_num:03d}',
                        'address': str(row[location_col]),
                        'start_time': str(row.get(time_col, '09:00')),
                        'duration_hours': duration,
                        'date': datetime.now().strftime('%Y-%m-%d'),  # Use today's date as default
                        'service_type': 'service'
                    }
                    bookings.append(booking)
                    booking_num += 1
                
                provider_data['bookings'] = bookings
                all_journeys.append(provider_data)
            
            # For now, return the first journey (can be extended to handle multiple)
            if all_journeys:
                return all_journeys[0]
            else:
                raise ValueError("No valid journey data found in Excel file")
            
        except Exception as e:
            raise ValueError(f"Error parsing Excel file: {str(e)}")
    
    @staticmethod
    def parse_planning_files(bookings_data: bytes, providers_data: bytes) -> List[Booking]:
        """Parse Excel files and return bookings with matched providers"""
        
        # Read providers
        providers_df = pd.read_excel(io.BytesIO(providers_data))
        all_providers = []
        
        for _, row in providers_df.iterrows():
            provider = Provider(
                id=str(row.get('ProviderID', '')),
                address=str(row.get('ProviderAddress', '')),
                postcode=''
            )
            provider.name = str(row.get('ProviderName', provider.id))
            provider.service_types = str(row.get('ServiceTypes', 'All'))
            provider.travel_mode = str(row.get('TravelMode', 'Car'))
            provider.service_cost = float(row.get('ServiceCost', 50.00))  # Flat service cost
            provider.travel_time_rate = float(row.get('TravelTimeRate', 15.00))  # Travel time rate
            provider.mileage_rate = float(row.get('MileageRate', 0.45))
            
            # For backward compatibility
            provider.hourly_rate = float(row.get('HourlyRate', provider.service_cost))
            
            all_providers.append(provider)
        
        # Read bookings
        bookings_df = pd.read_excel(io.BytesIO(bookings_data))
        bookings = []
        
        for _, row in bookings_df.iterrows():
            booking_id = str(row.get('BookingID', ''))
            address = str(row.get('CustomerAddress', ''))
            service_type = str(row.get('ServiceType', 'General'))
            
            if not booking_id or not address:
                continue
            
            # Match providers based on service type
            matched_providers = []
            for provider in all_providers:
                # Check if provider offers this service type
                provider_services = provider.service_types.split(',')
                provider_services = [s.strip() for s in provider_services]
                
                # Match if provider has 'All' or the specific service type
                if 'All' in provider_services or service_type in provider_services:
                    matched_providers.append(provider)
            
            # If no providers matched, add all providers as fallback
            if not matched_providers:
                print(f"Warning: No providers matched for {service_type}, using all providers")
                matched_providers = all_providers
            
            booking = Booking(
                booking_id=booking_id,
                customer_address=address,
                service_date=str(row.get('ServiceDate', '')),
                service_time=str(row.get('ServiceTime', '')),
                providers=matched_providers,
                booking_type='service'
            )
            booking.service_type = service_type
            booking.duration = float(row.get('Duration', 2.0))
            
            bookings.append(booking)
        
        return bookings
    
    @staticmethod
    def create_results_excel(results, report_type: str = 'planning') -> bytes:
        """Create Excel report with results"""
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            if report_type == 'planning':
                # Results sheet for planning
                data = []
                for result in results:
                    booking = result['booking']
                    best = result['best_provider']
                    
                    if best:
                        data.append({
                            'Booking_ID': booking.booking_id,
                            'Customer_Address': booking.customer_address,
                            'Service_Date': booking.service_date,
                            'Service_Time': booking.service_time,
                            'Service_Type': booking.service_type,
                            'Best_Provider': best['provider'].name,
                            'Provider_Address': best['provider'].address,
                            'Distance_Miles': round(best['distance'], 1),
                            'Travel_Minutes': round(best['duration'], 0),
                            'Travel_Cost': round(best['travel_cost'], 2),
                            'Service_Cost': round(best['service_cost'], 2),
                            'Total_Cost': round(best['total_cost'], 2)
                        })
                    else:
                        data.append({
                            'Booking_ID': booking.booking_id,
                            'Customer_Address': booking.customer_address,
                            'Service_Date': booking.service_date,
                            'Service_Time': booking.service_time,
                            'Service_Type': booking.service_type,
                            'Best_Provider': 'No Match',
                            'Provider_Address': '',
                            'Distance_Miles': 0,
                            'Travel_Minutes': 0,
                            'Travel_Cost': 0,
                            'Service_Cost': 0,
                            'Total_Cost': 0
                        })
                
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name='Results', index=False)
            
            else:  # journey report
                # Summary sheet
                summary_data = {
                    'Metric': ['Total Distance', 'Total Duration', 'Total Cost', 'Number of Stops'],
                    'Value': [
                        f"{results.get('total_distance_miles', 0)} miles",
                        f"{results.get('total_duration_minutes', 0)} minutes",
                        f"£{results.get('total_cost', 0):.2f}",
                        len(results.get('journey_legs', []))
                    ]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Journey legs
                if 'journey_legs' in results:
                    legs_data = []
                    for leg in results['journey_legs']:
                        legs_data.append({
                            'Booking ID': leg['booking_id'],
                            'From': leg['from'],
                            'To': leg['to'],
                            'Distance (miles)': leg['distance'],
                            'Duration (minutes)': leg['duration'],
                            'Cost (£)': leg['cost']
                        })
                    
                    legs_df = pd.DataFrame(legs_data)
                    legs_df.to_excel(writer, sheet_name='Journey_Details', index=False)
                
                # Cost breakdown
                if 'cost_breakdown' in results:
                    breakdown_data = []
                    for category, amount in results['cost_breakdown'].items():
                        breakdown_data.append({
                            'Category': category.replace('_', ' ').title(),
                            'Amount (£)': amount
                        })
                    
                    breakdown_df = pd.DataFrame(breakdown_data)
                    breakdown_df.to_excel(writer, sheet_name='Cost_Breakdown', index=False)
            
            # Format
            workbook = writer.book
            header_format = workbook.add_format({'bold': True, 'bg_color': '#4472C4', 'font_color': 'white'})
            
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                worksheet.set_row(0, 20, header_format)
                
                # Auto-fit columns
                if sheet_name == 'Results':
                    worksheet.set_column('A:A', 12)  # Booking ID
                    worksheet.set_column('B:B', 35)  # Customer Address
                    worksheet.set_column('C:E', 12)  # Dates, Times
                    worksheet.set_column('F:F', 15)  # Provider
                    worksheet.set_column('G:G', 25)  # Provider Address
                    worksheet.set_column('H:L', 12)  # Numbers
                else:
                    worksheet.set_column('A:Z', 15)
        
        return output.getvalue()