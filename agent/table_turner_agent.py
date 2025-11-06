"""Table Turner AI Agent with specific conversation flow."""
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
import google.generativeai as genai

class TableTurnerAgent:
    """Conversational AI agent for Table Turner reservation system."""
    
    # Conversation states
    STATE_INIT = "init"
    STATE_PHONE_AUTH = "phone_auth"
    STATE_NAME_COLLECTION = "name_collection"
    STATE_MAIN_MENU = "main_menu"
    STATE_RESTAURANT_SELECTION = "restaurant_selection"
    STATE_DATE_TIME_COLLECTION = "date_time_collection"
    STATE_PARTY_SIZE_COLLECTION = "party_size_collection"
    STATE_SLOT_CONFIRMATION = "slot_confirmation"
    STATE_BOOKING_CONFIRMED = "booking_confirmed"
    
    def __init__(self, api_key: str, database):
        """Initialize the agent."""
        genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=[self._get_function_declarations()]
        )
        
        self.database = database
        self.chat = None
        self.conversation_state = self.STATE_INIT
        self.user_context = {}
        
    def _get_function_declarations(self):
        """Define function declarations for the agent."""
        return [
            genai.protos.FunctionDeclaration(
                name="check_user_exists",
                description="Check if a user with given phone number exists in the database",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "phone_number": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="10-digit phone number"
                        )
                    },
                    required=["phone_number"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="create_new_user",
                description="Create a new user in the database",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "phone_number": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="10-digit phone number"
                        ),
                        "name": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Customer's name"
                        )
                    },
                    required=["phone_number", "name"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="get_current_date_time",
                description="Get the current date and time. Use this whenever user mentions 'today', 'tomorrow', or relative dates",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={}
                )
            ),
            genai.protos.FunctionDeclaration(
                name="parse_date_from_text",
                description="Parse relative dates like 'today', 'tomorrow', 'next Saturday' into actual dates",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "user_text": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="User's text containing date reference"
                        )
                    },
                    required=["user_text"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="search_restaurants",
                description="Search for restaurants by name, cuisine, or location",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "restaurant_name": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Name of the restaurant"
                        ),
                        "cuisine": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Type of cuisine"
                        ),
                        "location": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Location/area"
                        )
                    }
                )
            ),
            genai.protos.FunctionDeclaration(
                name="check_availability",
                description="Check available time slots for a restaurant on a specific date",
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
                            description="Preferred time in HH:MM format (24-hour)"
                        ),
                        "party_size": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="Number of people"
                        )
                    },
                    required=["restaurant_id", "date", "party_size"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="create_reservation",
                description="Create a reservation at a restaurant",
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
                            description="Time slot in HH:MM format"
                        ),
                        "party_size": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="Number of people"
                        ),
                        "table_size": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="Table size (2, 4, or 6)"
                        )
                    },
                    required=["restaurant_id", "date", "time", "party_size", "table_size"]
                )
            ),
        ]
    
    def _execute_function(self, function_name: str, function_args: Dict) -> Any:
        """Execute the requested function."""
        try:
            if function_name == "check_user_exists":
                phone = function_args["phone_number"]
                exists = self.database.check_user_exists(phone)
                
                if exists:
                    user = self.database.get_user(phone)
                    recent_reservations = self.database.get_user_reservations(phone, limit=1)
                    self.user_context = {
                        "phone_number": phone,
                        "name": user["name"],
                        "is_new_user": False,
                        "recent_reservations": recent_reservations
                    }
                    return {
                        "exists": True,
                        "user": user,
                        "recent_reservations": recent_reservations
                    }
                else:
                    self.user_context = {
                        "phone_number": phone,
                        "is_new_user": True
                    }
                    return {"exists": False}
            
            elif function_name == "create_new_user":
                user = self.database.create_user(
                    function_args["phone_number"],
                    function_args["name"]
                )
                self.user_context["name"] = user["name"]
                self.user_context["is_new_user"] = False
                return {"success": True, "user": user}
            
            elif function_name == "get_current_date_time":
                current_dt = self.database.get_current_datetime()
                self.user_context["current_datetime"] = current_dt.isoformat()
                return {
                    "current_date": current_dt.strftime("%Y-%m-%d"),
                    "current_time": current_dt.strftime("%H:%M"),
                    "current_datetime": current_dt.strftime("%Y-%m-%d %H:%M:%S"),
                    "day_of_week": current_dt.strftime("%A")
                }
            
            elif function_name == "parse_date_from_text":
                current_dt = self.database.get_current_datetime()
                parsed_date = self.database.parse_relative_date(
                    function_args["user_text"],
                    current_dt
                )
                return {"parsed_date": parsed_date}
            
            elif function_name == "search_restaurants":
                # Search by name first
                if "restaurant_name" in function_args:
                    restaurant = self.database.get_restaurant_by_name(
                        function_args["restaurant_name"]
                    )
                    if restaurant:
                        self.user_context["selected_restaurant"] = restaurant
                        return {"restaurants": [restaurant], "found_by": "name"}
                
                # Search by cuisine/location
                results = self.database.search_restaurants(
                    cuisine=function_args.get("cuisine"),
                    location=function_args.get("location")
                )
                return {"restaurants": results, "total": len(results)}
            
            elif function_name == "check_availability":
                restaurant_id = function_args["restaurant_id"]
                date = function_args["date"]
                party_size = function_args["party_size"]
                requested_time = function_args.get("time")
                
                # Validate 3-day advance booking
                is_valid, message = self.database.validate_booking_advance(date)
                if not is_valid:
                    return {"available": False, "message": message}
                
                if requested_time:
                    # Check specific time slot
                    nearest_slot = self.database.find_nearest_available_slot(
                        restaurant_id, date, requested_time, party_size
                    )
                    
                    if nearest_slot:
                        self.user_context["available_slot"] = nearest_slot
                        self.user_context["booking_details"] = {
                            "restaurant_id": restaurant_id,
                            "date": date,
                            "time": nearest_slot["time"],
                            "party_size": party_size,
                            "table_size": nearest_slot["table_size"]
                        }
                        return {
                            "available": True,
                            "slot": nearest_slot,
                            "message": "Slot available"
                        }
                    else:
                        return {
                            "available": False,
                            "message": "No slots available for this time. Would you like to check another day?"
                        }
                else:
                    # Get all available slots
                    slots = self.database.get_available_slots(restaurant_id, date, party_size)
                    return {
                        "available": len(slots) > 0,
                        "slots": slots[:10],  # Show first 10 slots
                        "total_slots": len(slots)
                    }
            
            elif function_name == "create_reservation":
                phone = self.user_context.get("phone_number")
                name = self.user_context.get("name")
                
                reservation, message = self.database.create_reservation(
                    restaurant_id=function_args["restaurant_id"],
                    phone_number=phone,
                    name=name,
                    date=function_args["date"],
                    time_slot=function_args["time"],
                    party_size=function_args["party_size"],
                    table_size=function_args["table_size"]
                )
                
                if reservation:
                    self.user_context["last_reservation"] = reservation
                    return {
                        "success": True,
                        "reservation": reservation,
                        "message": message
                    }
                else:
                    return {
                        "success": False,
                        "message": message
                    }
            
            else:
                return {"error": f"Unknown function: {function_name}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def start_chat(self):
        """Start a new chat session with initial greeting."""
        system_instruction = """You are Table Turner, a friendly AI assistant for GoodFoods restaurant reservations.

IMPORTANT RULES:
1. ALWAYS start by asking for the user's mobile number
2. If existing user: Greet by name and mention their recent reservation
3. If new user: Ask for their name first
4. Bookings can ONLY be made up to 3 days in advance
5. ALWAYS call get_current_date_time when user mentions "today", "tomorrow", or relative dates
6. Time slots are in 30-minute intervals from 11:00 AM to 11:00 PM
7. Tables come in sizes: 2, 4, 6 - book equal or just larger than party size
8. After booking, ask if they want to make another reservation

CONVERSATION FLOW:
1. Greet and ask for phone number
2. Check if user exists
3. If existing: Personalized greeting with recent reservation mention
4. If new: Ask for name, then greet
5. Ask if they want specific restaurant or need suggestions
6. If specific: Check availability for their date/time
7. If time slot taken: Offer nearest available slot
8. If user rejects: Offer other days within 3 days
9. Confirm booking and show reservation ID
10. Ask if they want another reservation

Be conversational, friendly, and follow this flow strictly."""
        
        self.chat = self.model.start_chat(history=[])
        self.conversation_state = self.STATE_INIT
        self.user_context = {}
        
        # Initial greeting
        return "Hey! This is Table Turner from GoodFoods, at your service today. 🍽️\n\nBefore we proceed forward, can I please get your mobile number?"
    
    def send_message(self, user_message: str) -> str:
        """Send a message and handle function calls."""
        if not self.chat:
            return self.start_chat()
        
        try:
            response = self.chat.send_message(user_message)
            
            # Handle function calls
            max_iterations = 5
            iteration = 0
            
            while iteration < max_iterations:
                iteration += 1
                
                if not response.candidates or not response.candidates[0].content.parts:
                    break
                
                part = response.candidates[0].content.parts[0]
                
                # Check if it's a function call
                if hasattr(part, 'function_call') and part.function_call:
                    function_call = part.function_call
                    function_name = function_call.name
                    function_args = dict(function_call.args)
                    
                    # Execute the function
                    function_response = self._execute_function(function_name, function_args)
                    
                    # Send function response back to the model
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
                    # Regular text response
                    break
            
            # Get the final text response
            final_response = response.text
            return final_response
            
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Could you please try again?"
    
    def get_user_context(self):
        """Get current user context."""
        return self.user_context
