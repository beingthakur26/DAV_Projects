"""
Titanic Model Retraining Script for Production
Retrains the model in the exact production environment and saves using joblib
to resolve version mismatch and numpy._core ModuleNotFoundError.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import sys

print(f"Python version: {sys.version}")
print(f"NumPy version: {np.__version__}")
import sklearn
print(f"Scikit-learn version: {sklearn.__version__}")
print(f"Pandas version: {pd.__version__}")
print(f"Joblib version: {joblib.__version__}")

# Get paths relative to script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
MODEL_DIR = os.path.join(BASE_DIR, '..', 'backend', 'models')

# Ensure directories exist
os.makedirs(MODEL_DIR, exist_ok=True)

data_path = os.path.join(DATA_DIR, 'titanic-data.csv')
if not os.path.exists(data_path):
    print("\nError: Dataset not found at " + data_path)
    sys.exit(1)

# Load the dataset
print("\nLoading Titanic dataset...")
data = pd.read_csv(data_path)

# Create a copy for modeling
model_data = data.copy()

# ============ DATA PREPROCESSING ============
print("Preprocessing data...")

# 1. Fill missing 'age' values with the median
median_age = model_data['Age'].median()
model_data['Age'] = model_data['Age'].fillna(median_age)

# 2. Fill missing 'embarked' values with the mode
mode_embarked = model_data['Embarked'].mode()[0]
model_data['Embarked'] = model_data['Embarked'].fillna(mode_embarked)

# 3. Convert 'sex' to numerical (0 for male, 1 for female)
model_data['Sex'] = model_data['Sex'].map({'male': 0, 'female': 1})

# ============ FEATURE ENGINEERING ============
print("Engineering features...")

# Calculate Family Size
model_data['family_size'] = model_data['SibSp'] + model_data['Parch'] + 1

# Create 'is_alone' feature
model_data['is_alone'] = 0
model_data.loc[model_data['family_size'] == 1, 'is_alone'] = 1

# One-Hot Encoding for Embarked
model_data = pd.get_dummies(model_data, columns=['Embarked'], prefix='port')

# ============ MODEL TRAINING ============
print("Training Random Forest model...")

# Select features (must match what the web app will use)
final_features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'family_size', 'is_alone', 
                  'port_C', 'port_Q', 'port_S']

X = model_data[final_features]
y = model_data['Survived']

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest with 100 trees
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ============ MODEL EVALUATION ============
print("\nModel Evaluation Results:")
print("-" * 50)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model Accuracy: {accuracy * 100:.2f}%")
print(f"Total Test Samples: {len(y_test)}")
print(f"Correct Predictions: {sum(y_pred == y_test)}")
print(f"Incorrect Predictions: {sum(y_pred != y_test)}")

# ============ SAVE THE MODEL USING JOBLIB ============
print("\nSaving model using joblib...")

# Save model
model_path = os.path.join(MODEL_DIR, 'titanic_model.joblib')
joblib.dump(model, model_path)

# Save feature names
features_path = os.path.join(MODEL_DIR, 'titanic_features.joblib')
joblib.dump(final_features, features_path)

# Save preprocessing info
preprocessing_info = {
    'median_age': median_age,
    'mode_embarked': mode_embarked
}
preprocessing_path = os.path.join(MODEL_DIR, 'titanic_preprocessing.joblib')
joblib.dump(preprocessing_info, preprocessing_path)

print(f"Model saved to: {model_path}")
print(f"Features saved to: {features_path}")
print(f"Preprocessing info saved to: {preprocessing_path}")
print("\nRetraining complete! Production models are ready.")
