# Setup Guide

## Prerequisites

1. **Python 3.9 or higher**
   ```bash
   python --version  # Should show 3.9+
   ```

2. **pip package manager**
   ```bash
   pip --version
   ```

3. **Google Gemini API Key**
   - Visit [Google AI Studio](https://aistudio.google.com/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the generated key

## Installation Steps

### 1. Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd restaurant-reservation-agent

# Or download and extract the ZIP file
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit==1.31.1` - Web interface
- `google-generativeai==0.8.3` - Gemini API
- `python-dotenv==1.0.1` - Environment variables
- `pandas==2.2.0` - Data handling

### 4. Configure API Key

**Option A: Using .env file (Recommended)**

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your key
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env
```

**Option B: Set in UI**
- Start the app without .env
- Enter API key in the sidebar when prompted

**Option C: Environment variable**

```bash
# On Mac/Linux
export GEMINI_API_KEY=your_api_key_here

# On Windows (Command Prompt)
set GEMINI_API_KEY=your_api_key_here

# On Windows (PowerShell)
$env:GEMINI_API_KEY="your_api_key_here"
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will:
1. Start the Streamlit server
2. Automatically open your default browser
3. Navigate to `http://localhost:8501`

## Verification

### Test the Installation

Run the test script:
```bash
python test_agent.py
```

This will run several test scenarios and verify:
- API connection works
- Function calling is operational
- Database is accessible
- Agent responds correctly

### Expected Output

You should see:
```
🤖 Initializing Restaurant Reservation Agent...
✅ Agent initialized!

============================================================
📋 Test Scenario: Simple Restaurant Search
============================================================

👤 User: I'm looking for Italian restaurants in Koramangala
🤖 Assistant: [Response with Italian restaurants]
...
```

## Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: "Invalid API Key"

**Solution:**
1. Verify your API key is correct
2. Check for extra spaces or quotes
3. Generate a new key if needed

### Issue: Port 8501 already in use

**Solution:**
```bash
# Kill existing process
# On Mac/Linux:
lsof -ti:8501 | xargs kill -9

# On Windows:
netstat -ano | findstr :8501
taskkill /PID <PID_NUMBER> /F

# Or use a different port:
streamlit run app.py --server.port 8502
```

### Issue: Streamlit not opening browser

**Solution:**
```bash
streamlit run app.py --server.headless false
```

Then manually navigate to `http://localhost:8501`

### Issue: API rate limits

**Solution:**
- Free tier has rate limits
- Wait a few seconds between requests
- Consider upgrading to paid tier for production

## Development Setup

### Enable Hot Reload

Streamlit automatically reloads on file changes. To disable:
```bash
streamlit run app.py --server.fileWatcherType none
```

### Debug Mode

```bash
streamlit run app.py --logger.level debug
```

### Custom Configuration

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"

[server]
port = 8501
headless = false
```

## Deployment

### Local Network Access

```bash
streamlit run app.py --server.address 0.0.0.0
```

Now accessible at `http://your-local-ip:8501`

### Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for:
- Streamlit Cloud deployment
- Docker containerization
- AWS/GCP deployment
- Environment variables

## Next Steps

1. ✅ Verify installation works
2. ✅ Test with sample queries
3. ✅ Read the [README.md](../README.md)
4. ✅ Review [BUSINESS_STRATEGY.md](./BUSINESS_STRATEGY.md)
5. ✅ Explore the codebase
6. 🎬 Record your demo video

## Support

For issues:
1. Check this troubleshooting guide
2. Review error messages
3. Check API key validity
4. Ensure all dependencies installed
5. Try fresh virtual environment

## System Requirements

**Minimum:**
- Python 3.9
- 2GB RAM
- 500MB disk space
- Internet connection

**Recommended:**
- Python 3.10+
- 4GB RAM
- 1GB disk space
- Stable internet (for API calls)

## API Usage

**Free Tier Limits:**
- 60 requests per minute
- 1,500 requests per day
- Sufficient for testing and demo

**Cost:**
- Gemini 1.5 Flash is free for most use cases
- Check [Google AI pricing](https://ai.google.dev/pricing) for details

---

**Setup Complete! 🎉**

You're ready to use the GoodFoods AI Reservation Assistant!
