from flask import Flask, render_template, request, jsonify, session, redirect, url_for
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
                
                # Store route data in session for maps page
                session["last_route_coords"] = coords
                session["destination_coords"] = destination_coords
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


# ---------- Update Real-time Location ----------
@app.route("/update_location", methods=["POST"])
def update_location():
    """Update user's current location during navigation"""
    data = request.get_json()
    if data and "lat" in data and "lng" in data:
        location = f"{data['lat']},{data['lng']}"
        session["current_location"] = location
        session["last_location"] = location
        session["location_timestamp"] = datetime.now().isoformat()
        
        # Calculate distance to destination if available
        destination_coords = session.get("destination_coords")
        distance_to_destination = None
        
        if destination_coords:
            try:
                dest_lat, dest_lng = destination_coords.split(",")
                # Simple distance calculation (you might want to use a more accurate method)
                import math
                
                lat1, lng1 = float(data['lat']), float(data['lng'])
                lat2, lng2 = float(dest_lat), float(dest_lng)
                
                # Haversine formula for distance
                R = 6371000  # Earth's radius in meters
                phi1 = math.radians(lat1)
                phi2 = math.radians(lat2)
                delta_phi = math.radians(lat2 - lat1)
                delta_lambda = math.radians(lng2 - lng1)
                
                a = (math.sin(delta_phi/2) * math.sin(delta_phi/2) +
                     math.cos(phi1) * math.cos(phi2) *
                     math.sin(delta_lambda/2) * math.sin(delta_lambda/2))
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
                
                distance_to_destination = R * c  # Distance in meters
                
            except Exception as e:
                print(f"Error calculating distance: {e}")
        
        return jsonify({
            "status": "ok",
            "distance_to_destination": distance_to_destination,
            "timestamp": session["location_timestamp"]
        })
    
    return jsonify({"status": "error", "message": "Invalid location data"}), 400


# ---------- Get Current Location ----------
@app.route("/get_current_location", methods=["GET"])
def get_current_location():
    """Get the user's last known location"""
    current_location = session.get("current_location")
    timestamp = session.get("location_timestamp")
    
    if current_location:
        lat, lng = current_location.split(",")
        return jsonify({
            "status": "ok",
            "location": {
                "lat": float(lat),
                "lng": float(lng)
            },
            "timestamp": timestamp
        })
    
    return jsonify({"status": "error", "message": "No location data available"}), 404


# ---------- Panic Button ----------
@app.route("/panic", methods=["POST"])
def panic():
    sender_name = session.get("name", "Unknown Student")
    sender_email = session.get("email", "unknown@example.com")
    last_location = session.get("last_location", "Not provided")
    current_location = session.get("current_location", last_location)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ✅ Always try to make Google Maps link
    maps_link = ","
    if current_location and "," in current_location:
        try:
            lat, lon = current_location.split(",")
            maps_link = f"https://maps.google.com/?q={lat.strip()},{lon.strip()}"
        except Exception as e:
            print("Error creating maps link:", e)

    # ✅ Build the panic email
    body = (
        f"🚨 Panic Alert!\n\n"
        f"👤 Name: {sender_name}\n"
        f"📧 Email: {sender_email}\n"
        f"📍 Current Location: {current_location}\n"
        f"🎯 Destination: {last_location}\n"
        f"🌍 Google Maps: {maps_link}\n"
        f"⏰ Time: {timestamp}\n"
    )
     

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


# ---------- MAPS ----------
@app.route("/maps")
def maps():
    # Get last route coordinates from session if available
    route_coords = session.get("last_route_coords", [])
    return render_template("maps.html", route_coords=route_coords)


# ---------- Navigation Mode ----------
@app.route("/navigate")
def navigate():
    """Real-time navigation page"""
    route_coords = session.get("last_route_coords", [])
    destination_coords = session.get("destination_coords")
    
    if not route_coords:
        return redirect(url_for('directions'))
    
    return render_template("navigate.html", 
                         route_coords=route_coords,
                         destination_coords=destination_coords)

   



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
