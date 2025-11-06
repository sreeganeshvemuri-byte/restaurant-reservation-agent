"""Test script for the restaurant reservation agent."""
import os
import sys
from dotenv import load_dotenv

sys.path.append(os.path.dirname(__file__))

from data.restaurants import ReservationDatabase
from agent.gemini_agent import RestaurantAgent

def test_conversations():
    """Test various conversation scenarios."""
    
    # Load environment
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in environment")
        print("Please set your API key in .env file or environment variable")
        return
    
    # Initialize
    print("🤖 Initializing Restaurant Reservation Agent...")
    db = ReservationDatabase()
    agent = RestaurantAgent(api_key, db)
    agent.start_chat()
    print("✅ Agent initialized!\n")
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Simple Restaurant Search",
            "queries": [
                "I'm looking for Italian restaurants in Koramangala",
            ]
        },
        {
            "name": "Recommendation Request",
            "queries": [
                "Can you recommend a restaurant for my anniversary?",
            ]
        },
        {
            "name": "Vegetarian Search",
            "queries": [
                "Show me vegetarian restaurants",
            ]
        },
        {
            "name": "Top Rated Restaurants",
            "queries": [
                "What are the highest rated restaurants?",
            ]
        },
        {
            "name": "Complete Booking Flow",
            "queries": [
                "I want to book a table at Bella Italia",
                "Check availability for Friday at 7 PM for 4 people",
                # This would continue with confirmation, but we'll stop here for demo
            ]
        },
    ]
    
    for scenario in test_scenarios:
        print(f"\n{'='*60}")
        print(f"📋 Test Scenario: {scenario['name']}")
        print(f"{'='*60}\n")
        
        for query in scenario['queries']:
            print(f"👤 User: {query}")
            response = agent.send_message(query)
            print(f"🤖 Assistant: {response}\n")
        
        print(f"\n{'='*60}\n")
    
    print("✅ All test scenarios completed!")
    print(f"\n📊 Total restaurants in database: {len(db.get_restaurants())}")
    print(f"📊 Total reservations made: {len(db.reservations)}")

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║   🍽️  GoodFoods Restaurant Reservation Agent Test      ║
║        Built for Sarvam AI Challenge                     ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    test_conversations()
