import os
from flask import Flask, render_template, jsonify, request
from algorithms import run_greedy_matching, run_optimal_matching

current_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(current_dir, "templates"),
    static_folder=os.path.join(current_dir, "static")
)

DEFAULT_INCIDENTS = [
    {"id": "INC-101", "desc": "Cardiac Arrest at City Mall", "urgency": 4, "required_type": "Ambulance", "location": [12, 35], "wait_time": 8},
    {"id": "INC-102", "desc": "Structural Factory Fire", "urgency": 4, "required_type": "Fire Engine", "location": [45, 60], "wait_time": 4},
    {"id": "INC-103", "desc": "Minor Traffic Collision", "urgency": 2, "required_type": "Police Patrol", "location": [20, 15], "wait_time": 15},
    {"id": "INC-104", "desc": "Pediatric Respiratory Crisis", "urgency": 3, "required_type": "Ambulance", "location": [30, 22], "wait_time": 10},
    {"id": "INC-105", "desc": "Residential Gas Flare", "urgency": 3, "required_type": "Fire Engine", "location": [50, 48], "wait_time": 5},
    {"id": "INC-106", "desc": "Public Order Disturbance", "urgency": 1, "required_type": "Police Patrol", "location": [15, 80], "wait_time": 25}
]

DEFAULT_RESOURCES = [
    {"id": "RES-A1", "name": "Medic-1 (Central Station)", "type": "Ambulance", "location": [10, 30], "available": True},
    {"id": "RES-A2", "name": "Medic-2 (North Clinic)", "type": "Ambulance", "location": [40, 30], "available": True},
    {"id": "RES-F1", "name": "Fire Tender-Alpha", "type": "Fire Engine", "location": [42, 58], "available": True},
    {"id": "RES-F2", "name": "Fire Tender-Beta", "type": "Fire Engine", "location": [10, 10], "available": True},
    {"id": "RES-P1", "name": "Cruiser-Unit 09", "type": "Police Patrol", "location": [18, 12], "available": True},
    {"id": "RES-P2", "name": "Cruiser-Unit 14", "type": "Police Patrol", "location": [55, 75], "available": True}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/run", methods=["POST"])
def run_algorithms():
    payload = request.get_json() or {}
    incidents = payload.get("incidents", DEFAULT_INCIDENTS)
    resources = payload.get("resources", DEFAULT_RESOURCES)
    
    greedy_res = run_greedy_matching(incidents, resources)
    optimal_res = run_optimal_matching(incidents, resources)
    
    return jsonify({
        "status": "success",
        "greedy": greedy_res,
        "optimal": optimal_res,
        "incidents": incidents,
        "resources": resources
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
