# from flask import Flask, request, jsonify
# from predict import PredictionEngine
# import json

# app = Flask(__name__)

# # ✅ REMOVE Flask CORS completely - let Nginx handle it
# # CORS(app, resources={...})

# # Load the ML model once at startup
# try:
#     prediction_engine = PredictionEngine()
#     print("✅ ML Model loaded successfully!")
# except Exception as e:
#     print(f"❌ Error loading ML model: {e}")
#     prediction_engine = None

# # ✅ REMOVE the @app.after_request decorator completely

# @app.route('/api/recommend', methods=['POST', 'OPTIONS'])
# def get_recommendations():
#     if request.method == 'OPTIONS':
#         # ✅ Simple response for OPTIONS - Nginx will add CORS headers
#         return jsonify({'status': 'OK'}), 200
        
#     if not prediction_engine:
#         return jsonify({'error': 'ML model not loaded'}), 500
        
#     try:
#         # Get student data from frontend form
#         student_data = request.json
        
#         # Convert string numbers to floats
#         processed_data = {}
#         for key, value in student_data.items():
#             if key in ['academic_score', 'english_score', 'max_tuition_fee']:
#                 try:
#                     processed_data[key] = float(value) if value else 0.0
#                 except (ValueError, TypeError):
#                     processed_data[key] = 0.0
#             else:
#                 processed_data[key] = value
        
#         # Validate required fields
#         required_fields = ['academic_score', 'score_type', 'field_of_study', 'max_tuition_fee', 'university_type', 'intake']
#         for field in required_fields:
#             if field not in processed_data:
#                 return jsonify({'error': f'Missing field: {field}'}), 400
        
#         # Get recommendations from ML model
#         recommendations = prediction_engine.get_top_recommendations(processed_data, top_k=10)
        
#         # Calculate intake statistics
#         intake_matches = len([r for r in recommendations if processed_data['intake'].lower() in [i.lower() for i in r['available_intakes']] or processed_data['intake'] == 'any'])
        
#         response = jsonify({
#             'success': True,
#             'recommendations': recommendations,
#             'summary': {
#                 'total_programs': len(recommendations),
#                 'average_score': sum(r['score_percentage'] for r in recommendations) / len(recommendations),
#                 'budget_friendly': len([r for r in recommendations if r['tuition_fee_usd'] <= processed_data['max_tuition_fee']]),
#                 'top_ranked': len([r for r in recommendations if r['world_ranking'] <= 100]),
#                 'public_universities': len([r for r in recommendations if r['university_type'] == 'Public']),
#                 'private_universities': len([r for r in recommendations if r['university_type'] == 'Private']),
#                 'intake_matches': intake_matches
#             }
#         })
        
#         return response
        
#     except Exception as e:
#         print(f"❌ Error in recommendation: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/fields', methods=['GET', 'OPTIONS'])
# def get_available_fields():
#     if request.method == 'OPTIONS':
#         return jsonify({'status': 'OK'}), 200
        
#     try:
#         if not prediction_engine:
#             return jsonify({'error': 'ML model not loaded'}), 500
            
#         fields = prediction_engine.data['field_of_study'].unique().tolist()
#         return jsonify({'fields': fields})
#     except Exception as e:
#         print(f"❌ Error getting fields: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/health', methods=['GET'])
# def health_check():
#     return jsonify({'status': 'healthy', 'model_loaded': prediction_engine is not None})

# if __name__ == '__main__':
#     print("🚀 Starting University Recommendation API...")
#     print("📡 API will be available at: http://localhost:8000")
#     app.run(debug=True, port=8000)

# app.py
# from flask import Flask, request, jsonify
# from predict import PredictionEngine
# import json

# app = Flask(__name__)

# # Load ML model
# try:
#     prediction_engine = PredictionEngine()
#     print("✅ ML Model loaded successfully!")
# except Exception as e:
#     print(f"❌ Error loading ML model: {e}")
#     prediction_engine = None

# @app.route('/api/recommend', methods=['POST', 'OPTIONS'])
# def get_recommendations():
#     if request.method == 'OPTIONS':
#         return jsonify({'status': 'OK'}), 200
        
#     if not prediction_engine:
#         return jsonify({'error': 'ML model not loaded'}), 500
        
#     try:
#         student_data = request.json
        
#         # Process data
#         processed_data = {}
#         for key, value in student_data.items():
#             if key in ['academic_score', 'english_score', 'max_tuition_fee', 'priority_1', 'priority_2', 'priority_3']:
#                 try:
#                     processed_data[key] = float(value) if value else 0.0
#                 except (ValueError, TypeError):
#                     processed_data[key] = 0.0
#             else:
#                 processed_data[key] = value
        
#         # Validate required fields
#         required_fields = ['academic_score', 'score_type', 'field_of_study', 'max_tuition_fee', 'priority_1', 'priority_2', 'priority_3']
#         for field in required_fields:
#             if field not in processed_data:
#                 return jsonify({'error': f'Missing field: {field}'}), 400
        
#         # Get recommendations
#         recommendations = prediction_engine.get_top_recommendations(processed_data, top_k=12)
        
#         # Calculate statistics
#         intake_matches = len([r for r in recommendations if processed_data['intake'].lower() in [i.lower() for i in r['available_intakes']] or processed_data['intake'] == 'any'])
        
#         response = jsonify({
#             'success': True,
#             'recommendations': recommendations,
#             'summary': {
#                 'total_programs': len(recommendations),
#                 'average_score': sum(r['score_percentage'] for r in recommendations) / len(recommendations),
#                 'budget_friendly': len([r for r in recommendations if r['tuition_fee_usd'] <= processed_data['max_tuition_fee']]),
#                 'top_ranked': len([r for r in recommendations if r['world_ranking'] <= 100]),
#                 'public_universities': len([r for r in recommendations if r['university_type'] == 'Public']),
#                 'private_universities': len([r for r in recommendations if r['university_type'] == 'Private']),
#                 'intake_matches': intake_matches
#             }
#         })
        
#         return response
        
#     except Exception as e:
#         print(f"❌ Error in recommendation: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/fields', methods=['GET', 'OPTIONS'])
# def get_available_fields():
#     if request.method == 'OPTIONS':
#         return jsonify({'status': 'OK'}), 200
        
#     try:
#         if not prediction_engine:
#             return jsonify({'error': 'ML model not loaded'}), 500
            
#         fields = prediction_engine.data['field_of_study'].unique().tolist()
#         return jsonify({'fields': fields})
#     except Exception as e:
#         print(f"❌ Error getting fields: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/specializations', methods=['GET', 'OPTIONS'])
# def get_specializations():
#     if request.method == 'OPTIONS':
#         return jsonify({'status': 'OK'}), 200
        
#     try:
#         if not prediction_engine:
#             return jsonify({'error': 'ML model not loaded'}), 500
            
#         specializations = prediction_engine.data['specialization'].dropna().unique().tolist()
#         return jsonify({'specializations': specializations})
#     except Exception as e:
#         print(f"❌ Error getting specializations: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/health', methods=['GET'])
# def health_check():
#     return jsonify({'status': 'healthy', 'model_loaded': prediction_engine is not None})

# if __name__ == '__main__':
#     print("🚀 Starting University Recommendation API...")
#     app.run(debug=True, port=8000)

from flask import Flask, request, jsonify
from predict import PredictionEngine
import json

app = Flask(__name__)
# working 
# ✅ COMPLETELY REMOVE ALL CORS HANDLING
# No flask_cors import, no CORS configuration

# Load the ML model once at startup
try:
    prediction_engine = PredictionEngine()
    print("✅ ML Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading ML model: {e}")
    prediction_engine = None

# ✅ REMOVE ALL after_request decorators and CORS handling

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    # ✅ REMOVE OPTIONS handling - Nginx will handle it
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
        
        return response
        
    except Exception as e:
        print(f"❌ Error in recommendation: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/fields', methods=['GET'])
def get_available_fields():
    try:
        if not prediction_engine:
            return jsonify({'error': 'ML model not loaded'}), 500
            
        fields = prediction_engine.data['field_of_study'].unique().tolist()
        return jsonify({'fields': fields})
    except Exception as e:
        print(f"❌ Error getting fields: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/specializations', methods=['GET'])
def get_specializations():
    try:
        if not prediction_engine:
            return jsonify({'error': 'ML model not loaded'}), 500
            
        specializations = prediction_engine.data['specialization'].dropna().unique().tolist()
        return jsonify({'specializations': specializations})
    except Exception as e:
        print(f"❌ Error getting specializations: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'model_loaded': prediction_engine is not None})

if __name__ == '__main__':
    print("🚀 Starting University Recommendation API...")
    print("📡 API will be available at: http://localhost:8001")
    app.run(debug=False, host='0.0.0.0', port=8001)