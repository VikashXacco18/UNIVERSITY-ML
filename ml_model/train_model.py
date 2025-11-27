# import pandas as pd
# import numpy as np
# from sklearn.ensemble import GradientBoostingRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_absolute_error
# import joblib
# from data_preprocessor import DataPreprocessor

# class UniversityRecommender:
#     def __init__(self):
#         self.model = None
#         self.preprocessor = None
#         self.feature_columns = []
        
#     def train(self, csv_path='../data/University Programs Database.csv'):
#         """Train the recommendation model"""
#         print("🎯 Training University Recommendation Model...")
        
#         # Load and preprocess data
#         self.preprocessor = DataPreprocessor()
#         data = self.preprocessor.load_data(csv_path)
#         data = self.preprocessor.clean_numeric_columns()
#         data = self.preprocessor.engineer_features()
#         data = self.preprocessor.encode_categorical_features()
#         X, y, self.feature_columns = self.preprocessor.prepare_training_data()
        
#         # Split data
#         X_train, X_test, y_train, y_test = train_test_split(
#             X, y, test_size=0.2, random_state=42
#         )
        
#         # Train model
#         self.model = GradientBoostingRegressor(
#             n_estimators=100,
#             max_depth=6,
#             learning_rate=0.1,
#             random_state=42
#         )
        
#         self.model.fit(X_train, y_train)
        
#         # Evaluate model
#         train_score = self.model.score(X_train, y_train)
#         test_score = self.model.score(X_test, y_test)
#         y_pred = self.model.predict(X_test)
#         mae = mean_absolute_error(y_test, y_pred)
        
#         print(f"✅ Model Training Completed!")
#         print(f"📊 Training R² Score: {train_score:.3f}")
#         print(f"📊 Test R² Score: {test_score:.3f}")
#         print(f"📊 Mean Absolute Error: {mae:.2f}")
        
#         return self.model
    
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
#         print(f"✅ Model saved to {model_path}")

# # Train and save the model
# if __name__ == "__main__":
#     recommender = UniversityRecommender()
#     model = recommender.train()
#     recommender.save_model()
#     print("🎉 ML Model training completed successfully!")

# train_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import joblib
from data_preprocessor import DataPreprocessor

class UniversityRecommender:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.feature_columns = []
        
    def train(self, csv_path='../data/University Programs Database.csv'):
        """Train the recommendation model"""
        print("🎯 Training University Recommendation Model...")
        
        # Load and preprocess data
        self.preprocessor = DataPreprocessor()
        data = self.preprocessor.load_data(csv_path)
        data = self.preprocessor.clean_numeric_columns()
        data = self.preprocessor.engineer_features()
        data = self.preprocessor.encode_categorical_features()
        X, y, self.feature_columns = self.preprocessor.prepare_training_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model = GradientBoostingRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        y_pred = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        
        print(f"✅ Model Training Completed!")
        print(f"📊 Training R² Score: {train_score:.3f}")
        print(f"📊 Test R² Score: {test_score:.3f}")
        print(f"📊 Mean Absolute Error: {mae:.2f}")
        
        return self.model
    
    def save_model(self, model_path='university_recommender_model.joblib'):
        """Save the trained model"""
        if self.model is None:
            raise ValueError("No model to save!")
            
        model_data = {
            'model': self.model,
            'feature_columns': self.feature_columns,
            'preprocessor': self.preprocessor
        }
        
        joblib.dump(model_data, model_path)
        print(f"✅ Model saved to {model_path}")

# Train and save the model
if __name__ == "__main__":
    recommender = UniversityRecommender()
    model = recommender.train()
    recommender.save_model()
    print("🎉 ML Model training completed successfully!")