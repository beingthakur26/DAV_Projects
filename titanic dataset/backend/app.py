"""
Titanic Survival Predictor - Flask Backend API
Serves the trained Random Forest model via REST API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# ============ LOAD SAVED MODEL & PREPROCESSING INFO ============
print("🔄 Loading model and preprocessing data...")

# Get the directory of this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load trained model
with open(os.path.join(BASE_DIR, 'models', 'titanic_model.pkl'), 'rb') as f:
    model = pickle.load(f)

# Load feature names
with open(os.path.join(BASE_DIR, 'models', 'titanic_features.pkl'), 'rb') as f:
    final_features = pickle.load(f)

# Load preprocessing information
with open(os.path.join(BASE_DIR, 'models', 'titanic_preprocessing.pkl'), 'rb') as f:
    preprocessing_info = pickle.load(f)

print("✅ Model loaded successfully")


# ============ HEALTH CHECK ENDPOINT ============
@app.route('/health', methods=['GET'])
def health_check():
    """Check if API is running"""
    return jsonify({
        'status': 'API is running ✅',
        'model': 'Titanic Survival Predictor',
        'accuracy': '81.56%'
    }), 200


# ============ PREDICTION ENDPOINT ============
@app.route('/predict', methods=['POST'])
def predict():
    """
    Make a prediction based on passenger data
    
    Expected JSON input:
    {
        "Pclass": 1,
        "Sex": "male",           # or "female"
        "Age": 25,
        "SibSp": 1,               # Number of siblings/spouses
        "Parch": 2,               # Number of parents/children
        "Embarked": "S"           # Port: C, Q, or S
    }
    """
    
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Embarked']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'status': 'error'
                }), 400
        
        # ========== DATA PREPROCESSING ==========
        # Convert Sex to numerical (0=male, 1=female)
        sex_map = {'male': 0, 'female': 1}
        if data['Sex'].lower() not in sex_map:
            return jsonify({
                'error': 'Sex must be "male" or "female"',
                'status': 'error'
            }), 400
        
        sex_encoded = sex_map[data['Sex'].lower()]
        
        # Handle missing age (use median)
        age = data.get('Age', preprocessing_info['median_age'])
        if pd.isna(age) or age is None:
            age = preprocessing_info['median_age']
        
        # Handle embarkation port
        embarked = data.get('Embarked', preprocessing_info['mode_embarked']).upper()
        if embarked not in ['C', 'Q', 'S']:
            return jsonify({
                'error': 'Embarked must be C (Cherbourg), Q (Queenstown), or S (Southampton)',
                'status': 'error'
            }), 400
        
        # Calculate family size
        sibsp = int(data['SibSp'])
        parch = int(data['Parch'])
        family_size = sibsp + parch + 1
        
        # Determine if alone
        is_alone = 1 if family_size == 1 else 0
        
        # One-hot encoding for port
        port_c = 1 if embarked == 'C' else 0
        port_q = 1 if embarked == 'Q' else 0
        port_s = 1 if embarked == 'S' else 0
        
        # Create feature vector using the same order as training
        feature_values = [
            int(data['Pclass']),
            sex_encoded,
            float(age),
            sibsp,
            parch,
            family_size,
            is_alone,
            port_c,
            port_q,
            port_s
        ]
        
        # Create DataFrame with correct column names
        input_df = pd.DataFrame([feature_values], columns=final_features)
        
        # ========== MAKE PREDICTION ==========
        prediction = model.predict(input_df)[0]
        probabilities = model.predict_proba(input_df)[0]
        
        # Format response
        response = {
            'status': 'success',
            'prediction': int(prediction),
            'prediction_text': 'SURVIVED ✅' if prediction == 1 else 'DID NOT SURVIVE ❌',
            'confidence': {
                'did_not_survive': float(probabilities[0]) * 100,
                'survived': float(probabilities[1]) * 100
            },
            'input_data': {
                'Pclass': int(data['Pclass']),
                'Sex': data['Sex'],
                'Age': float(age),
                'SibSp': sibsp,
                'Parch': parch,
                'Embarked': embarked,
                'FamilySize': family_size,
                'IsAlone': bool(is_alone)
            }
        }
        
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500


# ============ GET FEATURES ENDPOINT ============
@app.route('/features', methods=['GET'])
def get_features():
    """Get list of required features for predictions"""
    return jsonify({
        'features': final_features,
        'description': 'Features required to make a prediction'
    }), 200


# ============ EXAMPLE ENDPOINT ============
@app.route('/example', methods=['GET'])
def get_example():
    """Get example prediction request"""
    example_input = {
        "Pclass": 1,
        "Sex": "female",
        "Age": 25,
        "SibSp": 1,
        "Parch": 0,
        "Embarked": "S"
    }
    
    return jsonify({
        'example_input': example_input,
        'description': 'Example POST data to /predict endpoint',
        'notes': {
            'Pclass': 'Ticket class: 1 (1st), 2 (2nd), or 3 (3rd)',
            'Sex': '"male" or "female"',
            'Age': 'Age in years (float or int)',
            'SibSp': 'Number of siblings/spouses aboard',
            'Parch': 'Number of parents/children aboard',
            'Embarked': '"C" (Cherbourg), "Q" (Queenstown), or "S" (Southampton)'
        }
    }), 200


# ============ ERROR HANDLERS ============
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found', 'status': 'error'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error', 'status': 'error'}), 500


# ============ RUN SERVER ============
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Titanic Survival Predictor API")
    print("="*60)
    print("\n📍 Available Endpoints:")
    print("  • GET  /health           - Check if API is running")
    print("  • POST /predict          - Make a prediction")
    print("  • GET  /features         - Get required features")
    print("  • GET  /example          - Get example input")
    print("\n🔗 API Documentation:")
    print("  Base URL: https://titanic-survival-api-ef66.onrender.com")
    print("  POST https://titanic-survival-api-ef66.onrender.com/predict")
    print("\n" + "="*60 + "\n")
    
    # Run on all interfaces so it can be accessed from frontend
    app.run(debug=True, host='0.0.0.0', port=5000)
