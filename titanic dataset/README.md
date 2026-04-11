# 🚢 Titanic Survival Predictor

An end-to-end Machine Learning application that predicts the survival probability of Titanic passengers using a **Random Forest Classifier**. This project features a modular architecture with a Python Flask API and a premium, responsive web dashboard.

---

## 📂 Project Structure

The project has been organized into a professional, modular layout:

```text
titanic-project/
├── backend/                # Flask API and Model Logic
│   ├── app.py              # Main API entry point
│   ├── requirements.txt    # Python dependencies
│   └── models/             # Serialized ML models (.pkl)
├── frontend/               # Premium Web Interface
│   ├── index.html          # Main dashboard
│   └── assets/             # CSS, JS, and Images
├── data/                   # Raw & processed datasets
│   └── titanic-data.csv
├── notebooks/              # Research and EDA
│   └── EXP_1.ipynb         # Data analysis notebook
└── scripts/                # Utility & startup scripts
    ├── train_model.py      # Script to retrain the model
    └── run_all.ps1         # Unified startup script
```

---

## 🤖 How the Model Works

### 1. The Algorithm

The predictor uses a **Random Forest Classifier**, an ensemble learning method that builds multiple decision trees and merges them together to get a more accurate and stable prediction. It was chosen for its high accuracy (approx. **81.56%**) and robustness against feature noise.

### 2. Feature Engineering

The model doesn't just look at raw data; it extracts meaningful features:

* **Family Size**: Calculated as `SibSp + Parch + 1`.
* **Is Alone**: A binary indicator (1 if Family Size is 1, else 0).
* **Port Encoding**: Port of embarkation is one-hot encoded (Cherbourg, Queenstown, Southampton).
* **Gender Encoding**: Converted to binary (0 for male, 1 for female).

### 3. Data Preprocessing

* **Age Imputation**: Missing age values are filled with the **median** age of the dataset to prevent bias from outliers.
* **Embarkation Imputation**: Missing port values are filled with the **mode** (most frequent port).

---

## 🚀 Installation & Setup

### Prerequisites

* Python 3.8+
* A modern web browser

### 1. Install Dependencies

Navigate to the root directory and install the required Python libraries:

```bash
pip install -r backend/requirements.txt
```

### 2. Starting the Application

#### The Quick Way (Windows)

Run the orchestration script to launch the backend and frontend simultaneously:

```powershell
./scripts/run_all.ps1
```

#### The Manual Way

1. **Start Backend**:
   ```bash
   cd backend
   python app.py
   ```

2. **Open Frontend**:
   Navigate to `frontend/index.html` and open it in your browser (or use a local server like Live Server in VS Code).

---

## 📡 API Reference

The backend exposes a RESTful API on `http://localhost:5000`:

### `POST /predict`

Submit passenger data to get a prediction.

**Payload:**

```json
{
  "Pclass": 1,
  "Sex": "female",
  "Age": 25,
  "SibSp": 1,
  "Parch": 0,
  "Embarked": "S"
}
```

### `GET /health`

Returns the status of the API and model accuracy.

---

## 🧪 Development

To retrain the model with updated data, run:

```bash
python scripts/train_model.py
```

This will automatically update the `.pkl` files in the `backend/models/` directory.

---

### AI Historical Research Lab | 2026
