from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Configuration
API_BASE_URL = "https://fleetbots-production.up.railway.app/api"
VIDEO_FOLDER = 'static/videos'
ALLOWED_EXTENSIONS = {'mp4', 'webm', 'ogg'}
app.config['VIDEO_FOLDER'] = VIDEO_FOLDER

# Ensure video folder exists
os.makedirs(VIDEO_FOLDER, exist_ok=True)

@app.route('/')
def index():
    """
    Homepage with video support.
    Returns the HTML template with video if available.
    """
    # Get first available video file
    video_file = next(
        (f for f in os.listdir(app.config['VIDEO_FOLDER']) 
        if f.split('.')[-1].lower() in ALLOWED_EXTENSIONS
    ), None)
    
    return render_template('index.html', video_file=video_file)

# Rover Control API Endpoints
@app.route('/api/session/start', methods=['POST'])
def start_session():
    response = requests.post(f"{API_BASE_URL}/session/start")
    return jsonify(response.json()), response.status_code

@app.route('/api/fleet/status', methods=['GET'])
def fleet_status():
    session_id = request.args.get('session_id')
    response = requests.get(f"{API_BASE_URL}/fleet/status?session_id={session_id}")
    return jsonify(response.json()), response.status_code

@app.route('/api/rover/<rover_name>/status', methods=['GET'])
def rover_status(rover_name):
    session_id = request.args.get('session_id')
    response = requests.get(f"{API_BASE_URL}/rover/{rover_name}/status?session_id={session_id}")
    return jsonify(response.json()), response.status_code

@app.route('/api/rover/<rover_name>/sensor-data', methods=['GET'])
def sensor_data(rover_name):
    session_id = request.args.get('session_id')
    response = requests.get(f"{API_BASE_URL}/rover/{rover_name}/sensor-data?session_id={session_id}")
    return jsonify(response.json()), response.status_code

@app.route('/api/rover/<rover_name>/battery', methods=['GET'])
def battery_level(rover_name):
    session_id = request.args.get('session_id')
    response = requests.get(f"{API_BASE_URL}/rover/{rover_name}/battery?session_id={session_id}")
    return jsonify(response.json()), response.status_code

@app.route('/api/rover/<rover_name>/coordinates', methods=['GET'])
def coordinates(rover_name):
    session_id = request.args.get('session_id')
    response = requests.get(f"{API_BASE_URL}/rover/{rover_name}/coordinates?session_id={session_id}")
    return jsonify(response.json()), response.status_code

@app.route('/api/rover/<rover_name>/move', methods=['POST'])
def move_rover(rover_name):
    session_id = request.args.get('session_id')
    direction = request.args.get('direction')
    response = requests.post(f"{API_BASE_URL}/rover/{rover_name}/move?session_id={session_id}&direction={direction}")
    return jsonify(response.json()), response.status_code

@app.route('/api/rover/<rover_name>/reset', methods=['POST'])
def reset_rover(rover_name):
    session_id = request.args.get('session_id')
    response = requests.post(f"{API_BASE_URL}/rover/{rover_name}/reset?session_id={session_id}")
    return jsonify(response.json()), response.status_code

@app.route('/api/rover/<rover_name>/task', methods=['POST'])
def assign_task(rover_name):
    session_id = request.args.get('session_id')
    task = request.args.get('task')
    response = requests.post(f"{API_BASE_URL}/rover/{rover_name}/task?session_id={session_id}&task={task}")
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(debug=True)