from typing import List, Dict
from models.booking import Booking, Provider
from services.maps_service import MapsService

class CostCalculator:
    """Calculate travel and service costs"""
    
    def __init__(self):
        self.maps_service = MapsService()
    
    def calculate_best_provider(self, booking: Booking) -> Dict:
        """Find the best provider for a booking based on total cost"""
        
        best_provider = None
        min_cost = float('inf')
        best_data = None
        
        for provider in booking.providers:
            # Calculate costs for this provider
            cost_data = self.calculate_provider_cost(booking, provider)
            
            if cost_data and cost_data['total_cost'] < min_cost:
                min_cost = cost_data['total_cost']
                best_provider = provider
                best_data = cost_data
        
        return best_data
    
    def calculate_provider_cost(self, booking: Booking, provider: Provider) -> Dict:
        """Calculate total cost for a specific provider"""
        
        # Get route information
        route_info = self.maps_service.get_route_with_directions(
            provider.address,
            booking.customer_address
        )
        
        if not route_info['success']:
            return None
        
        distance = route_info['distance_miles']
        duration = route_info['duration_minutes']
        
        # Get provider rates
        hourly_rate = getattr(provider, 'hourly_rate', 25.00)
        mileage_rate = getattr(provider, 'mileage_rate', 0.45)
        
        # Calculate costs
        # Travel cost (round trip)
        mileage_cost = distance * 2 * mileage_rate
        travel_time_cost = (duration * 2 / 60) * hourly_rate
        travel_cost = mileage_cost + travel_time_cost
        
        # Service cost
        service_duration = getattr(booking, 'duration', 2.0)
        service_cost = service_duration * hourly_rate
        
        # Total cost
        total_cost = travel_cost + service_cost
        
        return {
            'provider': provider,
            'distance': distance,
            'duration': duration,
            'mileage_cost': mileage_cost,
            'travel_time_cost': travel_time_cost,
            'travel_cost': travel_cost,
            'service_cost': service_cost,
            'total_cost': total_cost,
            'route_info': route_info
        }
    
    def calculate_all_bookings(self, bookings: List[Booking]) -> List[Dict]:
        """Calculate best provider for all bookings"""
        
        results = []
        
        for booking in bookings:
            best_provider_data = self.calculate_best_provider(booking)
            results.append({
                'booking': booking,
                'best_provider': best_provider_data
            })
        
        return results