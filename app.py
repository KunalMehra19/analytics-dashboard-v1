import os
from flask import Flask, request, jsonify
from supabase import create_client
from dotenv import load_dotenv
from flask import render_template


from datetime import datetime

# 1. Install the library first: pip install flask-cors
from flask_cors import CORS 

app = Flask(__name__)
CORS(app) # This allows your HTML file to fetch data from the API

# Load keys from .env
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/track', methods=['POST'])
def track_activity():
    # Receive data from the "User"
    data = request.json
    
    # Validation: Ensure user_id and event_type exist
    if not data.get('user_id') or not data.get('event_type'):
        return jsonify({"error": "Missing user_id or event_type"}), 400

    # Send to Supabase Cloud
    try:
        response = supabase.table("user_activities").insert({
            "user_id": data['user_id'],
            "event_type": data['event_type'],
            "metadata": data.get('metadata', {})
        }).execute()
        return jsonify({"status": "success", "data": response.data}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/analytics/summary', methods=['GET'])
def get_analytics():
    try:
        # 1. Fetch all data from Supabase
        response = supabase.table("user_activities").select("*").execute()
        data = response.data

        if not data:
            return jsonify({"message": "No data found", "total": 0}), 200

        # 2. Calculate Professional Metrics
        total_events = len(data)
        unique_users = len(set(row['user_id'] for row in data))
        
        # Count occurrences of each event type
        event_counts = {}
        for row in data:
            etype = row['event_type']
            event_counts[etype] = event_counts.get(etype, 0) + 1

        # 3. Return a Structured Report
        return jsonify({
            "status": "success",
            "data_summary": {
                "total_activities": total_events,
                "unique_active_users": unique_users,
                "popular_actions": event_counts
            }
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/analytics/detailed', methods=['GET'])
def get_detailed_analytics():
    try:
        response = supabase.table("user_activities").select("*").execute()
        data = response.data
        
        # 1. Hourly Traffic
        hourly_map = {}
        for row in data:
            hour = row['created_at'][11:13] + ":00"
            hourly_map[hour] = hourly_map.get(hour, 0) + 1

        # 2. Funnel Counts
        searches = sum(1 for r in data if r['event_type'] == 'search')
        carts = sum(1 for r in data if r['event_type'] == 'add_to_cart')
        buys = sum(1 for r in data if r['event_type'] == 'checkout_success')

        # 3. MATCHING KEYS FOR FRONTEND
        return jsonify({
            "status": "success",
            "visual_data": {
                "line_chart_hourly_traffic": hourly_map,
                "funnel_conversion": {
                    "searches": searches,
                    "cart_adds": carts,
                    "purchases": buys
                },
                "overall_conversion_rate": f"{round((buys/searches)*100, 2) if searches > 0 else 0}%"
            },
            "user_insights": {
                "total_events": len(data),
                "unique_users": len(set(r['user_id'] for r in data))
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)