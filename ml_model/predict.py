# import pandas as pd
# import numpy as np
# import joblib
# from data_preprocessor import DataPreprocessor

# class PredictionEngine:
#     def __init__(self, model_path='university_recommender_model.joblib'):
#         try:
#             self.model_data = joblib.load(model_path)
#             self.model = self.model_data['model']
#             self.feature_columns = self.model_data['feature_columns']
#             self.preprocessor = self.model_data['preprocessor']
#             self.data = self.preprocessor.data
#             print("✅ Prediction engine loaded successfully!")
#         except Exception as e:
#             print(f"❌ Error loading model: {e}")
#             raise
    
#     def _safe_float_conversion(self, value, default=0.0):
#         """Safely convert any value to float"""
#         try:
#             if pd.isna(value) or value == 'N/A' or value == '':
#                 return default
#             return float(value)
#         except (ValueError, TypeError):
#             return default
    
#     def _safe_bool_conversion(self, value, default=False):
#         """Safely convert any value to boolean"""
#         try:
#             if pd.isna(value) or value == 'N/A' or value == '':
#                 return default
#             return bool(value)
#         except (ValueError, TypeError):
#             return default
    
#     def get_top_recommendations(self, student_data, top_k=10):
#         """Get top program recommendations for a student"""
#         print(f"🔍 Finding top {top_k} recommendations...")
        
#         recommendations = []
        
#         for _, program in self.data.iterrows():
#             # Calculate match score
#             score = self._calculate_match_score(program, student_data)
            
#             # Get available intakes
#             available_intakes = []
#             if self._safe_bool_conversion(program.get('intake_spring', False)):
#                 available_intakes.append('Spring')
#             if self._safe_bool_conversion(program.get('intake_summer', False)):
#                 available_intakes.append('Summer')
#             if self._safe_bool_conversion(program.get('intake_fall', False)):
#                 available_intakes.append('Fall')
#             if self._safe_bool_conversion(program.get('intake_winter', False)):
#                 available_intakes.append('Winter')
            
#             recommendations.append({
#                 'program_id': program['program_id'],
#                 'university_name': program['university_name'],
#                 'program_name': program['program_name'],
#                 'field_of_study': program['field_of_study'],
#                 'specialization': program['specialization'],
#                 'country': program['country'],
#                 'city': program['city'],
#                 'university_type': program['university_type'],
#                 'world_ranking': self._safe_float_conversion(program['world_ranking']),
#                 'tuition_fee_usd': self._safe_float_conversion(program['tuition_fee_usd']),
#                 'course_duration_months': self._safe_float_conversion(program['course_duration_months']),
#                 'job_placement_rate': self._safe_float_conversion(program.get('job_placement_rate_clean', program.get('job_placement_rate', 50))),
#                 'available_intakes': available_intakes,  # NEW
#                 'score_percentage': int(score)
#             })
        
#         # Sort by score and return top programs
#         top_programs = sorted(recommendations, key=lambda x: x['score_percentage'], reverse=True)[:top_k]
        
#         print(f"✅ Found {len(top_programs)} recommendations")
#         return top_programs
    
#     def _calculate_match_score(self, program, student_data):
#         """Calculate overall match score (0-100)"""
#         score = 0
        
#         # Academic match (25 points)
#         score += self._calculate_academic_match(program, student_data) * 25
        
#         # Budget match (20 points)
#         score += self._calculate_budget_match(program, student_data) * 20
        
#         # Preference match (35 points)
#         score += self._calculate_preference_match(program, student_data) * 35
        
#         # English match (20 points)
#         score += self._calculate_english_match(program, student_data) * 20
        
#         return min(score, 100)
    
#     def _calculate_academic_match(self, program, student_data):
#         """Calculate academic compatibility (0-1)"""
#         try:
#             student_score = self._safe_float_conversion(student_data.get('academic_score', 0))
            
#             if student_data.get('score_type') == 'gpa':
#                 min_required = self._safe_float_conversion(program.get('min_gpa_clean', program.get('min_gpa', 2.5)))
#             else:
#                 min_required = self._safe_float_conversion(program.get('min_percentage_clean', program.get('min_percentage', 60)))
            
#             if student_score >= min_required:
#                 return 1.0
#             elif student_score >= min_required * 0.9:
#                 return 0.7
#             elif student_score >= min_required * 0.8:
#                 return 0.4
#             else:
#                 return 0.1
#         except Exception as e:
#             print(f"⚠️ Academic match error: {e}")
#             return 0.1
    
#     def _calculate_budget_match(self, program, student_data):
#         """Calculate budget compatibility (0-1)"""
#         try:
#             student_budget = self._safe_float_conversion(student_data.get('max_tuition_fee', 25000))
#             program_fee = self._safe_float_conversion(program.get('tuition_fee_usd', 0))
            
#             if program_fee <= student_budget:
#                 return 1.0
#             elif program_fee <= student_budget * 1.2:
#                 return 0.6
#             else:
#                 return 0.2
#         except Exception as e:
#             print(f"⚠️ Budget match error: {e}")
#             return 0.2
    
#     def _calculate_preference_match(self, program, student_data):
#         """Calculate preference compatibility (0-1)"""
#         try:
#             score = 0
            
#             # Field of study match (12 points)
#             program_field = str(program.get('field_of_study', '')).strip().lower()
#             student_field = str(student_data.get('field_of_study', '')).strip().lower()
            
#             if program_field == student_field:
#                 score += 0.35
            
#             # Duration match (9 points)
#             preferred_duration = student_data.get('course_duration', '2 years')
#             program_duration = self._safe_float_conversion(program.get('course_duration_months', 24))
            
#             duration_match = {
#                 '1 year': (0, 12),
#                 '1.5 years': (13, 20),
#                 '2 years': (21, 36)
#             }
            
#             if preferred_duration in duration_match:
#                 min_dur, max_dur = duration_match[preferred_duration]
#                 if min_dur <= program_duration <= max_dur:
#                     score += 0.25
            
#             # Location match (6 points)
#             program_country = str(program.get('country', '')).strip().lower()
#             student_country = str(student_data.get('country', '')).strip().lower()
            
#             if student_country and program_country == student_country:
#                 score += 0.15
                
#             program_city = str(program.get('city', '')).strip().lower()
#             student_city = str(student_data.get('city', '')).strip().lower()
            
#             if student_city and program_city == student_city:
#                 score += 0.08
                
#             # University Type Match (3 points)
#             program_type = str(program.get('university_type', '')).strip().lower()
#             student_type = str(student_data.get('university_type', '')).strip().lower()
            
#             if student_type and program_type == student_type:
#                 score += 0.1
#             elif student_type == 'both':
#                 score += 0.05
                
#             # Intake Match (NEW - 5 points)
#             student_intake = student_data.get('intake', '').lower()
#             if student_intake:
#                 program_intakes = []
#                 if self._safe_bool_conversion(program.get('intake_spring', False)):
#                     program_intakes.append('spring')
#                 if self._safe_bool_conversion(program.get('intake_summer', False)):
#                     program_intakes.append('summer')
#                 if self._safe_bool_conversion(program.get('intake_fall', False)):
#                     program_intakes.append('fall')
#                 if self._safe_bool_conversion(program.get('intake_winter', False)):
#                     program_intakes.append('winter')
                
#                 if student_intake in program_intakes:
#                     score += 0.15  # ×35 = 5.25 points
#                 elif student_intake == 'any':
#                     # If student is flexible, give partial points for any intake availability
#                     if program_intakes:
#                         score += 0.08
                
#             return min(score, 1.0)
#         except Exception as e:
#             print(f"⚠️ Preference match error: {e}")
#             return 0.3
    
#     def _calculate_english_match(self, program, student_data):
#         """Calculate English test compatibility (0-1)"""
#         try:
#             english_test = student_data.get('english_test', 'none')
            
#             if english_test == 'none':
#                 # Check if MOI is accepted
#                 moi_accepted = str(program.get('moi_accepted', 'No')).strip().lower()
#                 return 1.0 if moi_accepted == 'yes' else 0.3
#             else:
#                 student_score = self._safe_float_conversion(student_data.get('english_score', 0))
#                 test_requirements = {
#                     'ielts': self._safe_float_conversion(program.get('ielts_overall', 6.5)),
#                     'toefl': self._safe_float_conversion(program.get('toefl_overall', 90)),
#                     'pte': self._safe_float_conversion(program.get('pte_overall', 58)),
#                     'duolingo': self._safe_float_conversion(program.get('duolingo_overall', 110))
#                 }
                
#                 required_score = test_requirements.get(english_test, 6.5)
#                 return 1.0 if student_score >= required_score else 0.5
#         except Exception as e:
#             print(f"⚠️ English match error: {e}")
#             return 0.5

# # Test the prediction engine
# if __name__ == "__main__":
#     # Sample student data for testing
#     test_student = {
#         'academic_score': '3.2',
#         'score_type': 'gpa',
#         'english_test': 'ielts',
#         'english_score': '7.0',
#         'degree_level': "Master's",
#         'field_of_study': 'Computer Science',
#         'specialization': 'Data Science',
#         'max_tuition_fee': '30000',
#         'course_duration': '2 years',
#         'country': 'Germany',
#         'university_type': 'public',
#         'intake': 'fall'  # NEW FIELD
#     }
    
#     try:
#         engine = PredictionEngine()
#         recommendations = engine.get_top_recommendations(test_student, 5)
        
#         print("\n🏆 Top Recommendations:")
#         for i, rec in enumerate(recommendations):
#             print(f"{i+1}. {rec['program_name']} - {rec['university_name']}")
#             print(f"   Type: {rec['university_type']} | Intakes: {', '.join(rec['available_intakes'])}")
#             print(f"   Score: {rec['score_percentage']}% | Cost: ${rec['tuition_fee_usd']}")
#             print()
#     except Exception as e:
#         print(f"❌ Error: {e}")

import pandas as pd
import numpy as np
import joblib
from data_preprocessor import DataPreprocessor

class PredictionEngine:
    def __init__(self, model_path='university_recommender_model.joblib'):
        try:
            self.model_data = joblib.load(model_path)
            self.model = self.model_data['model']
            self.feature_columns = self.model_data['feature_columns']
            self.preprocessor = self.model_data['preprocessor']
            self.data = self.preprocessor.data
            print("✅ Prediction engine loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def _safe_float_conversion(self, value, default=0.0):
        """Safely convert any value to float"""
        try:
            if pd.isna(value) or value == 'N/A' or value == '':
                return default
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def _safe_bool_conversion(self, value, default=False):
        """Safely convert any value to boolean"""
        try:
            if pd.isna(value) or value == 'N/A' or value == '' or value is None:
                return default
            
            if isinstance(value, (bool, np.bool_)):
                return bool(value)
            
            if isinstance(value, (int, float, np.number)):
                return bool(value)
            
            if isinstance(value, str):
                value_lower = value.strip().lower()
                if value_lower in ['yes', 'true', '1', 'y']:
                    return True
                elif value_lower in ['no', 'false', '0', 'n']:
                    return False
            
            return bool(value)
        except (ValueError, TypeError):
            return default
    
    def get_top_recommendations(self, student_data, top_k=10):
        """Get top program recommendations for a student"""
        print(f"🔍 Finding top {top_k} recommendations...")
        
        recommendations = []
        
        for _, program in self.data.iterrows():
            # Calculate match score
            score = self._calculate_match_score(program, student_data)
            
            # Get available intakes - FIXED
            available_intakes = []
            
            # Use the preprocessed boolean values directly
            if self._safe_bool_conversion(program.get('intake_spring', False)):
                available_intakes.append('Spring')
            if self._safe_bool_conversion(program.get('intake_summer', False)):
                available_intakes.append('Summer')
            if self._safe_bool_conversion(program.get('intake_fall', False)):
                available_intakes.append('Fall')
            if self._safe_bool_conversion(program.get('intake_winter', False)):
                available_intakes.append('Winter')
            
            recommendations.append({
                'program_id': program['program_id'],
                'university_name': program['university_name'],
                'program_name': program['program_name'],
                'field_of_study': program['field_of_study'],
                'specialization': program['specialization'],
                'country': program['country'],
                'city': program['city'],
                'university_type': program['university_type'],
                'world_ranking': self._safe_float_conversion(program['world_ranking']),
                'tuition_fee_usd': self._safe_float_conversion(program['tuition_fee_usd']),
                'course_duration_months': self._safe_float_conversion(program['course_duration_months']),
                'job_placement_rate': self._safe_float_conversion(program.get('job_placement_rate_clean', program.get('job_placement_rate', 50))),
                'available_intakes': available_intakes,
                'score_percentage': int(score)
            })
        
        # Sort by score and return top programs
        top_programs = sorted(recommendations, key=lambda x: x['score_percentage'], reverse=True)[:top_k]
        
        print(f"✅ Found {len(top_programs)} recommendations")
        return top_programs
    
    def _calculate_match_score(self, program, student_data):
        """Calculate overall match score (0-100)"""
        score = 0
        
        # Academic match (25 points)
        score += self._calculate_academic_match(program, student_data) * 25
        
        # Budget match (20 points)
        score += self._calculate_budget_match(program, student_data) * 20
        
        # Preference match (35 points)
        score += self._calculate_preference_match(program, student_data) * 35
        
        # English match (20 points)
        score += self._calculate_english_match(program, student_data) * 20
        
        return min(score, 100)
    
    def _calculate_academic_match(self, program, student_data):
        """Calculate academic compatibility (0-1)"""
        try:
            student_score = self._safe_float_conversion(student_data.get('academic_score', 0))
            
            if student_data.get('score_type') == 'gpa':
                min_required = self._safe_float_conversion(program.get('min_gpa_clean', program.get('min_gpa', 2.5)))
            else:
                min_required = self._safe_float_conversion(program.get('min_percentage_clean', program.get('min_percentage', 60)))
            
            if student_score >= min_required:
                return 1.0
            elif student_score >= min_required * 0.9:
                return 0.7
            elif student_score >= min_required * 0.8:
                return 0.4
            else:
                return 0.1
        except Exception as e:
            print(f"⚠️ Academic match error: {e}")
            return 0.1
    
    def _calculate_budget_match(self, program, student_data):
        """Calculate budget compatibility (0-1)"""
        try:
            student_budget = self._safe_float_conversion(student_data.get('max_tuition_fee', 25000))
            program_fee = self._safe_float_conversion(program.get('tuition_fee_usd', 0))
            
            if program_fee <= student_budget:
                return 1.0
            elif program_fee <= student_budget * 1.2:
                return 0.6
            else:
                return 0.2
        except Exception as e:
            print(f"⚠️ Budget match error: {e}")
            return 0.2
    
    def _calculate_preference_match(self, program, student_data):
        """Calculate preference compatibility (0-1)"""
        try:
            score = 0
            
            # Field of study match (12 points)
            program_field = str(program.get('field_of_study', '')).strip().lower()
            student_field = str(student_data.get('field_of_study', '')).strip().lower()
            
            if program_field == student_field:
                score += 0.35
            
            # Duration match (9 points)
            preferred_duration = student_data.get('course_duration', '2 years')
            program_duration = self._safe_float_conversion(program.get('course_duration_months', 24))
            
            duration_match = {
                '1 year': (0, 12),
                '1.5 years': (13, 20),
                '2 years': (21, 36)
            }
            
            if preferred_duration in duration_match:
                min_dur, max_dur = duration_match[preferred_duration]
                if min_dur <= program_duration <= max_dur:
                    score += 0.25
            
            # Location match (6 points)
            program_country = str(program.get('country', '')).strip().lower()
            student_country = str(student_data.get('country', '')).strip().lower()
            
            if student_country and program_country == student_country:
                score += 0.15
                
            program_city = str(program.get('city', '')).strip().lower()
            student_city = str(student_data.get('city', '')).strip().lower()
            
            if student_city and program_city == student_city:
                score += 0.08
                
            # University Type Match (3 points)
            program_type = str(program.get('university_type', '')).strip().lower()
            student_type = str(student_data.get('university_type', '')).strip().lower()
            
            if student_type and program_type == student_type:
                score += 0.1
            elif student_type == 'both':
                score += 0.05
                
            # Intake Match (5 points)
            student_intake = student_data.get('intake', '').lower()
            if student_intake:
                program_intakes = []
                if self._safe_bool_conversion(program.get('intake_spring', False)):
                    program_intakes.append('spring')
                if self._safe_bool_conversion(program.get('intake_summer', False)):
                    program_intakes.append('summer')
                if self._safe_bool_conversion(program.get('intake_fall', False)):
                    program_intakes.append('fall')
                if self._safe_bool_conversion(program.get('intake_winter', False)):
                    program_intakes.append('winter')
                
                if student_intake in program_intakes:
                    score += 0.15
                elif student_intake == 'any':
                    if program_intakes:
                        score += 0.08
                
            return min(score, 1.0)
        except Exception as e:
            print(f"⚠️ Preference match error: {e}")
            return 0.3
    
    def _calculate_english_match(self, program, student_data):
        """Calculate English test compatibility (0-1)"""
        try:
            english_test = student_data.get('english_test', 'none')
            
            if english_test == 'none':
                moi_accepted = str(program.get('moi_accepted', 'No')).strip().lower()
                return 1.0 if moi_accepted == 'yes' else 0.3
            else:
                student_score = self._safe_float_conversion(student_data.get('english_score', 0))
                test_requirements = {
                    'ielts': self._safe_float_conversion(program.get('ielts_overall', 6.5)),
                    'toefl': self._safe_float_conversion(program.get('toefl_overall', 90)),
                    'pte': self._safe_float_conversion(program.get('pte_overall', 58)),
                    'duolingo': self._safe_float_conversion(program.get('duolingo_overall', 110))
                }
                
                required_score = test_requirements.get(english_test, 6.5)
                return 1.0 if student_score >= required_score else 0.5
        except Exception as e:
            print(f"⚠️ English match error: {e}")
            return 0.5

# Test the prediction engine
if __name__ == "__main__":
    test_student = {
        'academic_score': '3.2',
        'score_type': 'gpa',
        'english_test': 'ielts',
        'english_score': '7.0',
        'degree_level': "Master's",
        'field_of_study': 'Computer Science',
        'specialization': 'Data Science',
        'max_tuition_fee': '30000',
        'course_duration': '2 years',
        'country': 'Germany',
        'university_type': 'public',
        'intake': 'fall'
    }
    
    try:
        engine = PredictionEngine()
        recommendations = engine.get_top_recommendations(test_student, 5)
        
        print("\n🏆 Top Recommendations:")
        for i, rec in enumerate(recommendations):
            print(f"{i+1}. {rec['program_name']} - {rec['university_name']}")
            print(f"   Type: {rec['university_type']} | Intakes: {', '.join(rec['available_intakes'])}")
            print(f"   Score: {rec['score_percentage']}% | Cost: ${rec['tuition_fee_usd']}")
            print()
    except Exception as e:
        print(f"❌ Error: {e}")