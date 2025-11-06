"""Hybrid AI Agent V3 - Natural conversation with smart data collection."""
import json
import re
from datetime import datetime
from typing import Any, Dict, Optional, Tuple
import google.generativeai as genai

class HybridAgentV3:
    """Intelligent conversational agent that adapts to user input style."""
    
    def __init__(self, api_key: str, database):
        """Initialize the hybrid agent."""
        genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=[self._get_function_declarations()]
        )
        
        self.database = database
        self.chat = None
        self.user_context = {
            "authenticated": False,
            "has_phone": False,
            "has_name": False,
            "phone_number": None,
            "name": None,
            "pending_booking": {}
        }
        
    def _get_function_declarations(self):
        """Define function declarations."""
        return [
            # Information extraction functions
            genai.protos.FunctionDeclaration(
                name="extract_and_verify_phone",
                description="Extract and verify phone number from user message. Call this if user mentions any numbers that could be a phone number.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "phone_number": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Extracted phone number (10 digits)"
                        )
                    },
                    required=["phone_number"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="extract_customer_name",
                description="Extract customer name from message when they introduce themselves (e.g., 'I'm John', 'My name is Sarah', 'This is Raj')",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "name": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Extracted customer name"
                        )
                    },
                    required=["name"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="extract_booking_details",
                description="Extract restaurant name, date, time, and party size from user message when they request a booking",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "restaurant_name": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Name of restaurant mentioned"
                        ),
                        "date_reference": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Date mentioned (e.g., 'tomorrow', 'next Friday', '2025-11-08')"
                        ),
                        "time_reference": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Time mentioned (e.g., '7 PM', '19:00', 'evening')"
                        ),
                        "party_size": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="Number of people mentioned"
                        )
                    }
                )
            ),
            
            # Core functions
            genai.protos.FunctionDeclaration(
                name="authenticate_user",
                description="Authenticate user with phone number, check if existing or new user",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "phone_number": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Phone number to authenticate"
                        )
                    },
                    required=["phone_number"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="register_new_user",
                description="Register a new user with phone and name",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "phone_number": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Phone number"
                        ),
                        "name": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Customer name"
                        )
                    },
                    required=["phone_number", "name"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="get_current_datetime",
                description="Get current date and time. ALWAYS call this when user mentions today, tomorrow, or any relative date.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={}
                )
            ),
            genai.protos.FunctionDeclaration(
                name="parse_date_time",
                description="Parse natural language date and time into structured format",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "date_text": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Date reference (today, tomorrow, next Friday, 2025-11-08)"
                        ),
                        "time_text": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Time reference (7 PM, 19:00, evening, lunch time)"
                        )
                    }
                )
            ),
            genai.protos.FunctionDeclaration(
                name="search_restaurants",
                description="Search for restaurants by name, cuisine, or get suggestions",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "restaurant_name": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Specific restaurant name"
                        ),
                        "cuisine": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Cuisine type for suggestions"
                        ),
                        "location": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Location/area"
                        )
                    }
                )
            ),
            genai.protos.FunctionDeclaration(
                name="check_availability_and_book",
                description="Check availability for a restaurant and proceed with booking if available. Call this when you have restaurant, date, time, and party size.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "restaurant_id": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="Restaurant ID"
                        ),
                        "date": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Date in YYYY-MM-DD format"
                        ),
                        "time": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Time in HH:MM format"
                        ),
                        "party_size": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="Number of people"
                        )
                    },
                    required=["restaurant_id", "date", "time", "party_size"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="confirm_and_create_reservation",
                description="Create the final reservation after user confirms. Only call after user explicitly confirms.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "confirmed": genai.protos.Schema(
                            type=genai.protos.Type.BOOLEAN,
                            description="Whether user confirmed the booking"
                        )
                    }
                )
            ),
        ]
    
    def _execute_function(self, function_name: str, function_args: Dict) -> Any:
        """Execute functions with context awareness."""
        try:
            if function_name == "extract_and_verify_phone":
                phone = function_args["phone_number"]
                # Clean phone number
                phone = re.sub(r'\D', '', phone)
                
                if len(phone) == 10:
                    self.user_context["phone_number"] = phone
                    self.user_context["has_phone"] = True
                    return {"success": True, "phone_number": phone}
                else:
                    return {"success": False, "error": "Invalid phone number format"}
            
            elif function_name == "extract_customer_name":
                name = function_args["name"]
                self.user_context["name"] = name
                self.user_context["has_name"] = True
                return {"success": True, "name": name}
            
            elif function_name == "extract_booking_details":
                details = {}
                if "restaurant_name" in function_args:
                    details["restaurant_name"] = function_args["restaurant_name"]
                if "date_reference" in function_args:
                    details["date_reference"] = function_args["date_reference"]
                if "time_reference" in function_args:
                    details["time_reference"] = function_args["time_reference"]
                if "party_size" in function_args:
                    details["party_size"] = function_args["party_size"]
                
                self.user_context["pending_booking"].update(details)
                return {"extracted": details, "success": True}
            
            elif function_name == "authenticate_user":
                phone = function_args["phone_number"]
                exists = self.database.check_user_exists(phone)
                
                if exists:
                    user = self.database.get_user(phone)
                    recent_reservations = self.database.get_user_reservations(phone, limit=1)
                    
                    self.user_context.update({
                        "authenticated": True,
                        "has_phone": True,
                        "has_name": True,
                        "phone_number": phone,
                        "name": user["name"],
                        "is_new_user": False,
                        "recent_reservations": recent_reservations
                    })
                    
                    return {
                        "exists": True,
                        "user": user,
                        "recent_reservations": recent_reservations
                    }
                else:
                    self.user_context.update({
                        "has_phone": True,
                        "phone_number": phone,
                        "is_new_user": True
                    })
                    return {"exists": False, "phone_number": phone}
            
            elif function_name == "register_new_user":
                user = self.database.create_user(
                    function_args["phone_number"],
                    function_args["name"]
                )
                self.user_context.update({
                    "authenticated": True,
                    "has_name": True,
                    "name": user["name"],
                    "is_new_user": False
                })
                return {"success": True, "user": user}
            
            elif function_name == "get_current_datetime":
                current_dt = self.database.get_current_datetime()
                self.user_context["current_datetime"] = current_dt.isoformat()
                return {
                    "current_date": current_dt.strftime("%Y-%m-%d"),
                    "current_time": current_dt.strftime("%H:%M"),
                    "day_of_week": current_dt.strftime("%A"),
                    "formatted": current_dt.strftime("%B %d, %Y at %I:%M %p")
                }
            
            elif function_name == "parse_date_time":
                current_dt = self.database.get_current_datetime()
                
                # Parse date
                date_text = function_args.get("date_text", "")
                parsed_date = self.database.parse_relative_date(date_text, current_dt)
                
                # Parse time
                time_text = function_args.get("time_text", "")
                parsed_time = self._parse_time(time_text, current_dt)
                
                return {
                    "date": parsed_date,
                    "time": parsed_time,
                    "success": parsed_date is not None
                }
            
            elif function_name == "search_restaurants":
                # Search by name first
                if "restaurant_name" in function_args and function_args["restaurant_name"]:
                    restaurant = self.database.get_restaurant_by_name(function_args["restaurant_name"])
                    if restaurant:
                        self.user_context["selected_restaurant"] = restaurant
                        self.user_context["pending_booking"]["restaurant_id"] = restaurant["id"]
                        return {"restaurants": [restaurant], "found": True, "total": 1}
                
                # Search by cuisine/location
                results = self.database.search_restaurants(
                    cuisine=function_args.get("cuisine"),
                    location=function_args.get("location")
                )
                return {"restaurants": results, "found": len(results) > 0, "total": len(results)}
            
            elif function_name == "check_availability_and_book":
                restaurant_id = function_args["restaurant_id"]
                date = function_args["date"]
                time = function_args["time"]
                party_size = function_args["party_size"]
                
                # Validate 3-day rule
                is_valid, message = self.database.validate_booking_advance(date)
                if not is_valid:
                    return {"available": False, "error": message}
                
                # Find available slot
                nearest_slot = self.database.find_nearest_available_slot(
                    restaurant_id, date, time, party_size
                )
                
                if nearest_slot:
                    # Store for confirmation
                    self.user_context["pending_booking"] = {
                        "restaurant_id": restaurant_id,
                        "table_id": nearest_slot["table_id"],
                        "date": date,
                        "time": nearest_slot["time"],
                        "party_size": party_size,
                        "table_capacity": nearest_slot["table_capacity"],
                        "is_exact_match": nearest_slot["time"] == time
                    }
                    
                    restaurant = self.database.get_restaurant_by_id(restaurant_id)
                    
                    return {
                        "available": True,
                        "slot": nearest_slot,
                        "restaurant": restaurant,
                        "is_exact_match": nearest_slot["time"] == time,
                        "needs_confirmation": True
                    }
                else:
                    # Try to find slots on other days within 3 days
                    alternate_dates = self._get_alternate_dates(date)
                    alternate_slots = []
                    
                    for alt_date in alternate_dates:
                        slots = self.database.get_available_slots(restaurant_id, alt_date, party_size)
                        if slots:
                            alternate_slots.append({
                                "date": alt_date,
                                "slots_available": len(slots),
                                "first_slot": slots[0]["time"]
                            })
                    
                    return {
                        "available": False,
                        "message": "No availability for requested time",
                        "alternate_dates": alternate_slots
                    }
            
            elif function_name == "confirm_and_create_reservation":
                if not function_args.get("confirmed"):
                    self.user_context["pending_booking"] = {}
                    return {"success": False, "message": "Booking cancelled by user"}
                
                # Create reservation from pending booking
                booking = self.user_context.get("pending_booking", {})
                phone = self.user_context.get("phone_number")
                name = self.user_context.get("name")
                
                if not all([booking, phone, name]):
                    return {"success": False, "error": "Missing booking details"}
                
                reservation, message = self.database.create_reservation(
                    restaurant_id=booking["restaurant_id"],
                    table_id=booking["table_id"],
                    phone_number=phone,
                    customer_name=name,
                    date=booking["date"],
                    time_slot=booking["time"],
                    party_size=booking["party_size"]
                )
                
                if reservation:
                    self.user_context["last_reservation"] = reservation
                    self.user_context["pending_booking"] = {}
                    return {
                        "success": True,
                        "reservation": reservation,
                        "message": "Reservation confirmed!"
                    }
                else:
                    return {"success": False, "message": message}
            
            else:
                return {"error": f"Unknown function: {function_name}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def _parse_time(self, time_text: str, current_dt: datetime) -> Optional[str]:
        """Parse time from natural language."""
        time_text_lower = time_text.lower()
        
        # Common time formats
        if "lunch" in time_text_lower:
            return "12:30"
        elif "breakfast" in time_text_lower:
            return "09:00"
        elif "brunch" in time_text_lower:
            return "11:00"
        elif "dinner" in time_text_lower or "evening" in time_text_lower:
            return "19:00"
        
        # Extract time patterns
        # Pattern: "7 PM", "7PM", "19:00", "7:30 PM"
        pm_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*pm', time_text_lower)
        am_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*am', time_text_lower)
        time_24_match = re.search(r'(\d{1,2}):(\d{2})', time_text)
        
        if pm_match:
            hour = int(pm_match.group(1))
            minute = int(pm_match.group(2)) if pm_match.group(2) else 0
            if hour != 12:
                hour += 12
            return f"{hour:02d}:{minute:02d}"
        elif am_match:
            hour = int(am_match.group(1))
            minute = int(am_match.group(2)) if am_match.group(2) else 0
            if hour == 12:
                hour = 0
            return f"{hour:02d}:{minute:02d}"
        elif time_24_match:
            hour = int(time_24_match.group(1))
            minute = int(time_24_match.group(2))
            return f"{hour:02d}:{minute:02d}"
        
        return None
    
    def _get_alternate_dates(self, original_date: str) -> list:
        """Get alternate dates within 3-day window."""
        from datetime import timedelta
        try:
            date_obj = datetime.strptime(original_date, "%Y-%m-%d")
            current = datetime.now().date()
            
            alternates = []
            for days_ahead in range(4):  # 0, 1, 2, 3 days
                check_date = current + timedelta(days=days_ahead)
                if check_date != date_obj.date():
                    alternates.append(check_date.strftime("%Y-%m-%d"))
            
            return alternates[:3]  # Return up to 3 alternate dates
        except:
            return []
    
    def start_chat(self):
        """Start chat with intelligent greeting."""
        system_instruction = """You are Table Turner, an intelligent and friendly AI assistant for GoodFoods restaurant reservations.

CORE PRINCIPLE: Be CONVERSATIONAL and ADAPTIVE, not rigid.

INTELLIGENT DATA COLLECTION:
1. If user provides info (phone, name, restaurant, date, time, party size) in their message → Extract it immediately using appropriate functions
2. Only ask for what's MISSING, not what they already told you
3. Process requests as efficiently as possible

REQUIRED DATA (must have before final booking):
- Phone number (for authentication and confirmation)
- Name (for reservation)
- Restaurant (which one)
- Date (within 3 days)
- Time (11:00-23:00, 30-min slots)
- Party size (number of people)

CONVERSATION STYLE:
✅ Natural and friendly
✅ Extract info from what user says
✅ Ask only for missing pieces
✅ Confirm before final booking
✅ Acknowledge what they've already told you

EXAMPLES OF GOOD RESPONSES:

User: "Book Bella Italia tomorrow at 7 PM for 4 people, I'm Raj 9876543210"
You: [Extract: phone, name, restaurant, date, time, party_size]
     "Perfect! Let me check availability at Bella Italia for tomorrow at 7 PM for 4 people..."
     [Check availability]
     "Great news! Available. Confirming for Raj at 9876543210?"

User: "I want a reservation"
You: "I'd be happy to help! To get started, could you tell me:
     - Your mobile number
     - Which restaurant you'd like (or I can suggest based on cuisine)
     - Date and time you prefer
     - How many people?"

User: "9876543210"
You: [Check if exists]
     If existing: "Hey {NAME}! Great to hear from you again. Hope you enjoyed {RECENT_RESTAURANT}! 
                   What can I help you book today?"
     If new: "Welcome to GoodFoods! May I have your name?"

STRICT RULES (ALWAYS ENFORCE):
- ⚠️ Bookings ONLY up to 3 days in advance
- ⚠️ Time slots: 11:00-23:00 in 30-min intervals
- ⚠️ When user says "today/tomorrow": CALL get_current_datetime first, then parse_date_time
- ⚠️ ALWAYS confirm booking details before creating reservation
- ⚠️ After booking: Ask "Would you like to make another reservation?"

FLOW:
1. Collect phone (extract if mentioned, else ask)
2. Authenticate user (existing vs new)
3. Collect name if new user
4. Collect booking details (extract from message or ask)
5. Check availability
6. Confirm with user
7. Create reservation
8. Show reservation ID
9. Ask if they want another booking

Be smart: If they give you everything at once, process it all. If they give piece by piece, guide them naturally."""
        
        self.chat = self.model.start_chat(history=[])
        
        return "Hey! This is Table Turner from GoodFoods, at your service today. 🍽️\n\nHow can I help you with your dining plans? (I'll need your mobile number to get started)"
    
    def send_message(self, user_message: str) -> str:
        """Send message with intelligent handling."""
        if not self.chat:
            return self.start_chat()
        
        try:
            response = self.chat.send_message(user_message)
            
            # Handle function calls
            max_iterations = 10
            iteration = 0
            
            while iteration < max_iterations:
                iteration += 1
                
                if not response.candidates or not response.candidates[0].content.parts:
                    break
                
                part = response.candidates[0].content.parts[0]
                
                if hasattr(part, 'function_call') and part.function_call:
                    function_call = part.function_call
                    function_name = function_call.name
                    function_args = dict(function_call.args)
                    
                    # Execute function
                    function_response = self._execute_function(function_name, function_args)
                    
                    # Send back to model
                    response = self.chat.send_message(
                        genai.protos.Content(
                            parts=[genai.protos.Part(
                                function_response=genai.protos.FunctionResponse(
                                    name=function_name,
                                    response={"result": function_response}
                                )
                            )]
                        )
                    )
                else:
                    break
            
            return response.text
            
        except Exception as e:
            return f"I apologize, I encountered an error: {str(e)}. Could you please try again?"
    
    def get_user_context(self):
        """Get current context."""
        return self.user_context
    
    def reset_conversation(self):
        """Reset for new conversation."""
        self.chat = None
        self.user_context = {
            "authenticated": False,
            "has_phone": False,
            "has_name": False,
            "phone_number": None,
            "name": None,
            "pending_booking": {}
        }
        return self.start_chat()
