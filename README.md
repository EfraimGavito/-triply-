# -triply-

Triply is your all-in-one app for afforadble and authentic travel. Triply will prompt search for the cheapest option between flights with different airlines (Delta, United, American, etc), transportation with different ride share apps (Uber, Lyft, Bolt, Waymo, etc), and include AI-powered local recommendations to find the cheapest options that tailor to the unique cultural experience based on your specific interests and inputs. 


This project demonstrates:
- Flight comparison
- Ride-share comparison
- Local travel recommendations
- Flask web development
- Dynamic HTML rendering
- User form handling


## Files
 
- `testapp.py`
  - Test version of the app that utilizes real flight data, AI-powered local recommendations, and simulated ride-share data due to Terms of Service limitations.
  - Is the current local host prototype and showcases how Triply will appear.

- `README.md`
  - Project documentation and setup instructions

---

## Requirements

1. Install Dependencies

Install required Python packages:

pip install flask requests anthropic
2. Set API Keys

Triply requires API keys for full functionality.

SerpApi (Flight Data)

Get a key from SerpApi and set:

Mac/Linux:

export SERPAPI_KEY="your_key_here"

Windows:

set SERPAPI_KEY=your_key_here
Anthropic (AI Recommendations)

Get a key from Anthropic and set:

Mac/Linux:

export ANTHROPIC_API_KEY="your_key_here"

Windows:

set ANTHROPIC_API_KEY=your_key_here
3. Run the App
python testapp.py

Then open your browser and go to:

http://127.0.0.1:5000
