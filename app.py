from flask import Flask, render_template, request, jsonify, session
import requests
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')  # Get secret key from environment variable

GRAPHOPPER_API_KEY = os.getenv('GRAPHHOPPER_API_KEY')


# ---------- Helper function to geocode ----------
def get_coordinates(location):
    """Convert a place name or 'lat,lon' string into coordinates."""
    # If already in "lat,lon" format
    if "," in location:
        try:
            lat, lon = location.split(",")
            return f"{lat.strip()},{lon.strip()}"
        except:
            return None

    # Otherwise, use GraphHopper Geocoding API
    geo_url = f"https://graphhopper.com/api/1/geocode?q={location}&locale=en&key={GRAPHOPPER_API_KEY}"
    response = requests.get(geo_url).json()

    if "hits" in response and len(response["hits"]) > 0:
        lat = response["hits"][0]["point"]["lat"]
        lon = response["hits"][0]["point"]["lng"]
        return f"{lat},{lon}"

    return None


# ---------- Login Page ----------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form["name"]
        session["email"] = request.form["email"]

    return render_template("login.html", session=session)


@app.route("/directions", methods=["GET", "POST"])
def directions():
    directions_list = []
    summary = None
    coords = []

    if request.method == "POST":
        current = request.form.get("current")
        destination = request.form.get("destination")

        current_coords = get_coordinates(current)
        destination_coords = get_coordinates(destination)

        if not current_coords or not destination_coords:
            directions_list = ["❌ Could not recognize one of the locations."]
        else:
            url = (f"https://graphhopper.com/api/1/route?"
                   f"point={current_coords}&point={destination_coords}"
                   f"&vehicle=foot&locale=en&key={GRAPHOPPER_API_KEY}&points_encoded=false")
            response = requests.get(url)
            data = response.json()

            if "paths" in data and len(data["paths"]) > 0:
                path = data["paths"][0]
                directions_list = [instr["text"] for instr in path["instructions"]]
                coords = path["points"]["coordinates"]
                distance_km = round(path["distance"] / 1000, 2)
                duration_min = round(path["time"] / 60000, 1)
                summary = {"distance_km": distance_km, "duration_min": duration_min}
            else:
                directions_list = ["❌ Error fetching directions."]

    return render_template(
        "directions.html",
        directions=directions_list,
        summary=summary,
        route_coords=coords
    )


# ---------- Save GPS Location (AJAX from browser) ----------
@app.route("/save_location", methods=["POST"])
def save_location():
    data = request.get_json()
    if data and "location" in data:
        session["last_location"] = data["location"]
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 400


# ---------- Panic Button ----------
@app.route("/panic", methods=["POST"])
def panic():
    sender_name = session.get("name", "Unknown Student")
    sender_email = session.get("email", "unknown@example.com")
    last_location = session.get("last_location", "Not provided")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ✅ Always try to make Google Maps link
    maps_link = ""
    if last_location and "," in last_location:
        try:
            lat, lon = last_location.split(",")
            maps_link = f"https://maps.google.com/?q={lat.strip()},{lon.strip()}"
        except Exception as e:
            print("Error creating maps link:", e)

    # ✅ Build the panic email
    body = (
        f"🚨 Panic Alert!\n\n"
        f"👤 Name: {sender_name}\n"
        f"📧 Email: {sender_email}\n"
        f"📍 Location: {last_location}\n"
    )
    if maps_link:
        body += f"🌍 Google Maps: {maps_link}\n"
    body += f"⏰ Time: {timestamp}"

    msg = MIMEText(body)
    msg["Subject"] = "🚨 UniNav Panic Alert"
    msg["From"] = "uninavalerts@gmail.com"
    msg["To"] = "annabella@aims.edu.gh"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(os.getenv("Serverlogin"), os.getenv("app_p"))
            server.sendmail("uninav.alerts@gmail.com", "annabella@aims.edu.gh", msg.as_string())
        return jsonify({"message": "🚨 Panic alert sent successfully!"})
    except Exception as e:
        return jsonify({"message": f"Error sending email: {e}"}), 500
    #.........................MAPS.......................................
@app.route("/maps")
def maps():
    # Get last route coordinates from session if available
    route_coords = session.get("last_route_coords", [])
    return render_template("maps.html", route_coords=route_coords)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
