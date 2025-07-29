from typing import Dict, List, Optional
from datetime import datetime

class UKTransportService:
    """Service for UK-specific transport costs and information"""
    
    def __init__(self):
        # Current UK costs (2024)
        self.fuel_price_per_litre = 1.50  # Average UK petrol price
        self.average_mpg = 40  # Average car fuel efficiency
        
        # Congestion and Clean Air Zone charges
        self.congestion_charges = {
            'london': {'charge': 15.00, 'name': 'Congestion Charge'},
            'london_ulez': {'charge': 12.50, 'name': 'ULEZ'},
            'birmingham': {'charge': 8.00, 'name': 'Clean Air Zone'},
            'bath': {'charge': 9.00, 'name': 'Clean Air Zone'},
            'bristol': {'charge': 9.00, 'name': 'Clean Air Zone'},
            'portsmouth': {'charge': 0, 'name': 'No charge'}
        }
        
        # Toll roads
        self.toll_roads = {
            'M6 Toll': {
                'locations': ['Birmingham', 'Wolverhampton', 'Stoke'],
                'car_charge': 7.10,
                'van_charge': 11.90
            },
            'Dartford Crossing': {
                'locations': ['Dartford', 'Thurrock'],
                'car_charge': 2.50,
                'van_charge': 3.00
            }
        }
        
        # Public transport estimates
        self.train_cost_per_mile = {
            'peak': 0.35,      # Peak time (6:30-9:30, 17:00-19:00)
            'off_peak': 0.20,  # Off-peak
            'advance': 0.15    # Advance booking
        }
        
        self.bus_cost_per_mile = 0.12  # National Express type coaches
        
    def calculate_fuel_cost(self, distance_miles: float) -> float:
        """Calculate fuel cost for journey"""
        gallons_needed = distance_miles / self.average_mpg
        litres_needed = gallons_needed * 4.54609  # Convert to litres
        return round(litres_needed * self.fuel_price_per_litre, 2)
    
    def get_congestion_charge(self, location: str) -> Dict:
        """Get congestion/CAZ charge for location"""
        location_lower = location.lower()
        
        # Check for London
        if any(area in location_lower for area in ['london', 'westminster', 'city of london']):
            # Central London has both charges
            if any(area in location_lower for area in ['ec', 'wc', 'sw1', 'se1', 'w1']):
                return {
                    'charge': 15.00 + 12.50,  # Congestion + ULEZ
                    'breakdown': {
                        'congestion': 15.00,
                        'ulez': 12.50
                    },
                    'name': 'London Congestion + ULEZ'
                }
            else:
                return self.congestion_charges['london_ulez']
        
        # Check other cities
        for city, charge_info in self.congestion_charges.items():
            if city in location_lower:
                return charge_info
        
        return {'charge': 0, 'name': 'No congestion charge'}
    
    def check_toll_roads(self, origin: str, destination: str) -> List[Dict]:
        """Check if route likely includes toll roads"""
        tolls = []
        route_text = f"{origin} {destination}".lower()
        
        for toll_name, toll_info in self.toll_roads.items():
            for location in toll_info['locations']:
                if location.lower() in route_text:
                    tolls.append({
                        'name': toll_name,
                        'car_charge': toll_info['car_charge'],
                        'van_charge': toll_info['van_charge']
                    })
                    break
        
        return tolls
    
    def get_parking_costs(self, location: str, duration_hours: float) -> Dict:
        """Estimate parking costs by location"""
        location_lower = location.lower()
        
        # City center parking rates (per hour)
        parking_rates = {
            'london': 6.00,
            'westminster': 7.00,
            'birmingham': 3.50,
            'manchester': 3.00,
            'leeds': 3.00,
            'bristol': 3.00,
            'southampton': 2.50,
            'portsmouth': 2.50,
            'hospital': 3.00,  # NHS hospitals
            'airport': 5.00,
            'default': 2.00
        }
        
        # Find applicable rate
        hourly_rate = parking_rates['default']
        for area, rate in parking_rates.items():
            if area in location_lower:
                hourly_rate = rate
                break
        
        # Calculate with daily caps
        daily_cap = hourly_rate * 8  # Most places cap at 8 hours
        if duration_hours >= 8:
            total_cost = daily_cap
        else:
            total_cost = round(hourly_rate * duration_hours, 2)
        
        return {
            'success': True,
            'hourly_rate': hourly_rate,
            'total_cost': total_cost,
            'daily_cap': daily_cap
        }
    
    def estimate_public_transport_cost(self, origin: str, destination: str, 
                                     distance_miles: float) -> Dict:
        """Estimate public transport costs"""
        origin_lower = origin.lower()
        destination_lower = destination.lower()
        
        # London Transport (TfL)
        if 'london' in origin_lower and 'london' in destination_lower:
            return {
                'type': 'London Transport',
                'options': {
                    'tube_bus': 2.80,  # Single journey cap
                    'daily_cap': 8.10  # Zone 1-2 daily cap
                },
                'duration_minutes': 45  # Average
            }
        
        # National Rail estimates
        is_peak = self._is_peak_time()
        train_rate = self.train_cost_per_mile['peak' if is_peak else 'off_peak']
        
        # Major routes have specific pricing
        route_key = self._get_route_key(origin, destination)
        specific_fares = {
            ('london', 'birmingham'): {'peak': 65, 'off_peak': 25},
            ('london', 'manchester'): {'peak': 85, 'off_peak': 35},
            ('london', 'southampton'): {'peak': 55, 'off_peak': 28},
            ('birmingham', 'manchester'): {'peak': 45, 'off_peak': 20}
        }
        
        if route_key in specific_fares:
            train_cost = specific_fares[route_key]['peak' if is_peak else 'off_peak']
        else:
            train_cost = distance_miles * train_rate
        
        # Coach option
        coach_cost = distance_miles * self.bus_cost_per_mile
        
        return {
            'train': {
                'cost': round(train_cost, 2),
                'is_peak': is_peak,
                'duration_minutes': distance_miles * 1.5  # Rough estimate
            },
            'coach': {
                'cost': round(coach_cost, 2),
                'duration_minutes': distance_miles * 2.5  # Coaches are slower
            },
            'recommended': 'train' if distance_miles < 100 else 'coach'
        }
    
    def get_total_driving_cost(self, distance_miles: float, origin: str, 
                              destination: str, duration_hours: float) -> Dict:
        """Calculate total driving cost including all factors"""
        # Fuel
        fuel_cost = self.calculate_fuel_cost(distance_miles)
        
        # Parking
        parking = self.get_parking_costs(destination, duration_hours)
        parking_cost = parking['total_cost']
        
        # Congestion charges
        congestion = self.get_congestion_charge(destination)
        
        # Tolls
        tolls = self.check_toll_roads(origin, destination)
        toll_cost = sum(toll['car_charge'] for toll in tolls)
        
        total = fuel_cost + parking_cost + congestion['charge'] + toll_cost
        
        return {
            'total': round(total, 2),
            'breakdown': {
                'fuel': fuel_cost,
                'parking': parking_cost,
                'congestion_charge': congestion['charge'],
                'tolls': toll_cost
            },
            'details': {
                'congestion_info': congestion,
                'toll_roads': tolls,
                'parking_info': parking
            }
        }
    
    def _is_peak_time(self, time: Optional[datetime] = None) -> bool:
        """Check if current time is peak hours"""
        if not time:
            time = datetime.now()
        
        # Peak: Mon-Fri 6:30-9:30 and 17:00-19:00
        if time.weekday() < 5:  # Monday to Friday
            hour = time.hour
            if (6 <= hour < 10) or (17 <= hour < 19):
                return True
        return False
    
    def _get_route_key(self, origin: str, destination: str) -> tuple:
        """Get standardized route key for fare lookup"""
        cities = ['london', 'birmingham', 'manchester', 'southampton', 'leeds', 'bristol']
        
        origin_city = None
        dest_city = None
        
        for city in cities:
            if city in origin.lower():
                origin_city = city
            if city in destination.lower():
                dest_city = city
        
        if origin_city and dest_city:
            # Return in alphabetical order for consistency
            return tuple(sorted([origin_city, dest_city]))
        
        return (None, None)