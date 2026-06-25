# Bootstrapped Prototype — Constitutional Adaptive Learning System

**Version:** 1.0.0  
**Cost:** <$1,000  
**Deployment Time:** ~30 minutes  
**Status:** 🚧 In Development

---

## 🎯 Purpose

This is the **bootstrapped prototype** of the Constitutional Adaptive Learning System — a fully functional, minimal-cost implementation that any researcher can deploy to validate the core CALSP framework before scaling to the megaproject.

**Key Features:**
- ✅ Constitutional AI safety filter
- ✅ Neuro-Adaptive Profile (m-NAP) with 10 items
- ✅ Dynamic trust calibration (m-DTCI)
- ✅ Three interface modes (text, voice, visual)
- ✅ Real-time cognitive load tracking
- ✅ Accessible design (WCAG 2.1 AA)
- ✅ One-click deployment
- ✅ IRB-ready data collection

---

## 🚀 Quick Start

### Option 1: One-Click Deploy (Recommended)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. Click the button above
2. Create a free Render account
3. Configure environment variables (see `.env.example`)
4. Deploy (takes ~5 minutes)
5. Your prototype is live at `https://your-app.onrender.com`

### Option 2: Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/constitutional-adaptive-learning.git
cd constitutional-adaptive-learning/bootstrapped-prototype

# Install dependencies
npm install
cd backend && pip install -r requirements.txt && cd ..

# Set up environment variables
cp .env.example .env
# Edit .env with your settings

# Start development servers
npm run dev
```

Visit `http://localhost:3000`

### Option 3: Docker (Reproducibility)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at http://localhost:3000
```

---

## 📋 Prerequisites

### For Demo (No Human Subjects)
- Node.js 18+ and npm
- Python 3.10+
- Modern web browser
- **No IRB approval needed** (synthetic data only)

### For Human Subjects Research
- ✅ All of the above
- ✅ **Institutional IRB exemption** (45 CFR 46.104(d)(3))
- ✅ Secure data storage (university server or approved cloud)
- ✅ Participant compensation method ($50 gift cards)

⚠️ **DO NOT collect human data without IRB approval**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│  - Accessible UI (high contrast, keyboard nav)          │
│  - Three interaction modes (text, voice, visual)        │
│  - Real-time cognitive load tracking                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              API Gateway (FastAPI)                       │
│  - Request routing                                       │
│  - Authentication (optional)                             │
│  - Rate limiting                                         │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
┌──────────────────┐    ┌──────────────────┐
│ Constitutional   │    │ Adaptation       │
│ Filter           │    │ Engine           │
│ - Safety rules   │    │ - NAP-driven     │
│ - Harm detection │    │ - Interface mode │
│ - CCI tracking   │    │ - Difficulty     │
└────────┬─────────┘    └────────┬─────────┘
         │                       │
         └───────────┬───────────┘
                     ▼
         ┌───────────────────────┐
         │   LLM Inference       │
         │   (Hugging Face API)  │
         │   - Free tier         │
         │   - Llama 3.1 8B      │
         └───────────┬───────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   Data Storage        │
         │   - SQLite (local)    │
         │   - PostgreSQL (prod) │
         │   - Audit logs        │
         └───────────────────────┘
```

---

## 📁 Project Structure

```
bootstrapped-prototype/
├── README.md                    # This file
├── package.json                 # Node dependencies
├── docker-compose.yml           # Docker setup
├── .env.example                 # Environment template
│
├── frontend/                    # React application
│   ├── src/
│   │   ├── components/
│   │   │   ├── ConsentForm.tsx
│   │   │   ├── NAPInventory.tsx
│   │   │   ├── LearningTask.tsx
│   │   │   ├── CognitiveLoadTracker.tsx
│   │   │   └── AccessibilityControls.tsx
│   │   ├── hooks/
│   │   │   ├── useNAP.ts
│   │   │   ├── useTrustCalibration.ts
│   │   │   └── useAccessibility.ts
│   │   ├── styles/
│   │   │   ├── high-contrast.css
│   │   │   └── accessible.css
│   │   └── App.tsx
│   ├── public/
│   └── package.json
│
├── backend/                     # FastAPI server
│   ├── main.py                  # API entry point
│   ├── routers/
│   │   ├── consent.py
│   │   ├── nap.py
│   │   ├── learning.py
│   │   └── data.py
│   ├── services/
│   │   ├── constitutional_filter.py
│   │   ├── adaptation_engine.py
│   │   ├── llm_client.py
│   │   └── cci_tracker.py
│   ├── models/
│   │   ├── nap.py
│   │   ├── session.py
│   │   └── response.py
│   ├── database/
│   │   ├── db.py
│   │   └── migrations/
│   ├── tests/
│   │   ├── test_constitutional_filter.py
│   │   ├── test_adaptation_engine.py
│   │   └── test_api.py
│   └── requirements.txt
│
├── constitutional-rules/        # Safety rules
│   ├── base-rules.yaml
│   ├── harm-categories.yaml
│   └── adaptation-constraints.yaml
│
├── instruments/                 # Research instruments
│   ├── m-nap.json              # Minimal NAP (10 items)
│   ├── paas-scale.json         # Cognitive load
│   ├── sus.json                # System Usability Scale
│   └── sensory-comfort.json
│
├── data/                        # Data storage
│   ├── synthetic/              # Demo data (no IRB needed)
│   ├── pilot/                  # Real data (IRB required)
│   └── audit-logs/
│
├── scripts/                     # Utility scripts
│   ├── setup.sh                # Initial setup
│   ├── deploy.sh               # Deployment
│   ├── test-adversarial.py     # Manual red-teaming
│   └── export-data.py          # Data export
│
└── docs/                        # Documentation
    ├── deployment-guide.md
    ├── api-reference.md
    ├── accessibility-testing.md
    └── troubleshooting.md
```

---

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Application
NODE_ENV=development
PORT=3000
API_URL=http://localhost:8000

# LLM Provider (choose one)
LLM_PROVIDER=huggingface  # or openai, anthropic
HUGGINGFACE_API_KEY=your_key_here  # Free tier available

# Database
DATABASE_URL=sqlite:///./data/pilot.db  # Local
# DATABASE_URL=postgresql://user:pass@host/db  # Production

# IRB Compliance
IRB_APPROVED=false  # Set to true only after IRB approval
IRB_PROTOCOL_NUMBER=  # Fill in after approval

# Data Collection
COLLECT_REAL_DATA=false  # Set to true only after IRB approval
PARTICIPANT_COMPENSATION=50  # USD

# Accessibility
DEFAULT_CONTRAST=high
DEFAULT_FONT_SIZE=16
ENABLE_SCREEN_READER=true

# Monitoring
ENABLE_AUDIT_LOG=true
AUDIT_LOG_PATH=./data/audit-logs/
```

---

## 🧪 Testing

### Run All Tests
```bash
npm test
```

### Test Constitutional Filter
```bash
cd backend
python -m pytest tests/test_constitutional_filter.py -v
```

### Test Accessibility
```bash
npm run a11y-test
```

### Manual Adversarial Testing
```bash
python scripts/test-adversarial.py
```

This runs a predefined set of adversarial prompts to test the constitutional filter.

---

## 📊 Demo Mode (No IRB Required)

To explore the system without collecting human data:

1. Ensure `IRB_APPROVED=false` in `.env`
2. Run `npm run demo`
3. System loads synthetic participant data
4. All features functional except real data storage

**Demo Features:**
- ✅ Complete UI walkthrough
- ✅ Synthetic NAP profiles
- ✅ Simulated learning tasks
- ✅ Mock cognitive load data
- ✅ Constitutional filter testing
- ❌ No real participant data collected

---

## 🔒 IRB Compliance

### Before Collecting Human Data

1. **Complete IRB Protocol**
   - Use template: `../../ethics/irb-protocol-template.md`
   - Submit to your institution's IRB
   - Request exemption under 45 CFR 46.104(d)(3)

2. **Wait for Approval**
   - Do NOT recruit participants before approval
   - Do NOT enable data collection before approval

3. **Configure System**
   ```bash
   # In .env
   IRB_APPROVED=true
   IRB_PROTOCOL_NUMBER=2026-12345
   COLLECT_REAL_DATA=true
   ```

4. **Set Up Secure Storage**
   - Use university server or approved cloud
   - Enable encryption
   - Restrict access to research team

5. **Test with Synthetic Data First**
   ```bash
   npm run test-irb-compliance
   ```

### During Data Collection

- Monitor audit logs daily
- Conduct weekly CHAE reviews (audit buddy)
- Report adverse events to IRB within 24 hours
- Maintain participant contact list separately from data

---

## 🎨 Accessibility Features

### Built-In Accommodations

1. **Visual:**
   - High-contrast mode (4.5:1 ratio minimum)
   - Adjustable font size (12-24px)
   - Dyslexia-friendly font option (OpenDyslexic)
   - No flashing content (seizure prevention)

2. **Auditory:**
   - Text-to-speech for all content (Web Speech API)
   - Visual captions for audio feedback
   - Volume control

3. **Motor:**
   - Full keyboard navigation (no mouse required)
   - Large click targets (44×44px minimum)
   - Adjustable interaction timing
   - Voice input option (experimental)

4. **Cognitive:**
   - Plain language (8th-grade reading level)
   - Visual progress indicators
   - Pause button on every screen
   - Task breakdowns with checklists

### Testing Accessibility

```bash
# Automated testing
npm run a11y-test

# Manual testing checklist
# 1. Navigate entire app with keyboard only (Tab, Enter, Esc)
# 2. Test with screen reader (NVDA, JAWS, VoiceOver)
# 3. Verify color contrast with browser DevTools
# 4. Test with browser zoom at 200%
# 5. Test with CSS disabled
```

---

## 📈 Monitoring

### Real-Time Dashboard

Access at `/dashboard` (requires authentication):

- **Constitutional Compliance Index (CCI):** % of responses within bounds
- **Trust Calibration:** Confidence vs. accuracy scatter plot
- **Cognitive Load:** Mean and variance over time
- **System Usability:** SUS score distribution
- **Audit Log:** Recent safety events

### Audit Logs

All system actions logged to `data/audit-logs/`:

```json
{
  "timestamp": "2026-06-23T10:30:00Z",
  "event_type": "constitutional_violation",
  "participant_id": "P001",
  "prompt": "[redacted]",
  "response": "[blocked]",
  "cci_score": 0.98,
  "action_taken": "response_blocked"
}
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** "IRB_APPROVED is false"  
**Solution:** This is intentional. Do not set to true without IRB approval.

**Issue:** "LLM API rate limit exceeded"  
**Solution:** Hugging Face free tier has limits. Upgrade or use local model.

**Issue:** "Database locked"  
**Solution:** SQLite doesn't support concurrent writes. Use PostgreSQL for production.

**Issue:** "Accessibility tests failing"  
**Solution:** Run `npm run fix-a11y` to auto-fix common issues.

**Issue:** "Constitutional filter too strict"  
**Solution:** Review `constitutional-rules/base-rules.yaml` and adjust thresholds. Document changes in audit log.

### Getting Help

- **GitHub Issues:** [Report a bug](https://github.com/yourusername/constitutional-adaptive-learning/issues)
- **Discord:** [#bootstrapped-prototype channel](https://discord.gg/calsp)
- **Email:** support@calsp.org

---

## 🚀 Deployment

### Free Tier Options

1. **Render** (Recommended)
   - Free tier: 750 hours/month
   - Auto-deploy from GitHub
   - Built-in SSL

2. **Fly.io**
   - Free tier: 3 shared VMs
   - Global edge network
   - Good for low-latency

3. **Railway**
   - Free tier: $5 credit/month
   - Simple deployment
   - PostgreSQL included

### Production Deployment

For the megaproject, see `../../megaproject-architecture/deployment-guide.md`

---

## 📊 Data Export

After study completion:

```bash
# Export de-identified data
python scripts/export-data.py --deidentify --output data/export/

# Generate data dictionary
python scripts/generate-data-dictionary.py

# Create reproducibility package
npm run create-repro-package
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

**Quick Contribution Ideas:**
- Add new accessibility features
- Improve constitutional rules
- Translate UI to other languages
- Write tests
- Improve documentation

---

## 📜 License

- **Code:** MIT License
- **Documentation:** CC BY 4.0

See [LICENSE](../../LICENSE) for details.

---

## 📚 Citation

If you use this prototype in your research:

```bibtex
@software{calsp_prototype2026,
  title={Constitutional Adaptive Learning System: Bootstrapped Prototype},
  author={[Your Name]},
  year={2026},
  version={1.0.0},
  url={https://github.com/yourusername/constitutional-adaptive-learning}
}
```

---

## 🎯 Next Steps

1. ✅ Deploy demo version
2. ✅ Test with synthetic data
3. ✅ Complete IRB protocol
4. ⏳ Submit to IRB
5. ⏳ Wait for approval
6. ⏳ Recruit N=10 participants
7. ⏳ Collect pilot data
8. ⏳ Analyze and publish results
9. ⏳ Use findings for megaproject proposal

---

**Questions?** Open an issue or join our Discord!

**Last Updated:** 2026-06-23  
**Maintainer:** [Your Name]