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
#         """Load and clean data"""
#         try:
#             self.data = pd.read_csv(csv_path)
#             print(f"✅ Loaded {len(self.data)} programs")
            
#             # Remove completely empty columns
#             self.data = self.data.loc[:, self.data.columns.notna()]
#             self.data = self.data.loc[:, ~self.data.columns.str.contains('Unnamed')]
            
#             # Clean column names
#             self.data.columns = self.data.columns.str.strip()
            
#             return self.data
#         except Exception as e:
#             print(f"❌ Error loading data: {e}")
#             raise
    
#     def _safe_bool_conversion(self, series):
#         """Safely convert a pandas series to boolean - handles mixed types"""
#         # Convert to string first
#         series = series.astype(str).str.strip().str.lower()
        
#         # Define boolean patterns
#         true_patterns = ['yes', 'true', '1', 'y', 'required', 'mandatory']
#         false_patterns = ['no', 'false', '0', 'n', 'not required', 'optional', 'none', 'n/a']
        
#         # Initialize result array
#         result = pd.Series(False, index=series.index)
        
#         # Check for true patterns
#         for pattern in true_patterns:
#             mask = series.str.contains(pattern, na=False)
#             result[mask] = True
        
#         # Check for false patterns
#         for pattern in false_patterns:
#             mask = series.str.contains(pattern, na=False)
#             result[mask] = False
        
#         # Handle numeric strings that might be years (like '2', '3')
#         numeric_mask = series.str.isnumeric()
#         result[numeric_mask] = series[numeric_mask].astype(int) > 0
        
#         return result
    
#     def _safe_numeric_conversion(self, series, default=0.0):
#         """Safely convert a pandas series to numeric"""
#         if series.dtype == 'object':
#             # First, clean the string values
#             series = series.astype(str).str.strip()
            
#             # Handle special cases
#             series = series.replace([
#                 'N/A', 'nan', 'null', '', 'None', 'NA', 'n/a', 
#                 'Unknown', 'unknown', 'NAN', 'NaN'
#             ], np.nan)
            
#             # Extract numbers from strings (e.g., "6.5" from "6.5/9.0")
#             def extract_number(x):
#                 if pd.isna(x):
#                     return np.nan
#                 try:
#                     # Try to find first number in string
#                     import re
#                     numbers = re.findall(r'[-+]?\d*\.\d+|\d+', x)
#                     if numbers:
#                         return float(numbers[0])
#                     else:
#                         return np.nan
#                 except:
#                     return np.nan
            
#             series = series.apply(extract_number)
            
#             # Convert to numeric
#             return pd.to_numeric(series, errors='coerce').fillna(default)
#         elif pd.api.types.is_numeric_dtype(series):
#             return series.fillna(default)
#         else:
#             return pd.to_numeric(series, errors='coerce').fillna(default)
    
#     def clean_numeric_columns(self):
#         """Clean numeric columns with proper handling of mixed types"""
#         print("🧹 Cleaning numeric columns...")
        
#         # Define all columns that should be numeric with their defaults
#         numeric_columns_defaults = {
#             'world_ranking': 500,
#             'tuition_fee_usd': 25000,
#             'tuition_fee_eur': 20000,
#             'application_fee_eur': 50,
#             'min_gpa': 2.5,
#             'min_percentage': 60,
#             'ielts_overall': 6.5,
#             'toefl_overall': 90,
#             'pte_overall': 58,
#             'duolingo_overall': 110,
#             'job_placement_rate': 70,
#             'visa_success_rate': 80,
#             'course_duration_months': 24,
#             'commission_rate': 10,
#             'scholarship_amount_max': 5000,
#             'living_cost_estimate_eur': 10000,
#             'min_gre_score': 300,
#             'min_gmat_score': 500
#         }
        
#         # Create missing columns with defaults
#         for col, default in numeric_columns_defaults.items():
#             if col not in self.data.columns:
#                 self.data[col] = default
#                 print(f"⚠️  Created missing column: {col}")
#             else:
#                 # Clean existing column
#                 self.data[col] = self._safe_numeric_conversion(self.data[col], default)
#                 print(f"✅ Cleaned {col}: {self.data[col].dtype}, {self.data[col].isna().sum()} missing")
        
#         # Clean boolean columns - with special handling
#         boolean_columns = [
#             'intake_spring', 'intake_summer', 'intake_fall', 'intake_winter',
#             'scholarships_available', 'internship_opportunities',
#             'part_time_work_allowed', 'rolling_admissions',
#             'gre_required', 'gmat_required', 'english_test_required',
#             'work_experience_required', 'moi_accepted'
#         ]
        
#         for col in boolean_columns:
#             if col in self.data.columns:
#                 self.data[col] = self._safe_bool_conversion(self.data[col])
#                 true_count = self.data[col].sum()
#                 false_count = len(self.data[col]) - true_count
#                 print(f"✅ Cleaned {col}: {true_count} True, {false_count} False")
#             else:
#                 self.data[col] = False
#                 print(f"⚠️  Created missing boolean column: {col}")
        
#         # Clean min_work_experience_years - special handling
#         if 'min_work_experience_years' in self.data.columns:
#             print(f"🔧 Processing min_work_experience_years...")
#             print(f"  Unique values before: {self.data['min_work_experience_years'].unique()[:10]}")
#             # Convert to numeric, handling 'No' as 0
#             self.data['min_work_experience_years'] = self.data['min_work_experience_years'].astype(str)
#             self.data['min_work_experience_years'] = self.data['min_work_experience_years'].replace(['No', 'no', 'N/A', ''], '0')
#             self.data['min_work_experience_years'] = pd.to_numeric(self.data['min_work_experience_years'], errors='coerce').fillna(0)
#             print(f"  Unique values after: {self.data['min_work_experience_years'].unique()[:10]}")
        
#         # Clean string columns
#         string_columns = [
#             'university_name', 'program_name', 'field_of_study', 
#             'specialization', 'country', 'city', 'language_of_instruction',
#             'partner_name', 'degree_level', 'last_education_required'
#         ]
        
#         for col in string_columns:
#             if col in self.data.columns:
#                 self.data[col] = self.data[col].astype(str).str.strip()
#                 # Replace empty strings with 'Unknown'
#                 self.data[col] = self.data[col].replace(['', 'nan', 'NaN', 'None'], 'Unknown')
#             else:
#                 self.data[col] = 'Unknown'
#                 print(f"⚠️  Created missing string column: {col}")
        
#         print("✅ Numeric columns cleaned!")
#         return self.data
    
#     def engineer_features(self):
#         """Create advanced features for ML with robust error handling"""
#         print("🛠️ Engineering features...")
        
#         # Ensure all required columns exist with defaults
#         academic_columns = {
#             'min_gpa': 2.5,
#             'min_percentage': 60,
#             'gre_required': False,
#             'gmat_required': False,
#             'work_experience_required': False,
#             'min_work_experience_years': 0
#         }
        
#         for col, default in academic_columns.items():
#             if col not in self.data.columns:
#                 self.data[col] = default
#                 print(f"⚠️  Created missing academic column: {col}")
        
#         # Academic Difficulty Score
#         print("📊 Calculating academic difficulty...")
#         try:
#             # Convert booleans to int safely
#             gre_score = self.data['gre_required'].astype(int) * 20
#             gmat_score = self.data['gmat_required'].astype(int) * 15
#             work_exp_score = self.data['work_experience_required'].astype(int) * 10
#             work_exp_years_score = self.data['min_work_experience_years'] * 5
            
#             self.data['academic_difficulty'] = (
#                 self.data['min_gpa'] * 10 + 
#                 self.data['min_percentage'] * 0.1 +
#                 gre_score + gmat_score + work_exp_score + work_exp_years_score
#             )
#             print(f"✅ Academic difficulty calculated: mean = {self.data['academic_difficulty'].mean():.2f}")
#         except Exception as e:
#             print(f"❌ Error calculating academic difficulty: {e}")
#             self.data['academic_difficulty'] = 50  # Default value
        
#         # Financial Accessibility Score
#         print("💰 Calculating financial accessibility...")
#         try:
#             self.data['financial_accessibility'] = np.where(
#                 self.data['tuition_fee_usd'] > 0,
#                 100000 / (self.data['tuition_fee_usd'] + 1),
#                 100
#             )
            
#             # Normalize to 0-1
#             max_val = self.data['financial_accessibility'].max()
#             if max_val > 0:
#                 self.data['financial_accessibility'] = self.data['financial_accessibility'] / max_val
            
#             print(f"✅ Financial accessibility calculated: mean = {self.data['financial_accessibility'].mean():.2f}")
#         except Exception as e:
#             print(f"❌ Error calculating financial accessibility: {e}")
#             self.data['financial_accessibility'] = 0.5
        
#         # Program Prestige Score
#         print("🏆 Calculating prestige score...")
#         try:
#             # Normalize world ranking (lower rank = better)
#             max_ranking = self.data['world_ranking'].max()
#             if max_ranking > 0:
#                 ranking_score = (max_ranking - self.data['world_ranking']) / max_ranking
#             else:
#                 ranking_score = 0.5
            
#             # Normalize placement and visa rates to 0-1
#             placement_score = self.data['job_placement_rate'] / 100
#             visa_score = self.data['visa_success_rate'] / 100
            
#             self.data['prestige_score'] = (
#                 ranking_score * 0.4 +
#                 placement_score * 0.4 +
#                 visa_score * 0.2
#             )
#             print(f"✅ Prestige score calculated: mean = {self.data['prestige_score'].mean():.2f}")
#         except Exception as e:
#             print(f"❌ Error calculating prestige score: {e}")
#             self.data['prestige_score'] = 0.5
        
#         # English Flexibility Score
#         print("🌍 Calculating English flexibility...")
#         try:
#             # MOI accepted score
#             moi_score = self.data['moi_accepted'].astype(int) * 0.3
            
#             # English test not required score
#             no_test_score = (~self.data['english_test_required']).astype(int) * 0.2
            
#             # Low IELTS requirement score
#             low_ielts_score = (self.data['ielts_overall'] <= 6.5).astype(int) * 0.1
            
#             self.data['english_flexibility'] = moi_score + no_test_score + low_ielts_score
#             print(f"✅ English flexibility calculated: mean = {self.data['english_flexibility'].mean():.2f}")
#         except Exception as e:
#             print(f"❌ Error calculating English flexibility: {e}")
#             self.data['english_flexibility'] = 0.3
        
#         # University Type Score
#         print("🏛️ Calculating university type score...")
#         try:
#             self.data['university_type_score'] = self.data['university_type'].apply(
#                 lambda x: 0.8 if str(x).lower() == 'public' else 0.6
#             )
#             print(f"✅ University type score calculated: mean = {self.data['university_type_score'].mean():.2f}")
#         except Exception as e:
#             print(f"❌ Error calculating university type score: {e}")
#             self.data['university_type_score'] = 0.7
        
#         # Intake Flexibility Score
#         print("📅 Calculating intake flexibility...")
#         try:
#             intake_cols = ['intake_spring', 'intake_summer', 'intake_fall', 'intake_winter']
#             available_intake_cols = [col for col in intake_cols if col in self.data.columns]
            
#             if available_intake_cols:
#                 intake_count = self.data[available_intake_cols].sum(axis=1)
#                 self.data['intake_flexibility'] = intake_count / len(available_intake_cols)
#             else:
#                 self.data['intake_flexibility'] = 0.25
            
#             print(f"✅ Intake flexibility calculated: mean = {self.data['intake_flexibility'].mean():.2f}")
#         except Exception as e:
#             print(f"❌ Error calculating intake flexibility: {e}")
#             self.data['intake_flexibility'] = 0.25
        
#         # Duration Score
#         print("⏱️ Calculating duration score...")
#         try:
#             self.data['duration_score'] = self.data['course_duration_months'].apply(
#                 lambda x: 1.0 if x <= 12 else (0.8 if x <= 18 else 0.6)
#             )
#             print(f"✅ Duration score calculated: mean = {self.data['duration_score'].mean():.2f}")
#         except Exception as e:
#             print(f"❌ Error calculating duration score: {e}")
#             self.data['duration_score'] = 0.7
        
#         # Scholarship Score
#         print("🎓 Calculating scholarship score...")
#         try:
#             self.data['scholarship_score'] = self.data['scholarships_available'].astype(int) * 0.5
#             print(f"✅ Scholarship score calculated: mean = {self.data['scholarship_score'].mean():.2f}")
#         except Exception as e:
#             print(f"❌ Error calculating scholarship score: {e}")
#             self.data['scholarship_score'] = 0.25
        
#         # Location Diversity Score
#         print("📍 Calculating location diversity...")
#         try:
#             if 'country' in self.data.columns and self.data['country'].nunique() > 1:
#                 country_counts = self.data['country'].value_counts()
#                 max_count = country_counts.max()
#                 self.data['location_diversity'] = 1 - (self.data['country'].map(country_counts) / max_count)
#             else:
#                 self.data['location_diversity'] = 0.5
            
#             print(f"✅ Location diversity calculated: mean = {self.data['location_diversity'].mean():.2f}")
#         except Exception as e:
#             print(f"❌ Error calculating location diversity: {e}")
#             self.data['location_diversity'] = 0.5
        
#         # Partner Accessibility Score
#         print("🤝 Calculating partner accessibility...")
#         try:
#             if 'commission_rate' in self.data.columns and 'partner_name' in self.data.columns:
#                 # Normalize commission rate (0-10% to 0-1)
#                 commission_score = self.data['commission_rate'] / 100
                
#                 # Partner available score
#                 partner_score = (self.data['partner_name'] != 'Unknown').astype(int) * 0.5
                
#                 self.data['partner_accessibility'] = commission_score + partner_score
#                 # Cap at 1.0
#                 self.data['partner_accessibility'] = self.data['partner_accessibility'].clip(0, 1)
#             else:
#                 self.data['partner_accessibility'] = 0.3
            
#             print(f"✅ Partner accessibility calculated: mean = {self.data['partner_accessibility'].mean():.2f}")
#         except Exception as e:
#             print(f"❌ Error calculating partner accessibility: {e}")
#             self.data['partner_accessibility'] = 0.3
        
#         print("✅ Feature engineering completed!")
#         return self.data
    
#     def encode_categorical_features(self):
#         """Encode categorical variables for ML"""
#         print("🔤 Encoding categorical features...")
        
#         categorical_columns = [
#             'university_type', 'country', 'field_of_study', 
#             'language_of_instruction', 'specialization', 'city',
#             'partner_name', 'degree_level'
#         ]
        
#         # Only encode columns that exist in the data and have multiple values
#         available_categorical = []
#         for col in categorical_columns:
#             if col in self.data.columns:
#                 # Check if column has more than 1 unique value
#                 unique_count = self.data[col].nunique()
#                 if unique_count > 1:
#                     available_categorical.append(col)
#                 else:
#                     print(f"   ⚠️  Skipping {col}: only {unique_count} unique value(s)")
        
#         for col in available_categorical:
#             try:
#                 self.label_encoders[col] = LabelEncoder()
#                 # Fill NaN values before encoding
#                 self.data[col] = self.data[col].fillna('Unknown')
#                 self.data[col + '_encoded'] = self.label_encoders[col].fit_transform(self.data[col])
#                 print(f"   ✅ Encoded: {col} -> {col}_encoded ({self.data[col].nunique()} categories)")
#             except Exception as e:
#                 print(f"   ❌ Error encoding {col}: {e}")
#                 self.data[col + '_encoded'] = 0
        
#         print("✅ Categorical encoding completed!")
#         return self.data
    
#     def prepare_training_data(self):
#         """Prepare final dataset for training"""
#         print("📊 Preparing training data...")
        
#         # Create target variable (program quality score)
#         print("🎯 Creating target score...")
#         try:
#             self.data['target_score'] = (
#                 self.data['prestige_score'] * 0.3 +
#                 self.data['financial_accessibility'] * 0.25 + 
#                 (self.data['job_placement_rate'] / 100) * 0.2 +
#                 self.data['university_type_score'] * 0.15 +
#                 self.data['intake_flexibility'] * 0.1
#             )
            
#             # Normalize target score to 0-100
#             max_score = self.data['target_score'].max()
#             min_score = self.data['target_score'].min()
            
#             if max_score > min_score:
#                 self.data['target_score'] = ((self.data['target_score'] - min_score) / (max_score - min_score)) * 100
#             else:
#                 self.data['target_score'] = 50  # Default if all values are same
            
#             print(f"✅ Target score created: {self.data['target_score'].min():.1f}-{self.data['target_score'].max():.1f}")
#         except Exception as e:
#             print(f"❌ Error creating target score: {e}")
#             self.data['target_score'] = 50
        
#         # Select features for model
#         base_features = [
#             'academic_difficulty', 'financial_accessibility', 'prestige_score',
#             'english_flexibility', 'duration_score', 'world_ranking',
#             'tuition_fee_usd', 'job_placement_rate', 'visa_success_rate',
#             'intake_flexibility', 'scholarship_score', 'location_diversity',
#             'partner_accessibility', 'university_type_score'
#         ]
        
#         # Add encoded categorical features
#         encoded_cols = [col for col in self.data.columns if col.endswith('_encoded')]
        
#         # Only include columns that exist and don't have too many NaN values
#         available_features = []
#         for col in base_features + encoded_cols:
#             if col in self.data.columns:
#                 # Check for NaN values
#                 nan_count = self.data[col].isna().sum()
#                 if nan_count == 0:
#                     available_features.append(col)
#                 elif nan_count < len(self.data[col]) * 0.3:  # Less than 30% missing
#                     # Fill with median for numeric, mode for categorical
#                     if pd.api.types.is_numeric_dtype(self.data[col]):
#                         self.data[col] = self.data[col].fillna(self.data[col].median())
#                     else:
#                         self.data[col] = self.data[col].fillna(self.data[col].mode()[0])
#                     available_features.append(col)
#                     print(f"⚠️  Filled {nan_count} missing values in {col}")
#                 else:
#                     print(f"❌ Skipping {col}: {nan_count} missing values ({nan_count/len(self.data[col])*100:.1f}%)")
        
#         print(f"📋 Using {len(available_features)} features")
#         print("Features:")
#         for i, feat in enumerate(available_features):
#             print(f"  {i+1:2d}. {feat}")
        
#         X = self.data[available_features].copy()
#         y = self.data['target_score'].copy()
        
#         # Final check for NaN
#         if X.isna().any().any():
#             print("⚠️  Still have NaN values, filling with column means...")
#             X = X.fillna(X.mean())
        
#         print(f"✅ Training data prepared: {X.shape[0]} samples, {X.shape[1]} features")
#         print(f"📊 Target score stats: mean={y.mean():.2f}, std={y.std():.2f}")
        
#         return X, y, available_features
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
        """Load and clean data"""
        try:
            self.data = pd.read_csv(csv_path)
            print(f"✅ Loaded {len(self.data)} programs")
            
            # Remove completely empty columns
            self.data = self.data.loc[:, self.data.columns.notna()]
            self.data = self.data.loc[:, ~self.data.columns.str.contains('Unnamed')]
            
            # Clean column names
            self.data.columns = self.data.columns.str.strip()
            
            return self.data
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            raise
    
    def _safe_bool_conversion(self, series):
        """Safely convert a pandas series to boolean - handles mixed types"""
        series = series.astype(str).str.strip().str.lower()
        
        true_patterns = ['yes', 'true', '1', 'y', 'required', 'mandatory']
        false_patterns = ['no', 'false', '0', 'n', 'not required', 'optional', 'none', 'n/a']
        
        result = pd.Series(False, index=series.index)
        
        for pattern in true_patterns:
            mask = series.str.contains(pattern, na=False)
            result[mask] = True
        
        for pattern in false_patterns:
            mask = series.str.contains(pattern, na=False)
            result[mask] = False
        
        numeric_mask = series.str.isnumeric()
        result[numeric_mask] = series[numeric_mask].astype(int) > 0
        
        return result
    
    def _safe_numeric_conversion(self, series, default=0.0):
        """Safely convert a pandas series to numeric"""
        if series.dtype == 'object':
            series = series.astype(str).str.strip()
            
            series = series.replace([
                'N/A', 'nan', 'null', '', 'None', 'NA', 'n/a', 
                'Unknown', 'unknown', 'NAN', 'NaN'
            ], np.nan)
            
            def extract_number(x):
                if pd.isna(x):
                    return np.nan
                try:
                    import re
                    numbers = re.findall(r'[-+]?\d*\.\d+|\d+', x)
                    if numbers:
                        return float(numbers[0])
                    else:
                        return np.nan
                except:
                    return np.nan
            
            series = series.apply(extract_number)
            
            return pd.to_numeric(series, errors='coerce').fillna(default)
        elif pd.api.types.is_numeric_dtype(series):
            return series.fillna(default)
        else:
            return pd.to_numeric(series, errors='coerce').fillna(default)
    
    def clean_numeric_columns(self):
        """Clean numeric columns with proper handling of mixed types"""
        print("🧹 Cleaning numeric columns...")
        
        numeric_columns_defaults = {
            'world_ranking': 1000,
            'tuition_fee_usd': 20000,
            'tuition_fee_eur': 18000,
            'application_fee_eur': 80,
            'min_gpa': 3.0,
            'min_percentage': 70,
            'ielts_overall': 6.5,
            'toefl_overall': 80,
            'pte_overall': 58,
            'duolingo_overall': 105,
            'job_placement_rate': 85,
            'visa_success_rate': 90,
            'course_duration_months': 18,
            'scholarship_amount_max': 3000,
            'living_cost_estimate_eur': 12000,
            'min_work_experience_years': 0
        }
        
        for col, default in numeric_columns_defaults.items():
            if col not in self.data.columns:
                self.data[col] = default
                print(f"⚠️  Created missing column: {col}")
            else:
                self.data[col] = self._safe_numeric_conversion(self.data[col], default)
                print(f"✅ Cleaned {col}: {self.data[col].dtype}, {self.data[col].isna().sum()} missing")
        
        boolean_columns = [
            'intake_spring', 'intake_summer', 'intake_fall', 'intake_winter',
            'scholarships_available', 'gre_required', 'gmat_required', 
            'english_test_required', 'work_experience_required', 'moi_accepted'
        ]
        
        for col in boolean_columns:
            if col in self.data.columns:
                self.data[col] = self._safe_bool_conversion(self.data[col])
                true_count = self.data[col].sum()
                false_count = len(self.data[col]) - true_count
                print(f"✅ Cleaned {col}: {true_count} True, {false_count} False")
            else:
                self.data[col] = False
                print(f"⚠️  Created missing boolean column: {col}")
        
        if 'min_work_experience_years' in self.data.columns:
            self.data['min_work_experience_years'] = self.data['min_work_experience_years'].astype(str)
            self.data['min_work_experience_years'] = self.data['min_work_experience_years'].replace(
                ['No', 'no', 'N/A', '', 'none'], '0'
            )
            self.data['min_work_experience_years'] = pd.to_numeric(
                self.data['min_work_experience_years'], errors='coerce'
            ).fillna(0)
        
        string_columns = [
            'university_name', 'program_name', 'field_of_study', 
            'specialization', 'country', 'city', 'partner_name',
            'last_education_required', 'program_website', 'university_website'
        ]
        
        for col in string_columns:
            if col in self.data.columns:
                self.data[col] = self.data[col].astype(str).str.strip()
                self.data[col] = self.data[col].replace(['', 'nan', 'NaN', 'None'], 'Unknown')
            else:
                self.data[col] = 'Unknown'
                print(f"⚠️  Created missing string column: {col}")
        
        print("✅ Numeric columns cleaned!")
        return self.data
    
    def engineer_features(self):
        """Create advanced features for ML"""
        print("🛠️ Engineering features...")
        
        academic_columns = {
            'min_gpa': 3.0,
            'min_percentage': 70,
            'gre_required': False,
            'gmat_required': False,
            'work_experience_required': False,
            'min_work_experience_years': 0
        }
        
        for col, default in academic_columns.items():
            if col not in self.data.columns:
                self.data[col] = default
                print(f"⚠️  Created missing academic column: {col}")
        
        print("📊 Calculating academic difficulty...")
        try:
            gre_score = self.data['gre_required'].astype(int) * 20
            gmat_score = self.data['gmat_required'].astype(int) * 15
            work_exp_score = self.data['work_experience_required'].astype(int) * 10
            work_exp_years_score = self.data['min_work_experience_years'] * 5
            
            self.data['academic_difficulty'] = (
                self.data['min_gpa'] * 10 + 
                self.data['min_percentage'] * 0.1 +
                gre_score + gmat_score + work_exp_score + work_exp_years_score
            )
            print(f"✅ Academic difficulty calculated: mean = {self.data['academic_difficulty'].mean():.2f}")
        except Exception as e:
            print(f"❌ Error calculating academic difficulty: {e}")
            self.data['academic_difficulty'] = 50
        
        print("💰 Calculating financial accessibility...")
        try:
            self.data['financial_accessibility'] = np.where(
                self.data['tuition_fee_usd'] > 0,
                100000 / (self.data['tuition_fee_usd'] + 1),
                100
            )
            
            max_val = self.data['financial_accessibility'].max()
            if max_val > 0:
                self.data['financial_accessibility'] = self.data['financial_accessibility'] / max_val
            
            print(f"✅ Financial accessibility calculated: mean = {self.data['financial_accessibility'].mean():.2f}")
        except Exception as e:
            print(f"❌ Error calculating financial accessibility: {e}")
            self.data['financial_accessibility'] = 0.5
        
        print("🏆 Calculating prestige score...")
        try:
            max_ranking = self.data['world_ranking'].max()
            if max_ranking > 0:
                ranking_score = (max_ranking - self.data['world_ranking']) / max_ranking
            else:
                ranking_score = 0.5
            
            placement_score = self.data['job_placement_rate'] / 100
            visa_score = self.data['visa_success_rate'] / 100
            
            self.data['prestige_score'] = (
                ranking_score * 0.4 +
                placement_score * 0.4 +
                visa_score * 0.2
            )
            print(f"✅ Prestige score calculated: mean = {self.data['prestige_score'].mean():.2f}")
        except Exception as e:
            print(f"❌ Error calculating prestige score: {e}")
            self.data['prestige_score'] = 0.5
        
        print("🌍 Calculating English flexibility...")
        try:
            moi_score = self.data['moi_accepted'].astype(int) * 0.3
            no_test_score = (~self.data['english_test_required']).astype(int) * 0.2
            low_ielts_score = (self.data['ielts_overall'] <= 6.5).astype(int) * 0.1
            
            self.data['english_flexibility'] = moi_score + no_test_score + low_ielts_score
            print(f"✅ English flexibility calculated: mean = {self.data['english_flexibility'].mean():.2f}")
        except Exception as e:
            print(f"❌ Error calculating English flexibility: {e}")
            self.data['english_flexibility'] = 0.3
        
        print("🏛️ Calculating university type score...")
        try:
            self.data['university_type_score'] = self.data['university_type'].apply(
                lambda x: 0.8 if str(x).lower() == 'public' else 0.6
            )
            print(f"✅ University type score calculated: mean = {self.data['university_type_score'].mean():.2f}")
        except Exception as e:
            print(f"❌ Error calculating university type score: {e}")
            self.data['university_type_score'] = 0.7
        
        print("📅 Calculating intake flexibility...")
        try:
            intake_cols = ['intake_spring', 'intake_summer', 'intake_fall', 'intake_winter']
            available_intake_cols = [col for col in intake_cols if col in self.data.columns]
            
            if available_intake_cols:
                intake_count = self.data[available_intake_cols].sum(axis=1)
                self.data['intake_flexibility'] = intake_count / len(available_intake_cols)
            else:
                self.data['intake_flexibility'] = 0.25
            
            print(f"✅ Intake flexibility calculated: mean = {self.data['intake_flexibility'].mean():.2f}")
        except Exception as e:
            print(f"❌ Error calculating intake flexibility: {e}")
            self.data['intake_flexibility'] = 0.25
        
        print("⏱️ Calculating duration score...")
        try:
            self.data['duration_score'] = self.data['course_duration_months'].apply(
                lambda x: 1.0 if x <= 12 else (0.8 if x <= 18 else 0.6)
            )
            print(f"✅ Duration score calculated: mean = {self.data['duration_score'].mean():.2f}")
        except Exception as e:
            print(f"❌ Error calculating duration score: {e}")
            self.data['duration_score'] = 0.7
        
        print("🎓 Calculating scholarship score...")
        try:
            self.data['scholarship_score'] = self.data['scholarships_available'].astype(int) * 0.5
            print(f"✅ Scholarship score calculated: mean = {self.data['scholarship_score'].mean():.2f}")
        except Exception as e:
            print(f"❌ Error calculating scholarship score: {e}")
            self.data['scholarship_score'] = 0.25
        
        print("🤝 Calculating partner accessibility...")
        try:
            if 'partner_name' in self.data.columns:
                partner_score = (self.data['partner_name'] != 'Unknown').astype(int) * 0.5
                self.data['partner_accessibility'] = partner_score
            else:
                self.data['partner_accessibility'] = 0.3
            
            print(f"✅ Partner accessibility calculated: mean = {self.data['partner_accessibility'].mean():.2f}")
        except Exception as e:
            print(f"❌ Error calculating partner accessibility: {e}")
            self.data['partner_accessibility'] = 0.3
        
        print("✅ Feature engineering completed!")
        return self.data
    
    def encode_categorical_features(self):
        """Encode categorical variables for ML"""
        print("🔤 Encoding categorical features...")
        
        categorical_columns = [
            'university_type', 'country', 'field_of_study', 
            'specialization', 'city', 'partner_name'
        ]
        
        available_categorical = []
        for col in categorical_columns:
            if col in self.data.columns:
                unique_count = self.data[col].nunique()
                if unique_count > 1:
                    available_categorical.append(col)
                else:
                    print(f"   ⚠️  Skipping {col}: only {unique_count} unique value(s)")
        
        for col in available_categorical:
            try:
                self.label_encoders[col] = LabelEncoder()
                self.data[col] = self.data[col].fillna('Unknown')
                self.data[col + '_encoded'] = self.label_encoders[col].fit_transform(self.data[col])
                print(f"   ✅ Encoded: {col} -> {col}_encoded ({self.data[col].nunique()} categories)")
            except Exception as e:
                print(f"   ❌ Error encoding {col}: {e}")
                self.data[col + '_encoded'] = 0
        
        print("✅ Categorical encoding completed!")
        return self.data
    
    def prepare_training_data(self):
        """Prepare final dataset for training"""
        print("📊 Preparing training data...")
        
        print("🎯 Creating target score...")
        try:
            self.data['target_score'] = (
                self.data['prestige_score'] * 0.3 +
                self.data['financial_accessibility'] * 0.25 + 
                (self.data['job_placement_rate'] / 100) * 0.2 +
                self.data['university_type_score'] * 0.15 +
                self.data['intake_flexibility'] * 0.1
            )
            
            max_score = self.data['target_score'].max()
            min_score = self.data['target_score'].min()
            
            if max_score > min_score:
                self.data['target_score'] = ((self.data['target_score'] - min_score) / (max_score - min_score)) * 100
            else:
                self.data['target_score'] = 50
            
            print(f"✅ Target score created: {self.data['target_score'].min():.1f}-{self.data['target_score'].max():.1f}")
        except Exception as e:
            print(f"❌ Error creating target score: {e}")
            self.data['target_score'] = 50
        
        base_features = [
            'academic_difficulty', 'financial_accessibility', 'prestige_score',
            'english_flexibility', 'duration_score', 'world_ranking',
            'tuition_fee_usd', 'job_placement_rate', 'visa_success_rate',
            'intake_flexibility', 'scholarship_score', 'partner_accessibility',
            'university_type_score'
        ]
        
        encoded_cols = [col for col in self.data.columns if col.endswith('_encoded')]
        
        available_features = []
        for col in base_features + encoded_cols:
            if col in self.data.columns:
                nan_count = self.data[col].isna().sum()
                if nan_count == 0:
                    available_features.append(col)
                elif nan_count < len(self.data[col]) * 0.3:
                    if pd.api.types.is_numeric_dtype(self.data[col]):
                        self.data[col] = self.data[col].fillna(self.data[col].median())
                    else:
                        self.data[col] = self.data[col].fillna(self.data[col].mode()[0])
                    available_features.append(col)
                    print(f"⚠️  Filled {nan_count} missing values in {col}")
                else:
                    print(f"❌ Skipping {col}: {nan_count} missing values ({nan_count/len(self.data[col])*100:.1f}%)")
        
        print(f"📋 Using {len(available_features)} features")
        print("Features:")
        for i, feat in enumerate(available_features):
            print(f"  {i+1:2d}. {feat}")
        
        X = self.data[available_features].copy()
        y = self.data['target_score'].copy()
        
        if X.isna().any().any():
            print("⚠️  Still have NaN values, filling with column means...")
            X = X.fillna(X.mean())
        
        print(f"✅ Training data prepared: {X.shape[0]} samples, {X.shape[1]} features")
        print(f"📊 Target score stats: mean={y.mean():.2f}, std={y.std():.2f}")
        
        return X, y, available_features