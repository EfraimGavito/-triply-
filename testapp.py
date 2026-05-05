"""
Triply - Flask Travel Comparison Demo App
----------------------------------------
This is a prototype travel app that demonstrates:
 
1. Flight comparison (with REAL data via SerpApi)
2. Ride-share comparison
3. Local recommendations
 
NOTE:
- Flight data now uses SerpApi for real-time results
- Ride data is still simulated (ready for API integration)
- Set SERPAPI_KEY environment variable to enable real flight data
"""
 
from flask import Flask, request, render_template_string
import random
import requests
import os

try:
    import anthropic
except ImportError:
    anthropic = None
 
# ---------------------------------------------------
# Flask App Initialization
# ---------------------------------------------------
app = Flask(__name__)
 
# ---------------------------------------------------
# API KEYS
# ---------------------------------------------------
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
 
# ---------------------------------------------------
# AIRPORT CODE VALIDATION
# ---------------------------------------------------
def is_valid_airport_code(code):
    """
    Validates that the airport code is a 3-letter IATA code.
    Returns True if valid, False otherwise.
    """
    if not code:
        return False
    
    code = code.strip().upper()
    
    # Must be exactly 3 letters
    if len(code) != 3:
        return False
    
    # Must contain only letters
    if not code.isalpha():
        return False
    
    return True
 
# ---------------------------------------------------
# Base HTML Layout
# Simple inline template for speed.
# In production, move this into templates/base.html
# ---------------------------------------------------
BASE_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Triply</title>
 
    <style>
        body {
            font-family: Arial;
            margin: 40px;
            background: #f5f7fb;
        }
 
        .card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,.08);
            margin: 15px 0;
        }
 
        table {
            width: 100%;
            border-collapse: collapse;
        }
 
        td, th {
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }
 
        .btn {
            background: #2563eb;
            color: white;
            padding: 10px 14px;
            border-radius: 8px;
            border: none;
            cursor: pointer;
        }
 
        .btn:hover {
            background: #1d4ed8;
        }
 
        input {
            padding: 8px;
            border-radius: 6px;
            border: 1px solid #ddd;
            margin: 5px 0;
        }
 
        .back-link {
            display: inline-block;
            margin: 10px 0;
            color: #2563eb;
            text-decoration: none;
        }
 
        .back-link:hover {
            text-decoration: underline;
        }
 
        .api-status {
            padding: 10px;
            border-radius: 6px;
            margin: 10px 0;
            font-size: 14px;
        }
 
        .api-status.enabled {
            background: #d1fae5;
            color: #065f46;
        }
 
        .api-status.disabled {
            background: #fee2e2;
            color: #991b1b;
        }
    </style>
</head>
 
<body>
    <h1>✈️ Triply</h1>
    {{ content|safe }}
</body>
</html>
"""
 
# ===================================================
# HOME PAGE
# ===================================================
@app.route("/", methods=["GET", "POST"])
def home():
    """
    GET  -> Show trip search form
    POST -> Process search request and show results
    """
 
    if request.method == "POST":
        form_data = request.form
        return flights_page(form_data)
 
    # API status indicator
    api_status = ""
    if SERPAPI_KEY:
        api_status = '<div class="api-status enabled">✓ SerpApi enabled - Real flight data active</div>'
    else:
        api_status = '<div class="api-status disabled">⚠ SerpApi key not set - Using simulated data. Set SERPAPI_KEY environment variable for real data.</div>'
 
    # Search form shown to user
    content = f"""
    <div class="card">
        <h2>Plan Your Trip</h2>
        
        {api_status}
 
        <form method="post">
 
            From (Airport Code):
            <input name="origin" 
                   placeholder="BOS" 
                   pattern="[A-Za-z]{{3}}" 
                   title="Enter a 3-letter airport code (e.g., BOS, LAX, JFK)"
                   maxlength="3"
                   style="text-transform: uppercase;"
                   required>
 
            To (Airport Code):
            <input name="dest" 
                   placeholder="LAX" 
                   pattern="[A-Za-z]{{3}}" 
                   title="Enter a 3-letter airport code (e.g., BOS, LAX, JFK)"
                   maxlength="3"
                   style="text-transform: uppercase;"
                   required>
 
            <br><br>
 
            Depart:
            <input type="date" name="date" required>
 
            Budget:
            <input name="budget" value="500" type="number">
 
            Preferences:
            <input name="pref"
                   placeholder="food, museums, nightlife">
 
            <br><br>
 
            <button class="btn">Search Trip</button>
        </form>
    </div>
    """
 
    return render_template_string(BASE_TEMPLATE, content=content)
 
 
# ===================================================
# FLIGHT ENGINE
# ===================================================
def sample_flights(
    origin,
    dest,
    date,
    budget,
    sort_by="value",
    max_price=None,
    nonstop=False
):
    """
    Fetches real flight data via SerpApi if API key is set.
    Falls back to simulated data if no API key.
    
    Replace/enhance with:
    - Amadeus API
    - Skyscanner API
    - Kiwi Tequila API
    """
 
    # Try to fetch real data if API key exists
    if SERPAPI_KEY:
        print(f"\n🔍 Fetching real flight data: {origin} → {dest} on {date}")
        flights = fetch_real_flights(origin, dest, date)
        
        if flights:
            print(f"✅ Found {len(flights)} real flights")
        else:
            print("⚠ SerpApi returned no results, falling back to simulated data")
            flights = generate_simulated_flights()
    else:
        print("⚠ No SERPAPI_KEY set, using simulated data")
        flights = generate_simulated_flights()
 
    # ----------------------------
    # Filters
    # ----------------------------
 
    if max_price:
        flights = [
            f for f in flights
            if f["price"] <= int(max_price)
        ]
 
    if nonstop:
        flights = [
            f for f in flights
            if f["layovers"] == 0
        ]
 
    # ----------------------------
    # Sorting Options
    # ----------------------------
 
    sort_map = {
        "value": "score",
        "price": "price",
        "time": "hours",
        "layovers": "layovers",
        "co2": "co2"
    }
 
    sort_key = sort_map.get(sort_by, "score")
    flights.sort(key=lambda x: x[sort_key])
 
    return flights
 
 
def fetch_real_flights(origin, dest, date):
    """
    Fetch real flight data from SerpApi
    """
    
    params = {
        "engine": "google_flights",
        "departure_id": origin.upper(),
        "arrival_id": dest.upper(),
        "outbound_date": date,
        "type": 2,  # One-way flights
        "currency": "USD",
        "hl": "en",
        "api_key": SERPAPI_KEY
    }
 
    try:
        response = requests.get(
            "https://serpapi.com/search",
            params=params,
            timeout=10
        )
 
        data = response.json()
 
        # Handle API errors
        if "error" in data:
            print(f"❌ SERPAPI ERROR: {data['error']}")
            return []
 
        # Flexible parsing - try multiple result locations
        all_results = (
            data.get("best_flights", []) +
            data.get("other_flights", [])
        )
 
        if not all_results:
            all_results = data.get("flights", [])
 
        if not all_results:
            print("❌ NO FLIGHTS RETURNED FROM API")
            return []
 
        flights = []
 
        for flight in all_results:
            
            price = flight.get("price") or 9999
 
            segments = flight.get("flights", [])
 
            airline = "Unknown"
            if segments:
                airline = segments[0].get("airline", "Unknown")
 
            layovers = max(len(segments) - 1, 0)
 
            duration = flight.get("total_duration", 0)
            hours = round(duration / 60, 1) if duration else 0
 
            co2 = flight.get("carbon_emissions", {}).get("this_flight", 0)
 
            # Composite ranking score
            score = (
                price +
                layovers * 40 +
                hours * 8 +
                co2 * 0.2
            )
 
            flights.append({
                "airline": airline,
                "price": price,
                "layovers": layovers,
                "hours": hours,
                "co2": co2,
                "score": score
            })
 
        return flights
 
    except Exception as e:
        print(f"❌ REQUEST FAILED: {e}")
        return []
 
 
def generate_simulated_flights():
    """
    Generate simulated flight data for demo purposes
    """
    
    airlines = [
        "Delta",
        "United",
        "American",
        "Southwest",
        "JetBlue",
        "Alaska"
    ]
 
    flights = []
 
    for airline in airlines:
 
        # Random demo values
        price = random.randint(120, 650)
        layovers = random.randint(0, 2)
        hours = random.randint(2, 12)
        co2 = random.randint(90, 420)
 
        # Composite ranking score
        score = (
            price +
            layovers * 40 +
            hours * 8 +
            co2 * 0.2
        )
 
        flights.append({
            "airline": airline,
            "price": price,
            "layovers": layovers,
            "hours": hours,
            "co2": co2,
            "score": score
        })
 
    return flights
 
 
# ===================================================
# FLIGHT RESULTS PAGE
# ===================================================
def flights_page(form_data):
    """
    Builds results page after search.
    """
 
    origin = form_data.get("origin", "").strip()
    dest = form_data.get("dest", "").strip()
    date = form_data.get("date")
    budget = form_data.get("budget")
 
    # Validate required fields
    if not origin or not dest or not date:
        return render_template_string(
            BASE_TEMPLATE,
            content='<div class="card"><h2>❌ Missing required fields</h2><p>Please provide origin, destination, and date.</p><a href="/" class="back-link">← Back to search</a></div>'
        )
 
    # Validate airport codes
    if not is_valid_airport_code(origin):
        return render_template_string(
            BASE_TEMPLATE,
            content=f'<div class="card"><h2>❌ Invalid Origin Airport Code</h2><p>"{origin}" is not a valid airport code. Please use 3-letter IATA codes (e.g., BOS, LAX, JFK).</p><a href="/" class="back-link">← Back to search</a></div>'
        )
    
    if not is_valid_airport_code(dest):
        return render_template_string(
            BASE_TEMPLATE,
            content=f'<div class="card"><h2>❌ Invalid Destination Airport Code</h2><p>"{dest}" is not a valid airport code. Please use 3-letter IATA codes (e.g., BOS, LAX, JFK).</p><a href="/" class="back-link">← Back to search</a></div>'
        )
 
    # Convert to uppercase for consistency
    origin = origin.upper()
    dest = dest.upper()
 
    sort_by = form_data.get("sort", "value")
    nonstop = True if form_data.get("nonstop") else False
 
    flights = sample_flights(
        origin=origin,
        dest=dest,
        date=date,
        budget=budget,
        sort_by=sort_by,
        max_price=form_data.get("max_price"),
        nonstop=nonstop
    )
 
    if not flights:
        return render_template_string(
            BASE_TEMPLATE,
            content='<div class="card">No flights found matching your criteria.<br><a href="/" class="back-link">← Back to search</a></div>'
        )
 
    best_flight = flights[0]
 
    # Build filter form with current values
    html = f"""
    <a href="/" class="back-link">← Back to search</a>
    
    <div class="card">
        <h2>Flight Results: {origin} → {dest}</h2>
        <p>Departure: {date}</p>
 
        <form method="post" style="margin: 15px 0;">
            <input type="hidden" name="origin" value="{origin}">
            <input type="hidden" name="dest" value="{dest}">
            <input type="hidden" name="date" value="{date}">
            <input type="hidden" name="budget" value="{budget}">
            <input type="hidden" name="pref" value="{form_data.get('pref', '')}">
            
            <label for="sort">Sort by:</label>
            <select name="sort" id="sort" onchange="this.form.submit()" style="padding: 8px; border-radius: 6px; border: 1px solid #ddd; margin-left: 10px;">
                <option value="value" {'selected' if sort_by == 'value' else ''}>Best Value</option>
                <option value="price" {'selected' if sort_by == 'price' else ''}>Price (Low to High)</option>
                <option value="layovers" {'selected' if sort_by == 'layovers' else ''}>Fewest Layovers</option>
                <option value="time" {'selected' if sort_by == 'time' else ''}>Shortest Duration</option>
                <option value="co2" {'selected' if sort_by == 'co2' else ''}>Lowest CO2</option>
            </select>
        </form>
 
        <table>
            <tr>
                <th>Airline</th>
                <th>Price</th>
                <th>Layovers</th>
                <th>Hours</th>
                <th>CO2</th>
            </tr>
    """
 
    for flight in flights:
 
        badge = ""
        if flight == best_flight:
            badge = " ⭐ Best Value"
 
        html += f"""
        <tr>
            <td>{flight["airline"]}{badge}</td>
            <td>${flight["price"]}</td>
            <td>{flight["layovers"]}</td>
            <td>{flight["hours"]}</td>
            <td>{flight["co2"]} kg</td>
        </tr>
        """
 
    html += "</table></div>"
 
    # Add other Triply sections
    html += rides_html(form_data)
    html += recommendations_html(
        destination=dest,
        preferences=form_data.get("pref", "")
    )
 
    return render_template_string(BASE_TEMPLATE, content=html)
 
 
# ===================================================
# RIDE SHARE ENGINE
# ===================================================
def rides_html(form_data):
    """
    Simulates ride-share comparison results with sorting.
    Ready for API integration with:
    - Uber API
    - Lyft API
    - Other ride-share providers
    """
 
    providers = ["Uber", "Lyft", "Bolt", "Waymo"]
 
    rides = []
 
    for company in providers:
        price = round(random.uniform(10, 35), 2)
        eta = random.randint(3, 12)
 
        rides.append({
            "company": company,
            "price": price,
            "eta": eta
        })
 
    # Get sort preference for rides
    ride_sort = form_data.get("ride_sort", "price")
    
    # Sort based on selection
    if ride_sort == "price":
        rides.sort(key=lambda x: x["price"])
    elif ride_sort == "eta":
        rides.sort(key=lambda x: x["eta"])
 
    best_ride = rides[0]
 
    html = f"""
    <div class="card">
        <h2>Ride Comparison</h2>
        
        <form method="post" style="margin: 15px 0;">
            <input type="hidden" name="origin" value="{form_data.get('origin', '')}">
            <input type="hidden" name="dest" value="{form_data.get('dest', '')}">
            <input type="hidden" name="date" value="{form_data.get('date', '')}">
            <input type="hidden" name="budget" value="{form_data.get('budget', '')}">
            <input type="hidden" name="pref" value="{form_data.get('pref', '')}">
            <input type="hidden" name="sort" value="{form_data.get('sort', 'value')}">
            
            <label for="ride_sort">Sort by:</label>
            <select name="ride_sort" id="ride_sort" onchange="this.form.submit()" style="padding: 8px; border-radius: 6px; border: 1px solid #ddd; margin-left: 10px;">
                <option value="price" {'selected' if ride_sort == 'price' else ''}>Lowest Price</option>
                <option value="eta" {'selected' if ride_sort == 'eta' else ''}>Fastest ETA</option>
            </select>
        </form>
        
        <table>
            <tr>
                <th>Provider</th>
                <th>ETA</th>
                <th>Price</th>
            </tr>
    """
 
    for ride in rides:
 
        badge = ""
        if ride == best_ride:
            if ride_sort == "price":
                badge = " 💸 Cheapest"
            elif ride_sort == "eta":
                badge = " ⚡ Fastest"
 
        html += f"""
        <tr>
            <td>{ride["company"]}{badge}</td>
            <td>{ride["eta"]} min</td>
            <td>${ride["price"]}</td>
        </tr>
        """
 
    html += "</table></div>"
 
    return html
 
 
# ===================================================
# LOCAL RECOMMENDATIONS
# ===================================================
def recommendations_html(destination, preferences):
    """
    Generates local travel ideas using Claude.
    """

    api_key = ANTHROPIC_API_KEY

    fallback_ideas = [
        "Ask a barista where locals actually eat nearby",
        "Look for a family-owned cafe away from the main tourist street",
        "Visit a neighborhood market instead of a chain shopping area",
        "Find a small live music venue or community arts space",
        "Take a walk through a residential neighborhood with local shops"
    ]

    if anthropic is not None and api_key:
        try:
            client = anthropic.Anthropic(api_key=api_key)

            prompt = f"""
You are Triply, a tasteful local travel recommendation assistant.

Give 5 specific, locally flavored recommendations for a traveler going to:
Destination: {destination}

Their interests are:
{preferences}

Avoid generic tourist advice. Suggest ideas that feel local, authentic, affordable, and culturally specific.
Return only a simple HTML unordered list with 5 <li> items.
Do not invent exact business names unless you are confident they are real.
"""

            message = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=500,
                temperature=0.8,
                system="You create concise, tasteful, locally grounded travel recommendations for Triply.",
                messages=[{"role": "user", "content": prompt}],
            )

            ideas_html = message.content[0].text

            return f"""
            <div class="card">
                <h2>Local Recommendations for {destination}</h2>
                <p>Based on your interests: {preferences}</p>
                {ideas_html}
            </div>
            """

        except Exception as e:
            print("Claude recommendations failed:", e)

    html = f"""
    <div class="card">
        <h2>Local Recommendations for {destination}</h2>
        <p>Based on your interests: {preferences}</p>
        <ul>
    """

    for item in fallback_ideas:
        html += f"<li>{item}</li>"

    html += "</ul></div>"

    return html

 
 
# ===================================================
# RUN APP
# ===================================================
if __name__ == "__main__":
    app.run(debug=True)
