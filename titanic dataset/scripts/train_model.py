"""
Titanic Model Training Script
Loads data, trains Random Forest model, and saves it for web app use
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

# Get paths relative to script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
MODEL_DIR = os.path.join(BASE_DIR, '..', 'backend', 'models')

# Create model directory if it doesn't exist
os.makedirs(MODEL_DIR, exist_ok=True)

# Load the dataset
print("📚 Loading Titanic dataset...")
data = pd.read_csv(os.path.join(DATA_DIR, 'titanic-data.csv'))

# Create a copy for modeling
model_data = data.copy()

# ============ DATA PREPROCESSING ============
print("🔧 Preprocessing data...")

# 1. Fill missing 'age' values with the median
median_age = model_data['Age'].median()
model_data['Age'] = model_data['Age'].fillna(median_age)

# 2. Fill missing 'embarked' values with the mode
mode_embarked = model_data['Embarked'].mode()[0]
model_data['Embarked'] = model_data['Embarked'].fillna(mode_embarked)

# 3. Convert 'sex' to numerical (0 for male, 1 for female)
model_data['Sex'] = model_data['Sex'].map({'male': 0, 'female': 1})

# ============ FEATURE ENGINEERING ============
print("⚙️ Engineering features...")

# Calculate Family Size
model_data['family_size'] = model_data['SibSp'] + model_data['Parch'] + 1

# Create 'is_alone' feature
model_data['is_alone'] = 0
model_data.loc[model_data['family_size'] == 1, 'is_alone'] = 1

# One-Hot Encoding for Embarked
model_data = pd.get_dummies(model_data, columns=['Embarked'], prefix='port')

# ============ MODEL TRAINING ============
print("🤖 Training Random Forest model...")

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
print("\n📊 Model Evaluation Results:")
print("-" * 50)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Model Accuracy: {accuracy * 100:.2f}%")
print(f"📈 Total Test Samples: {len(y_test)}")
print(f"✔️ Correct Predictions: {sum(y_pred == y_test)}")
print(f"✖️ Incorrect Predictions: {sum(y_pred != y_test)}")

print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred, target_names=['Did Not Survive', 'Survived']))

# ============ SAVE THE MODEL ============
print("\n💾 Saving model...")

# Save model
model_path = os.path.join(MODEL_DIR, 'titanic_model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(model, f)

# Save feature names (important for preprocessing)
features_path = os.path.join(MODEL_DIR, 'titanic_features.pkl')
with open(features_path, 'wb') as f:
    pickle.dump(final_features, f)

# Save preprocessing info (median age and mode embarked)
preprocessing_info = {
    'median_age': median_age,
    'mode_embarked': mode_embarked
}
preprocessing_path = os.path.join(MODEL_DIR, 'titanic_preprocessing.pkl')
with open(preprocessing_path, 'wb') as f:
    pickle.dump(preprocessing_info, f)

print(f"✅ Model saved to: {model_path}")
print(f"✅ Features saved to: {features_path}")
print(f"✅ Preprocessing info saved to: {preprocessing_path}")
print("\n🚀 Ready for web app deployment!")
