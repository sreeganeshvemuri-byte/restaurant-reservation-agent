# 🚀 Run Table Turner - Quick Start

## ⚡ Quick Commands

### In GitHub Codespaces or Terminal:

```bash
# Navigate to project
cd /workspaces/restaurant-reservation-agent

# Run the NEW Table Turner version
python3 -m streamlit run app_table_turner.py
```

---

## 🔄 Two Versions Available

### Version 1: Original (app.py)
- General purpose reservation agent
- Open-ended conversations
- 100 restaurants
- No user authentication

**Run**: `python3 -m streamlit run app.py`

### Version 2: Table Turner (app_table_turner.py) ⭐ NEW
- Phone number authentication
- Personalized greetings
- 30-minute time slots
- 3-day advance booking
- Voice/text input options
- Specific conversation flow

**Run**: `python3 -m streamlit run app_table_turner.py`

---

## 🎯 Test The New Flow

### Test Scenario 1: New User

1. **Start app**: `python3 -m streamlit run app_table_turner.py`
2. **Enter phone**: `9876543210` (new number)
3. **System asks for name**: Enter `John Doe`
4. **Greeting**: "Hey, John Doe! Glad to hear from you"
5. **Choose restaurant**: Say `Bella Italia`
6. **Choose date/time**: Say `tomorrow at 7 PM for 4 people`
7. **Confirm booking**: Say `yes`
8. **Get reservation ID**: TT1000
9. **Another booking?**: Say `no`

### Test Scenario 2: Existing User

1. **Start app**
2. **Enter same phone**: `9876543210`
3. **Personalized greeting**: "Hey, John Doe! Hope you had a good experience at Bella Italia"
4. **Continue booking**: Follow the flow

### Test Scenario 3: Date Parsing

Try these inputs:
- "I want to book for today at 6 PM"
- "Tomorrow evening around 7"
- "Next Saturday for lunch"
- "Day after tomorrow at 8 PM"

### Test Scenario 4: 3-Day Limit

Try:
- "I want to book for next week" → Should reject
- "Book for 5 days from now" → Should reject
- "Tomorrow" → Should accept
- "Day after tomorrow" → Should accept

---

## 🎨 UI Features

### What You'll See:

1. **Header**:
   - 🍽️ Table Turner logo
   - Purple gradient background
   - "by GoodFoods" tagline

2. **Messages**:
   - Each message has 🔊 volume icon
   - Click to hear message read aloud
   - User messages (blue), Assistant (gray)

3. **Input Options**:
   - 📝 Text Input button
   - 🎤 Voice Input button (coming soon)

4. **Info Panel**:
   - Expandable "About Table Turner" section
   - Booking rules
   - Features list

---

## 🔍 Key Differences from Original

### New Features:
✅ User authentication with phone number  
✅ Personalized returning user experience  
✅ 30-minute time slot system  
✅ 3-day advance booking validation  
✅ Table size optimization (2, 4, 6)  
✅ Relative date parsing  
✅ Unique reservation IDs (TT1000+)  
✅ Voice/text input toggle  
✅ Text-to-speech capability  
✅ Multiple bookings per session  

---

## 🧪 Testing Commands

```bash
# Run Table Turner
python3 -m streamlit run app_table_turner.py

# Check current time slots
python3 -c "from data.table_turner_db import TableTurnerDatabase; db = TableTurnerDatabase(); print(db.time_slots)"

# Test date parsing
python3 -c "from data.table_turner_db import TableTurnerDatabase; from datetime import datetime; db = TableTurnerDatabase(); print(db.parse_relative_date('tomorrow', datetime.now()))"
```

---

## 📊 Comparison Chart

| Feature | app.py | app_table_turner.py |
|---------|--------|---------------------|
| Restaurants | 100 | 10 (expandable) |
| User Auth | ❌ | ✅ Phone-based |
| Time Slots | Flexible | 30-min fixed |
| Booking Window | Anytime | 3 days max |
| Table Sizes | N/A | 2, 4, 6 |
| Conversation | Open | Guided flow |
| Voice Features | ❌ | ✅ TTS enabled |
| Personalization | Basic | Full history |
| Multi-booking | ❌ | ✅ Loop enabled |
| Reservation ID | Numbers | TT prefix |

---

## 🎯 For Sarvam AI Submission

### Which Version to Submit?

**Option 1**: Submit both versions
- Show versatility
- Original = general agent
- Table Turner = specific flow

**Option 2**: Submit Table Turner only
- Shows you can follow exact specs
- Demonstrates attention to detail
- Production-ready flow

**Recommended**: Submit **both** and explain the differences in your README

---

## 📝 Quick Reference

### Run Original:
```bash
python3 -m streamlit run app.py
```

### Run Table Turner:
```bash
python3 -m streamlit run app_table_turner.py
```

### Both use same:
- `.env` file (API key)
- `requirements.txt` (dependencies)
- Gemini 1.5 Flash (LLM)

---

## 🔊 Voice Features

### Text-to-Speech
- Currently uses ResponsiveVoice (browser-based)
- Click 🔊 icon on any message
- Reads message aloud
- Works in all modern browsers

### Voice Input (Placeholder)
- UI button ready
- Needs Web Speech API implementation
- Coming in next version

---

## 🐛 Troubleshooting

### "streamlit: command not found"
→ Use: `python3 -m streamlit run app_table_turner.py`

### "No module named 'streamlit'"
→ Run: `pip install -r requirements.txt`

### "API Key Error"
→ Check `.env` file has: `GEMINI_API_KEY=your_key`

### Voice not working
→ Make sure you're using HTTPS or localhost
→ Browser may block audio without user interaction

---

## 📦 Files Created

✅ `app_table_turner.py` - Enhanced UI with new flow  
✅ `data/table_turner_db.py` - User & time slot database  
✅ `agent/table_turner_agent.py` - Agent with guided flow  
✅ `TABLE_TURNER_README.md` - This documentation  

---

## ✨ What's Next?

1. Test the new flow
2. Add more restaurants (currently 10)
3. Record demo video showing both versions
4. Update main README
5. Push to GitHub
6. Submit to Sarvam AI

---

**Run Table Turner now and see the enhanced flow in action! 🍽️**

```bash
python3 -m streamlit run app_table_turner.py
```
