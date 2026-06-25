# Quick Start Guide — Constitutional Adaptive Learning Systems Protocol

**Version:** 4.3  
**For:** Researchers, Developers, and Community Members  
**Time to First Action:** 5 minutes

---

## 🎯 What Is This?

CALSP is a complete research template for investigating constitutional AI systems that adapt to cognitive diversity. It's designed to be:

- **Neurodivergent-First:** Co-designed with and governed by neurodivergent individuals
- **Bootstrappable:** Start with <$1,000 and scale to $7.2M
- **Constitutional:** Built on The Living Constitution 2.0 framework
- **Open-Source:** Fully reproducible and community-driven

---

## 🚀 Three Pathways

### 1. I Want to Use This Template (Researcher)

**Goal:** Adapt CALSP for your own research

**Steps:**
1. Read [README.md](README.md) (10 min)
2. Review [VERIFICATION_AND_TRUTH.md](VERIFICATION_AND_TRUTH.md) to understand what exists vs. what's planned
3. Check [ethics/minimal-ethics-checklist.md](ethics/minimal-ethics-checklist.md) for IRB requirements
4. Customize [docs/executive-summary.md](docs/executive-summary.md) for your context
5. Follow [bootstrapped-prototype/README.md](bootstrapped-prototype/README.md) to deploy

**Key Files:**
- `ethics/irb-protocol-template.md` — IRB submission template
- `instruments/neuro-adaptive-profile.md` — NAP instrument
- `docs/budget-justification.md` — Budget template

**Timeline:** 4-6 weeks to adapt, 28 weeks to execute bootstrapped pilot

---

### 2. I Want to Contribute (Developer/Designer)

**Goal:** Improve the template or build the prototype

**Steps:**
1. Read [CONTRIBUTING.md](CONTRIBUTING.md) (15 min)
2. Review [community/CODE_OF_CONDUCT.md](community/CODE_OF_CONDUCT.md)
3. Check [GitHub Issues](https://github.com/yourusername/constitutional-adaptive-learning/issues) for `good-first-issue`
4. Fork the repository
5. Make your changes
6. Submit a pull request

**Priority Contributions:**
- Implement bootstrapped prototype code (frontend, backend)
- Add accessibility features (WCAG 2.1 AA)
- Translate instruments to other languages
- Improve documentation clarity
- Add visual diagrams

**Recognition:** All contributors acknowledged in publications

---

### 3. I Want to Understand the Theory (Academic)

**Goal:** Learn about Constitutional Adaptive Learning Theory (CALT)

**Reading Order:**
1. [docs/executive-summary.md](docs/executive-summary.md) — Overview (10 min)
2. [TLC_INTEGRATION.md](TLC_INTEGRATION.md) — TLC 2.0 alignment (20 min)
3. [instruments/neuro-adaptive-profile.md](instruments/neuro-adaptive-profile.md) — Core construct (15 min)
4. [VERIFICATION_AND_TRUTH.md](VERIFICATION_AND_TRUTH.md) — Current status (15 min)

**Key Concepts:**
- **CCI (Constitutional Compliance Index):** Real-time safety metric
- **NAP (Neuro-Adaptive Profile):** Participant-owned cognitive profile
- **DTCI (Dynamic Trust Calibration Index):** Confidence-performance alignment
- **CAMM (Constitutional Adaptive Mixed-Methods):** Research protocol
- **CHAE (Continuous Human Audit Engine):** 24/7 ethical oversight

**Publications:** See [docs/executive-summary.md](docs/executive-summary.md) for target venues

---

## 📂 Repository Map

```
constitutional-adaptive-learning/
│
├── README.md                          ← Start here
├── QUICK_START.md                     ← You are here
├── VERIFICATION_AND_TRUTH.md          ← What exists vs. what's planned
├── TLC_INTEGRATION.md                 ← TLC 2.0 alignment
├── CHANGELOG.md                       ← Version history
├── CONTRIBUTING.md                    ← How to contribute
├── LICENSE                            ← CC BY 4.0 + MIT
│
├── docs/                              ← Core documentation
│   ├── executive-summary.md           ← NSF-format summary
│   └── budget-justification.md        ← $7.2M budget details
│
├── ethics/                            ← Ethics & compliance
│   ├── irb-protocol-template.md       ← IRB submission template
│   └── minimal-ethics-checklist.md    ← Pre-submission checklist
│
├── instruments/                       ← Research instruments
│   └── neuro-adaptive-profile.md      ← NAP (30 items)
│
├── bootstrapped-prototype/            ← <$1K starter kit
│   ├── README.md                      ← Deployment guide
│   ├── package.json                   ← NPM config
│   └── .env.example                   ← Environment template
│
└── community/                         ← Community resources
    └── CODE_OF_CONDUCT.md             ← Neurodivergent-first CoC
```

---

## ⚡ Common Tasks

### Task 1: Deploy the Bootstrapped Prototype

```bash
cd bootstrapped-prototype
npm install
cp .env.example .env
# Edit .env with your settings
npm run dev
```

Visit `http://localhost:3000`

**Note:** This is a demo. For human subjects research, you MUST obtain IRB approval first.

---

### Task 2: Submit IRB Exemption

1. Read `ethics/minimal-ethics-checklist.md`
2. Complete all checklist items
3. Customize `ethics/irb-protocol-template.md`
4. Submit to your institutional IRB
5. Wait for approval before recruiting participants

**Timeline:** 2-4 weeks for exemption determination

---

### Task 3: Recruit Neurodivergent Advisory Board

1. Post on social media (Twitter, Mastodon, Reddit)
2. Reach out to neurodivergent advocacy organizations
3. Offer compensation ($50-100/meeting)
4. Schedule bi-weekly meetings
5. Document decisions in public GitHub Issues

**Target:** 2-3 volunteers for bootstrapped pilot, 8-10 for megaproject

---

### Task 4: Adapt Budget for Your Institution

1. Open `docs/budget-justification.md`
2. Replace personnel salaries with your institution's scales
3. Update F&A rate to your institution's negotiated rate
4. Adjust equipment costs for your infrastructure
5. Recalculate total budget

**Tool:** Spreadsheet template available on request

---

### Task 5: Translate Instruments

1. Choose target language
2. Translate `instruments/neuro-adaptive-profile.md`
3. Back-translate to English
4. Conduct cognitive interviews (N=5-10)
5. Submit translation as pull request

**Recognition:** Co-authorship on instrument validation paper

---

## 🎓 Learning Resources

### For Beginners
- [What is Constitutional AI?](https://www.anthropic.com/constitutional-ai) — Anthropic
- [Universal Design for Learning](https://www.cast.org/impact/universal-design-for-learning-udl) — CAST
- [Neurodiversity Paradigm](https://neuroqueer.com/neurodiversity-terms-and-definitions/) — Nick Walker

### For Researchers
- [Mixed-Methods Research](https://methods.sagepub.com/book/designing-and-conducting-mixed-methods-research-3e) — Creswell & Plano Clark
- [Structural Equation Modeling](https://www.guilford.com/books/Principles-and-Practice-of-Structural-Equation-Modeling/Rex-Kline/9781462523344) — Rex Kline
- [Cross-Cultural Validation](https://www.tandfonline.com/doi/full/10.1080/1047840X.2020.1732231) — Measurement Invariance

### For Developers
- [Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/) — WCAG 2.1
- [React Accessibility](https://react.dev/learn/accessibility) — React Docs
- [FastAPI Documentation](https://fastapi.tiangolo.com/) — FastAPI

### For Community Members
- [Participatory Action Research](https://www.participatorymethods.org/) — IDS
- [Disability Justice](https://www.sinsinvalid.org/blog/10-principles-of-disability-justice) — Sins Invalid
- [Open Science](https://www.cos.io/initiatives/open-science) — Center for Open Science

---

## 🤝 Getting Help

### Questions?
- **GitHub Discussions:** [Ask a question](https://github.com/yourusername/constitutional-adaptive-learning/discussions)
- **Discord:** [Join our community](https://discord.gg/calsp)
- **Email:** support@calsp.org

### Found a Bug?
- **GitHub Issues:** [Report a bug](https://github.com/yourusername/constitutional-adaptive-learning/issues/new?template=bug_report.md)

### Want to Propose a Feature?
- **GitHub Issues:** [Request a feature](https://github.com/yourusername/constitutional-adaptive-learning/issues/new?template=feature_request.md)

### Need Accessibility Support?
- **Email:** accessibility@calsp.org
- **We provide:** Screen reader support, alternative formats, extended time

---

## 📅 Timeline Overview

### Bootstrapped Pilot (28 weeks, <$1K)
- **Weeks 1-4:** IRB exemption submission
- **Weeks 5-8:** Prototype deployment
- **Weeks 9-16:** Data collection (N=10)
- **Weeks 17-24:** Analysis and write-up
- **Weeks 25-28:** Tier-1 Compliance Report v1

### Megaproject (36 months, $7.2M)
- **Months 1-6:** Funding secured, governance established
- **Months 7-12:** Infrastructure deployment, hub setup
- **Months 13-24:** Data collection (N=1,000)
- **Months 25-30:** Analysis and manuscript preparation
- **Months 31-36:** Publication and dissemination

---

## ✅ Pre-Flight Checklist

Before starting, ensure you have:

- [ ] Read README.md
- [ ] Reviewed VERIFICATION_AND_TRUTH.md
- [ ] Understood TLC 2.0 alignment (TLC_INTEGRATION.md)
- [ ] Completed minimal ethics checklist
- [ ] Identified institutional IRB contact
- [ ] Secured faculty advisor (if student)
- [ ] Planned recruitment strategy
- [ ] Allocated time for 28-week pilot
- [ ] Joined Discord community
- [ ] Starred the GitHub repository

---

## 🎯 Success Criteria

You'll know you're on track when:

### Week 4
- ✅ IRB exemption submitted
- ✅ Neurodivergent advisory circle recruited (2-3 people)
- ✅ Prototype deployed locally

### Week 8
- ✅ IRB exemption received
- ✅ Recruitment materials approved
- ✅ First participant consented

### Week 16
- ✅ N=10 participants completed
- ✅ Data quality verified
- ✅ No adverse events

### Week 28
- ✅ Analysis complete
- ✅ Tier-1 Compliance Report v1 published
- ✅ OSF preregistration submitted
- ✅ Instruments validated

---

## 🚨 Common Pitfalls

### Pitfall 1: Starting Without IRB Approval
**Problem:** Collecting data before IRB exemption  
**Solution:** Complete ethics checklist, submit to IRB, wait for approval

### Pitfall 2: Claiming "Working" Status Prematurely
**Problem:** Saying the system "works" before verification  
**Solution:** Follow TLC 2.0 truth-state classification (SPECIFIED → PARTIAL → VERIFIED → VALIDATED)

### Pitfall 3: Advisory-Only Neurodivergent Participation
**Problem:** Treating NAB as consultants, not co-leaders  
**Solution:** Give NAB veto power, co-authorship, and equal decision-making authority

### Pitfall 4: Skipping the Bootstrapped Pilot
**Problem:** Jumping straight to megaproject without validation  
**Solution:** Run N=10 pilot first to validate instruments and estimate effect sizes

### Pitfall 5: Ignoring Accessibility
**Problem:** Building for neurotypical users only  
**Solution:** Follow WCAG 2.1 AA, test with neurodivergent users, provide multiple modalities

---

## 📞 Contact

**Project Lead:** [Your Name]  
**Neurodivergent Co-Lead:** [To be recruited]  
**Email:** info@calsp.org  
**GitHub:** https://github.com/yourusername/constitutional-adaptive-learning  
**Discord:** https://discord.gg/calsp

---

## 📜 License

- **Documentation:** CC BY 4.0 (free to use with attribution)
- **Code:** MIT License (free to use, modify, distribute)

See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

This template builds on:
- The Living Constitution 2.0 (Corey Alejandro)
- TALSP Template v4.2 (integrated into TLC)
- Constitutional AI (Anthropic)
- Universal Design for Learning (CAST)
- Neurodiversity movement (many contributors)

---

**Last Updated:** 2026-06-23  
**Version:** 4.3  
**Status:** Ready to use (documentation complete, code pending)

**Next Step:** Read [README.md](README.md) for full overview, then choose your pathway above.