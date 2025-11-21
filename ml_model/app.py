from flask import Flask, request, jsonify
from flask_cors import CORS
from predict import PredictionEngine
import json

app = Flask(__name__)

# Configure CORS properly
CORS(app, 
     resources={
         r"/api/*": {
             "origins": ["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
             "methods": ["GET", "POST", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"]
         }
     })

# Load the ML model once at startup
try:
    prediction_engine = PredictionEngine()
    print("✅ ML Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading ML model: {e}")
    prediction_engine = None

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5174')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/api/recommend', methods=['POST', 'OPTIONS'])
def get_recommendations():
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
        
    if not prediction_engine:
        return jsonify({'error': 'ML model not loaded'}), 500
        
    try:
        # Get student data from frontend form
        student_data = request.json
        
        # Convert string numbers to floats
        processed_data = {}
        for key, value in student_data.items():
            if key in ['academic_score', 'english_score', 'max_tuition_fee']:
                try:
                    processed_data[key] = float(value) if value else 0.0
                except (ValueError, TypeError):
                    processed_data[key] = 0.0
            else:
                processed_data[key] = value
        
        # Validate required fields
        required_fields = ['academic_score', 'score_type', 'field_of_study', 'max_tuition_fee', 'university_type', 'intake']
        for field in required_fields:
            if field not in processed_data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Get recommendations from ML model
        recommendations = prediction_engine.get_top_recommendations(processed_data, top_k=10)
        
        # Calculate intake statistics
        intake_matches = len([r for r in recommendations if processed_data['intake'].lower() in [i.lower() for i in r['available_intakes']] or processed_data['intake'] == 'any'])
        
        response = jsonify({
            'success': True,
            'recommendations': recommendations,
            'summary': {
                'total_programs': len(recommendations),
                'average_score': sum(r['score_percentage'] for r in recommendations) / len(recommendations),
                'budget_friendly': len([r for r in recommendations if r['tuition_fee_usd'] <= processed_data['max_tuition_fee']]),
                'top_ranked': len([r for r in recommendations if r['world_ranking'] <= 100]),
                'public_universities': len([r for r in recommendations if r['university_type'] == 'Public']),
                'private_universities': len([r for r in recommendations if r['university_type'] == 'Private']),
                'intake_matches': intake_matches
            }
        })
        
        return _corsify_actual_response(response)
        
    except Exception as e:
        print(f"❌ Error in recommendation: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/fields', methods=['GET', 'OPTIONS'])
def get_available_fields():
    """Get available fields of study for dropdown"""
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
        
    try:
        if not prediction_engine:
            return jsonify({'error': 'ML model not loaded'}), 500
            
        fields = prediction_engine.data['field_of_study'].unique().tolist()
        response = jsonify({'fields': fields})
        return _corsify_actual_response(response)
    except Exception as e:
        print(f"❌ Error getting fields: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'model_loaded': prediction_engine is not None})

def _build_cors_preflight_response():
    response = jsonify({'status': 'OK'})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    print("🚀 Starting University Recommendation API...")
    print("📡 API will be available at: http://localhost:8000")
    app.run(debug=True, port=8000)