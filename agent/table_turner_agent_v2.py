"""Table Turner AI Agent V2 with SQLite database integration."""
import json
from datetime import datetime
from typing import Any, Dict
import google.generativeai as genai

class TableTurnerAgentV2:
    """Enhanced AI agent using SQLite database for scalability."""
    
    def __init__(self, api_key: str, database):
        """Initialize the agent with SQLite database."""
        genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=[self._get_function_declarations()]
        )
        
        self.database = database
        self.chat = None
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
                description="Get the current date and time. Call this whenever user mentions 'today', 'tomorrow', or any relative date",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={}
                )
            ),
            genai.protos.FunctionDeclaration(
                name="parse_date_from_text",
                description="Parse relative dates like 'today', 'tomorrow', 'next Saturday' into actual dates (YYYY-MM-DD format)",
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
                            description="Name of the restaurant to search for"
                        ),
                        "cuisine": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Type of cuisine (Indian, Italian, Chinese, etc.)"
                        ),
                        "location": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Location/area in the city"
                        )
                    }
                )
            ),
            genai.protos.FunctionDeclaration(
                name="check_availability",
                description="Check available time slots for a restaurant on a specific date for given party size",
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
                            description="Preferred time in HH:MM format (24-hour), e.g., 19:00 for 7 PM"
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
                description="Create a confirmed reservation at a restaurant",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "restaurant_id": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="Restaurant ID"
                        ),
                        "table_id": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="Table ID from availability check"
                        ),
                        "date": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Date in YYYY-MM-DD format"
                        ),
                        "time_slot": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Time slot in HH:MM format"
                        ),
                        "party_size": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="Number of people"
                        )
                    },
                    required=["restaurant_id", "table_id", "date", "time_slot", "party_size"]
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
                if parsed_date:
                    self.user_context["parsed_date"] = parsed_date
                return {"parsed_date": parsed_date, "success": parsed_date is not None}
            
            elif function_name == "search_restaurants":
                # Search by name first
                if "restaurant_name" in function_args and function_args["restaurant_name"]:
                    restaurant = self.database.get_restaurant_by_name(
                        function_args["restaurant_name"]
                    )
                    if restaurant:
                        self.user_context["selected_restaurant"] = restaurant
                        return {"restaurants": [restaurant], "found_by": "name", "total": 1}
                
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
                    return {"available": False, "error": message}
                
                if requested_time:
                    # Check specific time slot and find nearest available
                    nearest_slot = self.database.find_nearest_available_slot(
                        restaurant_id, date, requested_time, party_size
                    )
                    
                    if nearest_slot:
                        self.user_context["available_slot"] = nearest_slot
                        self.user_context["booking_details"] = {
                            "restaurant_id": restaurant_id,
                            "table_id": nearest_slot["table_id"],
                            "date": date,
                            "time_slot": nearest_slot["time"],
                            "party_size": party_size,
                            "table_capacity": nearest_slot["table_capacity"]
                        }
                        is_exact_match = nearest_slot["time"] == requested_time
                        return {
                            "available": True,
                            "slot": nearest_slot,
                            "is_exact_match": is_exact_match,
                            "message": "Slot available" if is_exact_match else f"Requested time not available. Nearest slot is {nearest_slot['time']}"
                        }
                    else:
                        return {
                            "available": False,
                            "message": "No slots available for this date. Would you like to check another day?"
                        }
                else:
                    # Get all available slots
                    slots = self.database.get_available_slots(restaurant_id, date, party_size)
                    return {
                        "available": len(slots) > 0,
                        "slots": slots[:10],
                        "total_slots": len(slots)
                    }
            
            elif function_name == "create_reservation":
                phone = self.user_context.get("phone_number")
                name = self.user_context.get("name")
                
                reservation, message = self.database.create_reservation(
                    restaurant_id=function_args["restaurant_id"],
                    table_id=function_args["table_id"],
                    phone_number=phone,
                    customer_name=name,
                    date=function_args["date"],
                    time_slot=function_args["time_slot"],
                    party_size=function_args["party_size"]
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
        """Start a new chat session."""
        system_instruction = """You are Table Turner, a friendly AI assistant for GoodFoods restaurant reservations.

STRICT CONVERSATION FLOW:
1. Start by asking for mobile number: "Hey! This is Table Turner from GoodFoods, at your service today. Before we proceed forward, can I please get your mobile number?"

2. When you receive the phone number, immediately call check_user_exists function.

3a. If EXISTING user (check_user_exists returns exists=True):
   - Use their name from the response
   - Mention their recent reservation if available
   - Say: "Hey {NAME}, hope you are doing good, glad to hear from you again. Hope you had a good experience at {RECENT_RESTAURANT}."

3b. If NEW user (check_user_exists returns exists=False):
   - Ask: "Hey, welcome to GoodFoods! Can I know your good name before we proceed?"
   - When they provide name, call create_new_user
   - Then say: "Hey {NAME}, glad to hear from you!"

4. Ask: "Are you looking for reserving a table at any specific restaurant or do you need any suggestions based on any specific cuisine?"

5. If specific restaurant mentioned:
   - Search for it using search_restaurants
   - Ask for date, time, and party size if not provided

6. IMPORTANT: When user mentions "today", "tomorrow", or relative dates:
   - ALWAYS call get_current_date_time first
   - Then call parse_date_from_text to convert to actual date

7. Once you have restaurant, date, time, party size:
   - Call check_availability
   - If exact time available: Confirm with user
   - If exact time NOT available: Offer the nearest available slot
   - If user rejects: Suggest other days within 3 days

8. When user confirms:
   - Call create_reservation with all details from availability check
   - Show full reservation details including reservation ID (format: TT1000)

9. After booking:
   - Say: "Thank you! Here are your reservation details: [details]"
   - Ask: "Would you like to make another reservation?"
   - If yes: Go back to step 4
   - If no: Thank them

CRITICAL RULES:
- Bookings ONLY up to 3 days in advance
- Time slots are 30-minute intervals (11:00 to 23:00)
- Tables are sizes 2, 4, or 6 - always book equal or just larger
- Always use function results, don't make up data
- Be conversational but follow the flow strictly
- Keep responses concise and friendly"""
        
        self.chat = self.model.start_chat(history=[])
        self.user_context = {}
        
        return "Hey! This is Table Turner from GoodFoods, at your service today. 🍽️\n\nBefore we proceed forward, can I please get your mobile number?"
    
    def send_message(self, user_message: str) -> str:
        """Send message and handle function calls."""
        if not self.chat:
            return self.start_chat()
        
        try:
            response = self.chat.send_message(user_message)
            
            # Handle function calls (up to 10 iterations for complex flows)
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
                    
                    # Send response back to model
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
            return f"I apologize, but I encountered an error: {str(e)}. Could you please try again?"
    
    def get_user_context(self):
        """Get current user context."""
        return self.user_context
    
    def reset_conversation(self):
        """Reset conversation for new session."""
        self.chat = None
        self.user_context = {}
        return self.start_chat()
