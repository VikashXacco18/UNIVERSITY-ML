# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import LabelEncoder, StandardScaler
# import joblib

# class DataPreprocessor:
#     def __init__(self):
#         self.data = None
#         self.scaler = StandardScaler()
#         self.label_encoders = {}
        
#     def load_data(self, csv_path):
#         """Load and basic clean of data"""
#         self.data = pd.read_csv(csv_path)
#         print(f"✅ Loaded {len(self.data)} programs")
#         print(f"📊 Columns: {list(self.data.columns)}")
#         return self.data
    
#     def clean_numeric_columns(self):
#         """Clean numeric columns that have text values"""
#         print("🧹 Cleaning numeric columns...")
        
#         # Fix commission_rate - handle dates and percentages
#         def clean_commission_rate(value):
#             if pd.isna(value):
#                 return 0.0
#             value_str = str(value)
#             if '%' in value_str:
#                 return float(value_str.rstrip('%'))
#             elif '-' in value_str:
#                 return 15.0
#             else:
#                 try:
#                     return float(value_str)
#                 except:
#                     return 0.0
        
#         self.data['commission_rate'] = self.data['commission_rate'].apply(clean_commission_rate)
        
#         # Clean tuition fees
#         self.data['tuition_fee_usd'] = pd.to_numeric(self.data['tuition_fee_usd'], errors='coerce').fillna(0)
#         self.data['tuition_fee_eur'] = pd.to_numeric(self.data['tuition_fee_eur'], errors='coerce').fillna(0)
        
#         # Clean world ranking
#         self.data['world_ranking'] = pd.to_numeric(self.data['world_ranking'], errors='coerce').fillna(500)
        
#         # Clean test scores
#         self.data['ielts_overall'] = pd.to_numeric(self.data['ielts_overall'], errors='coerce').fillna(6.5)
#         self.data['toefl_overall'] = pd.to_numeric(self.data['toefl_overall'], errors='coerce').fillna(90)
#         self.data['pte_overall'] = pd.to_numeric(self.data['pte_overall'], errors='coerce').fillna(58)
#         self.data['duolingo_overall'] = pd.to_numeric(self.data['duolingo_overall'], errors='coerce').fillna(110)
        
#         # Clean intake columns (convert Yes/No to boolean)
#         intake_columns = ['intake_spring', 'intake_summer', 'intake_fall', 'intake_winter']
#         for col in intake_columns:
#             if col in self.data.columns:
#                 self.data[col] = self.data[col].map({'Yes': True, 'No': False}).fillna(False)
        
#         print("✅ Numeric columns cleaned!")
#         return self.data
    
#     def engineer_features(self):
#         """Create advanced features for ML"""
#         print("🛠️ Engineering features...")
        
#         # Academic Difficulty Score
#         self.data['min_gpa_clean'] = pd.to_numeric(self.data['min_gpa'], errors='coerce').fillna(2.5)
#         self.data['min_percentage_clean'] = pd.to_numeric(self.data['min_percentage'], errors='coerce').fillna(60)
        
#         self.data['academic_difficulty'] = (
#             self.data['min_gpa_clean'] * 10 + 
#             self.data['min_percentage_clean'] * 0.1 +
#             (self.data['gre_required'] == 'Yes').astype(int) * 20 +
#             (self.data['gmat_required'] == 'Yes').astype(int) * 15
#         )
        
#         # Financial Accessibility Score
#         self.data['financial_accessibility'] = np.where(
#             self.data['tuition_fee_usd'] > 0,
#             1 / (self.data['tuition_fee_usd'] + 1),
#             1.0
#         )
        
#         # Program Prestige Score
#         self.data['job_placement_rate_clean'] = pd.to_numeric(
#             self.data['job_placement_rate'], errors='coerce'
#         ).fillna(50)
        
#         self.data['visa_success_rate_clean'] = pd.to_numeric(
#             self.data['visa_success_rate'], errors='coerce'
#         ).fillna(70)
        
#         self.data['prestige_score'] = (
#             (1000 - self.data['world_ranking']) * 0.1 +
#             self.data['job_placement_rate_clean'] * 0.5 +
#             self.data['visa_success_rate_clean'] * 0.3
#         )
        
#         # English Flexibility Score
#         self.data['english_flexibility'] = (
#             (self.data['moi_accepted'] == 'Yes').astype(int) * 30 +
#             (self.data['english_test_required'] == 'No').astype(int) * 20 +
#             (self.data['ielts_overall'] <= 6.5).astype(int) * 10
#         )
        
#         # University Type Score
#         self.data['university_type_score'] = self.data['university_type'].apply(
#             lambda x: 100 if x == 'Public' else (80 if x == 'Private' else 60)
#         )
        
#         # Intake Flexibility Score (NEW)
#         self.data['intake_flexibility'] = (
#             self.data['intake_spring'].astype(int) * 25 +
#             self.data['intake_summer'].astype(int) * 25 +
#             self.data['intake_fall'].astype(int) * 25 +
#             self.data['intake_winter'].astype(int) * 25
#         )
        
#         # Duration Score
#         self.data['duration_score'] = self.data['course_duration_months'].apply(
#             lambda x: 100 if x <= 12 else (80 if x <= 18 else 60)
#         )
        
#         print("✅ Feature engineering completed!")
#         return self.data
    
#     def encode_categorical_features(self):
#         """Encode categorical variables for ML"""
#         print("🔤 Encoding categorical features...")
        
#         categorical_columns = [
#             'university_type', 'country', 'field_of_study', 
#             'language_of_instruction'
#         ]
        
#         for col in categorical_columns:
#             if col in self.data.columns:
#                 self.label_encoders[col] = LabelEncoder()
#                 self.data[col + '_encoded'] = self.label_encoders[col].fit_transform(self.data[col])
        
#         print("✅ Categorical encoding completed!")
#         return self.data
    
#     def prepare_training_data(self):
#         """Prepare final dataset for training"""
#         print("📊 Preparing training data...")
        
#         # Create target variable (program quality score)
#         self.data['target_score'] = (
#             self.data['prestige_score'] * 0.2 +        # Reduced weights
#             self.data['financial_accessibility'] * 0.2 + 
#             self.data['commission_rate'] * 0.2 +
#             self.data['job_placement_rate_clean'] * 0.2 +
#             self.data['university_type_score'] * 0.1 +
#             self.data['intake_flexibility'] * 0.1      # NEW: Intake flexibility importance
#         )
        
#         # Select features for model
#         feature_columns = [
#             'academic_difficulty', 'financial_accessibility', 'prestige_score',
#             'english_flexibility', 'duration_score', 'world_ranking',
#             'tuition_fee_usd', 'job_placement_rate_clean', 'visa_success_rate_clean',
#             'university_type_encoded', 'country_encoded', 'field_of_study_encoded',
#             'intake_flexibility'  # NEW
#         ]
        
#         # Only include columns that exist
#         available_features = [col for col in feature_columns if col in self.data.columns]
#         X = self.data[available_features]
#         y = self.data['target_score']
        
#         print(f"✅ Training data prepared: {X.shape[0]} samples, {X.shape[1]} features")
#         return X, y, available_features

# # Test the preprocessor
# if __name__ == "__main__":
#     preprocessor = DataPreprocessor()
#     data = preprocessor.load_data('../data/University Programs Database.csv')
#     data = preprocessor.clean_numeric_columns()
#     data = preprocessor.engineer_features()
#     data = preprocessor.encode_categorical_features()
#     X, y, features = preprocessor.prepare_training_data()
#     print("✅ DataPreprocessor test successful!")
#     print(f"📊 Final features: {features}")

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib

class DataPreprocessor:
    def __init__(self):
        self.data = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def load_data(self, csv_path):
        """Load and basic clean of data"""
        self.data = pd.read_csv(csv_path)
        print(f"✅ Loaded {len(self.data)} programs")
        return self.data
    
    def clean_numeric_columns(self):
        """Clean numeric columns that have text values"""
        print("🧹 Cleaning numeric columns...")
        
        # Fix commission_rate - handle dates and percentages
        def clean_commission_rate(value):
            if pd.isna(value):
                return 0.0
            value_str = str(value)
            if '%' in value_str:
                return float(value_str.rstrip('%'))
            elif '-' in value_str:
                return 15.0
            else:
                try:
                    return float(value_str)
                except:
                    return 0.0
        
        self.data['commission_rate'] = self.data['commission_rate'].apply(clean_commission_rate)
        
        # Clean tuition fees
        self.data['tuition_fee_usd'] = pd.to_numeric(self.data['tuition_fee_usd'], errors='coerce').fillna(0)
        self.data['tuition_fee_eur'] = pd.to_numeric(self.data['tuition_fee_eur'], errors='coerce').fillna(0)
        
        # Clean world ranking
        self.data['world_ranking'] = pd.to_numeric(self.data['world_ranking'], errors='coerce').fillna(500)
        
        # Clean test scores
        self.data['ielts_overall'] = pd.to_numeric(self.data['ielts_overall'], errors='coerce').fillna(6.5)
        self.data['toefl_overall'] = pd.to_numeric(self.data['toefl_overall'], errors='coerce').fillna(90)
        self.data['pte_overall'] = pd.to_numeric(self.data['pte_overall'], errors='coerce').fillna(58)
        self.data['duolingo_overall'] = pd.to_numeric(self.data['duolingo_overall'], errors='coerce').fillna(110)
        
        # Clean intake columns - FIXED PROPERLY
        intake_columns = ['intake_spring', 'intake_summer', 'intake_fall', 'intake_winter']
        for col in intake_columns:
            if col in self.data.columns:
                # Convert to string first, then handle different cases
                self.data[col] = self.data[col].astype(str).str.strip().str.lower()
                self.data[col] = self.data[col].map({
                    'yes': True,
                    'no': False,
                    'true': True,
                    'false': False,
                    '1': True,
                    '0': False
                }).fillna(False)
        
        print("✅ Numeric columns cleaned!")
        return self.data
    
    def engineer_features(self):
        """Create advanced features for ML"""
        print("🛠️ Engineering features...")
        
        # Academic Difficulty Score
        self.data['min_gpa_clean'] = pd.to_numeric(self.data['min_gpa'], errors='coerce').fillna(2.5)
        self.data['min_percentage_clean'] = pd.to_numeric(self.data['min_percentage'], errors='coerce').fillna(60)
        
        self.data['academic_difficulty'] = (
            self.data['min_gpa_clean'] * 10 + 
            self.data['min_percentage_clean'] * 0.1 +
            (self.data['gre_required'] == 'Yes').astype(int) * 20 +
            (self.data['gmat_required'] == 'Yes').astype(int) * 15
        )
        
        # Financial Accessibility Score
        self.data['financial_accessibility'] = np.where(
            self.data['tuition_fee_usd'] > 0,
            1 / (self.data['tuition_fee_usd'] + 1),
            1.0
        )
        
        # Program Prestige Score
        self.data['job_placement_rate_clean'] = pd.to_numeric(
            self.data['job_placement_rate'], errors='coerce'
        ).fillna(50)
        
        self.data['visa_success_rate_clean'] = pd.to_numeric(
            self.data['visa_success_rate'], errors='coerce'
        ).fillna(70)
        
        self.data['prestige_score'] = (
            (1000 - self.data['world_ranking']) * 0.1 +
            self.data['job_placement_rate_clean'] * 0.5 +
            self.data['visa_success_rate_clean'] * 0.3
        )
        
        # English Flexibility Score
        self.data['english_flexibility'] = (
            (self.data['moi_accepted'] == 'Yes').astype(int) * 30 +
            (self.data['english_test_required'] == 'No').astype(int) * 20 +
            (self.data['ielts_overall'] <= 6.5).astype(int) * 10
        )
        
        # University Type Score
        self.data['university_type_score'] = self.data['university_type'].apply(
            lambda x: 100 if x == 'Public' else (80 if x == 'Private' else 60)
        )
        
        # Intake Flexibility Score
        self.data['intake_flexibility'] = (
            self.data['intake_spring'].astype(int) * 25 +
            self.data['intake_summer'].astype(int) * 25 +
            self.data['intake_fall'].astype(int) * 25 +
            self.data['intake_winter'].astype(int) * 25
        )
        
        # Duration Score
        self.data['duration_score'] = self.data['course_duration_months'].apply(
            lambda x: 100 if x <= 12 else (80 if x <= 18 else 60)
        )
        
        print("✅ Feature engineering completed!")
        return self.data
    
    def encode_categorical_features(self):
        """Encode categorical variables for ML"""
        print("🔤 Encoding categorical features...")
        
        categorical_columns = [
            'university_type', 'country', 'field_of_study', 
            'language_of_instruction'
        ]
        
        for col in categorical_columns:
            if col in self.data.columns:
                self.label_encoders[col] = LabelEncoder()
                self.data[col + '_encoded'] = self.label_encoders[col].fit_transform(self.data[col])
        
        print("✅ Categorical encoding completed!")
        return self.data
    
    def prepare_training_data(self):
        """Prepare final dataset for training"""
        print("📊 Preparing training data...")
        
        # Create target variable (program quality score)
        self.data['target_score'] = (
            self.data['prestige_score'] * 0.2 +
            self.data['financial_accessibility'] * 0.2 + 
            self.data['commission_rate'] * 0.2 +
            self.data['job_placement_rate_clean'] * 0.2 +
            self.data['university_type_score'] * 0.1 +
            self.data['intake_flexibility'] * 0.1
        )
        
        # Select features for model
        feature_columns = [
            'academic_difficulty', 'financial_accessibility', 'prestige_score',
            'english_flexibility', 'duration_score', 'world_ranking',
            'tuition_fee_usd', 'job_placement_rate_clean', 'visa_success_rate_clean',
            'university_type_encoded', 'country_encoded', 'field_of_study_encoded',
            'intake_flexibility'
        ]
        
        # Only include columns that exist
        available_features = [col for col in feature_columns if col in self.data.columns]
        X = self.data[available_features]
        y = self.data['target_score']
        
        print(f"✅ Training data prepared: {X.shape[0]} samples, {X.shape[1]} features")
        return X, y, available_features

# Test the preprocessor
if __name__ == "__main__":
    preprocessor = DataPreprocessor()
    data = preprocessor.load_data('../data/University Programs Database.csv')
    data = preprocessor.clean_numeric_columns()
    data = preprocessor.engineer_features()
    data = preprocessor.encode_categorical_features()
    X, y, features = preprocessor.prepare_training_data()
    print("✅ DataPreprocessor test successful!")