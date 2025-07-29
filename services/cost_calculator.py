from typing import List, Dict, Optional
from models.booking import Booking, Provider
from services.maps_service import MapsService
from services.uk_transport import UKTransportService
from datetime import datetime, timedelta

class CostCalculator:
    """Calculate travel and service costs with flat service rates"""
    
    def __init__(self):
        self.maps_service = MapsService()
        self.uk_transport = UKTransportService()
    
    def calculate_best_provider(self, booking: Booking) -> Dict:
        """Find the best provider for a booking based on total cost"""
        
        best_provider = None
        min_cost = float('inf')
        best_data = None
        all_provider_costs = []
        
        # Debug: log number of providers
        print(f"Booking {booking.booking_id}: Evaluating {len(booking.providers)} providers")
        
        for provider in booking.providers:
            # Calculate costs for this provider
            cost_data = self.calculate_provider_cost(booking, provider)
            
            if cost_data:
                all_provider_costs.append({
                    'provider_name': provider.name,
                    'provider_id': provider.id,
                    'total_cost': cost_data['total_cost'],
                    'distance': cost_data['distance'],
                    'duration': cost_data['duration'],
                    'travel_cost': cost_data['travel_cost'],
                    'service_cost': cost_data['service_cost'],
                    'available': cost_data['is_available']
                })
                
                # Only consider available providers
                if cost_data['is_available'] and cost_data['total_cost'] < min_cost:
                    min_cost = cost_data['total_cost']
                    best_provider = provider
                    best_data = cost_data
        
        # If no available providers, pick the cheapest regardless
        if not best_data and all_provider_costs:
            print(f"Warning: No available providers for {booking.booking_id}, selecting cheapest")
            best_data = min((cd for cd in [self.calculate_provider_cost(booking, p) for p in booking.providers] if cd), 
                           key=lambda x: x['total_cost'])
        
        # Add all provider costs to best_data for comparison
        if best_data:
            best_data['all_providers'] = all_provider_costs
            best_data['total_providers_evaluated'] = len(booking.providers)
        
        return best_data
    
    def calculate_provider_cost(self, booking: Booking, provider: Provider) -> Optional[Dict]:
        """Calculate total cost for a specific provider with detailed travel costs"""
        
        # Get route information
        route_info = self.maps_service.get_route_with_directions(
            provider.address,
            booking.customer_address
        )
        
        if not route_info['success']:
            return None
        
        distance = route_info['distance_miles']
        duration = route_info['duration_minutes']
        
        # Get provider rates (from the file)
        service_cost = getattr(provider, 'service_cost', 50.00)  # Flat service cost
        travel_time_rate = getattr(provider, 'travel_time_rate', 15.00)  # Per hour for travel
        mileage_rate = getattr(provider, 'mileage_rate', 0.45)  # Per mile
        travel_mode = getattr(provider, 'travel_mode', 'Car')
        
        # Debug: Print rates being used
        print(f"Provider {provider.name}: Service Cost: £{service_cost} (flat), Travel Rate: £{travel_time_rate}/hr, Mileage: £{mileage_rate}/mi, Mode: {travel_mode}")
        
        # Calculate detailed travel costs
        travel_breakdown = {}
        
        if travel_mode in ['Car', 'Van']:
            # 1. Mileage cost (round trip) - covers fuel and vehicle wear
            mileage_cost = round(distance * 2 * mileage_rate, 2)
            travel_breakdown['mileage'] = mileage_cost
            
            # 2. Parking costs at customer location
            service_duration = getattr(booking, 'duration', 2.0)
            parking = self.uk_transport.get_parking_costs(
                booking.customer_address, 
                service_duration
            )
            if parking['success'] and parking['total_cost'] > 0:
                travel_breakdown['parking'] = parking['total_cost']
            
            # 3. Congestion charges (if applicable)
            congestion = self.uk_transport.get_congestion_charge(booking.customer_address)
            if congestion['charge'] > 0:
                travel_breakdown['congestion_charge'] = congestion['charge']
                travel_breakdown['congestion_zone'] = congestion.get('name', 'Charge Zone')
            
            # 4. Toll roads (if any on the route)
            tolls = self.uk_transport.check_toll_roads(
                provider.address,
                booking.customer_address
            )
            if tolls:
                toll_cost = sum(toll['car_charge'] if travel_mode == 'Car' 
                              else toll['van_charge'] for toll in tolls)
                travel_breakdown['tolls'] = toll_cost
                travel_breakdown['toll_roads'] = [toll['name'] for toll in tolls]
        
        else:  # Public Transport
            # Get detailed public transport costs
            public_costs = self.uk_transport.estimate_public_transport_cost(
                provider.address,
                booking.customer_address,
                distance
            )
            
            if 'train' in public_costs:
                # Choose between train and coach based on recommendation
                recommended = public_costs.get('recommended', 'train')
                if recommended == 'train':
                    travel_breakdown['public_transport'] = public_costs['train']['cost'] * 2  # Round trip
                    travel_breakdown['transport_type'] = 'Train'
                    travel_breakdown['is_peak'] = public_costs['train'].get('is_peak', False)
                else:
                    travel_breakdown['public_transport'] = public_costs['coach']['cost'] * 2
                    travel_breakdown['transport_type'] = 'Coach'
            else:
                # Fallback estimate
                travel_breakdown['public_transport'] = round(distance * 2 * 0.20, 2)
                travel_breakdown['transport_type'] = 'Bus (estimated)'
        
        # 5. Travel time compensation (round trip)
        travel_time_hours = (duration * 2) / 60  # Convert to hours and multiply by 2 for round trip
        travel_time_cost = round(travel_time_hours * travel_time_rate, 2)
        travel_breakdown['travel_time'] = travel_time_cost
        
        # Calculate total travel cost
        travel_cost = sum(v for k, v in travel_breakdown.items() if isinstance(v, (int, float)))
        
        # Total cost = Travel + Service (flat rate)
        total_cost = round(travel_cost + service_cost, 2)
        
        # Check provider availability
        is_available = self._check_provider_availability(provider, booking)
        
        # Create detailed route information
        route_details = {
            'distance_miles': distance,
            'duration_minutes': duration,
            'route_info': route_info,
            'traffic_conditions': self._estimate_traffic(booking.service_time),
            'weather_impact': 'Normal',  # Could be enhanced with weather API
        }
        
        return {
            'provider': provider,
            'distance': distance,
            'duration': duration,
            'travel_breakdown': travel_breakdown,
            'travel_cost': round(travel_cost, 2),
            'service_cost': service_cost,
            'total_cost': total_cost,
            'route_info': route_info,
            'route_details': route_details,
            'is_available': is_available,
            'cost_details': {
                'service_cost': service_cost,
                'travel_time_rate': travel_time_rate,
                'mileage_rate': mileage_rate,
                'travel_mode': travel_mode,
                'round_trip_distance': distance * 2,
                'round_trip_duration': duration * 2,
                'service_duration': getattr(booking, 'duration', 2.0)
            }
        }
    
    def _check_provider_availability(self, provider: Provider, booking: Booking) -> bool:
        """Check if provider is available for the booking time"""
        if not provider.other_bookings:
            return True
        
        # Parse booking time
        try:
            booking_datetime = datetime.strptime(
                f"{booking.service_date} {booking.service_time}", 
                "%Y-%m-%d %H:%M"
            )
            booking_end = booking_datetime + timedelta(hours=getattr(booking, 'duration', 2.0))
        except:
            return True  # If can't parse, assume available
        
        # Check conflicts with other bookings
        for other in provider.other_bookings:
            try:
                other_start = datetime.strptime(
                    f"{booking.service_date} {other.start_time}", 
                    "%Y-%m-%d %H:%M"
                )
                other_end = other_start + timedelta(hours=other.duration_hours)
                
                # Check for overlap
                if (booking_datetime < other_end and booking_end > other_start):
                    return False
            except:
                continue
        
        return True
    
    def _estimate_traffic(self, service_time: str) -> str:
        """Estimate traffic conditions based on time"""
        try:
            hour = int(service_time.split(':')[0])
            if 7 <= hour <= 9 or 17 <= hour <= 19:
                return "Heavy (Rush Hour)"
            elif 10 <= hour <= 16:
                return "Moderate"
            else:
                return "Light"
        except:
            return "Unknown"
    
    def calculate_all_bookings(self, bookings: List[Booking]) -> List[Dict]:
        """Calculate best provider for all bookings with optimization"""
        
        results = []
        assigned_providers = {}  # Track provider assignments
        
        # Sort bookings by priority (if available) or by time
        sorted_bookings = sorted(bookings, 
                               key=lambda b: (getattr(b, 'priority', 'normal') != 'high',
                                            b.service_date, 
                                            b.service_time))
        
        for booking in sorted_bookings:
            best_provider_data = self.calculate_best_provider(booking)
            
            # If provider already assigned nearby, add travel cost savings
            if best_provider_data and best_provider_data['provider'].id in assigned_providers:
                last_booking = assigned_providers[best_provider_data['provider'].id]
                # Check if this booking is on the same day and nearby
                if (booking.service_date == last_booking['date'] and 
                    self._are_bookings_nearby(last_booking['address'], booking.customer_address)):
                    # Reduce travel cost as provider is already in the area
                    best_provider_data['travel_cost'] *= 0.5
                    best_provider_data['total_cost'] = (
                        best_provider_data['travel_cost'] + 
                        best_provider_data['service_cost']
                    )
                    best_provider_data['optimized'] = True
            
            # Track assignment
            if best_provider_data:
                assigned_providers[best_provider_data['provider'].id] = {
                    'date': booking.service_date,
                    'address': booking.customer_address
                }
            
            results.append({
                'booking': booking,
                'best_provider': best_provider_data
            })
        
        return results
    
    def _are_bookings_nearby(self, address1: str, address2: str) -> bool:
        """Check if two addresses are nearby (within 5 miles)"""
        route = self.maps_service.get_distance_duration(address1, address2)
        if route['success']:
            return route['distance_miles'] < 5
        return False