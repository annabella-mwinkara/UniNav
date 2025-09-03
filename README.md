# UniNav

UniNav is a web-based navigation and safety application designed for university students. It provides walking directions, real-time location tracking, and a panic alert feature to enhance campus safety.

## Features

- **Login:** Simple login page for user identification.
- **Directions:** Get walking directions between locations using the GraphHopper API.
- **Maps:** Visualize routes on an interactive map.
- **Real-time Navigation:** Track your location and progress along a route.
- **Panic Button:** Instantly send a safety alert email with your location.

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd UniNav2\ (copy)
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Create a `.env` file in the project root with the following keys:
     ```
     FLASK_SECRET_KEY=your_secret_key
     GRAPHHOPPER_API_KEY=your_graphhopper_api_key
     Serverlogin=your_gmail_address
     app_p=your_gmail_app_password
     ```

4. **Run the app:**
   ```bash
   python app.py
   ```

## Usage

- Open the app in your browser at `http://localhost:5000`.
- Log in with your name and email.
- Enter your current location and destination to get directions.
- Use the navigation mode for real-time tracking.
- Press the panic button to send a safety alert email with your location.

## Technologies

- Python (Flask)
- GraphHopper API
- HTML/CSS/JavaScript
- SMTP (Gmail) for email alerts

## License

This project is for educational purposes.
