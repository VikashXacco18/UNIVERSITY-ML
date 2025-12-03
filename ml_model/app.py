# # app.py
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


# Working Before
# from flask import Flask, request, jsonify
# from predict import PredictionEngine
# import json

# app = Flask(__name__)
# # working  is odne 
# # ✅ COMPLETELY REMOVE ALL CORS HANDLING
# # No flask_cors import, no CORS configuration

# # Load the ML model once at startup
# try:
#     prediction_engine = PredictionEngine()
#     print("✅ ML Model loaded successfully!")
# except Exception as e:
#     print(f"❌ Error loading ML model: {e}")
#     prediction_engine = None

# # ✅ REMOVE ALL after_request decorators and CORS handling

# @app.route('/api/recommend', methods=['POST'])
# def get_recommendations():
#     # ✅ REMOVE OPTIONS handling - Nginx will handle it
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

# @app.route('/api/fields', methods=['GET'])
# def get_available_fields():
#     try:
#         if not prediction_engine:
#             return jsonify({'error': 'ML model not loaded'}), 500
            
#         fields = prediction_engine.data['field_of_study'].unique().tolist()
#         return jsonify({'fields': fields})
#     except Exception as e:
#         print(f"❌ Error getting fields: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/specializations', methods=['GET'])
# def get_specializations():
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
#     print("📡 API will be available at: http://localhost:8001")
#     app.run(debug=False, host='0.0.0.0', port=8000)


# New Codebase 
from flask import Flask, request, jsonify
from predict import PredictionEngine
import json

app = Flask(__name__)

# Load the ML model once at startup
try:
    prediction_engine = PredictionEngine()
    print("✅ ML Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading ML model: {e}")
    prediction_engine = None

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    if not prediction_engine:
        return jsonify({'error': 'ML model not loaded'}), 500
        
    try:
        # Get student data from frontend
        student_data = request.json
        
        # Convert string numbers to floats/int
        processed_data = {}
        for key, value in student_data.items():
            if key in ['academic_score', 'english_score', 'max_tuition_fee']:
                try:
                    if value:
                        processed_data[key] = float(value)
                    else:
                        processed_data[key] = 0.0
                except (ValueError, TypeError):
                    processed_data[key] = 0.0
            elif key == 'course_duration':
                # Handle both array and string formats
                if isinstance(value, list) and len(value) > 0:
                    processed_data[key] = value[0]
                elif value:
                    processed_data[key] = value
                else:
                    processed_data[key] = '2 years'
            elif key == 'intake':
                # Handle both array and string formats
                if isinstance(value, list) and len(value) > 0:
                    processed_data[key] = value[0]
                elif value:
                    processed_data[key] = value
                else:
                    processed_data[key] = 'fall'
            elif key == 'university_type':
                # Map 'both' to empty string for filtering
                if value == 'both':
                    processed_data[key] = ''
                else:
                    processed_data[key] = value
            elif key in ['country', 'city']:
                processed_data[key] = str(value).strip()
            else:
                processed_data[key] = value
        
        # Ensure required fields
        required_fields = ['field_of_study', 'max_tuition_fee']
        for field in required_fields:
            if field not in processed_data:
                processed_data[field] = ''
        
        print(f"📝 Processing request with data: {json.dumps(processed_data, indent=2)}")
        
        # Get recommendations
        recommendations = prediction_engine.get_top_recommendations(processed_data, top_k=10)
        
        # Calculate statistics
        total_programs = len(recommendations)
        if total_programs > 0:
            avg_score = sum(r['score_percentage'] for r in recommendations) / total_programs
            budget_friendly = len([r for r in recommendations if r['tuition_fee_usd'] <= processed_data.get('max_tuition_fee', 25000)])
            top_ranked = len([r for r in recommendations if r['world_ranking'] <= 100])
            public_unis = len([r for r in recommendations if r['university_type'] == 'Public'])
            private_unis = len([r for r in recommendations if r['university_type'] == 'Private'])
            
            # Count intake matches
            student_intake = processed_data.get('intake', 'fall').lower()
            intake_matches = len([
                r for r in recommendations 
                if student_intake == 'any' or student_intake in [i.lower() for i in r['available_intakes']]
            ])
        else:
            avg_score = 0
            budget_friendly = 0
            top_ranked = 0
            public_unis = 0
            private_unis = 0
            intake_matches = 0
        
        response = {
            'success': True,
            'recommendations': recommendations,
            'summary': {
                'total_programs': total_programs,
                'average_score': round(avg_score, 1),
                'budget_friendly': budget_friendly,
                'top_ranked': top_ranked,
                'public_universities': public_unis,
                'private_universities': private_unis,
                'intake_matches': intake_matches
            }
        }
        
        print(f"✅ Generated {total_programs} recommendations")
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Error in recommendation: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/fields', methods=['GET'])
def get_available_fields():
    try:
        if not prediction_engine:
            return jsonify({'error': 'ML model not loaded'}), 500
            
        # Get unique fields from data
        fields = prediction_engine.data['field_of_study'].dropna().unique().tolist()
        fields = [str(f).strip() for f in fields if f and str(f).strip()]
        
        # Sort and deduplicate
        fields = sorted(list(set(fields)))
        
        return jsonify({'fields': fields})
    except Exception as e:
        print(f"❌ Error getting fields: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/specializations', methods=['GET'])
def get_specializations():
    try:
        if not prediction_engine:
            return jsonify({'error': 'ML model not loaded'}), 500
            
        # Get unique specializations
        specializations = prediction_engine.data['specialization'].dropna().unique().tolist()
        specializations = [str(s).strip() for s in specializations if s and str(s).strip()]
        
        # Sort and deduplicate
        specializations = sorted(list(set(specializations)))
        
        return jsonify({'specializations': specializations})
    except Exception as e:
        print(f"❌ Error getting specializations: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'model_loaded': prediction_engine is not None,
        'programs_loaded': len(prediction_engine.data) if prediction_engine else 0
    })

@app.route('/api/program/<program_id>', methods=['GET'])
def get_program_details(program_id):
    try:
        if not prediction_engine:
            return jsonify({'error': 'ML model not loaded'}), 500
            
        # Find program by ID
        program = prediction_engine.data[prediction_engine.data['program_id'] == program_id].iloc[0].to_dict()
        
        # Format response
        response = {
            'program_id': program.get('program_id'),
            'university_name': program.get('university_name'),
            'program_name': program.get('program_name'),
            'description': program.get('program_highlights', 'N/A'),
            'requirements': {
                'min_gpa': program.get('min_gpa'),
                'min_percentage': program.get('min_percentage'),
                'ielts': program.get('ielts_overall'),
                'toefl': program.get('toefl_overall'),
                'gre_required': program.get('gre_required'),
                'gmat_required': program.get('gmat_required'),
                'work_experience': program.get('work_experience_required')
            },
            'fees': {
                'tuition_usd': program.get('tuition_fee_usd'),
                'application_fee': program.get('application_fee_eur'),
                'living_cost': program.get('living_cost_estimate_eur')
            },
            'details': {
                'duration_months': program.get('course_duration_months'),
                'placement_rate': program.get('job_placement_rate'),
                'visa_success_rate': program.get('visa_success_rate'),
                'commission_rate': program.get('commission_rate'),
                'website': program.get('program_website')
            }
        }
        
        return jsonify(response)
    except Exception as e:
        print(f"❌ Error getting program details: {e}")
        return jsonify({'error': 'Program not found'}), 404

if __name__ == '__main__':
    print("🚀 Starting University Recommendation API...")
    print("📡 API will be available at: http://localhost:8001")
    app.run(debug=True, host='0.0.0.0', port=8001)