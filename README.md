# -triply-

Triply is your all-in-one app for afforadble and authentic travel. Triply will prompt search for the cheapest option between flights with different airlines (Delta, United, American, etc), transportation with different ride share apps (Uber, Lyft, Bolt, Waymo, etc), and food delivery options (UberEats, DoorDash, Grubhub, etc.) to find the cheapest options and tailor it to the unique cultural recommendation that the app builds from your  user imput and create a unique user profile. 


At this stage, the project currently includes:
- a socket-based client/server prototype
- a basic Flask web interface prototype
- code structure for future travel price and recommendation features

The current socket implementation allows a user to enter a destination in the client, send that destination to the server, and receive a response back from the server. This demonstrates communication between different parts of the application.

## Files
- `client.py` — asks the user for a destination and sends it to the server
- `server.py` — receives the destination and sends back a response
- `socket32.py` — custom socket helper used by the client and server
- `README.md` — project documentation

## Requirements / Setup
This project requires:
- Python 3
- Flask installed for the web interface

Install Flask with:

```bash
pip install flask
