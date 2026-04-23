"""
Triply - Flask Travel Comparison Demo App
----------------------------------------
This is a prototype travel app that demonstrates:

1. Flight comparison
2. Ride-share comparison
3. Local recommendations

NOTE:
Current flight + ride data is simulated using random values.
This structure is designed so real APIs can be plugged in later.
"""

from flask import Flask, request, render_template_string
import random

# ---------------------------------------------------
# Flask App Initialization
# ---------------------------------------------------
app = Flask(__name__)

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

    # Search form shown to user
    content = """
    <div class="card">
        <h2>Plan Your Trip</h2>

        <form method="post">

            From:
            <input name="origin" required>

            To:
            <input name="dest" required>

            <br><br>

            Depart:
            <input type="date" name="date" required>

            Budget:
            <input name="budget" value="500">

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
    budget,
    sort_by="value",
    max_price=None,
    nonstop=False
):
    """
    Simulates flight search results.

    Replace this function later with:
    - Amadeus API
    - Skyscanner API
    - Kiwi Tequila API
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


# ===================================================
# FLIGHT RESULTS PAGE
# ===================================================
def flights_page(form_data):
    """
    Builds results page after search.
    """

    sort_by = form_data.get("sort", "value")
    nonstop = True if form_data.get("nonstop") else False

    flights = sample_flights(
        origin=form_data["origin"],
        dest=form_data["dest"],
        budget=form_data["budget"],
        sort_by=sort_by,
        max_price=form_data.get("max_price"),
        nonstop=nonstop
    )

    if not flights:
        return render_template_string(
            BASE_TEMPLATE,
            content="<div class='card'>No flights found.</div>"
        )

    best_flight = flights[0]

    html = f"""
    <div class="card">

        <a href="/" class="btn" style="text-decoration:none;">
            ← New Flight Search
        </a>

        <br><br>

        <h2>Flight Results</h2>

        <!-- Ranking Dropdown -->
        <form method="post">

            <!-- Keep previous search values -->
            <input type="hidden" name="origin" value="{form_data['origin']}">
            <input type="hidden" name="dest" value="{form_data['dest']}">
            <input type="hidden" name="date" value="{form_data['date']}">
            <input type="hidden" name="budget" value="{form_data['budget']}">
            <input type="hidden" name="pref" value="{form_data.get('pref','')}">

            <label><b>Rank Flights By:</b></label>

            <select name="sort">
                <option value="value">Best Value</option>
                <option value="price">Lowest Price</option>
                <option value="time">Shortest Flight</option>
                <option value="layovers">Fewest Layovers</option>
                <option value="co2">Lowest CO2</option>
            </select>

            <button class="btn">Apply</button>
        </form>

        <br>

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
    ride_sort = form_data.get("ride_sort", "price")
    html += rides_html(ride_sort, form_data)
    html += recommendations_html(
        destination=form_data["dest"],
        preferences=form_data.get("pref", "")
    )

    return render_template_string(BASE_TEMPLATE, content=html)


# ===================================================
# RIDE SHARE ENGINE
# ===================================================
def rides_html(sort_by="price", form_data=None):
    """
    Simulates ride-share comparison results.
    """

    providers = ["Uber", "Lyft", "Bolt", "Waymo"]
    rides = []

    for company in providers:
        rides.append({
            "company": company,
            "price": round(random.uniform(10, 35), 2),
            "eta": random.randint(3, 12)
        })

    # Sort rides
    if sort_by == "eta":
        rides.sort(key=lambda x: x["eta"])
    else:
        rides.sort(key=lambda x: x["price"])

    best = rides[0]["company"]

    html = f"""
    <div class="card">

        <h2>Ride Comparison</h2>

        <form method="post">

            <!-- Preserve original search -->
            <input type="hidden" name="origin" value="{form_data['origin']}">
            <input type="hidden" name="dest" value="{form_data['dest']}">
            <input type="hidden" name="date" value="{form_data['date']}">
            <input type="hidden" name="budget" value="{form_data['budget']}">
            <input type="hidden" name="pref" value="{form_data.get('pref','')}">

            <label><b>Rank Rides By:</b></label>

            <select name="ride_sort">
                <option value="price">Lowest Price</option>
                <option value="eta">Fastest Arrival</option>
            </select>

            <button class="btn">Apply</button>
        </form>

        <br>

        <table>
            <tr>
                <th>Provider</th>
                <th>ETA</th>
                <th>Price</th>
            </tr>
    """

    for ride in rides:

        badge = " ⭐ Best" if ride["company"] == best else ""

        html += f"""
        <tr>
            <td>{ride['company']}{badge}</td>
            <td>{ride['eta']} min</td>
            <td>${ride['price']}</td>
        </tr>
        """

    html += "</table></div>"

    return html

    rides = []

    for company in providers:
        price = round(random.uniform(10, 35), 2)
        eta = random.randint(3, 12)

        rides.append({
            "company": company,
            "price": price,
            "eta": eta
        })

    rides.sort(key=lambda x: x["price"])
    cheapest = rides[0]["company"]

    for ride in rides:

        badge = ""
        if ride["company"] == cheapest:
            badge = " 💸 Cheapest"

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
    Generates local travel ideas.
    """

    ideas = [
        "Hidden taco stand",
        "Local jazz bar",
        "Street art district",
        "Family-owned cafe",
        "Budget museum pass",
        "Sunset viewpoint",
        "Walking food tour"
    ]

    random.shuffle(ideas)

    html = f"""
    <div class="card">
        <h2>Local Recommendations for {destination}</h2>
        <p>Based on your interests: {preferences}</p>
        <ul>
    """

    for item in ideas[:5]:
        html += f"<li>{item}</li>"

    html += "</ul></div>"

    return html


# ===================================================
# RUN APP
# ===================================================
if __name__ == "__main__":
    app.run(debug=True)