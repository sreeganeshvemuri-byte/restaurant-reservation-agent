"""AI Agent using Google Gemini with function calling."""
import json
import os
from typing import Any, Dict, List
import google.generativeai as genai
from datetime import datetime

class RestaurantAgent:
    """Conversational AI agent for restaurant reservations."""
    
    def __init__(self, api_key: str, database):
        """Initialize the agent with Gemini API."""
        genai.configure(api_key=api_key)
        
        # Using gemini-2.0-flash-exp or gemini-1.5-flash
        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            tools=[self._get_function_declarations()]
        )
        
        self.database = database
        self.chat = None
        self.conversation_history = []
        
    def _get_function_declarations(self):
        """Define all function declarations for the agent."""
        return [
            genai.protos.FunctionDeclaration(
                name="search_restaurants",
                description="Search for restaurants based on various criteria like cuisine, location, rating, or price range",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "cuisine": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Type of cuisine (e.g., Italian, Indian, Chinese, Japanese, etc.)"
                        ),
                        "location": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Area or location (e.g., Koramangala, Indiranagar, MG Road)"
                        ),
                        "min_rating": genai.protos.Schema(
                            type=genai.protos.Type.NUMBER,
                            description="Minimum rating (0.0 to 5.0)"
                        ),
                        "price_range": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Price range ($, $$, $$$, $$$$)"
                        )
                    }
                )
            ),
            genai.protos.FunctionDeclaration(
                name="get_restaurant_details",
                description="Get detailed information about a specific restaurant by its ID",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "restaurant_id": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="The unique ID of the restaurant"
                        )
                    },
                    required=["restaurant_id"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="check_availability",
                description="Check if a restaurant has availability for a specific date, time, and party size",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "restaurant_id": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="The ID of the restaurant"
                        ),
                        "date": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Date in YYYY-MM-DD format"
                        ),
                        "time": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Time in HH:MM format (24-hour)"
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
                name="create_reservation",
                description="Create a new restaurant reservation",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "restaurant_id": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="The ID of the restaurant"
                        ),
                        "customer_name": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Name of the customer"
                        ),
                        "customer_phone": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Phone number of the customer"
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
                        ),
                        "special_requests": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Any special requests or dietary requirements"
                        )
                    },
                    required=["restaurant_id", "customer_name", "customer_phone", "date", "time", "party_size"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="cancel_reservation",
                description="Cancel an existing reservation",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "reservation_id": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="The ID of the reservation to cancel"
                        )
                    },
                    required=["reservation_id"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="get_reservation_details",
                description="Get details of an existing reservation",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "reservation_id": genai.protos.Schema(
                            type=genai.protos.Type.INTEGER,
                            description="The ID of the reservation"
                        )
                    },
                    required=["reservation_id"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="recommend_restaurants",
                description="Get personalized restaurant recommendations based on user preferences, occasion, or dietary restrictions",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "occasion": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Type of occasion (e.g., romantic dinner, business meeting, family gathering, casual dining)"
                        ),
                        "dietary_restrictions": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Any dietary restrictions (e.g., vegetarian, vegan, gluten-free)"
                        ),
                        "preferences": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Any specific preferences like ambiance, cuisine style, etc."
                        )
                    }
                )
            )
        ]
    
    def _execute_function(self, function_name: str, function_args: Dict) -> Any:
        """Execute the requested function."""
        try:
            if function_name == "search_restaurants":
                filters = {}
                if "cuisine" in function_args:
                    filters["cuisine"] = function_args["cuisine"]
                if "location" in function_args:
                    filters["location"] = function_args["location"]
                if "min_rating" in function_args:
                    filters["min_rating"] = function_args["min_rating"]
                if "price_range" in function_args:
                    filters["price_range"] = function_args["price_range"]
                
                results = self.database.get_restaurants(filters if filters else None)
                return {"restaurants": results[:10], "total_found": len(results)}
            
            elif function_name == "get_restaurant_details":
                restaurant = self.database.get_restaurant_by_id(function_args["restaurant_id"])
                return {"restaurant": restaurant} if restaurant else {"error": "Restaurant not found"}
            
            elif function_name == "check_availability":
                available, message = self.database.check_availability(
                    function_args["restaurant_id"],
                    function_args["date"],
                    function_args["time"],
                    function_args["party_size"]
                )
                return {"available": available, "message": message}
            
            elif function_name == "create_reservation":
                reservation, message = self.database.create_reservation(
                    function_args["restaurant_id"],
                    function_args["customer_name"],
                    function_args["customer_phone"],
                    function_args["date"],
                    function_args["time"],
                    function_args["party_size"],
                    function_args.get("special_requests", "")
                )
                if reservation:
                    return {"success": True, "reservation": reservation, "message": message}
                else:
                    return {"success": False, "message": message}
            
            elif function_name == "cancel_reservation":
                success, message = self.database.cancel_reservation(function_args["reservation_id"])
                return {"success": success, "message": message}
            
            elif function_name == "get_reservation_details":
                reservation = self.database.get_reservation(function_args["reservation_id"])
                return {"reservation": reservation} if reservation else {"error": "Reservation not found"}
            
            elif function_name == "recommend_restaurants":
                # Recommendation logic based on occasion and preferences
                all_restaurants = self.database.get_restaurants()
                
                recommendations = []
                occasion = function_args.get("occasion", "").lower()
                dietary = function_args.get("dietary_restrictions", "").lower()
                
                # Simple recommendation logic
                if "romantic" in occasion or "date" in occasion:
                    # Prefer fine dining, Italian, French
                    recommendations = [r for r in all_restaurants if r["price_range"] in ["$$$", "$$$$"] 
                                     and r["cuisine"] in ["Italian", "French", "Continental"]]
                elif "business" in occasion or "meeting" in occasion:
                    # Prefer quiet, upscale places
                    recommendations = [r for r in all_restaurants if r["price_range"] in ["$$", "$$$"] 
                                     and r["rating"] >= 4.3]
                elif "family" in occasion:
                    # Prefer larger capacity, varied options
                    recommendations = [r for r in all_restaurants if r["capacity"] >= 50]
                elif "vegetarian" in dietary or "vegan" in dietary:
                    recommendations = [r for r in all_restaurants if r["cuisine"] in ["Vegetarian", "Vegan", "Indian", "Mediterranean"]]
                else:
                    # General high-rated recommendations
                    recommendations = [r for r in all_restaurants if r["rating"] >= 4.4]
                
                # Sort by rating and return top 5
                recommendations.sort(key=lambda x: x["rating"], reverse=True)
                return {"recommendations": recommendations[:5]}
            
            else:
                return {"error": f"Unknown function: {function_name}"}
                
        except Exception as e:
            return {"error": str(e)}
    
    def start_chat(self):
        """Start a new chat session."""
        system_instruction = """You are a helpful and friendly restaurant reservation assistant. Your role is to:
1. Help users find restaurants based on their preferences
2. Provide recommendations for different occasions
3. Check availability and make reservations
4. Answer questions about restaurants and their offerings
5. Help manage existing reservations

Be conversational, friendly, and proactive. Ask clarifying questions when needed.
When users mention dates, times, or party sizes, use the appropriate functions to check availability.
Always confirm details before making a reservation.
Provide personalized recommendations based on the user's needs."""
        
        self.chat = self.model.start_chat(history=[])
        self.conversation_history = []
        return "Chat started! How can I help you with restaurant reservations today?"
    
    def send_message(self, user_message: str) -> str:
        """Send a message and handle function calls."""
        if not self.chat:
            self.start_chat()
        
        self.conversation_history.append({"role": "user", "content": user_message})
        
        try:
            response = self.chat.send_message(user_message)
            
            # Handle function calls
            while response.candidates[0].content.parts:
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
            self.conversation_history.append({"role": "assistant", "content": final_response})
            
            return final_response
            
        except Exception as e:
            error_msg = f"I'm sorry, I encountered an error: {str(e)}"
            self.conversation_history.append({"role": "assistant", "content": error_msg})
            return error_msg
    
    def get_conversation_history(self):
        """Get the conversation history."""
        return self.conversation_history
