# FinGuardian AI 🛡️

**AI-Powered Financial Intelligence Platform**

A comprehensive multi-agent system for real-time transaction risk assessment, combining fraud detection, compliance checking, and credit evaluation with a modern web interface.

![FinGuardian AI](https://img.shields.io/badge/AI-Powered-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.127.0-green) ![Python](https://img.shields.io/badge/Python-3.12-blue) ![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🌟 Features

- **🔍 Fraud Detection Agent** - ML-based anomaly detection using Isolation Forest
- **📋 Compliance Agent** - Rule-based regulatory compliance checking
- **💳 Credit Assessment Agent** - Creditworthiness evaluation and scoring
- **🎨 Modern Web Interface** - Real-time analysis dashboard with dark theme
- **📱 SMS Alerts** - Twilio integration for high-risk transaction notifications
- **🔄 Real-time API** - FastAPI backend with CORS support

---

## 🏗️ Architecture

```
┌─────────────────┐
│  Web Frontend   │
│   (HTML/CSS/JS) │
└────────┬────────┘
         │ HTTP POST
         ▼
┌─────────────────┐
│  FastAPI Backend│
│   (Orchestrator)│
└────────┬────────┘
         │
    ┌────┴────┬────────┬────────┐
    ▼         ▼        ▼        ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Fraud  │ │Complnce│ │ Credit │ │Twilio  │
│ Agent  │ │ Agent  │ │ Agent  │ │ Alerts │
└────────┘ └────────┘ └────────┘ └────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Git
- Twilio account (optional, for SMS alerts)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/ManglamX/FinGuardian.git
cd FinGuardian
```

2. **Create virtual environment**
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Create .env file
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_NUMBER=your_twilio_number
```

5. **Train the ML model**
```bash
python train_dummy_model.py
```

6. **Start the backend server**
```bash
uvicorn app:app --reload
```

7. **Open the frontend**
```
Open frontend/index.html in your browser
```

---

## 📊 API Usage

### Health Check
```bash
GET http://localhost:8000/
```

### Analyze Transaction
```bash
POST http://localhost:8000/analyze
Content-Type: application/json

{
  "transaction": {
    "amount": 9500.0,
    "hour_of_day": 14,
    "txn_frequency_1h": 5,
    "is_new_account": 0,
    "is_suspicious_type": 0,
    "type": "TRANSFER",
    "oldbalanceOrg": 10000.0,
    "newbalanceOrig": 500.0
  },
  "user_profile": {
    "avg_transaction_amount": 500.0,
    "txn_count": 50,
    "avg_txn_frequency": 2.5,
    "balance_stability": 0.9
  }
}
```

### Response
```json
{
  "fraud": {
    "fraud_score": 0.10,
    "fraud_label": "LOW_RISK",
    "risk_factors": ["Transaction amount much higher than normal pattern"]
  },
  "compliance": {
    "compliance_flag": true,
    "risk_level": "MEDIUM",
    "violated_rules": ["Account balance rapidly depleted after transaction"]
  },
  "credit": {
    "credit_score": 720,
    "credit_risk": "MEDIUM",
    "credit_reasons": ["Consistent transaction activity", "Stable spending behavior"]
  },
  "overall_status": "BLOCK"
}
```

---

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_agents.py
```

Tests include:
- Individual agent functionality
- Full orchestrator integration
- SMS alert verification

---

## 📁 Project Structure

```
FinGuardian/
├── frontend/
│   ├── index.html          # Main UI
│   ├── styles.css          # Dark theme styling
│   └── script.js           # API integration
├── agents/
│   ├── fraud_agent/        # ML-based fraud detection
│   ├── compliance_agent/   # Rule-based compliance
│   └── credit_agent/       # Credit scoring
├── orchestrator/
│   ├── controller.py       # Agent coordination
│   └── schemas.py          # Pydantic models
├── alerts/
│   └── twilio_notifier.py  # SMS alerts
├── app.py                  # FastAPI entry point
├── test_agents.py          # Test suite
├── train_dummy_model.py    # Model training script
└── requirements.txt        # Dependencies
```

---

## 🎨 Frontend Features

- **Real-time API Status** - Connection indicator
- **Comprehensive Input Forms** - Transaction and user profile data
- **Dynamic Results Dashboard** - Animated visualizations
- **Risk Indicators** - Color-coded status badges
- **Responsive Design** - Works on all screen sizes

---

## 🔒 Security Notes

- **Never commit `.env` file** - Contains sensitive credentials
- **Use environment variables** - For all API keys and secrets
- **CORS Configuration** - Update `allow_origins` for production
- **Twilio Verification** - Verify phone numbers in trial mode

---

## 🛠️ Technologies Used

- **Backend:** FastAPI, Python 3.12, Pydantic
- **ML/AI:** scikit-learn, Isolation Forest, NLTK
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Alerts:** Twilio SMS API
- **Testing:** Custom test suite

---

## 📈 Future Enhancements

- [ ] User authentication and authorization
- [ ] Database integration for transaction history
- [ ] Real-time dashboard with WebSocket updates
- [ ] Advanced ML models with real financial data
- [ ] Docker containerization
- [ ] Cloud deployment (AWS/GCP/Azure)
- [ ] Historical analytics and reporting

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Manglam**
- GitHub: [@ManglamX](https://github.com/ManglamX)

---

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- scikit-learn for ML capabilities
- Twilio for SMS integration
- The open-source community

---

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

**Built with ❤️ for financial security**
