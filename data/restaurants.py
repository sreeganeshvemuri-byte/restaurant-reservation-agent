"""Restaurant database with diverse locations and cuisines."""
import json
import random
from datetime import datetime, timedelta

# Restaurant data
RESTAURANTS = [
    # Indian Cuisine
    {"id": 1, "name": "Spice Garden", "cuisine": "Indian", "location": "Koramangala", "city": "Bangalore", "capacity": 50, "price_range": "$$", "rating": 4.5, "specialties": ["Biryani", "Tandoori", "North Indian"]},
    {"id": 2, "name": "Curry House", "cuisine": "Indian", "location": "Indiranagar", "city": "Bangalore", "capacity": 40, "price_range": "$$", "rating": 4.3, "specialties": ["South Indian", "Dosa", "Idli"]},
    {"id": 3, "name": "Maharaja Palace", "cuisine": "Indian", "location": "MG Road", "city": "Bangalore", "capacity": 80, "price_range": "$$$", "rating": 4.7, "specialties": ["Royal Thali", "Mughlai", "Fine Dining"]},
    {"id": 4, "name": "Namaste Cafe", "cuisine": "Indian", "location": "Whitefield", "city": "Bangalore", "capacity": 35, "price_range": "$", "rating": 4.1, "specialties": ["Street Food", "Chaat", "Snacks"]},
    {"id": 5, "name": "The Tandoor", "cuisine": "Indian", "location": "HSR Layout", "city": "Bangalore", "capacity": 60, "price_range": "$$", "rating": 4.4, "specialties": ["Kebabs", "Tikka", "Naan"]},
    
    # Italian Cuisine
    {"id": 6, "name": "Bella Italia", "cuisine": "Italian", "location": "Koramangala", "city": "Bangalore", "capacity": 45, "price_range": "$$$", "rating": 4.6, "specialties": ["Pizza", "Pasta", "Risotto"]},
    {"id": 7, "name": "Luigi's Kitchen", "cuisine": "Italian", "location": "Brigade Road", "city": "Bangalore", "capacity": 55, "price_range": "$$", "rating": 4.2, "specialties": ["Lasagna", "Carbonara", "Tiramisu"]},
    {"id": 8, "name": "Roma Trattoria", "cuisine": "Italian", "location": "UB City", "city": "Bangalore", "capacity": 70, "price_range": "$$$$", "rating": 4.8, "specialties": ["Fine Dining", "Wine Selection", "Authentic Italian"]},
    {"id": 9, "name": "Pasta Paradise", "cuisine": "Italian", "location": "Jayanagar", "city": "Bangalore", "capacity": 30, "price_range": "$$", "rating": 4.0, "specialties": ["Fresh Pasta", "Handmade", "Family Style"]},
    {"id": 10, "name": "Venice Bistro", "cuisine": "Italian", "location": "Marathahalli", "city": "Bangalore", "capacity": 40, "price_range": "$$", "rating": 4.3, "specialties": ["Seafood Pasta", "Gelato", "Italian Desserts"]},
    
    # Chinese Cuisine
    {"id": 11, "name": "Dragon Wok", "cuisine": "Chinese", "location": "Koramangala", "city": "Bangalore", "capacity": 50, "price_range": "$$", "rating": 4.4, "specialties": ["Dim Sum", "Szechuan", "Noodles"]},
    {"id": 12, "name": "Golden Chopsticks", "cuisine": "Chinese", "location": "Commercial Street", "city": "Bangalore", "capacity": 45, "price_range": "$", "rating": 4.1, "specialties": ["Fried Rice", "Manchurian", "Hakka"]},
    {"id": 13, "name": "Beijing Dynasty", "cuisine": "Chinese", "location": "Residency Road", "city": "Bangalore", "capacity": 65, "price_range": "$$$", "rating": 4.5, "specialties": ["Peking Duck", "Hotpot", "Authentic Chinese"]},
    {"id": 14, "name": "Wok Express", "cuisine": "Chinese", "location": "Electronic City", "city": "Bangalore", "capacity": 35, "price_range": "$", "rating": 3.9, "specialties": ["Quick Service", "Combo Meals", "Takeaway"]},
    {"id": 15, "name": "Shanghai Nights", "cuisine": "Chinese", "location": "Lavelle Road", "city": "Bangalore", "capacity": 55, "price_range": "$$", "rating": 4.3, "specialties": ["Soup Dumplings", "Stir Fry", "Bubble Tea"]},
    
    # Continental
    {"id": 16, "name": "The Continental", "cuisine": "Continental", "location": "Indiranagar", "city": "Bangalore", "capacity": 60, "price_range": "$$$", "rating": 4.6, "specialties": ["Steaks", "Grills", "Fine Dining"]},
    {"id": 17, "name": "Olive Garden", "cuisine": "Continental", "location": "Koramangala", "city": "Bangalore", "capacity": 50, "price_range": "$$", "rating": 4.2, "specialties": ["Salads", "Soups", "Mediterranean"]},
    {"id": 18, "name": "Bistro 42", "cuisine": "Continental", "location": "MG Road", "city": "Bangalore", "capacity": 40, "price_range": "$$", "rating": 4.4, "specialties": ["French Toast", "Omelettes", "Brunch"]},
    {"id": 19, "name": "The Grill House", "cuisine": "Continental", "location": "Whitefield", "city": "Bangalore", "capacity": 70, "price_range": "$$$", "rating": 4.5, "specialties": ["BBQ", "Ribs", "Burgers"]},
    {"id": 20, "name": "European Delights", "cuisine": "Continental", "location": "HSR Layout", "city": "Bangalore", "capacity": 45, "price_range": "$$", "rating": 4.1, "specialties": ["European Mix", "Wine", "Cheese Platters"]},
    
    # Mexican
    {"id": 21, "name": "Taco Fiesta", "cuisine": "Mexican", "location": "Koramangala", "city": "Bangalore", "capacity": 40, "price_range": "$$", "rating": 4.3, "specialties": ["Tacos", "Burritos", "Nachos"]},
    {"id": 22, "name": "Chili's Cantina", "cuisine": "Mexican", "location": "Brigade Road", "city": "Bangalore", "capacity": 55, "price_range": "$$", "rating": 4.4, "specialties": ["Fajitas", "Quesadillas", "Margaritas"]},
    {"id": 23, "name": "Casa Mexicana", "cuisine": "Mexican", "location": "Indiranagar", "city": "Bangalore", "capacity": 50, "price_range": "$$", "rating": 4.2, "specialties": ["Enchiladas", "Chimichangas", "Guacamole"]},
    {"id": 24, "name": "Burrito Bowl", "cuisine": "Mexican", "location": "Electronic City", "city": "Bangalore", "capacity": 30, "price_range": "$", "rating": 4.0, "specialties": ["Build Your Bowl", "Quick Service", "Fresh Ingredients"]},
    {"id": 25, "name": "Aztec Kitchen", "cuisine": "Mexican", "location": "Whitefield", "city": "Bangalore", "capacity": 45, "price_range": "$$", "rating": 4.3, "specialties": ["Authentic Mexican", "Mole", "Churros"]},
    
    # Japanese
    {"id": 26, "name": "Sakura Sushi", "cuisine": "Japanese", "location": "UB City", "city": "Bangalore", "capacity": 35, "price_range": "$$$", "rating": 4.7, "specialties": ["Sushi", "Sashimi", "Rolls"]},
    {"id": 27, "name": "Tokyo Kitchen", "cuisine": "Japanese", "location": "Koramangala", "city": "Bangalore", "capacity": 40, "price_range": "$$", "rating": 4.4, "specialties": ["Ramen", "Udon", "Tempura"]},
    {"id": 28, "name": "Wasabi House", "cuisine": "Japanese", "location": "MG Road", "city": "Bangalore", "capacity": 45, "price_range": "$$$", "rating": 4.5, "specialties": ["Teppanyaki", "Bento Box", "Sake"]},
    {"id": 29, "name": "Zen Garden", "cuisine": "Japanese", "location": "Indiranagar", "city": "Bangalore", "capacity": 50, "price_range": "$$", "rating": 4.2, "specialties": ["Donburi", "Gyoza", "Japanese Curry"]},
    {"id": 30, "name": "Miso Bowl", "cuisine": "Japanese", "location": "HSR Layout", "city": "Bangalore", "capacity": 30, "price_range": "$", "rating": 4.1, "specialties": ["Quick Bowls", "Healthy Options", "Miso Soup"]},
    
    # Thai
    {"id": 31, "name": "Thai Orchid", "cuisine": "Thai", "location": "Koramangala", "city": "Bangalore", "capacity": 45, "price_range": "$$", "rating": 4.4, "specialties": ["Pad Thai", "Green Curry", "Tom Yum"]},
    {"id": 32, "name": "Bangkok Street", "cuisine": "Thai", "location": "Commercial Street", "city": "Bangalore", "capacity": 40, "price_range": "$", "rating": 4.2, "specialties": ["Street Food", "Spring Rolls", "Thai Tea"]},
    {"id": 33, "name": "Siam Spice", "cuisine": "Thai", "location": "Whitefield", "city": "Bangalore", "capacity": 50, "price_range": "$$", "rating": 4.3, "specialties": ["Red Curry", "Massaman", "Papaya Salad"]},
    {"id": 34, "name": "Lotus Thai", "cuisine": "Thai", "location": "Brigade Road", "city": "Bangalore", "capacity": 55, "price_range": "$$", "rating": 4.5, "specialties": ["Royal Thai", "Coconut Soup", "Thai BBQ"]},
    {"id": 35, "name": "Chiang Mai Kitchen", "cuisine": "Thai", "location": "Indiranagar", "city": "Bangalore", "capacity": 35, "price_range": "$$", "rating": 4.1, "specialties": ["Northern Thai", "Sticky Rice", "Mango Sticky Rice"]},
    
    # Mediterranean
    {"id": 36, "name": "Olive & Thyme", "cuisine": "Mediterranean", "location": "UB City", "city": "Bangalore", "capacity": 60, "price_range": "$$$", "rating": 4.6, "specialties": ["Greek", "Hummus", "Falafel"]},
    {"id": 37, "name": "Santorini Grill", "cuisine": "Mediterranean", "location": "Koramangala", "city": "Bangalore", "capacity": 50, "price_range": "$$", "rating": 4.4, "specialties": ["Gyros", "Souvlaki", "Baklava"]},
    {"id": 38, "name": "Lebanon Express", "cuisine": "Mediterranean", "location": "MG Road", "city": "Bangalore", "capacity": 40, "price_range": "$", "rating": 4.2, "specialties": ["Shawarma", "Tabbouleh", "Pita Bread"]},
    {"id": 39, "name": "Mediterranean Breeze", "cuisine": "Mediterranean", "location": "Whitefield", "city": "Bangalore", "capacity": 45, "price_range": "$$", "rating": 4.3, "specialties": ["Seafood", "Mezze", "Fresh Herbs"]},
    {"id": 40, "name": "Cyprus Kitchen", "cuisine": "Mediterranean", "location": "HSR Layout", "city": "Bangalore", "capacity": 35, "price_range": "$$", "rating": 4.0, "specialties": ["Halloumi", "Dolma", "Turkish Coffee"]},
    
    # American
    {"id": 41, "name": "All American Diner", "cuisine": "American", "location": "Brigade Road", "city": "Bangalore", "capacity": 60, "price_range": "$$", "rating": 4.3, "specialties": ["Burgers", "Fries", "Milkshakes"]},
    {"id": 42, "name": "Brooklyn Burger", "cuisine": "American", "location": "Koramangala", "city": "Bangalore", "capacity": 45, "price_range": "$$", "rating": 4.4, "specialties": ["Gourmet Burgers", "Wings", "Craft Beer"]},
    {"id": 43, "name": "Texas BBQ Pit", "cuisine": "American", "location": "Whitefield", "city": "Bangalore", "capacity": 70, "price_range": "$$$", "rating": 4.5, "specialties": ["Smoked Meats", "Brisket", "Pulled Pork"]},
    {"id": 44, "name": "Manhattan Steakhouse", "cuisine": "American", "location": "UB City", "city": "Bangalore", "capacity": 80, "price_range": "$$$$", "rating": 4.7, "specialties": ["Premium Steaks", "Wine List", "Fine Dining"]},
    {"id": 45, "name": "West Coast Grill", "cuisine": "American", "location": "Indiranagar", "city": "Bangalore", "capacity": 55, "price_range": "$$", "rating": 4.2, "specialties": ["Sandwiches", "Salads", "American Comfort Food"]},
    
    # Korean
    {"id": 46, "name": "Seoul Kitchen", "cuisine": "Korean", "location": "Koramangala", "city": "Bangalore", "capacity": 40, "price_range": "$$", "rating": 4.5, "specialties": ["BBQ", "Kimchi", "Bibimbap"]},
    {"id": 47, "name": "K-Pop Kitchen", "cuisine": "Korean", "location": "Indiranagar", "city": "Bangalore", "capacity": 35, "price_range": "$$", "rating": 4.3, "specialties": ["Korean Fried Chicken", "Tteokbokki", "Bubble Tea"]},
    {"id": 48, "name": "Gangnam Grill", "cuisine": "Korean", "location": "Whitefield", "city": "Bangalore", "capacity": 50, "price_range": "$$", "rating": 4.4, "specialties": ["Table BBQ", "Banchan", "Soju"]},
    {"id": 49, "name": "Hanok House", "cuisine": "Korean", "location": "Brigade Road", "city": "Bangalore", "capacity": 45, "price_range": "$$", "rating": 4.2, "specialties": ["Hot Pot", "Japchae", "Korean Stew"]},
    {"id": 50, "name": "Kimchi Corner", "cuisine": "Korean", "location": "HSR Layout", "city": "Bangalore", "capacity": 30, "price_range": "$", "rating": 4.0, "specialties": ["Quick Bites", "Korean Street Food", "Kimbap"]},
    
    # French
    {"id": 51, "name": "La Petite Paris", "cuisine": "French", "location": "UB City", "city": "Bangalore", "capacity": 50, "price_range": "$$$$", "rating": 4.8, "specialties": ["Fine French", "Foie Gras", "Wine Pairing"]},
    {"id": 52, "name": "Bistro du Soleil", "cuisine": "French", "location": "MG Road", "city": "Bangalore", "capacity": 40, "price_range": "$$$", "rating": 4.5, "specialties": ["Croissants", "Quiche", "French Pastries"]},
    {"id": 53, "name": "Provence Kitchen", "cuisine": "French", "location": "Koramangala", "city": "Bangalore", "capacity": 45, "price_range": "$$", "rating": 4.3, "specialties": ["Ratatouille", "Bouillabaisse", "Crêpes"]},
    {"id": 54, "name": "Le Cafe", "cuisine": "French", "location": "Indiranagar", "city": "Bangalore", "capacity": 35, "price_range": "$$", "rating": 4.2, "specialties": ["Coffee", "Macarons", "French Toast"]},
    {"id": 55, "name": "Paris Bistro", "cuisine": "French", "location": "Brigade Road", "city": "Bangalore", "capacity": 40, "price_range": "$$$", "rating": 4.4, "specialties": ["Escargot", "Coq au Vin", "Crème Brûlée"]},
    
    # Vietnamese
    {"id": 56, "name": "Pho Street", "cuisine": "Vietnamese", "location": "Koramangala", "city": "Bangalore", "capacity": 35, "price_range": "$", "rating": 4.3, "specialties": ["Pho", "Banh Mi", "Fresh Herbs"]},
    {"id": 57, "name": "Saigon Cafe", "cuisine": "Vietnamese", "location": "Whitefield", "city": "Bangalore", "capacity": 40, "price_range": "$$", "rating": 4.2, "specialties": ["Spring Rolls", "Vietnamese Coffee", "Vermicelli"]},
    {"id": 58, "name": "Hanoi Kitchen", "cuisine": "Vietnamese", "location": "HSR Layout", "city": "Bangalore", "capacity": 30, "price_range": "$", "rating": 4.1, "specialties": ["Noodle Soups", "Street Food", "Fresh Ingredients"]},
    {"id": 59, "name": "Lotus Bowl", "cuisine": "Vietnamese", "location": "Indiranagar", "city": "Bangalore", "capacity": 35, "price_range": "$$", "rating": 4.0, "specialties": ["Rice Bowls", "Healthy Options", "Vegetarian Friendly"]},
    {"id": 60, "name": "Viet Fusion", "cuisine": "Vietnamese", "location": "Brigade Road", "city": "Bangalore", "capacity": 45, "price_range": "$$", "rating": 4.3, "specialties": ["Fusion Vietnamese", "Modern Twist", "Craft Cocktails"]},
    
    # Spanish
    {"id": 61, "name": "Tapas Bar", "cuisine": "Spanish", "location": "UB City", "city": "Bangalore", "capacity": 50, "price_range": "$$$", "rating": 4.5, "specialties": ["Tapas", "Paella", "Sangria"]},
    {"id": 62, "name": "Barcelona Bites", "cuisine": "Spanish", "location": "Koramangala", "city": "Bangalore", "capacity": 45, "price_range": "$$", "rating": 4.3, "specialties": ["Pintxos", "Churros", "Spanish Wine"]},
    {"id": 63, "name": "Madrid Grill", "cuisine": "Spanish", "location": "MG Road", "city": "Bangalore", "capacity": 55, "price_range": "$$", "rating": 4.4, "specialties": ["Grilled Seafood", "Jamón", "Spanish Omelette"]},
    {"id": 64, "name": "Seville Kitchen", "cuisine": "Spanish", "location": "Whitefield", "city": "Bangalore", "capacity": 40, "price_range": "$$", "rating": 4.2, "specialties": ["Gazpacho", "Seafood Paella", "Flan"]},
    {"id": 65, "name": "Ibiza Lounge", "cuisine": "Spanish", "location": "Indiranagar", "city": "Bangalore", "capacity": 60, "price_range": "$$$", "rating": 4.4, "specialties": ["Cocktails", "Live Music", "Spanish Fusion"]},
    
    # Middle Eastern
    {"id": 66, "name": "Arabian Nights", "cuisine": "Middle Eastern", "location": "Brigade Road", "city": "Bangalore", "capacity": 50, "price_range": "$$", "rating": 4.3, "specialties": ["Kebabs", "Mezze", "Arabic Coffee"]},
    {"id": 67, "name": "Damascus Kitchen", "cuisine": "Middle Eastern", "location": "Koramangala", "city": "Bangalore", "capacity": 45, "price_range": "$$", "rating": 4.2, "specialties": ["Syrian Food", "Falafel", "Hummus"]},
    {"id": 68, "name": "Persian Palace", "cuisine": "Middle Eastern", "location": "UB City", "city": "Bangalore", "capacity": 60, "price_range": "$$$", "rating": 4.6, "specialties": ["Persian Kebabs", "Saffron Rice", "Baklava"]},
    {"id": 69, "name": "Istanbul Cafe", "cuisine": "Middle Eastern", "location": "Whitefield", "city": "Bangalore", "capacity": 40, "price_range": "$", "rating": 4.1, "specialties": ["Turkish Kebab", "Pide", "Turkish Delight"]},
    {"id": 70, "name": "Beirut Grill", "cuisine": "Middle Eastern", "location": "Indiranagar", "city": "Bangalore", "capacity": 45, "price_range": "$$", "rating": 4.3, "specialties": ["Lebanese Food", "Grilled Meats", "Fresh Salads"]},
    
    # Pan Asian
    {"id": 71, "name": "Asia Fusion", "cuisine": "Pan Asian", "location": "Koramangala", "city": "Bangalore", "capacity": 60, "price_range": "$$", "rating": 4.4, "specialties": ["Mixed Asian", "Fusion Cuisine", "Variety"]},
    {"id": 72, "name": "Oriental Kitchen", "cuisine": "Pan Asian", "location": "Brigade Road", "city": "Bangalore", "capacity": 55, "price_range": "$$", "rating": 4.3, "specialties": ["Noodles", "Rice Dishes", "Asian Soups"]},
    {"id": 73, "name": "East Meets West", "cuisine": "Pan Asian", "location": "UB City", "city": "Bangalore", "capacity": 70, "price_range": "$$$", "rating": 4.5, "specialties": ["Fusion", "Creative Dishes", "Modern Asian"]},
    {"id": 74, "name": "Bamboo House", "cuisine": "Pan Asian", "location": "Whitefield", "city": "Bangalore", "capacity": 50, "price_range": "$$", "rating": 4.2, "specialties": ["Thai & Chinese Mix", "Family Style", "Dim Sum"]},
    {"id": 75, "name": "Silk Route", "cuisine": "Pan Asian", "location": "HSR Layout", "city": "Bangalore", "capacity": 45, "price_range": "$$", "rating": 4.1, "specialties": ["Asian Street Food", "Spicy Options", "Bubble Tea"]},
    
    # Cafe/Bakery
    {"id": 76, "name": "The Coffee Bean", "cuisine": "Cafe", "location": "Koramangala", "city": "Bangalore", "capacity": 30, "price_range": "$", "rating": 4.4, "specialties": ["Coffee", "Pastries", "Sandwiches"]},
    {"id": 77, "name": "Sweet Treats Bakery", "cuisine": "Bakery", "location": "Indiranagar", "city": "Bangalore", "capacity": 25, "price_range": "$", "rating": 4.5, "specialties": ["Cakes", "Cookies", "Breads"]},
    {"id": 78, "name": "Brew & Bake", "cuisine": "Cafe", "location": "MG Road", "city": "Bangalore", "capacity": 35, "price_range": "$", "rating": 4.3, "specialties": ["Fresh Brew", "Breakfast", "Wi-Fi Friendly"]},
    {"id": 79, "name": "The Patisserie", "cuisine": "Bakery", "location": "UB City", "city": "Bangalore", "capacity": 30, "price_range": "$$", "rating": 4.6, "specialties": ["French Pastries", "Croissants", "Artisan Bread"]},
    {"id": 80, "name": "Corner Cafe", "cuisine": "Cafe", "location": "Whitefield", "city": "Bangalore", "capacity": 40, "price_range": "$", "rating": 4.2, "specialties": ["Quick Bites", "Smoothies", "Workspace"]},
    
    # Seafood
    {"id": 81, "name": "Coastal Catch", "cuisine": "Seafood", "location": "Brigade Road", "city": "Bangalore", "capacity": 50, "price_range": "$$$", "rating": 4.5, "specialties": ["Fresh Fish", "Lobster", "Prawns"]},
    {"id": 82, "name": "The Fisherman's Wharf", "cuisine": "Seafood", "location": "UB City", "city": "Bangalore", "capacity": 60, "price_range": "$$$", "rating": 4.6, "specialties": ["Goan Seafood", "Fish Curry", "Beach Vibes"]},
    {"id": 83, "name": "Ocean Breeze", "cuisine": "Seafood", "location": "Koramangala", "city": "Bangalore", "capacity": 45, "price_range": "$$", "rating": 4.3, "specialties": ["Fish Fry", "Seafood Platter", "Coastal Cuisine"]},
    {"id": 84, "name": "Crab Shack", "cuisine": "Seafood", "location": "Whitefield", "city": "Bangalore", "capacity": 40, "price_range": "$$", "rating": 4.2, "specialties": ["Crab", "Oysters", "Clams"]},
    {"id": 85, "name": "Tuna Bay", "cuisine": "Seafood", "location": "HSR Layout", "city": "Bangalore", "capacity": 35, "price_range": "$$", "rating": 4.1, "specialties": ["Sushi Grade Fish", "Poke Bowls", "Grilled Fish"]},
    
    # Vegetarian/Vegan
    {"id": 86, "name": "Green Leaf", "cuisine": "Vegetarian", "location": "Koramangala", "city": "Bangalore", "capacity": 40, "price_range": "$", "rating": 4.4, "specialties": ["Pure Veg", "Organic", "Healthy"]},
    {"id": 87, "name": "The Vegan Kitchen", "cuisine": "Vegan", "location": "Indiranagar", "city": "Bangalore", "capacity": 35, "price_range": "$$", "rating": 4.3, "specialties": ["Plant Based", "Vegan Burgers", "Smoothie Bowls"]},
    {"id": 88, "name": "Sprouts & Roots", "cuisine": "Vegetarian", "location": "Whitefield", "city": "Bangalore", "capacity": 30, "price_range": "$", "rating": 4.2, "specialties": ["Farm Fresh", "Salads", "Fresh Juices"]},
    {"id": 89, "name": "Earthen Pot", "cuisine": "Vegetarian", "location": "HSR Layout", "city": "Bangalore", "capacity": 45, "price_range": "$", "rating": 4.1, "specialties": ["North Indian Veg", "Thali", "Traditional"]},
    {"id": 90, "name": "Nature's Plate", "cuisine": "Vegan", "location": "MG Road", "city": "Bangalore", "capacity": 40, "price_range": "$$", "rating": 4.4, "specialties": ["Innovative Vegan", "Desserts", "Superfoods"]},
    
    # Additional Varied Cuisines
    {"id": 91, "name": "Havana Nights", "cuisine": "Cuban", "location": "Brigade Road", "city": "Bangalore", "capacity": 50, "price_range": "$$", "rating": 4.3, "specialties": ["Cuban Sandwiches", "Mojitos", "Live Music"]},
    {"id": 92, "name": "Aloha Poke", "cuisine": "Hawaiian", "location": "Koramangala", "city": "Bangalore", "capacity": 30, "price_range": "$", "rating": 4.2, "specialties": ["Poke Bowls", "Fresh Fish", "Island Vibes"]},
    {"id": 93, "name": "Buenos Aires Steakhouse", "cuisine": "Argentinian", "location": "UB City", "city": "Bangalore", "capacity": 70, "price_range": "$$$$", "rating": 4.7, "specialties": ["Argentine Beef", "Chimichurri", "Wine Selection"]},
    {"id": 94, "name": "Ethiopian Spice", "cuisine": "Ethiopian", "location": "Whitefield", "city": "Bangalore", "capacity": 35, "price_range": "$", "rating": 4.0, "specialties": ["Injera", "Wat", "Traditional Ethiopian"]},
    {"id": 95, "name": "Moroccan Nights", "cuisine": "Moroccan", "location": "Indiranagar", "city": "Bangalore", "capacity": 45, "price_range": "$$", "rating": 4.3, "specialties": ["Tagine", "Couscous", "Mint Tea"]},
    {"id": 96, "name": "Swiss Chalet", "cuisine": "Swiss", "location": "MG Road", "city": "Bangalore", "capacity": 40, "price_range": "$$$", "rating": 4.4, "specialties": ["Fondue", "Raclette", "Swiss Chocolate"]},
    {"id": 97, "name": "Bavarian Beer House", "cuisine": "German", "location": "Koramangala", "city": "Bangalore", "capacity": 80, "price_range": "$$", "rating": 4.4, "specialties": ["Sausages", "Pretzels", "German Beer"]},
    {"id": 98, "name": "The Outback", "cuisine": "Australian", "location": "Whitefield", "city": "Bangalore", "capacity": 60, "price_range": "$$$", "rating": 4.5, "specialties": ["Kangaroo Steak", "Barramundi", "Australian Wine"]},
    {"id": 99, "name": "Caribbean Kitchen", "cuisine": "Caribbean", "location": "HSR Layout", "city": "Bangalore", "capacity": 40, "price_range": "$$", "rating": 4.1, "specialties": ["Jerk Chicken", "Rice & Peas", "Rum Cocktails"]},
    {"id": 100, "name": "Nordic Table", "cuisine": "Scandinavian", "location": "UB City", "city": "Bangalore", "capacity": 45, "price_range": "$$$", "rating": 4.5, "specialties": ["Nordic Cuisine", "Smoked Salmon", "Minimalist"]},
]

class ReservationDatabase:
    """Manages restaurant reservations."""
    
    def __init__(self):
        self.reservations = []
        self.next_id = 1
        
    def get_restaurants(self, filters=None):
        """Get restaurants with optional filters."""
        results = RESTAURANTS.copy()
        
        if filters:
            if "cuisine" in filters:
                results = [r for r in results if r["cuisine"].lower() == filters["cuisine"].lower()]
            if "location" in filters:
                results = [r for r in results if r["location"].lower() == filters["location"].lower()]
            if "min_rating" in filters:
                results = [r for r in results if r["rating"] >= filters["min_rating"]]
            if "price_range" in filters:
                results = [r for r in results if r["price_range"] == filters["price_range"]]
                
        return results
    
    def get_restaurant_by_id(self, restaurant_id):
        """Get a specific restaurant by ID."""
        for restaurant in RESTAURANTS:
            if restaurant["id"] == restaurant_id:
                return restaurant
        return None
    
    def check_availability(self, restaurant_id, date, time, party_size):
        """Check if a restaurant has availability."""
        restaurant = self.get_restaurant_by_id(restaurant_id)
        if not restaurant:
            return False, "Restaurant not found"
        
        # Count existing reservations for this time slot
        existing = sum(1 for r in self.reservations 
                      if r["restaurant_id"] == restaurant_id 
                      and r["date"] == date 
                      and r["time"] == time 
                      and r["status"] == "confirmed")
        
        # Simple availability logic (could be more sophisticated)
        total_capacity = restaurant["capacity"]
        used_capacity = existing * 4  # Assume average party of 4
        
        if used_capacity + party_size <= total_capacity:
            return True, "Available"
        else:
            return False, "Fully booked for this time"
    
    def create_reservation(self, restaurant_id, customer_name, customer_phone, 
                          date, time, party_size, special_requests=""):
        """Create a new reservation."""
        available, message = self.check_availability(restaurant_id, date, time, party_size)
        
        if not available:
            return None, message
        
        reservation = {
            "id": self.next_id,
            "restaurant_id": restaurant_id,
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "date": date,
            "time": time,
            "party_size": party_size,
            "special_requests": special_requests,
            "status": "confirmed",
            "created_at": datetime.now().isoformat()
        }
        
        self.reservations.append(reservation)
        self.next_id += 1
        
        return reservation, "Reservation created successfully"
    
    def get_reservation(self, reservation_id):
        """Get a reservation by ID."""
        for reservation in self.reservations:
            if reservation["id"] == reservation_id:
                return reservation
        return None
    
    def cancel_reservation(self, reservation_id):
        """Cancel a reservation."""
        reservation = self.get_reservation(reservation_id)
        if reservation:
            reservation["status"] = "cancelled"
            return True, "Reservation cancelled successfully"
        return False, "Reservation not found"
    
    def modify_reservation(self, reservation_id, **kwargs):
        """Modify an existing reservation."""
        reservation = self.get_reservation(reservation_id)
        if not reservation:
            return None, "Reservation not found"
        
        # Update fields
        for key, value in kwargs.items():
            if key in reservation and key not in ["id", "created_at"]:
                reservation[key] = value
        
        return reservation, "Reservation modified successfully"
