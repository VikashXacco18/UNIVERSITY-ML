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
        
#         # Clean intake columns - FIXED PROPERLY
#         intake_columns = ['intake_spring', 'intake_summer', 'intake_fall', 'intake_winter']
#         for col in intake_columns:
#             if col in self.data.columns:
#                 # Convert to string first, then handle different cases
#                 self.data[col] = self.data[col].astype(str).str.strip().str.lower()
#                 self.data[col] = self.data[col].map({
#                     'yes': True,
#                     'no': False,
#                     'true': True,
#                     'false': False,
#                     '1': True,
#                     '0': False
#                 }).fillna(False)
        
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
        
#         # Intake Flexibility Score
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
#             self.data['prestige_score'] * 0.2 +
#             self.data['financial_accessibility'] * 0.2 + 
#             self.data['commission_rate'] * 0.2 +
#             self.data['job_placement_rate_clean'] * 0.2 +
#             self.data['university_type_score'] * 0.1 +
#             self.data['intake_flexibility'] * 0.1
#         )
        
#         # Select features for model
#         feature_columns = [
#             'academic_difficulty', 'financial_accessibility', 'prestige_score',
#             'english_flexibility', 'duration_score', 'world_ranking',
#             'tuition_fee_usd', 'job_placement_rate_clean', 'visa_success_rate_clean',
#             'university_type_encoded', 'country_encoded', 'field_of_study_encoded',
#             'intake_flexibility'
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


# data_preprocessor.py
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
        print(f"📊 Available columns: {list(self.data.columns)}")
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
        
        # Only process commission_rate if it exists
        if 'commission_rate' in self.data.columns:
            self.data['commission_rate'] = self.data['commission_rate'].apply(clean_commission_rate)
        else:
            self.data['commission_rate'] = 10.0  # Default value
        
        # Clean tuition fees - create if missing
        if 'tuition_fee_usd' not in self.data.columns:
            # Try to find alternative fee columns
            fee_columns = [col for col in self.data.columns if 'fee' in col.lower() or 'tuition' in col.lower()]
            if fee_columns:
                self.data['tuition_fee_usd'] = pd.to_numeric(self.data[fee_columns[0]], errors='coerce').fillna(25000)
            else:
                self.data['tuition_fee_usd'] = 25000  # Default value
        
        self.data['tuition_fee_usd'] = pd.to_numeric(self.data['tuition_fee_usd'], errors='coerce').fillna(25000)
        
        # Clean world ranking - create if missing
        if 'world_ranking' not in self.data.columns:
            self.data['world_ranking'] = 500  # Default ranking
        else:
            self.data['world_ranking'] = pd.to_numeric(self.data['world_ranking'], errors='coerce').fillna(500)
        
        # Clean test scores with defaults
        test_scores = {
            'ielts_overall': 6.5,
            'toefl_overall': 90,
            'pte_overall': 58,
            'duolingo_overall': 110
        }
        
        for test, default in test_scores.items():
            if test in self.data.columns:
                self.data[test] = pd.to_numeric(self.data[test], errors='coerce').fillna(default)
            else:
                self.data[test] = default
        
        # Clean intake columns
        intake_columns = ['intake_spring', 'intake_summer', 'intake_fall', 'intake_winter']
        for col in intake_columns:
            if col in self.data.columns:
                self.data[col] = self.data[col].astype(str).str.strip().str.lower()
                self.data[col] = self.data[col].map({
                    'yes': True, 'true': True, '1': True,
                    'no': False, 'false': False, '0': False
                }).fillna(False)
            else:
                # Set default intake values
                self.data[col] = True if 'fall' in col else False
        
        # Clean scholarship information - create if missing
        if 'scholarship_available' not in self.data.columns:
            self.data['scholarship_available'] = True  # Default to True for better recommendations
        
        self.data['scholarship_available'] = self.data['scholarship_available'].astype(str).str.strip().str.lower()
        self.data['scholarship_available'] = self.data['scholarship_available'].map({
            'yes': True, 'true': True, 'available': True, '1': True,
            'no': False, 'false': False, 'not available': False, '0': False
        }).fillna(True)  # Default to True
        
        # Ensure required columns exist
        required_columns = {
            'min_gpa': 2.5,
            'min_percentage': 60,
            'job_placement_rate': 50,
            'visa_success_rate': 70,
            'course_duration_months': 24,
            'application_fee': 0,
            'course_link': '#',
            'language_requirements': 'English',
            'campus_location': 'Main Campus'
        }
        
        for col, default in required_columns.items():
            if col not in self.data.columns:
                self.data[col] = default
                print(f"⚠️  Created missing column: {col} with default value: {default}")
        
        print("✅ Numeric columns cleaned!")
        return self.data
    
    def engineer_features(self):
        """Create advanced features for ML"""
        print("🛠️ Engineering features...")
        
        # Academic Difficulty Score
        self.data['min_gpa_clean'] = pd.to_numeric(self.data['min_gpa'], errors='coerce').fillna(2.5)
        self.data['min_percentage_clean'] = pd.to_numeric(self.data['min_percentage'], errors='coerce').fillna(60)
        
        # Handle missing GRE/GMAT columns
        if 'gre_required' not in self.data.columns:
            self.data['gre_required'] = 'No'
        if 'gmat_required' not in self.data.columns:
            self.data['gmat_required'] = 'No'
        
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
        if 'moi_accepted' not in self.data.columns:
            self.data['moi_accepted'] = 'Yes'
        if 'english_test_required' not in self.data.columns:
            self.data['english_test_required'] = 'Yes'
        
        self.data['english_flexibility'] = (
            (self.data['moi_accepted'] == 'Yes').astype(int) * 30 +
            (self.data['english_test_required'] == 'No').astype(int) * 20 +
            (self.data['ielts_overall'] <= 6.5).astype(int) * 10
        )
        
        # University Type Score - create if missing
        if 'university_type' not in self.data.columns:
            self.data['university_type'] = 'Public'
        
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
        
        # Scholarship Score
        self.data['scholarship_score'] = self.data['scholarship_available'].astype(int) * 50
        
        print("✅ Feature engineering completed!")
        return self.data
    
    def encode_categorical_features(self):
        """Encode categorical variables for ML"""
        print("🔤 Encoding categorical features...")
        
        categorical_columns = [
            'university_type', 'country', 'field_of_study', 
            'language_of_instruction', 'specialization'
        ]
        
        # Only encode columns that exist in the data
        available_categorical = [col for col in categorical_columns if col in self.data.columns]
        
        for col in available_categorical:
            self.label_encoders[col] = LabelEncoder()
            # Fill NaN values before encoding
            self.data[col] = self.data[col].fillna('General')
            self.data[col + '_encoded'] = self.label_encoders[col].fit_transform(self.data[col])
            print(f"   ✅ Encoded: {col} -> {col}_encoded")
        
        # Create missing categorical columns with defaults
        for col in set(categorical_columns) - set(available_categorical):
            print(f"⚠️  Creating missing categorical column: {col}")
            if col == 'specialization':
                self.data[col] = 'General'
            elif col == 'language_of_instruction':
                self.data[col] = 'English'
            elif col == 'country':
                self.data[col] = 'USA'
            elif col == 'university_type':
                self.data[col] = 'Public'
            
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
            'specialization_encoded', 'intake_flexibility', 'scholarship_score'
        ]
        
        # Only include columns that exist
        available_features = [col for col in feature_columns if col in self.data.columns]
        print(f"📋 Using features: {available_features}")
        
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