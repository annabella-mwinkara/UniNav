# UniNav

<<<<<<< HEAD
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
=======
UniNav is a campus navigation and safety web application built with Flask featuring user authentication, real-time directions, interactive maps, and emergency panic alerts.

## Features
- **User Authentication**: Login/Register with password security and profile updates
- **Smart Navigation**: Real-time directions using GraphHopper API
- **Interactive Campus Maps**: OpenStreetMap integration with Leaflet.js
- **Emergency Safety**: SOS Panic button with email alerts and location tracking
- **Responsive Design**: Mobile-friendly interface with hamburger navigation
- **Location Services**: Browser geolocation integration

## Project Structure
```
app.py                # Main Flask application with authentication
requirements.txt      # Python dependencies
static/style.css      # Responsive CSS styles
templates/            # HTML templates (login, directions, maps)
users.json           # JSON-based user storage (auto-created)
.env                 # Environment variables (create manually)
```

## Complete Setup Guide (10 Steps)

### Step 1: Clone the Repository
```bash
git clone https://github.com/annabella-mwinkara/UniNav.git
cd UniNav
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Generate Flask Secret Key
```bash
python -c "import secrets; print('FLASK_SECRET_KEY=' + secrets.token_hex(32))"
```

### Step 5: Create Environment File
Create a `.env` file in the project root:
```env
FLASK_SECRET_KEY=your_generated_secret_key_from_step_4
GRAPHHOPPER_API_KEY=your_graphhopper_api_key
Serverlogin=your_gmail_address
app_p=your_gmail_app_password
```

### Step 6: Get GraphHopper API Key
1. Visit [GraphHopper](https://www.graphhopper.com/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add it to your `.env` file

### Step 7: Configure Email Settings (Optional - for Panic Alerts)
1. Enable 2-factor authentication on your Gmail account
2. Generate an app-specific password
3. Add your Gmail and app password to `.env`

### Step 8: Run the Application
```bash
python app.py
```

### Step 9: Access the Application
1. Open your browser
2. Navigate to `http://localhost:5000`
3. Create an account or login
4. Explore the navigation and maps features

### Step 10: Test Key Features
- **Authentication**: Register a new account and login
- **Navigation**: Use the Directions page to get routes
- **Maps**: View interactive campus maps
- **Panic Button**: Test the emergency alert system
- **Mobile**: Test responsive design on mobile devices

## User Guide

### Authentication
- **Register**: Enter name, email, and password on the home page
- **Login**: Use existing email and password
- **Profile Update**: Modify name and password after login

### Navigation
- **Get Directions**: Enter current location and destination
- **Use My Location**: Click button to auto-fill current coordinates
- **View on Map**: See route displayed on interactive map

### Safety Features
- **Panic Button**: Available on all pages
- **Location Tracking**: Automatically saves your location
- **Email Alerts**: Sends emergency notifications with location

## API Dependencies
- **GraphHopper**: For routing and geocoding services
- **OpenStreetMap**: For map tiles and geographical data
- **Leaflet.js**: For interactive map rendering

## Mobile Features
- Responsive design for all screen sizes
- Hamburger navigation menu
- Touch-friendly interface
- Optimized panic button for emergencies

## Troubleshooting

### Common Issues
1. **Session Errors**: Ensure `FLASK_SECRET_KEY` is set in `.env`
2. **No Directions**: Check your GraphHopper API key
3. **Email Fails**: Verify Gmail credentials and app password
4. **Map Not Loading**: Check internet connection and Leaflet.js CDN

### Development
- **Debug Mode**: App runs in debug mode by default
- **Port**: Default port is 5000
- **Database**: Uses JSON file storage (users.json)

## License
MIT License

>>>>>>> 439cd599701d80e8e97b2ce8360be51c6c504afc
