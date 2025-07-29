import googlemaps
from typing import Dict, Optional, List
from config import GOOGLE_MAPS_API_KEY

class MapsService:
    def __init__(self):
        if GOOGLE_MAPS_API_KEY:
            self.client = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        else:
            self.client = None
    
    def get_route_with_directions(self, origin: str, destination: str) -> Dict:
        """Get complete route information including polyline for map display"""
        if not self.client:
            # Mock data for testing without API key
            return {
                'success': True,
                'distance_miles': 25.5,
                'duration_minutes': 35,
                'polyline': None,
                'bounds': None,
                'start_location': {'lat': 52.4862, 'lng': -1.8904},
                'end_location': {'lat': 52.5062, 'lng': -1.8704}
            }
        
        try:
            # Get directions which includes polyline
            directions = self.client.directions(
                origin=origin,
                destination=destination,
                mode="driving",
                units="imperial"
            )
            
            if directions:
                route = directions[0]
                leg = route['legs'][0]
                
                # Extract route polyline for drawing on map
                polyline = route['overview_polyline']['points']
                
                # Get bounds for map fitting
                bounds = route['bounds']
                
                return {
                    'success': True,
                    'distance_miles': leg['distance']['value'] / 1609.34,
                    'duration_minutes': leg['duration']['value'] / 60,
                    'polyline': polyline,
                    'bounds': bounds,
                    'start_location': leg['start_location'],
                    'end_location': leg['end_location']
                }
            else:
                return {
                    'success': False,
                    'error': 'No route found'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_distance_duration(self, origin: str, destination: str) -> Dict:
        """Get distance and duration between two points"""
        if not self.client:
            # Mock data for testing without API key
            return {
                'success': True,
                'distance_miles': 25.5,
                'duration_minutes': 35
            }
        
        try:
            result = self.client.distance_matrix(
                origins=[origin],
                destinations=[destination],
                mode="driving",
                units="imperial"
            )
            
            if result['rows'][0]['elements'][0]['status'] == 'OK':
                element = result['rows'][0]['elements'][0]
                
                return {
                    'success': True,
                    'distance_miles': element['distance']['value'] / 1609.34,
                    'duration_minutes': element['duration']['value'] / 60
                }
            else:
                return {
                    'success': False,
                    'error': 'Route not found'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def geocode_address(self, address: str) -> Optional[Dict[str, float]]:
        """Convert address to coordinates"""
        if not self.client:
            # Mock coordinates for testing
            return {'lat': 52.4862, 'lng': -1.8904}  # Birmingham
        
        try:
            result = self.client.geocode(address)
            if result:
                location = result[0]['geometry']['location']
                return {'lat': location['lat'], 'lng': location['lng']}
            return None
        except:
            return None
    
    def get_parking_costs(self, destination: str, duration_hours: float) -> Dict:
        """Estimate parking costs for a destination"""
        # Simple estimation based on location
        if any(city in destination.lower() for city in ['london', 'westminster']):
            hourly_rate = 6.00
        elif any(city in destination.lower() for city in ['birmingham', 'manchester', 'leeds']):
            hourly_rate = 3.00
        else:
            hourly_rate = 2.00
        
        total_cost = min(hourly_rate * duration_hours, hourly_rate * 8)  # Daily cap
        
        return {
            'success': True,
            'hourly_rate': hourly_rate,
            'total_cost': round(total_cost, 2)
        }
    
    def get_congestion_charge(self, destination: str) -> Dict:
        """Check if destination has congestion charges"""
        destination_lower = destination.lower()
        
        if 'london' in destination_lower:
            if any(zone in destination_lower for zone in ['ec', 'wc', 'sw1', 'se1']):
                return {'charge': 15.00, 'zone': 'Central London'}
            else:
                return {'charge': 0, 'zone': 'Outside congestion zone'}
        elif 'birmingham' in destination_lower:
            return {'charge': 8.00, 'zone': 'Clean Air Zone'}
        elif 'bath' in destination_lower:
            return {'charge': 9.00, 'zone': 'Clean Air Zone'}
        else:
            return {'charge': 0, 'zone': 'No charge'}