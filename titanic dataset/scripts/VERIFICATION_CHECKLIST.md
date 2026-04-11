# ✅ Titanic Survival Predictor - Setup Verification Checklist

## 📋 Pre-Requisites
- [ ] Python 3.7+ installed
- [ ] pip (Python package manager) installed
- [ ] Node.js and npm installed
- [ ] Git (optional, for version control)

## 🔧 Installation Steps

### Step 1: Install Python Dependencies
```bash
cd "c:\Users\singh\Desktop\DA&V Projects\titanic dataset"
pip install -r requirements.txt
```
**Expected packages:**
- Flask==2.3.3 ✅
- Flask-CORS==4.0.0 ✅
- pandas==2.0.3 ✅
- numpy==1.24.3 ✅
- scikit-learn==1.3.0 ✅

### Step 2: Verify Model Files Exist
Check these files are present:
- [ ] `titanic_model.pkl` (Model artifact)
- [ ] `titanic_features.pkl` (Feature names)
- [ ] `titanic_preprocessing.pkl` (Preprocessing parameters)
- [ ] `titanic-data.csv` (Dataset)

### Step 3: Install Frontend Dependencies
```bash
cd titanic-frontend
npm install
```

Expected packages:
- [ ] React ^18.2.0
- [ ] React-DOM ^18.2.0
- [ ] Vite ^4.4.5
- [ ] TypeScript ^5.0.2

## 🚀 Running the Application

### Quick Start (All-in-One)
**Option A: Batch Script (Windows)**
```bash
START_APP.bat
```

**Option B: PowerShell Script**
```powershell
.\START_APP.ps1
```

### Manual Start (Separate terminals)

**Terminal 1 - Backend API:**
```bash
cd "c:\Users\singh\Desktop\DA&V Projects\titanic dataset"
python app.py
```
Expected: `Running on http://127.0.0.1:5000` ✅

**Terminal 2 - Frontend:**
```bash
cd "c:\Users\singh\Desktop\DA&V Projects\titanic dataset\titanic-frontend"
npm run dev
```
Expected: `Local: http://localhost:5173` ✅

## 🌐 Access Points

| Service | URL | Default Port |
|---------|-----|--------------|
| **Frontend** | http://localhost:5173 | 5173 |
| **Backend API** | http://localhost:5000 | 5000 |
| **Health Check** | http://localhost:5000/health | 5000 |

## ✨ Features Checklist

- [ ] Form loads with all input fields
- [ ] Can enter passenger data
- [ ] Submit button triggers prediction
- [ ] Prediction result displays
- [ ] Confidence bars show percentages
- [ ] Factors/analysis section appears
- [ ] Prediction history tracks previous guesses
- [ ] Clear form button resets inputs
- [ ] Error messages display if API unreachable
- [ ] Responsive design works on mobile

## 🧪 Test Case Examples

### Test 1: First Class Female (High Survival)
```
Class: 1st (1)
Gender: Female
Age: 25
SibSp: 1
Parch: 0
Embarked: Southampton
Expected: SURVIVED ✅ (~84% confidence)
```

### Test 2: Third Class Male (Low Survival)
```
Class: 3rd (3)
Gender: Male
Age: 40
SibSp: 0
Parch: 0
Embarked: Southampton
Expected: DID NOT SURVIVE ❌ (~75% confidence)
```

### Test 3: Child
```
Class: Any (1, 2, or 3)
Gender: Female or Male
Age: 5
SibSp: 0
Parch: 1
Embarked: Any (S, C, or Q)
Expected: SURVIVED ✅ (Children had priority)
```

## 🔍 API Endpoints (For Testing)

### 1. Health Check
```bash
curl http://localhost:5000/health
```

### 2. Get Features
```bash
curl http://localhost:5000/features
```

### 3. Get Example Input
```bash
curl http://localhost:5000/example
```

### 4. Make Prediction
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Pclass": 1,
    "Sex": "female",
    "Age": 25,
    "SibSp": 1,
    "Parch": 0,
    "Embarked": "S"
  }'
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Port 5000 already in use** | Change port in `app.py` line: `app.run(port=5001)` |
| **Port 5173 already in use** | Change port in `vite.config.ts` or `npm run dev -- --port 5174` |
| **Model not found** | Run `python train_model.py` in the root directory |
| **CORS errors** | Already handled in `app.py` with `CORS(app)` |
| **npm install fails** | Delete `node_modules` and `package-lock.json`, then retry |
| **Python version issues** | Ensure Python 3.7+ with `python --version` |

## 📊 Model Information

| Metric | Value |
|--------|-------|
| **Algorithm** | Random Forest (100 trees) |
| **Training Samples** | 712 (80%) |
| **Test Samples** | 179 (20%) |
| **Overall Accuracy** | 81.56% |
| **Survived Recall** | ~78% |
| **Not Survived Recall** | ~84% |

## 📁 File Structure (After Setup)

```
titanic dataset/
├── ✅ app.py                          (Flask API)
├── ✅ train_model.py                  (Training script)
├── ✅ requirements.txt                (Python deps)
├── ✅ titanic-data.csv                (Dataset)
├── ✅ titanic_model.pkl               (Model - 10MB)
├── ✅ titanic_features.pkl            (Features)
├── ✅ titanic_preprocessing.pkl       (Preprocessing)
├── ✅ SETUP_INSTRUCTIONS.md           (Instructions)
├── ✅ START_APP.bat                   (Quick start)
├── ✅ START_APP.ps1                   (PowerShell start)
├── ✅ VERIFICATION_CHECKLIST.md       (This file)
└── ✅ titanic-frontend/
    ├── node_modules/                  (Created by npm install)
    ├── src/
    │   ├── App.jsx                    (Main component)
    │   ├── App.css                    (Styling)
    │   ├── main.jsx                   (Entry point)
    │   └── index.css                  (Global styles)
    ├── public/
    ├── index.html                     (HTML)
    ├── package.json                   (Dependencies)
    ├── vite.config.ts                 (Build config)
    └── tsconfig.json                  (TS config)
```

## ✅ Final Verification

Before declaring success, verify:
1. [ ] `python app.py` starts without errors
2. [ ] Flask shows "Running on http://127.0.0.1:5000"
3. [ ] `npm run dev` starts without errors
4. [ ] Vite shows "Local: http://localhost:5173"
5. [ ] Desktop URL opens the UI
6. [ ] Form loads with all fields
7. [ ] API request succeeds
8. [ ] Prediction displays with correct format
9. [ ] Confidence bars render properly
10. [ ] No console errors in browser DevTools

---

## 🎉 You're All Set!

Your Titanic Survival Predictor web app is ready! Start with the Quick Start section and enjoy predicting survival chances! 🚢
