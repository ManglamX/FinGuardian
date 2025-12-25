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
