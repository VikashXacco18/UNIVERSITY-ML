# import pandas as pd
# import numpy as np
# from sklearn.ensemble import GradientBoostingRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_absolute_error, r2_score
# import joblib
# import warnings
# from data_preprocessor import DataPreprocessor

# # Suppress warnings
# warnings.filterwarnings('ignore')

# class UniversityRecommender:
#     def __init__(self):
#         self.model = None
#         self.preprocessor = None
#         self.feature_columns = []
        
#     def train(self, csv_path='../data/University Programs Database'):
#         """Train the recommendation model"""
#         print("🎯 Training University Recommendation Model...")
#         print("=" * 60)
        
#         try:
#             # Load and preprocess data
#             self.preprocessor = DataPreprocessor()
#             print("\n1️⃣  Loading data...")
#             data = self.preprocessor.load_data(csv_path)
            
#             print("\n2️⃣  Cleaning numeric columns...")
#             data = self.preprocessor.clean_numeric_columns()
            
#             print("\n3️⃣  Engineering features...")
#             data = self.preprocessor.engineer_features()
            
#             print("\n4️⃣  Encoding categorical features...")
#             data = self.preprocessor.encode_categorical_features()
            
#             print("\n5️⃣  Preparing training data...")
#             X, y, self.feature_columns = self.preprocessor.prepare_training_data()
            
#             print(f"\n📊 Data Summary:")
#             print(f"   Samples: {X.shape[0]}")
#             print(f"   Features: {X.shape[1]}")
#             print(f"   Target range: {y.min():.1f} - {y.max():.1f}")
            
#             # Split data
#             print("\n6️⃣  Splitting data...")
#             X_train, X_test, y_train, y_test = train_test_split(
#                 X, y, test_size=0.2, random_state=42, shuffle=True
#             )
            
#             print(f"   Train: {X_train.shape[0]} samples")
#             print(f"   Test: {X_test.shape[0]} samples")
            
#             # Train model
#             print("\n7️⃣  Training Gradient Boosting model...")
#             self.model = GradientBoostingRegressor(
#                 n_estimators=100,
#                 max_depth=5,
#                 learning_rate=0.1,
#                 min_samples_split=10,
#                 min_samples_leaf=4,
#                 random_state=42,
#                 verbose=0
#             )
            
#             self.model.fit(X_train, y_train)
            
#             # Evaluate model
#             print("\n8️⃣  Evaluating model...")
#             train_pred = self.model.predict(X_train)
#             test_pred = self.model.predict(X_test)
            
#             train_score = r2_score(y_train, train_pred)
#             test_score = r2_score(y_test, test_pred)
#             train_mae = mean_absolute_error(y_train, train_pred)
#             test_mae = mean_absolute_error(y_test, test_pred)
            
#             print("\n" + "=" * 60)
#             print("✅ MODEL TRAINING COMPLETE!")
#             print("=" * 60)
#             print(f"\n📊 Performance Metrics:")
#             print(f"   Training R² Score: {train_score:.3f}")
#             print(f"   Test R² Score: {test_score:.3f}")
#             print(f"   Training MAE: {train_mae:.2f}")
#             print(f"   Test MAE: {test_mae:.2f}")
            
#             # Show feature importances
#             if hasattr(self.model, 'feature_importances_'):
#                 print(f"\n🏆 Top 5 Important Features:")
#                 feature_importance = pd.DataFrame({
#                     'feature': self.feature_columns,
#                     'importance': self.model.feature_importances_
#                 }).sort_values('importance', ascending=False)
                
#                 for i, row in feature_importance.head(5).iterrows():
#                     print(f"   {i+1}. {row['feature']}: {row['importance']:.3f}")
            
#             return self.model
            
#         except Exception as e:
#             print(f"\n❌ Error during training: {e}")
#             import traceback
#             traceback.print_exc()
#             return None
    
#     def save_model(self, model_path='university_recommender_model.joblib'):
#         """Save the trained model"""
#         if self.model is None:
#             raise ValueError("No model to save!")
            
#         model_data = {
#             'model': self.model,
#             'feature_columns': self.feature_columns,
#             'preprocessor': self.preprocessor
#         }
        
#         joblib.dump(model_data, model_path)
#         print(f"\n💾 Model saved to: {model_path}")
#         print(f"   Model size: {os.path.getsize(model_path) / 1024 / 1024:.2f} MB")

# # Main execution
# if __name__ == "__main__":
#     import os
    
#     print("=" * 60)
#     print("UNIVERSITY RECOMMENDER SYSTEM - MODEL TRAINING")
#     print("=" * 60)
    
#     # Check if data file exists
#     data_file = '../data/University Programs Database.csv'
#     if not os.path.exists(data_file):
#         print(f"\n❌ Data file not found: {data_file}")
#         print("Please ensure the CSV file is in the current directory.")
#         print(f"Current directory: {os.getcwd()}")
#         exit(1)
    
#     # Train the model
#     recommender = UniversityRecommender()
#     model = recommender.train(data_file)
    
#     if model is not None:
#         # Save the model
#         recommender.save_model()
#         print("\n🎉 Training completed successfully!")
#     else:
#         print("\n❌ Training failed. Please check the error messages above.")

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import warnings
import os
from data_preprocessor import DataPreprocessor

warnings.filterwarnings('ignore')

class UniversityRecommender:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.feature_columns = []
        
    def train(self, csv_path='Final_Dataset.csv'):
        print("🎯 Training University Recommendation Model...")
        print("=" * 60)
        
        try:
            self.preprocessor = DataPreprocessor()
            print("\n1️⃣  Loading data...")
            data = self.preprocessor.load_data(csv_path)
            
            print("\n2️⃣  Cleaning numeric columns...")
            data = self.preprocessor.clean_numeric_columns()
            
            print("\n3️⃣  Engineering features...")
            data = self.preprocessor.engineer_features()
            
            print("\n4️⃣  Encoding categorical features...")
            data = self.preprocessor.encode_categorical_features()
            
            print("\n5️⃣  Preparing training data...")
            X, y, self.feature_columns = self.preprocessor.prepare_training_data()
            
            print(f"\n📊 Data Summary:")
            print(f"   Samples: {X.shape[0]}")
            print(f"   Features: {X.shape[1]}")
            print(f"   Target range: {y.min():.1f} - {y.max():.1f}")
            
            print("\n6️⃣  Splitting data...")
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, shuffle=True
            )
            
            print(f"   Train: {X_train.shape[0]} samples")
            print(f"   Test: {X_test.shape[0]} samples")
            
            print("\n7️⃣  Training Gradient Boosting model...")
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                min_samples_split=10,
                min_samples_leaf=4,
                random_state=42,
                verbose=0
            )
            
            self.model.fit(X_train, y_train)
            
            print("\n8️⃣  Evaluating model...")
            train_pred = self.model.predict(X_train)
            test_pred = self.model.predict(X_test)
            
            train_score = r2_score(y_train, train_pred)
            test_score = r2_score(y_test, test_pred)
            train_mae = mean_absolute_error(y_train, train_pred)
            test_mae = mean_absolute_error(y_test, test_pred)
            
            print("\n" + "=" * 60)
            print("✅ MODEL TRAINING COMPLETE!")
            print("=" * 60)
            print(f"\n📊 Performance Metrics:")
            print(f"   Training R² Score: {train_score:.3f}")
            print(f"   Test R² Score: {test_score:.3f}")
            print(f"   Training MAE: {train_mae:.2f}")
            print(f"   Test MAE: {test_mae:.2f}")
            
            if hasattr(self.model, 'feature_importances_'):
                print(f"\n🏆 Top 5 Important Features:")
                feature_importance = pd.DataFrame({
                    'feature': self.feature_columns,
                    'importance': self.model.feature_importances_
                }).sort_values('importance', ascending=False)
                
                for i, row in feature_importance.head(5).iterrows():
                    print(f"   {i+1}. {row['feature']}: {row['importance']:.3f}")
            
            return self.model
            
        except Exception as e:
            print(f"\n❌ Error during training: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def save_model(self, model_path='university_recommender_model.joblib'):
        if self.model is None:
            raise ValueError("No model to save!")
            
        model_data = {
            'model': self.model,
            'feature_columns': self.feature_columns,
            'preprocessor': self.preprocessor
        }
        
        joblib.dump(model_data, model_path)
        print(f"\n💾 Model saved to: {model_path}")
        if os.path.exists(model_path):
            print(f"   Model size: {os.path.getsize(model_path) / 1024 / 1024:.2f} MB")

if __name__ == "__main__":
    import os
    
    print("=" * 60)
    print("UNIVERSITY RECOMMENDER SYSTEM - MODEL TRAINING")
    print("=" * 60)
    
    data_file = '../data/Final_Dataset.csv'
    if not os.path.exists(data_file):
        print(f"\n❌ Data file not found: {data_file}")
        print(f"Current directory: {os.getcwd()}")
        exit(1)
    
    recommender = UniversityRecommender()
    model = recommender.train(data_file)
    
    if model is not None:
        recommender.save_model()
        print("\n🎉 Training completed successfully!")
    else:
        print("\n❌ Training failed. Please check the error messages above.")