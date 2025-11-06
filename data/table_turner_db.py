"""Enhanced restaurant database with user management and time slot reservations."""
import json
from datetime import datetime, timedelta, time
from typing import Dict, List, Optional

# Restaurant data
RESTAURANTS = [
    {"id": 1, "name": "Spice Garden", "cuisine": "Indian", "location": "Koramangala", "city": "Bangalore"},
    {"id": 2, "name": "Curry House", "cuisine": "Indian", "location": "Indiranagar", "city": "Bangalore"},
    {"id": 3, "name": "Maharaja Palace", "cuisine": "Indian", "location": "MG Road", "city": "Bangalore"},
    {"id": 4, "name": "Bella Italia", "cuisine": "Italian", "location": "Koramangala", "city": "Bangalore"},
    {"id": 5, "name": "Luigi's Kitchen", "cuisine": "Italian", "location": "Brigade Road", "city": "Bangalore"},
    {"id": 6, "name": "Dragon Wok", "cuisine": "Chinese", "location": "Koramangala", "city": "Bangalore"},
    {"id": 7, "name": "Golden Chopsticks", "cuisine": "Chinese", "location": "Commercial Street", "city": "Bangalore"},
    {"id": 8, "name": "The Continental", "cuisine": "Continental", "location": "Indiranagar", "city": "Bangalore"},
    {"id": 9, "name": "Taco Fiesta", "cuisine": "Mexican", "location": "Koramangala", "city": "Bangalore"},
    {"id": 10, "name": "Sakura Sushi", "cuisine": "Japanese", "location": "UB City", "city": "Bangalore"},
]

class TableTurnerDatabase:
    """Enhanced database for Table Turner reservation system."""
    
    def __init__(self):
        self.users = {}  # phone_number -> user_data
        self.reservations = []  # List of all reservations
        self.time_slots = self._generate_time_slots()
        self.next_reservation_id = 1000
        
    def _generate_time_slots(self):
        """Generate 30-minute time slots from 11:00 AM to 11:00 PM."""
        slots = []
        start_time = time(11, 0)  # 11:00 AM
        end_time = time(23, 0)    # 11:00 PM
        
        current = datetime.combine(datetime.today(), start_time)
        end = datetime.combine(datetime.today(), end_time)
        
        while current <= end:
            slots.append(current.strftime("%H:%M"))
            current += timedelta(minutes=30)
        
        return slots
    
    def get_current_datetime(self):
        """Get current date and time."""
        return datetime.now()
    
    def parse_relative_date(self, user_input: str, current_date: datetime) -> Optional[str]:
        """Parse relative dates like 'today', 'tomorrow', 'next Saturday'."""
        user_input_lower = user_input.lower()
        
        if "today" in user_input_lower:
            return current_date.strftime("%Y-%m-%d")
        elif "tomorrow" in user_input_lower:
            return (current_date + timedelta(days=1)).strftime("%Y-%m-%d")
        elif "day after tomorrow" in user_input_lower:
            return (current_date + timedelta(days=2)).strftime("%Y-%m-%d")
        elif "next" in user_input_lower:
            # Handle "next Monday", "next Saturday", etc.
            days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            for i, day in enumerate(days_of_week):
                if day in user_input_lower:
                    current_weekday = current_date.weekday()
                    days_ahead = (i - current_weekday) % 7
                    if days_ahead == 0:
                        days_ahead = 7
                    target_date = current_date + timedelta(days=days_ahead)
                    return target_date.strftime("%Y-%m-%d")
        
        return None
    
    def validate_booking_advance(self, booking_date: str) -> tuple[bool, str]:
        """Validate that booking is within 3 days from today."""
        current_date = datetime.now().date()
        try:
            target_date = datetime.strptime(booking_date, "%Y-%m-%d").date()
            
            # Check if date is in the past
            if target_date < current_date:
                return False, "Cannot book for past dates"
            
            # Check if date is within 3 days
            days_diff = (target_date - current_date).days
            if days_diff > 3:
                return False, f"Bookings can only be made up to 3 days in advance. Please choose a date within {3 - days_diff} days."
            
            return True, "Valid date"
        except ValueError:
            return False, "Invalid date format"
    
    def check_user_exists(self, phone_number: str) -> bool:
        """Check if user exists in database."""
        return phone_number in self.users
    
    def get_user(self, phone_number: str) -> Optional[Dict]:
        """Get user details."""
        return self.users.get(phone_number)
    
    def create_user(self, phone_number: str, name: str) -> Dict:
        """Create new user."""
        user = {
            "phone_number": phone_number,
            "name": name,
            "created_at": datetime.now().isoformat(),
            "total_reservations": 0
        }
        self.users[phone_number] = user
        return user
    
    def get_user_reservations(self, phone_number: str, limit: int = 5) -> List[Dict]:
        """Get recent reservations for a user."""
        user_reservations = [
            r for r in self.reservations 
            if r.get("phone_number") == phone_number and r.get("status") != "cancelled"
        ]
        # Sort by date descending
        user_reservations.sort(
            key=lambda x: datetime.fromisoformat(x.get("created_at", "2000-01-01")),
            reverse=True
        )
        return user_reservations[:limit]
    
    def get_available_slots(self, restaurant_id: int, date: str, party_size: int) -> List[Dict]:
        """Get available time slots for a restaurant on a specific date."""
        # Get all existing reservations for this restaurant and date
        existing_reservations = [
            r for r in self.reservations
            if r["restaurant_id"] == restaurant_id
            and r["date"] == date
            and r["status"] == "confirmed"
        ]
        
        available_slots = []
        
        # Check each time slot
        for time_slot in self.time_slots:
            # For each table size (2, 4, 6)
            for table_size in [2, 4, 6]:
                # Check if this table size can accommodate party
                if table_size >= party_size:
                    # Check if this slot is already booked
                    slot_booked = any(
                        r["time"] == time_slot and r["table_size"] == table_size
                        for r in existing_reservations
                    )
                    
                    if not slot_booked:
                        available_slots.append({
                            "time": time_slot,
                            "table_size": table_size,
                            "available": True
                        })
                        break  # Found an available table for this time slot
        
        return available_slots
    
    def find_nearest_available_slot(self, restaurant_id: int, date: str, 
                                    requested_time: str, party_size: int) -> Optional[Dict]:
        """Find the nearest available slot after requested time."""
        available_slots = self.get_available_slots(restaurant_id, date, party_size)
        
        # Filter slots that are after the requested time
        requested_time_obj = datetime.strptime(requested_time, "%H:%M").time()
        future_slots = [
            slot for slot in available_slots
            if datetime.strptime(slot["time"], "%H:%M").time() >= requested_time_obj
        ]
        
        return future_slots[0] if future_slots else None
    
    def create_reservation(self, restaurant_id: int, phone_number: str, name: str,
                          date: str, time_slot: str, party_size: int, 
                          table_size: int) -> tuple[Optional[Dict], str]:
        """Create a new reservation."""
        # Validate date is within 3 days
        is_valid, message = self.validate_booking_advance(date)
        if not is_valid:
            return None, message
        
        # Check if slot is still available
        existing = any(
            r["restaurant_id"] == restaurant_id
            and r["date"] == date
            and r["time"] == time_slot
            and r["table_size"] == table_size
            and r["status"] == "confirmed"
            for r in self.reservations
        )
        
        if existing:
            return None, "This slot has just been booked. Please choose another time."
        
        # Generate unique reservation ID
        reservation_id = f"TT{self.next_reservation_id}"
        self.next_reservation_id += 1
        
        reservation = {
            "reservation_id": reservation_id,
            "restaurant_id": restaurant_id,
            "phone_number": phone_number,
            "customer_name": name,
            "date": date,
            "time": time_slot,
            "party_size": party_size,
            "table_size": table_size,
            "status": "confirmed",
            "created_at": datetime.now().isoformat()
        }
        
        self.reservations.append(reservation)
        
        # Update user's reservation count
        if phone_number in self.users:
            self.users[phone_number]["total_reservations"] += 1
        
        return reservation, "Reservation created successfully"
    
    def get_restaurant_by_id(self, restaurant_id: int) -> Optional[Dict]:
        """Get restaurant details by ID."""
        for restaurant in RESTAURANTS:
            if restaurant["id"] == restaurant_id:
                return restaurant
        return None
    
    def get_restaurant_by_name(self, name: str) -> Optional[Dict]:
        """Get restaurant by name (case-insensitive partial match)."""
        name_lower = name.lower()
        for restaurant in RESTAURANTS:
            if name_lower in restaurant["name"].lower():
                return restaurant
        return None
    
    def search_restaurants(self, cuisine: Optional[str] = None, 
                          location: Optional[str] = None) -> List[Dict]:
        """Search restaurants by cuisine or location."""
        results = RESTAURANTS.copy()
        
        if cuisine:
            results = [r for r in results if r["cuisine"].lower() == cuisine.lower()]
        if location:
            results = [r for r in results if r["location"].lower() == location.lower()]
        
        return results
    
    def get_all_restaurants(self) -> List[Dict]:
        """Get all restaurants."""
        return RESTAURANTS.copy()
