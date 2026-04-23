# -triply-

Triply is your all-in-one app for afforadble and authentic travel. Triply will prompt search for the cheapest option between flights with different airlines (Delta, United, American, etc), transportation with different ride share apps (Uber, Lyft, Bolt, Waymo, etc), and food delivery options (UberEats, DoorDash, Grubhub, etc.) to find the cheapest options and tailor it to the unique cultural recommendation that the app builds from your  user imput and create a unique user profile. 


# Triply

## Project Description
Triply is a Flask-based travel comparison demo app that helps users explore affordable travel options. The app allows users to enter trip details and receive simulated comparisons for flights, ride-share options, and local recommendations.

This project demonstrates:
- Flight comparison
- Ride-share comparison
- Local travel recommendations
- Flask web development
- Dynamic HTML rendering
- User form handling

**Important Note:**  
Current flight and ride-share data are simulated using random values for demonstration purposes. The project is structured so that real travel APIs can be connected later.

---

## Files

- `app.py`
  - Main Flask application
  - Handles routes, user input, and page rendering
  - Generates flight comparisons, ride-share comparisons, and recommendations

- `client.py`
  - Socket-based client prototype
  - Sends user destination input to the server

- `server.py`
  - Socket-based server prototype
  - Receives client input and returns a response

- `socket32.py`
  - Helper module for simplified socket creation

- `README.md`
  - Project documentation and setup instructions

---

## Requirements

Install Python 3 and Flask.

Install Flask:

```bash
pip install flask
