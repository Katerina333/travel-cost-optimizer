from dataclasses import dataclass, field
from typing import List, Optional, Dict

@dataclass
class OtherBooking:
    """Other bookings for a provider"""
    booking_id: str
    address: str
    start_time: str
    duration_hours: float
    
@dataclass
class Provider:
    """Provider/freelancer information"""
    id: str
    address: str
    postcode: str = ""
    other_bookings: List[OtherBooking] = field(default_factory=list)
    
    # Additional attributes set after creation
    name: Optional[str] = None
    service_types: Optional[str] = None
    services: Optional[str] = None
    specializations: Optional[str] = None
    languages: Optional[str] = None
    gender: Optional[str] = None
    travel_mode: Optional[str] = None
    travel_type: Optional[str] = None
    hourly_rate: Optional[float] = None
    mileage_rate: Optional[float] = None
    travel_time_cost: Optional[float] = None
    mileage_cost: Optional[float] = None
    max_distance: Optional[float] = None

@dataclass
class Booking:
    """Booking/job information"""
    booking_id: str
    customer_address: str
    service_date: str
    service_time: str
    providers: List[Provider]
    booking_type: str = "service"
    
    # Additional attributes
    service_type: Optional[str] = None
    service_required: Optional[str] = None
    specialization_required: Optional[str] = None
    language: Optional[str] = None
    specialty: Optional[str] = None
    gender_preference: Optional[str] = None
    duration: Optional[float] = None
    booking_duration: Optional[float] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    customer_name: Optional[str] = None
    supported_costs: Optional[Dict[str, bool]] = None

@dataclass
class TravelCost:
    """Travel cost result"""
    provider_id: str
    distance_miles: float
    duration_minutes: float
    travel_cost: float
    breakdown: Dict[str, float]
    
    # Optional fields
    ai_recommended: bool = False
    ai_recommendation: Optional[str] = None
    ai_reasoning: Optional[str] = None
    cost_saving_tips: Optional[List[str]] = None
    public_transport_option: Optional[Dict] = None
    
    # Additional provider info
    provider_name: Optional[str] = None
    provider_services: Optional[str] = None
    provider_specializations: Optional[str] = None
    provider_address: Optional[str] = None
    travel_mode: Optional[str] = None
    services: Optional[str] = None
    polyline: Optional[str] = None
    match_score: Optional[int] = None
    match_reasons: Optional[List[str]] = None