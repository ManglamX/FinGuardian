// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingOverlay = document.getElementById('loadingOverlay');
const resultsSection = document.getElementById('resultsSection');
const apiStatus = document.getElementById('apiStatus');

// Check API Status
async function checkAPIStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        const data = await response.json();

        if (data.status) {
            apiStatus.innerHTML = `
                <span class="status-dot"></span>
                <span class="status-text">API Connected</span>
            `;
        }
    } catch (error) {
        apiStatus.innerHTML = `
            <span class="status-dot" style="background: var(--danger);"></span>
            <span class="status-text">API Offline</span>
        `;
    }
}

// Get Form Data
function getFormData() {
    return {
        transaction: {
            amount: parseFloat(document.getElementById('amount').value),
            hour_of_day: parseInt(document.getElementById('hourOfDay').value),
            txn_frequency_1h: parseInt(document.getElementById('txnFrequency').value),
            is_new_account: document.getElementById('isNewAccount').checked ? 1 : 0,
            is_suspicious_type: document.getElementById('isSuspiciousType').checked ? 1 : 0,
            type: document.getElementById('txnType').value,
            oldbalanceOrg: parseFloat(document.getElementById('oldBalance').value),
            newbalanceOrig: parseFloat(document.getElementById('newBalance').value)
        },
        user_profile: {
            avg_transaction_amount: parseFloat(document.getElementById('avgTxnAmount').value),
            txn_count: parseInt(document.getElementById('txnCount').value),
            avg_txn_frequency: parseFloat(document.getElementById('avgTxnFreq').value),
            balance_stability: parseFloat(document.getElementById('balanceStability').value)
        }
    };
}

// Display Results
function displayResults(data) {
    // Overall Status
    const statusCard = document.getElementById('statusCard');
    const overallStatus = document.getElementById('overallStatus');
    const statusDescription = document.getElementById('statusDescription');

    overallStatus.textContent = data.overall_status;
    overallStatus.className = `status-badge ${data.overall_status.toLowerCase()}`;

    const statusMessages = {
        'CLEAR': 'Transaction approved. All risk indicators are within acceptable limits.',
        'FLAG': 'Transaction flagged for review. Some risk factors detected.',
        'BLOCK': 'Transaction blocked. High-risk indicators detected across multiple agents.'
    };

    statusDescription.textContent = statusMessages[data.overall_status] || 'Analysis complete.';

    // Fraud Agent
    displayFraudResults(data.fraud);

    // Compliance Agent
    displayComplianceResults(data.compliance);

    // Credit Agent
    displayCreditResults(data.credit);

    // New Agents
    if (data.behavioral) {
        displayBehavioralResults(data.behavioral);
    }

    if (data.stress) {
        displayStressResults(data.stress);
    }

    if (data.regret) {
        displayRegretResults(data.regret);
    }

    // Total Risk Score & Decision
    if (data.total_risk_score !== undefined) {
        document.getElementById('totalRiskScore').textContent = data.total_risk_score.toFixed(2);
    }

    if (data.decision) {
        const decisionBadge = document.getElementById('decisionType');
        decisionBadge.textContent = data.decision;
        decisionBadge.className = `status-badge ${data.decision.toLowerCase()}`;
    }

    // Explanation List
    if (data.explanation && data.explanation.length > 0) {
        const explanationList = document.getElementById('explanationList');
        explanationList.innerHTML = '';
        data.explanation.forEach(factor => {
            const div = document.createElement('div');
            div.className = 'risk-factor-item';
            div.textContent = factor;
            explanationList.appendChild(div);
        });
    }

    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Display Fraud Results
function displayFraudResults(fraud) {
    const fraudScore = document.getElementById('fraudScore');
    const fraudProgress = document.getElementById('fraudProgress');
    const fraudLabel = document.getElementById('fraudLabel');
    const fraudFactors = document.getElementById('fraudFactors');

    fraudScore.textContent = fraud.fraud_score.toFixed(2);
    fraudProgress.style.width = `${fraud.fraud_score * 100}%`;

    fraudLabel.textContent = fraud.fraud_label.replace('_', ' ');
    fraudLabel.className = 'risk-label';

    if (fraud.fraud_label.includes('HIGH')) {
        fraudLabel.classList.add('high');
    } else if (fraud.fraud_label.includes('MEDIUM')) {
        fraudLabel.classList.add('medium');
    } else {
        fraudLabel.classList.add('low');
    }

    fraudFactors.innerHTML = '';
    if (fraud.risk_factors && fraud.risk_factors.length > 0) {
        fraud.risk_factors.forEach(factor => {
            const div = document.createElement('div');
            div.className = 'risk-factor-item';
            div.textContent = factor;
            fraudFactors.appendChild(div);
        });
    } else {
        fraudFactors.innerHTML = '<div class="risk-factor-item" style="border-left-color: var(--success);">No risk factors detected</div>';
    }
}

// Display Compliance Results
function displayComplianceResults(compliance) {
    const complianceFlag = document.getElementById('complianceFlag');
    const complianceRisk = document.getElementById('complianceRisk');
    const violationsContainer = document.getElementById('violationsContainer');

    complianceFlag.textContent = compliance.compliance_flag ? 'VIOLATION' : 'COMPLIANT';
    complianceFlag.className = compliance.compliance_flag ? 'compliance-flag fail' : 'compliance-flag pass';

    complianceRisk.textContent = `Risk: ${compliance.risk_level}`;
    complianceRisk.className = 'compliance-risk';

    violationsContainer.innerHTML = '';
    if (compliance.violated_rules && compliance.violated_rules.length > 0) {
        compliance.violated_rules.forEach(rule => {
            const div = document.createElement('div');
            div.className = 'violation-item';
            div.textContent = rule;
            violationsContainer.appendChild(div);
        });
    } else {
        violationsContainer.innerHTML = '<div class="violation-item" style="border-left-color: var(--success);">All compliance checks passed</div>';
    }
}

// Display Credit Results
function displayCreditResults(credit) {
    const creditScore = document.getElementById('creditScore');
    const creditCircle = document.getElementById('creditCircle');
    const creditRisk = document.getElementById('creditRisk');
    const creditReasons = document.getElementById('creditReasons');

    creditScore.textContent = credit.credit_score;

    // Animate credit circle
    const percentage = ((credit.credit_score - 300) / 550) * 100; // 300-850 range
    const offset = 314 - (314 * percentage / 100);
    creditCircle.style.strokeDashoffset = offset;

    // Add gradient definition if not exists
    if (!document.getElementById('creditGradient')) {
        const svg = document.querySelector('.credit-circle-svg');
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
        const gradient = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
        gradient.setAttribute('id', 'creditGradient');
        gradient.innerHTML = `
            <stop offset="0%" stop-color="#10b981"/>
            <stop offset="100%" stop-color="#6366f1"/>
        `;
        defs.appendChild(gradient);
        svg.appendChild(defs);
    }

    creditRisk.textContent = `${credit.credit_risk} RISK`;
    creditRisk.className = 'risk-label';

    if (credit.credit_risk === 'HIGH') {
        creditRisk.classList.add('high');
    } else if (credit.credit_risk === 'MEDIUM') {
        creditRisk.classList.add('medium');
    } else {
        creditRisk.classList.add('low');
    }

    creditReasons.innerHTML = '';
    if (credit.credit_reasons && credit.credit_reasons.length > 0) {
        credit.credit_reasons.forEach(reason => {
            const div = document.createElement('div');
            div.className = 'credit-reason-item';
            div.textContent = reason;
            creditReasons.appendChild(div);
        });
    }
}

// Display Behavioral Results
function displayBehavioralResults(behavioral) {
    const behaviorScore = document.getElementById('behaviorScore');
    const behaviorProgress = document.getElementById('behaviorProgress');
    const behaviorReasons = document.getElementById('behaviorReasons');

    behaviorScore.textContent = behavioral.behavior_score.toFixed(2);
    behaviorProgress.style.width = `${behavioral.behavior_score * 100}%`;

    behaviorReasons.innerHTML = '';
    if (behavioral.behavior_reasons && behavioral.behavior_reasons.length > 0) {
        behavioral.behavior_reasons.forEach(reason => {
            const div = document.createElement('div');
            div.className = 'risk-factor-item';
            div.textContent = reason;
            behaviorReasons.appendChild(div);
        });
    } else {
        behaviorReasons.innerHTML = '<div class="risk-factor-item" style="border-left-color: var(--success);">No behavioral anomalies detected</div>';
    }
}

// Display Financial Stress Results
function displayStressResults(stress) {
    const stressScore = document.getElementById('stressScore');
    const stressProgress = document.getElementById('stressProgress');
    const stressReasons = document.getElementById('stressReasons');

    stressScore.textContent = stress.stress_score.toFixed(2);
    stressProgress.style.width = `${stress.stress_score * 100}%`;

    stressReasons.innerHTML = '';
    if (stress.stress_reasons && stress.stress_reasons.length > 0) {
        stress.stress_reasons.forEach(reason => {
            const div = document.createElement('div');
            div.className = 'risk-factor-item';
            div.textContent = reason;
            stressReasons.appendChild(div);
        });
    } else {
        stressReasons.innerHTML = '<div class="risk-factor-item" style="border-left-color: var(--success);">No financial stress detected</div>';
    }
}

// Display Regret Results
function displayRegretResults(regret) {
    const regretScore = document.getElementById('regretScore');
    const regretProgress = document.getElementById('regretProgress');
    const regretReasons = document.getElementById('regretReasons');

    regretScore.textContent = regret.regret_score.toFixed(2);
    regretProgress.style.width = `${regret.regret_score * 100}%`;

    regretReasons.innerHTML = '';
    if (regret.regret_reasons && regret.regret_reasons.length > 0) {
        regret.regret_reasons.forEach(reason => {
            const div = document.createElement('div');
            div.className = 'risk-factor-item';
            div.textContent = reason;
            regretReasons.appendChild(div);
        });
    } else {
        regretReasons.innerHTML = '<div class="risk-factor-item" style="border-left-color: var(--success);">No regret patterns detected</div>';
    }
}

// Analyze Transaction
async function analyzeTransaction() {
    try {
        // Show loading
        loadingOverlay.style.display = 'flex';

        // Get form data
        const formData = getFormData();

        // Make API request
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }

        const data = await response.json();

        // Hide loading
        loadingOverlay.style.display = 'none';

        // Display results
        displayResults(data);

    } catch (error) {
        console.error('Error analyzing transaction:', error);
        loadingOverlay.style.display = 'none';
        alert('Error analyzing transaction. Please check if the API is running.');
    }
}

// Event Listeners
analyzeBtn.addEventListener('click', analyzeTransaction);

// Check API status on load
checkAPIStatus();

// Recheck API status every 30 seconds
setInterval(checkAPIStatus, 30000);
