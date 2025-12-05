# import pandas as pd
# import numpy as np
# import joblib
# from data_preprocessor import DataPreprocessor

# class PredictionEngine:
#     def __init__(self, model_path='university_recommender_model.joblib'):
#         try:
#             print("🔧 Loading prediction engine...")
#             self.model_data = joblib.load(model_path)
#             self.model = self.model_data['model']
#             self.feature_columns = self.model_data['feature_columns']
#             self.preprocessor = self.model_data['preprocessor']
#             self.data = self.preprocessor.data
            
#             # Create a reference to original data for recommendations
#             self.programs_data = self.data.copy()
            
#             print("✅ Prediction engine loaded successfully!")
#             print(f"📊 Programs in database: {len(self.data)}")
#             print(f"📊 Available features: {len(self.feature_columns)}")
            
#         except Exception as e:
#             print(f"❌ Error loading model: {e}")
#             raise
    
#     def _safe_float_conversion(self, value, default=0.0):
#         """Safely convert any value to float"""
#         try:
#             if pd.isna(value) or value in ['N/A', 'nan', 'null', '', 'None']:
#                 return default
#             return float(value)
#         except (ValueError, TypeError):
#             return default
    
#     def _safe_bool_conversion(self, value, default=False):
#         """Safely convert any value to boolean"""
#         try:
#             if pd.isna(value) or value in ['N/A', 'nan', 'null', '', 'None']:
#                 return default
            
#             if isinstance(value, (bool, np.bool_)):
#                 return bool(value)
            
#             if isinstance(value, (int, float, np.number)):
#                 return bool(value)
            
#             if isinstance(value, str):
#                 value_lower = value.strip().lower()
#                 if value_lower in ['yes', 'true', '1', 'y']:
#                     return True
#                 elif value_lower in ['no', 'false', '0', 'n']:
#                     return False
            
#             return bool(value)
#         except (ValueError, TypeError):
#             return default

#     def get_top_recommendations(self, student_data, top_k=12):
#         """Get top program recommendations for a student"""
#         print(f"\n🔍 Getting recommendations for student...")
#         print(f"Student preferences: {student_data}")
        
#         recommendations = []
        
#         # Filter programs based on basic criteria first
#         filtered_programs = self.data.copy()
        
#         # Field of study filter
#         if 'field_of_study' in student_data and student_data['field_of_study']:
#             field = student_data['field_of_study'].strip().lower()
#             filtered_programs = filtered_programs[
#                 filtered_programs['field_of_study'].astype(str).str.lower().str.contains(field, na=False)
#             ]
        
#         # University type filter
#         if 'university_type' in student_data and student_data['university_type'] not in ['both', '']:
#             uni_type = student_data['university_type'].strip().lower()
#             if uni_type in ['public', 'private']:
#                 filtered_programs = filtered_programs[
#                     filtered_programs['university_type'].astype(str).str.lower() == uni_type
#                 ]
        
#         # Intake filter
#         if 'intake' in student_data and student_data['intake'] not in ['any', '']:
#             intake = student_data['intake'].strip().lower()
#             intake_col = f'intake_{intake}'
#             if intake_col in filtered_programs.columns:
#                 filtered_programs = filtered_programs[filtered_programs[intake_col] == True]
        
#         print(f"📊 Programs after filtering: {len(filtered_programs)}")
        
#         if len(filtered_programs) == 0:
#             print("⚠️ No programs match the filters, using all programs")
#             filtered_programs = self.data
        
#         # Calculate match scores for filtered programs
#         for _, program in filtered_programs.iterrows():
#             score = self._calculate_comprehensive_match_score(program, student_data)
            
#             # Get available intakes
#             available_intakes = []
#             for intake in ['spring', 'summer', 'fall', 'winter']:
#                 if self._safe_bool_conversion(program.get(f'intake_{intake}', False)):
#                     available_intakes.append(intake.capitalize())
            
#             # Get deadlines
#             deadline = self._get_nearest_deadline(program)
            
#             # Build recommendation
#             recommendation = {
#                 'program_id': program.get('program_id', f"program_{_}"),
#                 'university_name': program.get('university_name', 'Unknown University'),
#                 'program_name': program.get('program_name', 'Unknown Program'),
#                 'field_of_study': program.get('field_of_study', 'General'),
#                 'specialization': program.get('specialization', 'General'),
#                 'country': program.get('country', 'Unknown'),
#                 'city': program.get('city', 'Unknown'),
#                 'campus_location': program.get('city', 'Unknown'),
#                 'university_type': program.get('university_type', 'Public'),
#                 'world_ranking': int(self._safe_float_conversion(program.get('world_ranking', 500))),
#                 'tuition_fee_usd': int(self._safe_float_conversion(program.get('tuition_fee_usd', 25000))),
#                 'application_fee': int(self._safe_float_conversion(program.get('application_fee_eur', 0))),
#                 'course_duration_months': int(self._safe_float_conversion(program.get('course_duration_months', 24))),
#                 'job_placement_rate': int(self._safe_float_conversion(program.get('job_placement_rate', 50))),
#                 'visa_success_rate': int(self._safe_float_conversion(program.get('visa_success_rate', 70))),
#                 'available_intakes': available_intakes,
#                 'application_deadline': deadline,
#                 'scholarship_available': self._safe_bool_conversion(program.get('scholarships_available', True)),
#                 'course_link': program.get('program_website', program.get('university_website', '#')),
#                 'language_requirements': program.get('language_of_instruction', 'English'),
#                 'ielts_required': self._safe_float_conversion(program.get('ielts_overall', 6.5)),
#                 'toefl_required': self._safe_float_conversion(program.get('toefl_overall', 90)),
#                 'score_percentage': min(int(score * 100), 100),
#                 'commission_rate': self._safe_float_conversion(program.get('commission_rate', 10)),
#                 'partner_name': program.get('partner_name', 'Direct'),
#                 'program_highlights': program.get('program_highlights', 'N/A')
#             }
            
#             recommendations.append(recommendation)
        
#         # Sort by score and get top K
#         recommendations.sort(key=lambda x: x['score_percentage'], reverse=True)
#         top_programs = recommendations[:top_k]
        
#         print(f"✅ Found {len(top_programs)} recommendations")
#         return top_programs

#     def _calculate_comprehensive_match_score(self, program, student_data):
#         """Calculate match score with multiple factors"""
#         score = 0.0
#         factors = []
        
#         # 1. Academic match (30%)
#         academic_score = self._calculate_academic_match(program, student_data)
#         score += academic_score * 0.3
#         factors.append(('Academic', academic_score))
        
#         # 2. Budget match (25%)
#         budget_score = self._calculate_budget_match(program, student_data)
#         score += budget_score * 0.25
#         factors.append(('Budget', budget_score))
        
#         # 3. Location match (20%)
#         location_score = self._calculate_location_match(program, student_data)
#         score += location_score * 0.2
#         factors.append(('Location', location_score))
        
#         # 4. Course/Program match (15%)
#         course_score = self._calculate_course_match(program, student_data)
#         score += course_score * 0.15
#         factors.append(('Course', course_score))
        
#         # 5. English requirements match (10%)
#         english_score = self._calculate_english_match(program, student_data)
#         score += english_score * 0.1
#         factors.append(('English', english_score))
        
#         # Debug output
#         if len(program.get('program_id', '')) == 8:  # Show for one program
#             print(f"Program {program.get('program_id')}:")
#             for factor, factor_score in factors:
#                 print(f"  {factor}: {factor_score:.2f}")
#             print(f"  Total: {score:.2f}")
        
#         return score

#     def _calculate_academic_match(self, program, student_data):
#         """Calculate academic compatibility (0-1)"""
#         try:
#             student_score = self._safe_float_conversion(student_data.get('academic_score', 0))
            
#             if student_data.get('score_type', 'gpa') == 'gpa':
#                 min_required = self._safe_float_conversion(program.get('min_gpa', 2.5))
#                 # GPA on 4.0 scale
#                 if student_score >= min_required:
#                     return 1.0
#                 elif student_score >= min_required * 0.9:
#                     return 0.8
#                 elif student_score >= min_required * 0.8:
#                     return 0.6
#                 else:
#                     return 0.3
#             else:
#                 min_required = self._safe_float_conversion(program.get('min_percentage', 60))
#                 # Percentage
#                 if student_score >= min_required:
#                     return 1.0
#                 elif student_score >= min_required * 0.9:
#                     return 0.8
#                 elif student_score >= min_required * 0.8:
#                     return 0.6
#                 else:
#                     return 0.3
#         except Exception as e:
#             print(f"⚠️ Academic match error: {e}")
#             return 0.5

#     def _calculate_budget_match(self, program, student_data):
#         """Calculate budget compatibility (0-1)"""
#         try:
#             student_budget = self._safe_float_conversion(student_data.get('max_tuition_fee', 25000))
#             program_fee = self._safe_float_conversion(program.get('tuition_fee_usd', 25000))
            
#             if program_fee <= student_budget:
#                 return 1.0
#             elif program_fee <= student_budget * 1.1:
#                 return 0.8
#             elif program_fee <= student_budget * 1.2:
#                 return 0.6
#             elif program_fee <= student_budget * 1.5:
#                 return 0.4
#             else:
#                 return 0.2
#         except Exception as e:
#             print(f"⚠️ Budget match error: {e}")
#             return 0.5

#     def _calculate_location_match(self, program, student_data):
#         """Calculate location compatibility (0-1)"""
#         try:
#             score = 0.0
            
#             # Country match (70% of location score)
#             program_country = str(program.get('country', '')).strip().lower()
#             student_country = str(student_data.get('country', '')).strip().lower()
            
#             if student_country and program_country == student_country:
#                 score += 0.7
#             elif not student_country:  # No country preference
#                 score += 0.35
#             else:
#                 score += 0.1  # Different country
            
#             # City match (30% of location score)
#             program_city = str(program.get('city', '')).strip().lower()
#             student_city = str(student_data.get('city', '')).strip().lower()
            
#             if student_city and program_city == student_city:
#                 score += 0.3
            
#             return min(score, 1.0)
#         except Exception as e:
#             print(f"⚠️ Location match error: {e}")
#             return 0.5

#     def _calculate_course_match(self, program, student_data):
#         """Calculate course compatibility (0-1)"""
#         try:
#             score = 0.0
            
#             # Field of study match (40%)
#             program_field = str(program.get('field_of_study', '')).strip().lower()
#             student_field = str(student_data.get('field_of_study', '')).strip().lower()
            
#             if student_field and program_field and student_field in program_field:
#                 score += 0.4
            
#             # Specialization match (30%)
#             program_spec = str(program.get('specialization', '')).strip().lower()
#             student_spec = str(student_data.get('specialization', '')).strip().lower()
            
#             if student_spec and program_spec and student_spec in program_spec:
#                 score += 0.3
#             elif not student_spec:  # No specialization preference
#                 score += 0.15
            
#             # Duration match (30%)
#             if 'course_duration' in student_data and student_data['course_duration']:
#                 try:
#                     preferred_duration = str(student_data['course_duration']).strip().lower()
#                     program_duration = self._safe_float_conversion(program.get('course_duration_months', 24))
                    
#                     # Convert preferred duration to months
#                     duration_map = {
#                         '1 year': 12,
#                         '1.5 years': 18,
#                         '2 years': 24
#                     }
                    
#                     if preferred_duration in duration_map:
#                         preferred_months = duration_map[preferred_duration]
#                         diff = abs(program_duration - preferred_months)
                        
#                         if diff == 0:
#                             score += 0.3
#                         elif diff <= 6:
#                             score += 0.2
#                         elif diff <= 12:
#                             score += 0.1
#                 except:
#                     pass
            
#             return min(score, 1.0)
#         except Exception as e:
#             print(f"⚠️ Course match error: {e}")
#             return 0.5

#     def _calculate_english_match(self, program, student_data):
#         """Calculate English test compatibility (0-1)"""
#         try:
#             english_test = student_data.get('english_test', 'none').lower()
            
#             if english_test == 'none':
#                 # Check if medium of instruction accepted
#                 if 'moi_accepted' in program and self._safe_bool_conversion(program['moi_accepted'], False):
#                     return 1.0
#                 else:
#                     return 0.5
#             else:
#                 student_score = self._safe_float_conversion(student_data.get('english_score', 0))
                
#                 # Get required score based on test type
#                 test_requirements = {
#                     'ielts': self._safe_float_conversion(program.get('ielts_overall', 6.5)),
#                     'toefl': self._safe_float_conversion(program.get('toefl_overall', 90)),
#                     'pte': self._safe_float_conversion(program.get('pte_overall', 58)),
#                     'duolingo': self._safe_float_conversion(program.get('duolingo_overall', 110))
#                 }
                
#                 required_score = test_requirements.get(english_test, 6.5)
                
#                 if student_score >= required_score:
#                     return 1.0
#                 elif student_score >= required_score * 0.9:
#                     return 0.8
#                 elif student_score >= required_score * 0.8:
#                     return 0.6
#                 else:
#                     return 0.4
#         except Exception as e:
#             print(f"⚠️ English match error: {e}")
#             return 0.5

#     def _get_nearest_deadline(self, program):
#         """Get the nearest application deadline"""
#         try:
#             deadlines = {}
            
#             for intake in ['spring', 'summer', 'fall', 'winter']:
#                 deadline_col = f'{intake}_deadline'
#                 if deadline_col in program and pd.notna(program[deadline_col]):
#                     deadlines[intake] = str(program[deadline_col])
            
#             if deadlines:
#                 # Return the first deadline
#                 return next(iter(deadlines.values()))
#             else:
#                 return 'Varies'
#         except:
#             return 'Varies'

# # Test the prediction engine
# if __name__ == "__main__":
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
#         'city': '',
#         'university_type': 'both',
#         'intake': 'fall',
#         'priority_1': 'course',
#         'priority_2': 'budget',
#         'priority_3': 'location'
#     }
    
#     try:
#         engine = PredictionEngine()
#         recommendations = engine.get_top_recommendations(test_student, 5)
        
#         print("\n" + "="*50)
#         print("🏆 TOP RECOMMENDATIONS")
#         print("="*50)
        
#         for i, rec in enumerate(recommendations):
#             print(f"\n{i+1}. {rec['program_name']}")
#             print(f"   🎓 {rec['university_name']}")
#             print(f"   📍 {rec['city']}, {rec['country']} | 🏫 {rec['university_type']}")
#             print(f"   💰 ${rec['tuition_fee_usd']:,} | 📊 Score: {rec['score_percentage']}%")
#             print(f"   🏆 Rank: #{rec['world_ranking']} | 📅 Intakes: {', '.join(rec['available_intakes'])}")
            
#     except Exception as e:
#         print(f"❌ Error: {e}")
#         import traceback
#         traceback.print_exc()

import pandas as pd
import numpy as np
import joblib
from data_preprocessor import DataPreprocessor

class PredictionEngine:
    def __init__(self, model_path='university_recommender_model.joblib'):
        try:
            print("🔧 Loading prediction engine...")
            self.model_data = joblib.load(model_path)
            self.model = self.model_data['model']
            self.feature_columns = self.model_data['feature_columns']
            self.preprocessor = self.model_data['preprocessor']
            self.data = self.preprocessor.data
            
            self.programs_data = self.data.copy()
            
            print("✅ Prediction engine loaded successfully!")
            print(f"📊 Programs in database: {len(self.data)}")
            print(f"📊 Available features: {len(self.feature_columns)}")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def _safe_float_conversion(self, value, default=0.0):
        try:
            if pd.isna(value) or value in ['N/A', 'nan', 'null', '', 'None']:
                return default
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def _safe_bool_conversion(self, value, default=False):
        try:
            if pd.isna(value) or value in ['N/A', 'nan', 'null', '', 'None']:
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

    def get_top_recommendations(self, student_data, top_k=12):
        print(f"\n🔍 Getting recommendations for student...")
        print(f"Student preferences: {student_data}")
        
        recommendations = []
        
        filtered_programs = self.data.copy()
        
        if 'field_of_study' in student_data and student_data['field_of_study']:
            field = student_data['field_of_study'].strip().lower()
            filtered_programs = filtered_programs[
                filtered_programs['field_of_study'].astype(str).str.lower().str.contains(field, na=False)
            ]
        
        if 'university_type' in student_data and student_data['university_type'] not in ['both', '']:
            uni_type = student_data['university_type'].strip().lower()
            if uni_type in ['public', 'private']:
                filtered_programs = filtered_programs[
                    filtered_programs['university_type'].astype(str).str.lower() == uni_type
                ]
        
        if 'intake' in student_data and student_data['intake'] not in ['any', '']:
            intake = student_data['intake'].strip().lower()
            intake_col = f'intake_{intake}'
            if intake_col in filtered_programs.columns:
                filtered_programs = filtered_programs[filtered_programs[intake_col] == True]
        
        print(f"📊 Programs after filtering: {len(filtered_programs)}")
        
        if len(filtered_programs) == 0:
            print("⚠️ No programs match the filters, using all programs")
            filtered_programs = self.data
        
        for _, program in filtered_programs.iterrows():
            score = self._calculate_comprehensive_match_score(program, student_data)
            
            available_intakes = []
            for intake in ['spring', 'summer', 'fall', 'winter']:
                if self._safe_bool_conversion(program.get(f'intake_{intake}', False)):
                    available_intakes.append(intake.capitalize())
            
            recommendation = {
                'program_id': program.get('program_id', f"program_{_}"),
                'university_name': program.get('university_name', 'Unknown University'),
                'program_name': program.get('program_name', 'Unknown Program'),
                'field_of_study': program.get('field_of_study', 'General'),
                'specialization': program.get('specialization', 'General'),
                'country': program.get('country', 'Unknown'),
                'city': program.get('city', 'Unknown'),
                'campus_location': program.get('city', 'Unknown'),
                'university_type': program.get('university_type', 'Public'),
                'world_ranking': int(self._safe_float_conversion(program.get('world_ranking', 500))),
                'tuition_fee_usd': int(self._safe_float_conversion(program.get('tuition_fee_usd', 25000))),
                'application_fee': int(self._safe_float_conversion(program.get('application_fee_eur', 0))),
                'course_duration_months': int(self._safe_float_conversion(program.get('course_duration_months', 24))),
                'job_placement_rate': int(self._safe_float_conversion(program.get('job_placement_rate', 50))),
                'visa_success_rate': int(self._safe_float_conversion(program.get('visa_success_rate', 70))),
                'available_intakes': available_intakes,
                'application_deadline': 'Varies',
                'scholarship_available': self._safe_bool_conversion(program.get('scholarships_available', True)),
                'course_link': program.get('program_website', program.get('university_website', '#')),
                'language_requirements': 'English',
                'ielts_required': self._safe_float_conversion(program.get('ielts_overall', 6.5)),
                'toefl_required': self._safe_float_conversion(program.get('toefl_overall', 90)),
                'score_percentage': min(int(score * 100), 100),
                'commission_rate': 10,
                'partner_name': program.get('partner_name', 'Direct'),
                'program_highlights': 'N/A'
            }
            
            recommendations.append(recommendation)
        
        recommendations.sort(key=lambda x: x['score_percentage'], reverse=True)
        top_programs = recommendations[:top_k]
        
        print(f"✅ Found {len(top_programs)} recommendations")
        return top_programs

    def _calculate_comprehensive_match_score(self, program, student_data):
        score = 0.0
        factors = []
        
        academic_score = self._calculate_academic_match(program, student_data)
        score += academic_score * 0.3
        factors.append(('Academic', academic_score))
        
        budget_score = self._calculate_budget_match(program, student_data)
        score += budget_score * 0.25
        factors.append(('Budget', budget_score))
        
        location_score = self._calculate_location_match(program, student_data)
        score += location_score * 0.2
        factors.append(('Location', location_score))
        
        course_score = self._calculate_course_match(program, student_data)
        score += course_score * 0.15
        factors.append(('Course', course_score))
        
        english_score = self._calculate_english_match(program, student_data)
        score += english_score * 0.1
        factors.append(('English', english_score))
        
        if len(program.get('program_id', '')) == 8:
            print(f"Program {program.get('program_id')}:")
            for factor, factor_score in factors:
                print(f"  {factor}: {factor_score:.2f}")
            print(f"  Total: {score:.2f}")
        
        return score

    def _calculate_academic_match(self, program, student_data):
        try:
            student_score = self._safe_float_conversion(student_data.get('academic_score', 0))
            
            if student_data.get('score_type', 'gpa') == 'gpa':
                min_required = self._safe_float_conversion(program.get('min_gpa', 2.5))
                if student_score >= min_required:
                    return 1.0
                elif student_score >= min_required * 0.9:
                    return 0.8
                elif student_score >= min_required * 0.8:
                    return 0.6
                else:
                    return 0.3
            else:
                min_required = self._safe_float_conversion(program.get('min_percentage', 60))
                if student_score >= min_required:
                    return 1.0
                elif student_score >= min_required * 0.9:
                    return 0.8
                elif student_score >= min_required * 0.8:
                    return 0.6
                else:
                    return 0.3
        except Exception as e:
            print(f"⚠️ Academic match error: {e}")
            return 0.5

    def _calculate_budget_match(self, program, student_data):
        try:
            student_budget = self._safe_float_conversion(student_data.get('max_tuition_fee', 25000))
            program_fee = self._safe_float_conversion(program.get('tuition_fee_usd', 25000))
            
            if program_fee <= student_budget:
                return 1.0
            elif program_fee <= student_budget * 1.1:
                return 0.8
            elif program_fee <= student_budget * 1.2:
                return 0.6
            elif program_fee <= student_budget * 1.5:
                return 0.4
            else:
                return 0.2
        except Exception as e:
            print(f"⚠️ Budget match error: {e}")
            return 0.5

    def _calculate_location_match(self, program, student_data):
        try:
            score = 0.0
            
            program_country = str(program.get('country', '')).strip().lower()
            student_country = str(student_data.get('country', '')).strip().lower()
            
            if student_country and program_country == student_country:
                score += 0.7
            elif not student_country:
                score += 0.35
            else:
                score += 0.1
            
            program_city = str(program.get('city', '')).strip().lower()
            student_city = str(student_data.get('city', '')).strip().lower()
            
            if student_city and program_city == student_city:
                score += 0.3
            
            return min(score, 1.0)
        except Exception as e:
            print(f"⚠️ Location match error: {e}")
            return 0.5

    def _calculate_course_match(self, program, student_data):
        try:
            score = 0.0
            
            program_field = str(program.get('field_of_study', '')).strip().lower()
            student_field = str(student_data.get('field_of_study', '')).strip().lower()
            
            if student_field and program_field and student_field in program_field:
                score += 0.4
            
            program_spec = str(program.get('specialization', '')).strip().lower()
            student_spec = str(student_data.get('specialization', '')).strip().lower()
            
            if student_spec and program_spec and student_spec in program_spec:
                score += 0.3
            elif not student_spec:
                score += 0.15
            
            if 'course_duration' in student_data and student_data['course_duration']:
                try:
                    preferred_duration = str(student_data['course_duration']).strip().lower()
                    program_duration = self._safe_float_conversion(program.get('course_duration_months', 24))
                    
                    duration_map = {
                        '1 year': 12,
                        '1.5 years': 18,
                        '2 years': 24
                    }
                    
                    if preferred_duration in duration_map:
                        preferred_months = duration_map[preferred_duration]
                        diff = abs(program_duration - preferred_months)
                        
                        if diff == 0:
                            score += 0.3
                        elif diff <= 6:
                            score += 0.2
                        elif diff <= 12:
                            score += 0.1
                except:
                    pass
            
            return min(score, 1.0)
        except Exception as e:
            print(f"⚠️ Course match error: {e}")
            return 0.5

    def _calculate_english_match(self, program, student_data):
        try:
            english_test = student_data.get('english_test', 'none').lower()
            
            if english_test == 'none':
                if 'moi_accepted' in program and self._safe_bool_conversion(program['moi_accepted'], False):
                    return 1.0
                else:
                    return 0.5
            else:
                student_score = self._safe_float_conversion(student_data.get('english_score', 0))
                
                test_requirements = {
                    'ielts': self._safe_float_conversion(program.get('ielts_overall', 6.5)),
                    'toefl': self._safe_float_conversion(program.get('toefl_overall', 90)),
                    'pte': self._safe_float_conversion(program.get('pte_overall', 58)),
                    'duolingo': self._safe_float_conversion(program.get('duolingo_overall', 110))
                }
                
                required_score = test_requirements.get(english_test, 6.5)
                
                if student_score >= required_score:
                    return 1.0
                elif student_score >= required_score * 0.9:
                    return 0.8
                elif student_score >= required_score * 0.8:
                    return 0.6
                else:
                    return 0.4
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
        'city': '',
        'university_type': 'both',
        'intake': 'fall',
        'priority_1': 'course',
        'priority_2': 'budget',
        'priority_3': 'location'
    }
    
    try:
        engine = PredictionEngine()
        recommendations = engine.get_top_recommendations(test_student, 5)
        
        print("\n" + "="*50)
        print("🏆 TOP RECOMMENDATIONS")
        print("="*50)
        
        for i, rec in enumerate(recommendations):
            print(f"\n{i+1}. {rec['program_name']}")
            print(f"   🎓 {rec['university_name']}")
            print(f"   📍 {rec['city']}, {rec['country']} | 🏫 {rec['university_type']}")
            print(f"   💰 ${rec['tuition_fee_usd']:,} | 📊 Score: {rec['score_percentage']}%")
            print(f"   🏆 Rank: #{rec['world_ranking']} | 📅 Intakes: {', '.join(rec['available_intakes'])}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()