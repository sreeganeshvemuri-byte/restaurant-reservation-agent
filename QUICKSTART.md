# ⚡ Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

- Python 3.9+
- Gemini API key ([Get one free](https://aistudio.google.com/apikey))

## 🚀 Installation (3 steps)

### 1. Install Dependencies

```bash
cd restaurant-reservation-agent
pip install -r requirements.txt
```

### 2. Set API Key

```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

### 3. Run the App

```bash
streamlit run app.py
```

✅ **Done!** The app opens automatically at `http://localhost:8501`

---

## 🎯 Try These Examples

Once the app is running:

### Example 1: Search Restaurants
```
"Show me Italian restaurants in Koramangala"
```

### Example 2: Get Recommendations
```
"Recommend a restaurant for my anniversary"
```

### Example 3: Make a Reservation
```
"Book a table for 4 at Bella Italia on Friday at 7 PM"
```

### Example 4: Dietary Needs
```
"Show me vegetarian options"
```

---

## 📁 Project Structure

```
restaurant-reservation-agent/
├── app.py                          # ← Start here!
├── agent/gemini_agent.py          # AI logic
├── data/restaurants.py            # 100 restaurants
├── docs/
│   ├── BUSINESS_STRATEGY.md      # Business case
│   ├── SETUP.md                  # Detailed setup
│   └── EXAMPLE_CONVERSATIONS.md  # Use cases
└── README.md                      # Full documentation
```

---

## 🎬 Next Steps

1. ✅ Test the app with example queries
2. ✅ Read the full [README.md](./README.md)
3. ✅ Review [BUSINESS_STRATEGY.md](./docs/BUSINESS_STRATEGY.md)
4. ✅ Check [EXAMPLE_CONVERSATIONS.md](./docs/EXAMPLE_CONVERSATIONS.md)
5. 🎥 Record your demo video
6. 📦 Create private GitHub repo
7. 📧 Share with Sarvam AI team

---

## 🐛 Troubleshooting

### "Module not found" error?
```bash
pip install -r requirements.txt --force-reinstall
```

### "Invalid API Key" error?
- Check your `.env` file
- Verify no extra spaces in the key
- Get a new key if needed

### Port already in use?
```bash
streamlit run app.py --server.port 8502
```

---

## 📚 Documentation

- **Quick Start**: You are here!
- **Full README**: [README.md](./README.md)
- **Setup Guide**: [docs/SETUP.md](./docs/SETUP.md)
- **Business Strategy**: [docs/BUSINESS_STRATEGY.md](./docs/BUSINESS_STRATEGY.md)
- **Example Conversations**: [docs/EXAMPLE_CONVERSATIONS.md](./docs/EXAMPLE_CONVERSATIONS.md)

---

## 🎯 Key Features

✅ **100 Restaurants** - Diverse cuisines & locations  
✅ **Natural Language** - Talk like a human  
✅ **Smart Recommendations** - AI-powered suggestions  
✅ **Function Calling** - Dynamic intent recognition  
✅ **Full Booking Flow** - Search → Reserve → Confirm  

---

## 💡 Tips

- Use the **Quick Action buttons** in the UI for common tasks
- The agent remembers conversation context
- You can modify or cancel reservations using their ID
- Try asking for recommendations based on occasions

---

**Ready to impress Sarvam AI? Let's go! 🚀**
