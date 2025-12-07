from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# ✅ Fixed 9 team members
team_members = [
    "sujeesh", "jayasree", "Raji", "Eshewara", "sri",
    "Lakshmi", "yugesh", "prem", "srihitha"
]

TOTAL_MEMBERS = len(team_members)

# ✅ Store addresses
addresses = {}

# ✅ Store final secret santa assignments
assignments = {}

# ✅ Store who already viewed their result
players_who_spun = []

@app.route("/")
def home():
    return "🎁 Secret Santa Backend Running Successfully!"

# ✅ STEP 1: Submit Address
@app.route("/submit_address", methods=["POST"])
def submit_address():
    data = request.json
    name = data.get("name")
    address = data.get("address")

    if name not in team_members:
        return jsonify({"message": "❌ Invalid team member"})

    addresses[name] = address

    return jsonify({
        "message": f"✅ Address stored for {name}",
        "total_submitted": len(addresses),
        "total_required": TOTAL_MEMBERS
    })

# ✅ STEP 2: Generate Perfect Secret Santa Pairs (AUTO)
@app.route("/generate", methods=["POST"])
def generate_pairs():
    if len(addresses) < TOTAL_MEMBERS:
        return jsonify({
            "message": f"❌ Wait! Only {len(addresses)}/{TOTAL_MEMBERS} addresses submitted"
        })

    shuffled = team_members.copy()
    random.shuffle(shuffled)

    # ✅ PERFECT CIRCULAR ASSIGNMENT
    for i in range(len(shuffled)):
        giver = shuffled[i]
        receiver = shuffled[(i + 1) % len(shuffled)]
        assignments[giver] = receiver

    return jsonify({
        "message": "✅ Secret Santa pairs generated successfully!"
    })

# ✅ STEP 3: SPIN (Only shows already assigned result)
@app.route("/spin", methods=["POST"])
def spin():
    data = request.json
    player_name = data.get("name")

    if player_name in players_who_spun:
        return jsonify({
            "message": "❌ You already saw your Secret Santa"
        })

    if player_name not in assignments:
        return jsonify({
            "message": "❌ Pairs not generated yet"
        })

    selected_person = assignments[player_name]
    selected_address = addresses[selected_person]

    players_who_spun.append(player_name)

    return jsonify({
        "selected_name": selected_person,
        "selected_address": selected_address
    })


if __name__ == "__main__":
    app.run(debug=True)
