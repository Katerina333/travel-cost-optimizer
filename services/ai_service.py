import google.generativeai as genai
from typing import Dict, List, Optional
import json
from config import GEMINI_API_KEY

class AIService:
    """AI service for smart cost optimization (optional)"""
    
    def __init__(self):
        if GEMINI_API_KEY:
            try:
                genai.configure(api_key=GEMINI_API_KEY)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.enabled = True
                print("✅ Gemini AI initialized successfully")
            except Exception as e:
                print(f"❌ Gemini initialization error: {e}")
                self.model = None
                self.enabled = False
        else:
            self.model = None
            self.enabled = False
    
    def optimize_provider_selection(self, booking, travel_costs) -> Dict:
        """Smart provider recommendation considering all factors"""
        if not self.enabled or not travel_costs:
            return {"best_provider": travel_costs[0].provider_id if travel_costs else None}
        
        try:
            # Build context
            providers_info = []
            for cost in travel_costs:
                providers_info.append({
                    "id": cost.provider_id,
                    "travel_cost": cost.travel_cost,
                    "distance": cost.distance_miles,
                    "duration": cost.duration_minutes
                })
            
            prompt = f"""
            Select the best service provider considering:
            - Service location: {booking.customer_address}
            - Service date: {booking.service_date}
            - Providers: {json.dumps(providers_info)}
            
            Consider:
            1. Total cost (not just cheapest)
            2. Travel time and reliability
            3. Environmental impact
            4. Peak traffic times
            5. Provider availability
            
            Return JSON:
            {{
                "best_provider": "provider_id",
                "reasoning": "explanation",
                "alternative": "second_best_provider_id",
                "cost_saving_tips": ["tip1", "tip2"]
            }}
            """
            
            response = self.model.generate_content(prompt)
            text = response.text
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0]
            elif '```' in text:
                text = text.split('```')[1].split('```')[0]
                
            return json.loads(text.strip())
            
        except Exception as e:
            print(f"AI optimization error: {e}")
            return {"best_provider": travel_costs[0].provider_id if travel_costs else None}
    
    def analyze_travel_options(self, origin: str, destination: str, 
                             distance_miles: float, time_of_day: str = "09:00") -> Dict:
        """AI analysis of best travel options"""
        if not self.enabled:
            return self._get_default_analysis(distance_miles)
        
        try:
            prompt = f"""
            Analyze travel options for UK journey:
            From: {origin}
            To: {destination}
            Distance: {distance_miles} miles
            Travel time: {time_of_day}
            
            Consider UK-specific factors:
            1. Public transport availability
            2. Traffic patterns
            3. Parking costs
            4. Environmental impact
            
            Provide recommendation in JSON format:
            {{
                "recommendation": "driving or public_transport",
                "reasoning": "why this option is best",
                "estimated_cost": 0.0,
                "tips": ["helpful tips"]
            }}
            """
            
            response = self.model.generate_content(prompt)
            text = response.text
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0]
            elif '```' in text:
                text = text.split('```')[1].split('```')[0]
            
            return json.loads(text.strip())
            
        except Exception as e:
            print(f"AI error: {e}")
            return self._get_default_analysis(distance_miles)
    
    def _get_default_analysis(self, distance_miles: float) -> Dict:
        """Default analysis without AI"""
        return {
            "recommendation": "driving" if distance_miles < 50 else "consider_public_transport",
            "reasoning": "Based on distance",
            "estimated_cost": distance_miles * 0.45,
            "tips": ["Check traffic before departure", "Consider carpooling"]
        }