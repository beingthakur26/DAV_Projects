// Use your deployed Render URL here
const PRODUCTION_API_URL = 'https://titanic-survival-api-ef66.onrender.com'; 
const LOCAL_API_URL = 'https://titanic-survival-api-ef66.onrender.com';

const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? LOCAL_API_URL 
    : PRODUCTION_API_URL;

// DOM Elements
const form = document.getElementById('predictor-form');
const predictBtn = document.getElementById('predict-btn');
const resultSide = document.getElementById('result-side');
const loadingOverlay = document.getElementById('loading-overlay');
const statusDot = document.getElementById('api-status-dot');
const statusText = document.getElementById('api-status-text');

// Result elements
const resBadge = document.getElementById('status-badge');
const resOutput = document.getElementById('prediction-text');
const resConfidencePct = document.getElementById('confidence-percentage');
const resConfidenceFill = document.getElementById('confidence-fill');
const resClass = document.getElementById('res-class');
const resFamily = document.getElementById('res-family');
const resetBtn = document.getElementById('reset-btn');


// ✅ FIX 1: Proper timeout (fetch doesn't support timeout)
function fetchWithTimeout(url, options = {}, timeout = 20000) {
    return Promise.race([
        fetch(url, options),
        new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Request Timeout')), timeout)
        )
    ]);
}

// ✅ FIX 2: Retry logic (handles Render cold start)
async function fetchWithRetry(url, options, retries = 2) {
    for (let i = 0; i <= retries; i++) {
        try {
            return await fetchWithTimeout(url, options);
        } catch (err) {
            if (i === retries) throw err;
        }
    }
}


/**
 * Check Backend API Status
 */
async function checkApiStatus() {
    try {
        const response = await fetchWithTimeout(`${API_BASE}/health`);
        if (response.ok) {
            statusDot.className = 'status-dot online';
            statusText.innerText = 'System Online (AI Model Ready)';
        } else {
            throw new Error();
        }
    } catch (err) {
        statusDot.className = 'status-dot offline';
        statusText.innerText = 'System Offline (Server waking up or unreachable)';
    }
}


/**
 * Handle Form Submission
 */
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Show loading
    loadingOverlay.classList.remove('hidden');
    resultSide.classList.add('hidden');
    
    // Gather form data
    const formData = new FormData(form);
    const data = {
        Pclass: parseInt(formData.get('Pclass')),
        Sex: formData.get('Sex'),
        Age: parseFloat(formData.get('Age')),
        SibSp: parseInt(formData.get('SibSp')),
        Parch: parseInt(formData.get('Parch')),
        Embarked: formData.get('Embarked')
    };

    try {
        const response = await fetchWithRetry(`${API_BASE}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.status === 'success') {
            displayResults(result);
        } else {
            alert(`Error: ${result.error || 'Prediction failed'}`);
        }
    } catch (err) {
        console.error('Prediction Error:', err);

        // ✅ FIX 3: Realistic error message
        alert('Server is waking up or unreachable. Try again in a few seconds.');
    } finally {
        loadingOverlay.classList.add('hidden');
    }
});


/**
 * Display Prediction Results with Animations
 */
function displayResults(data) {
    const survived = data.prediction === 1;
    const confidence = survived ? data.confidence.survived : data.confidence.did_not_survive;

    // Update Text & Badge
    resBadge.innerText = survived ? 'Survives' : 'Perishes';
    resBadge.className = `badge ${survived ? 'survived' : 'perished'}`;
    
    resOutput.innerText = data.prediction_text;
    resOutput.style.color = survived ? '#4caf50' : '#f44336';

    // Update Confidence Bar
    resConfidencePct.innerText = `${Math.round(confidence)}%`;
    resConfidenceFill.style.width = '0%';
    
    // Update Details
    const classNames = { 1: '1st Class', 2: '2nd Class', 3: '3rd Class' };
    resClass.innerText = classNames[data.input_data.Pclass];
    resFamily.innerText = `${data.input_data.FamilySize} Member(s)`;

    // Show Result
    resultSide.classList.remove('hidden');
    
    setTimeout(() => {
        resConfidenceFill.style.width = `${confidence}%`;
    }, 100);
}


/**
 * Reset UI
 */
resetBtn.addEventListener('click', () => {
    resultSide.classList.add('hidden');
    form.reset();
});


// Initial Status Check
checkApiStatus();

// Periodic health check
setInterval(checkApiStatus, 15000);