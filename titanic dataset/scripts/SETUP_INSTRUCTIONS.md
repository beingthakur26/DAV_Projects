# 🚢 Titanic Survival Predictor - Complete Web App Setup

## ✅ What's Included

### Backend (Flask API)
- **app.py** - Flask REST API with prediction endpoint
- **train_model.py** - Model training script
- **requirements.txt** - Python dependencies
- **titanic_model.pkl** - Trained Random Forest model
- **titanic_features.pkl** - Feature names for preprocessing
- **titanic_preprocessing.pkl** - Preprocessing parameters (median age, mode embarked)
- **titanic-data.csv** - Original dataset (891 passengers)

### Frontend (React + Vite)
- **titanic-frontend/** - Complete React application
  - **App.jsx** - Main component with form and predictions
  - **App.css** - Beautiful styling with gradients
  - **main.jsx** - React entry point
  - **index.html** - HTML template
  - **package.json** - Dependencies configured
  - **vite.config.ts** - Vite bundler config
  - **tsconfig.json** - TypeScript config

---

## 🚀 Quick Start Guide

### Step 1: Install Backend Dependencies
```bash
cd "c:\Users\singh\Desktop\DA&V Projects\titanic dataset"
pip install -r requirements.txt
```

### Step 2: Start Flask API Server
```bash
python app.py
```
✅ API will run on: **http://localhost:5000**

API Endpoints:
- `GET /health` - Check if API is running
- `POST /predict` - Make a prediction
- `GET /example` - Get example input format

### Step 3: Start Frontend Development Server
In a **new terminal**:
```bash
cd "c:\Users\singh\Desktop\DA&V Projects\titanic dataset\titanic-frontend"
npm run dev
```
✅ Frontend will run on: **http://localhost:5173**

---

## 📊 Model Information

| Aspect | Details |
|--------|---------|
| **Algorithm** | Random Forest Classifier (100 trees) |
| **Accuracy** | 81.56% |
| **Training Data** | 712 samples (80%) |
| **Test Data** | 179 samples (20%) |
| **Features** | 10 engineered features |

### Input Features Required:
```json
{
  "Pclass": 1,          // 1=1st, 2=2nd, 3=3rd Class
  "Sex": "female",      // "male" or "female"
  "Age": 25,            // Age in years
  "SibSp": 1,           // Number of siblings/spouses
  "Parch": 2,           // Number of parents/children
  "Embarked": "S"       // "S"=Southampton, "C"=Cherbourg, "Q"=Queenstown
}
```

### Prediction Output:
```json
{
  "status": "success",
  "prediction": 1,                    // 0 = Did Not Survive, 1 = Survived
  "prediction_text": "SURVIVED ✅",
  "confidence": {
    "did_not_survive": 15.5,
    "survived": 84.5
  },
  "input_data": {...}
}
```

---

## 🧪 Test the API (Without Frontend)

Using PowerShell or Command Prompt:

```powershell
# Test 1: Check API is running
Invoke-WebRequest http://localhost:5000/health

# Test 2: Make a prediction (Female, 1st Class, Age 25)
$body = @{
    Pclass = 1
    Sex = "female"
    Age = 25
    SibSp = 1
    Parch = 0
    Embarked = "S"
} | ConvertTo-Json

Invoke-WebRequest -Uri http://localhost:5000/predict `
  -Method POST `
  -Body $body `
  -ContentType "application/json"
```

---

## 📁 Folder Structure
```
titanic dataset/
├── app.py                         # Flask API
├── train_model.py                 # Model training script
├── requirements.txt               # Python dependencies
├── titanic-data.csv              # Dataset
├── titanic_model.pkl             # ✅ Trained model
├── titanic_features.pkl          # ✅ Features list
├── titanic_preprocessing.pkl     # ✅ Preprocessing info
├── SETUP_INSTRUCTIONS.md          # This file
└── titanic-frontend/             # React frontend
    ├── src/
    │   ├── App.jsx               # Main component
    │   ├── App.css               # Styling
    │   ├── main.jsx              # Entry point
    │   └── index.css             # Global styles
    ├── index.html                # HTML template
    ├── package.json              # Dependencies
    ├── vite.config.ts            # Vite config
    └── node_modules/             # (Created after npm install)
```

---

## ⚙️ Features of the Web App

✅ **Beautiful UI** - Gradient background, smooth animations
✅ **Real-time Predictions** - Instant survival prediction
✅ **Confidence Scores** - See percentage probabilities
✅ **Prediction History** - Track last 10 predictions
✅ **Feature Analysis** - Understand factors affecting survival
✅ **Responsive Design** - Works on mobile & desktop
✅ **Error Handling** - Validates input and shows errors
✅ **Educational Content** - Explains historical context

---

## 🔧 Troubleshooting

### "Connection Refused" Error?
- [ ] Make sure Flask API is running (`python app.py`)
- [ ] Check API is on port 5000
- [ ] Try `http://localhost:5000/health`

### "Module Not Found" Error?
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend not loading?
```bash
# Reinstall frontend dependencies
cd titanic-frontend
npm install
npm run dev
```

### Model pickle files missing?
```bash
# Retrain the model
python train_model.py
```

---

## 📈 Next Steps (Advanced)

### Deploy to Production:
1. **Backend**: Deploy Flask app to Heroku/AWS/Railway
2. **Frontend**: Deploy React build to Vercel/Netlify
3. **Update API URL** in App.jsx to production endpoint

### Improvements:
- Add model performance metrics dashboard
- Add batch prediction testing
- Create admin panel for model retraining
- Add user authentication & data logging
- Export predictions to CSV

---

## 📞 Support

For issues with:
- **Flask API**: Check [Flask Documentation](https://flask.palletsprojects.com/)
- **React**: Check [React Documentation](https://react.dev/)
- **Scikit-learn**: Check [Scikit-learn Docs](https://scikit-learn.org/)

---

**Ready to predict Titanic survival probabilities! 🚢**
