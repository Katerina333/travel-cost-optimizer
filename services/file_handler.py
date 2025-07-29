import json
from models.booking import Booking, Provider, OtherBooking

def parse_booking_file(file_content: str, service_type: str) -> Booking:
    """Parse JSON file into Booking object"""
    try:
        data = json.loads(file_content)
        
        # Parse providers
        providers = []
        for p in data.get('providers', []):
            # Parse other bookings if present
            other_bookings = []
            for ob in p.get('other_bookings', []):
                other_booking = OtherBooking(
                    booking_id=ob.get('booking_id', ''),
                    address=ob.get('address', ''),
                    start_time=ob.get('start_time', ''),
                    duration_hours=ob.get('duration_hours', 0)
                )
                other_bookings.append(other_booking)
            
            provider = Provider(
                id=p.get('id', ''),
                address=p.get('address', p.get('location', '')),
                postcode=p.get('postcode', ''),
                other_bookings=other_bookings
            )
            providers.append(provider)
        
        # Create booking
        booking = Booking(
            booking_id=data.get('booking_id', ''),
            customer_address=data.get('customer_address', ''),
            service_date=data.get('service_date', ''),
            service_time=data.get('service_time', '09:00'),
            providers=providers,
            booking_type=service_type
        )
        
        # Add interpreting fields if present
        if service_type == 'interpreting':
            booking.language = data.get('language', '')
            booking.booking_duration = data.get('booking_duration', 0)
            booking.supported_costs = data.get('supported_costs', {
                'vehicle_mileage': True,
                'travelling_time': True,
                'other_expenses': False
            })
        
        return booking
        
    except Exception as e:
        raise ValueError(f"Error parsing JSON: {str(e)}")

def get_example_json(service_type: str) -> dict:
    """Get example JSON for service type"""
    if service_type == 'plumbing':
        return {
            "booking_id": "B001",
            "customer_address": "123 High Street, Birmingham, B1 1AA",
            "service_date": "2024-03-20",
            "service_time": "14:00",
            "providers": [
                {
                    "id": "P001",
                    "address": "45 Station Road, Birmingham",
                    "postcode": "B2 4QA",
                    "other_bookings": []
                },
                {
                    "id": "P002",
                    "address": "78 London Road, Solihull",
                    "postcode": "B91 1JH",
                    "other_bookings": [
                        {
                            "booking_id": "B099",
                            "address": "56 Park Lane, Birmingham, B3 2RS",
                            "start_time": "10:00",
                            "duration_hours": 2
                        }
                    ]
                }
            ]
        }
    else:  # interpreting
        return {
            "booking_id": "INT001",
            "customer_address": "Princess Anne Hospital, Coxford Road, Southampton, SO165YA",
            "service_date": "2024-03-25",
            "service_time": "09:00",
            "language": "Spanish",
            "booking_duration": 2.5,
            "supported_costs": {
                "vehicle_mileage": True,
                "travelling_time": True,
                "other_expenses": False
            },
            "providers": [
                {
                    "id": "INT_P001",
                    "location": "Portsmouth, PO1 2UP",
                    "other_bookings": [
                        {
                            "booking_id": "INT099",
                            "address": "QA Hospital, Portsmouth, PO6 3LY",
                            "start_time": "13:00",
                            "duration_hours": 2
                        }
                    ]
                },
                {
                    "id": "INT_P002",
                    "location": "Southampton, SO14 3HH",
                    "other_bookings": []
                }
            ]
        }

def get_provider_journey_example() -> dict:
    """Get example JSON for provider journey"""
    return {
        "provider_id": "PROV001",
        "start_location": "Birmingham, B1 1AA",
        "travel_mode": "car",
        "bookings": [
            {
                "booking_id": "B001",
                "address": "123 High Street, Solihull, B91 1AA",
                "date": "2024-03-20",
                "start_time": "09:00",
                "duration_hours": 2.0,
                "service_type": "plumbing"
            },
            {
                "booking_id": "B002",
                "address": "456 Park Lane, Coventry, CV1 2AB",
                "date": "2024-03-20",
                "start_time": "14:00",
                "duration_hours": 1.5,
                "service_type": "plumbing"
            },
            {
                "booking_id": "B003",
                "address": "789 Queen Street, Birmingham, B2 4QZ",
                "date": "2024-03-20",
                "start_time": "16:30",
                "duration_hours": 1.0,
                "service_type": "emergency"
            }
        ]
    }