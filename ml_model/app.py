# # New Codebase 
# from flask import Flask, request, jsonify
# from predict import PredictionEngine
# import json

# app = Flask(__name__)

# # Load the ML model once at startup
# try:
#     prediction_engine = PredictionEngine()
#     print("✅ ML Model loaded successfully!")
# except Exception as e:
#     print(f"❌ Error loading ML model: {e}")
#     prediction_engine = None

# @app.route('/api/recommend', methods=['POST'])
# def get_recommendations():
#     if not prediction_engine:
#         return jsonify({'error': 'ML model not loaded'}), 500
        
#     try:
#         # Get student data from frontend
#         student_data = request.json
        
#         # Convert string numbers to floats/int
#         processed_data = {}
#         for key, value in student_data.items():
#             if key in ['academic_score', 'english_score', 'max_tuition_fee']:
#                 try:
#                     if value:
#                         processed_data[key] = float(value)
#                     else:
#                         processed_data[key] = 0.0
#                 except (ValueError, TypeError):
#                     processed_data[key] = 0.0
#             elif key == 'course_duration':
#                 # Handle both array and string formats
#                 if isinstance(value, list) and len(value) > 0:
#                     processed_data[key] = value[0]
#                 elif value:
#                     processed_data[key] = value
#                 else:
#                     processed_data[key] = '2 years'
#             elif key == 'intake':
#                 # Handle both array and string formats
#                 if isinstance(value, list) and len(value) > 0:
#                     processed_data[key] = value[0]
#                 elif value:
#                     processed_data[key] = value
#                 else:
#                     processed_data[key] = 'fall'
#             elif key == 'university_type':
#                 # Map 'both' to empty string for filtering
#                 if value == 'both':
#                     processed_data[key] = ''
#                 else:
#                     processed_data[key] = value
#             elif key in ['country', 'city']:
#                 processed_data[key] = str(value).strip()
#             else:
#                 processed_data[key] = value
        
#         # Ensure required fields
#         required_fields = ['field_of_study', 'max_tuition_fee']
#         for field in required_fields:
#             if field not in processed_data:
#                 processed_data[field] = ''
        
#         print(f"📝 Processing request with data: {json.dumps(processed_data, indent=2)}")
        
#         # Get recommendations
#         recommendations = prediction_engine.get_top_recommendations(processed_data, top_k=10)
        
#         # Calculate statistics
#         total_programs = len(recommendations)
#         if total_programs > 0:
#             avg_score = sum(r['score_percentage'] for r in recommendations) / total_programs
#             budget_friendly = len([r for r in recommendations if r['tuition_fee_usd'] <= processed_data.get('max_tuition_fee', 25000)])
#             top_ranked = len([r for r in recommendations if r['world_ranking'] <= 100])
#             public_unis = len([r for r in recommendations if r['university_type'] == 'Public'])
#             private_unis = len([r for r in recommendations if r['university_type'] == 'Private'])
            
#             # Count intake matches
#             student_intake = processed_data.get('intake', 'fall').lower()
#             intake_matches = len([
#                 r for r in recommendations 
#                 if student_intake == 'any' or student_intake in [i.lower() for i in r['available_intakes']]
#             ])
#         else:
#             avg_score = 0
#             budget_friendly = 0
#             top_ranked = 0
#             public_unis = 0
#             private_unis = 0
#             intake_matches = 0
        
#         response = {
#             'success': True,
#             'recommendations': recommendations,
#             'summary': {
#                 'total_programs': total_programs,
#                 'average_score': round(avg_score, 1),
#                 'budget_friendly': budget_friendly,
#                 'top_ranked': top_ranked,
#                 'public_universities': public_unis,
#                 'private_universities': private_unis,
#                 'intake_matches': intake_matches
#             }
#         }
        
#         print(f"✅ Generated {total_programs} recommendations")
#         return jsonify(response)
        
#     except Exception as e:
#         print(f"❌ Error in recommendation: {e}")
#         import traceback
#         traceback.print_exc()
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/fields', methods=['GET'])
# def get_available_fields():
#     try:
#         if not prediction_engine:
#             return jsonify({'error': 'ML model not loaded'}), 500
            
#         # Get unique fields from data
#         fields = prediction_engine.data['field_of_study'].dropna().unique().tolist()
#         fields = [str(f).strip() for f in fields if f and str(f).strip()]
        
#         # Sort and deduplicate
#         fields = sorted(list(set(fields)))
        
#         return jsonify({'fields': fields})
#     except Exception as e:
#         print(f"❌ Error getting fields: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/specializations', methods=['GET'])
# def get_specializations():
#     try:
#         if not prediction_engine:
#             return jsonify({'error': 'ML model not loaded'}), 500
            
#         # Get unique specializations
#         specializations = prediction_engine.data['specialization'].dropna().unique().tolist()
#         specializations = [str(s).strip() for s in specializations if s and str(s).strip()]
        
#         # Sort and deduplicate
#         specializations = sorted(list(set(specializations)))
        
#         return jsonify({'specializations': specializations})
#     except Exception as e:
#         print(f"❌ Error getting specializations: {e}")
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/health', methods=['GET'])
# def health_check():
#     return jsonify({
#         'status': 'healthy', 
#         'model_loaded': prediction_engine is not None,
#         'programs_loaded': len(prediction_engine.data) if prediction_engine else 0
#     })

# @app.route('/api/program/<program_id>', methods=['GET'])
# def get_program_details(program_id):
#     try:
#         if not prediction_engine:
#             return jsonify({'error': 'ML model not loaded'}), 500
            
#         # Find program by ID
#         program = prediction_engine.data[prediction_engine.data['program_id'] == program_id].iloc[0].to_dict()
        
#         # Format response
#         response = {
#             'program_id': program.get('program_id'),
#             'university_name': program.get('university_name'),
#             'program_name': program.get('program_name'),
#             'description': program.get('program_highlights', 'N/A'),
#             'requirements': {
#                 'min_gpa': program.get('min_gpa'),
#                 'min_percentage': program.get('min_percentage'),
#                 'ielts': program.get('ielts_overall'),
#                 'toefl': program.get('toefl_overall'),
#                 'gre_required': program.get('gre_required'),
#                 'gmat_required': program.get('gmat_required'),
#                 'work_experience': program.get('work_experience_required')
#             },
#             'fees': {
#                 'tuition_usd': program.get('tuition_fee_usd'),
#                 'application_fee': program.get('application_fee_eur'),
#                 'living_cost': program.get('living_cost_estimate_eur')
#             },
#             'details': {
#                 'duration_months': program.get('course_duration_months'),
#                 'placement_rate': program.get('job_placement_rate'),
#                 'visa_success_rate': program.get('visa_success_rate'),
#                 'commission_rate': program.get('commission_rate'),
#                 'website': program.get('program_website')
#             }
#         }
        
#         return jsonify(response)
#     except Exception as e:
#         print(f"❌ Error getting program details: {e}")
#         return jsonify({'error': 'Program not found'}), 404

# if __name__ == '__main__':
#     print("🚀 Starting University Recommendation API...")
#     print("📡 API will be available at: http://localhost:8001")
#     app.run(debug=True, host='0.0.0.0', port=8001)

from flask import Flask, request, jsonify
from predict import PredictionEngine
import json

app = Flask(__name__)

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
        student_data = request.json
        
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
                if isinstance(value, list) and len(value) > 0:
                    processed_data[key] = value[0]
                elif value:
                    processed_data[key] = value
                else:
                    processed_data[key] = '2 years'
            elif key == 'intake':
                if isinstance(value, list) and len(value) > 0:
                    processed_data[key] = value[0]
                elif value:
                    processed_data[key] = value
                else:
                    processed_data[key] = 'fall'
            elif key == 'university_type':
                if value == 'both':
                    processed_data[key] = ''
                else:
                    processed_data[key] = value
            elif key in ['country', 'city']:
                processed_data[key] = str(value).strip()
            else:
                processed_data[key] = value
        
        required_fields = ['field_of_study', 'max_tuition_fee']
        for field in required_fields:
            if field not in processed_data:
                processed_data[field] = ''
        
        print(f"📝 Processing request with data: {json.dumps(processed_data, indent=2)}")
        
        recommendations = prediction_engine.get_top_recommendations(processed_data, top_k=10)
        
        total_programs = len(recommendations)
        if total_programs > 0:
            avg_score = sum(r['score_percentage'] for r in recommendations) / total_programs
            budget_friendly = len([r for r in recommendations if r['tuition_fee_usd'] <= processed_data.get('max_tuition_fee', 25000)])
            top_ranked = len([r for r in recommendations if r['world_ranking'] <= 100])
            public_unis = len([r for r in recommendations if r['university_type'] == 'Public'])
            private_unis = len([r for r in recommendations if r['university_type'] == 'Private'])
            
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
            
        fields = prediction_engine.data['field_of_study'].dropna().unique().tolist()
        fields = [str(f).strip() for f in fields if f and str(f).strip()]
        fields = sorted(list(set(fields)))
        
        return jsonify({'fields': fields})
    except Exception as e:
        print(f"❌ Error getting fields: {e}")
        return jsonify({'error': str(e)}), 500
    
# @app.route('/api/specializations/<field>', methods=['GET'])
# def get_specializations_by_field(field):
#     """Get specializations filtered by field of study"""
#     try:
#         if not prediction_engine:
#             return jsonify({'error': 'ML model not loaded'}), 500
            
#         # Decode URL parameter
#         field = field.replace('+', ' ').strip()
        
#         # Filter programs by field of study
#         if field and field.lower() != 'all':
#             filtered_data = prediction_engine.data[
#                 prediction_engine.data['field_of_study'].astype(str).str.lower().str.contains(
#                     field.lower(), na=False
#                 )
#             ]
#         else:
#             filtered_data = prediction_engine.data
        
#         # Get unique specializations from filtered data
#         specializations = filtered_data['specialization'].dropna().unique().tolist()
#         specializations = [str(s).strip() for s in specializations if s and str(s).strip()]
        
#         # Remove "Unknown" and sort
#         specializations = [s for s in specializations if s.lower() != 'unknown']
#         specializations = sorted(list(set(specializations)))
        
#         return jsonify({
#             'field': field,
#             'specializations': specializations,
#             'count': len(specializations)
#         })
#     except Exception as e:
#         print(f"❌ Error getting specializations by field: {e}")
#         return jsonify({'error': str(e)}), 500
@app.route('/api/specializations/<field>', methods=['GET'])
def get_specializations_by_field(field):
    """Get specializations filtered by field of study"""
    try:
        if not prediction_engine:
            return jsonify({'error': 'ML model not loaded'}), 500
        
        # Decode URL parameter
        field = field.replace('+', ' ').strip().lower()
        
        # Filter programs by field of study
        filtered_programs = prediction_engine.data[
            prediction_engine.data['field_of_study'].astype(str).str.lower().str.contains(field, na=False)
        ]
        
        # Get unique specializations from filtered data
        specializations = filtered_programs['specialization'].dropna().unique().tolist()
        specializations = [str(s).strip() for s in specializations if s and str(s).strip()]
        
        # Remove "Unknown" and sort
        specializations = [s for s in specializations if s.lower() != 'unknown']
        specializations = sorted(list(set(specializations)))
        
        # If we have no specializations for this field, show generic ones
        if len(specializations) == 0:
            field_keywords = {
                'computer': ['Artificial Intelligence', 'Machine Learning', 'Data Science', 
                           'Software Engineering', 'Cybersecurity', 'Cloud Computing'],
                'business': ['Marketing', 'Finance', 'Management', 'Human Resources', 
                           'International Business', 'Entrepreneurship'],
                'engineering': ['Mechanical Engineering', 'Electrical Engineering', 
                              'Civil Engineering', 'Chemical Engineering', 'Aerospace'],
                'data': ['Data Analytics', 'Machine Learning', 'Big Data', 
                        'Data Engineering', 'Business Intelligence'],
                'finance': ['Financial Management', 'Investment Banking', 'Risk Management',
                          'Corporate Finance', 'Fintech'],
                'marketing': ['Digital Marketing', 'Brand Management', 'Market Research',
                            'Advertising', 'Social Media Marketing'],
                'science': ['Biotechnology', 'Chemistry', 'Physics', 'Mathematics',
                          'Environmental Science']
            }
            
            for keyword, specs in field_keywords.items():
                if keyword in field:
                    specializations = specs
                    break
        
        # Always include "any" as the first option
        specializations = ["any"] + specializations if specializations else ["any"]
        
        return jsonify({
            'field': field,
            'specializations': specializations,
            'count': len(specializations)
        })
    except Exception as e:
        print(f"❌ Error getting specializations by field: {e}")
        # Return empty array on error
        return jsonify({'specializations': ["any"]})    


@app.route('/api/specializations', methods=['GET'])
def get_specializations():
    """Get all specializations (for compatibility)"""
    try:
        if not prediction_engine:
            return jsonify({'error': 'ML model not loaded'}), 500
            
        specializations = prediction_engine.data['specialization'].dropna().unique().tolist()
        specializations = [str(s).strip() for s in specializations if s and str(s).strip()]
        specializations = [s for s in specializations if s.lower() != 'unknown']
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
            
        program = prediction_engine.data[prediction_engine.data['program_id'] == program_id].iloc[0].to_dict()
        
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