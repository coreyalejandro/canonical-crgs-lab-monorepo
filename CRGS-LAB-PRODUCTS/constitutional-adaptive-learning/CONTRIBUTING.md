# Contributing to Constitutional Adaptive Learning Systems Protocol (CALSP)

Thank you for your interest in contributing to CALSP! This project is built on the principle of **neurodivergent-first, community-driven research**, and we welcome contributions from researchers, developers, neurodivergent individuals, and anyone passionate about ethical AI.

## 🌟 Our Values

1. **Nothing About Us Without Us** — Neurodivergent voices lead all decisions
2. **Radical Transparency** — All governance decisions are public and auditable
3. **Accessibility First** — Every contribution must be accessible
4. **Community Ownership** — This research belongs to everyone
5. **Continuous Evolution** — The system improves through community input

## 🎯 Ways to Contribute

### 1. Research Contributions
- **Propose new hypotheses** for CALT framework
- **Suggest instrument improvements** (NAP, CCI, DTCI)
- **Share cross-cultural adaptations** of research protocols
- **Contribute analysis scripts** (R, Python, Stan)
- **Write literature reviews** for specific domains

### 2. Code Contributions
- **Improve bootstrapped prototype** (frontend, backend, safety filters)
- **Add accessibility features** (screen reader support, keyboard navigation)
- **Optimize performance** (latency reduction, caching)
- **Write tests** (unit, integration, end-to-end)
- **Fix bugs** (see GitHub Issues)

### 3. Documentation Contributions
- **Translate materials** into other languages
- **Simplify technical language** for broader audiences
- **Create tutorials** and how-to guides
- **Improve accessibility** of existing docs
- **Add examples** and case studies

### 4. Community Contributions
- **Participate in governance** (NAB, CGB, OSSC meetings)
- **Provide feedback** on research design
- **Share lived experiences** as neurodivergent individual
- **Mentor new contributors**
- **Organize community events** (hackathons, reading groups)

### 5. Governance Contributions
- **Propose constitutional rule changes**
- **Review pull requests** for ethical alignment
- **Participate in CHAE** (Continuous Human Audit Engine)
- **Suggest governance improvements**

## 🚀 Getting Started

### Step 1: Read the Code of Conduct
Please read our [Code of Conduct](community/CODE_OF_CONDUCT.md) before contributing. We are committed to providing a welcoming, inclusive, and harassment-free environment.

### Step 2: Join the Community
- **Discord:** [Join our server](https://discord.gg/calsp)
- **Community Calls:** Bi-weekly on Wednesdays at 3pm ET ([Calendar](https://calendar.google.com/calsp))
- **Mailing List:** [Subscribe](https://groups.google.com/calsp)

### Step 3: Find an Issue
Browse our [GitHub Issues](https://github.com/yourusername/constitutional-adaptive-learning/issues) for:
- `good-first-issue` — Great for newcomers
- `help-wanted` — We need your expertise
- `neurodivergent-priority` — Flagged by NAB as high-impact
- `accessibility` — Accessibility improvements
- `documentation` — Documentation needs

### Step 4: Claim an Issue
Comment on the issue saying you'd like to work on it. A maintainer will assign it to you and provide guidance.

## 📋 Contribution Process

### For Code Contributions

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/constitutional-adaptive-learning.git
   cd constitutional-adaptive-learning
   git checkout -b feature/your-feature-name
   ```

2. **Set up development environment**
   ```bash
   cd bootstrapped-prototype
   npm install
   npm run dev
   ```

3. **Make your changes**
   - Follow our [Style Guide](#style-guide)
   - Write tests for new features
   - Ensure accessibility (WCAG 2.1 AA minimum)
   - Update documentation

4. **Test your changes**
   ```bash
   npm test
   npm run lint
   npm run a11y-test
   ```

5. **Commit with clear messages**
   ```bash
   git add .
   git commit -m "feat: add high-contrast mode toggle"
   ```
   Use [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` — New feature
   - `fix:` — Bug fix
   - `docs:` — Documentation only
   - `style:` — Formatting, no code change
   - `refactor:` — Code restructuring
   - `test:` — Adding tests
   - `chore:` — Maintenance

6. **Push and create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a PR on GitHub with:
   - Clear description of changes
   - Link to related issue
   - Screenshots (if UI change)
   - Accessibility testing results

### For Research Contributions

1. **Open a Discussion**
   - Go to [GitHub Discussions](https://github.com/yourusername/constitutional-adaptive-learning/discussions)
   - Choose "Research Proposals" category
   - Describe your idea with rationale

2. **Get Community Feedback**
   - NAB members will review within 1 week
   - Community can comment and suggest improvements
   - OSSC will assess technical feasibility

3. **Submit Formal Proposal**
   - If approved, create a PR with:
     - Updated research protocol
     - New instrument (if applicable)
     - Analysis plan modifications
     - Bibliography updates

4. **Governance Review**
   - NAB votes (requires majority approval)
   - CGB reviews for alignment with megaproject
   - CHAE reviews for ethical implications

### For Documentation Contributions

1. **Identify documentation gap**
   - Missing explanation
   - Unclear language
   - Accessibility issue
   - Translation needed

2. **Create or update file**
   - Use plain language (8th-grade reading level)
   - Add alt text for all images
   - Include table of contents for long docs
   - Provide examples

3. **Submit PR**
   - Tag with `documentation` label
   - Request review from community manager

## 🎨 Style Guide

### Code Style

**JavaScript/TypeScript:**
- Use ESLint config (`.eslintrc.json`)
- Prettier for formatting
- Prefer functional components (React)
- Use TypeScript for type safety

**Python:**
- Follow PEP 8
- Use Black for formatting
- Type hints required
- Docstrings for all functions

**Accessibility:**
- All interactive elements must be keyboard-accessible
- ARIA labels for screen readers
- Color contrast ratio ≥4.5:1 (WCAG AA)
- Focus indicators visible
- No flashing content (seizure risk)

### Documentation Style

- **Plain language:** Avoid jargon; explain technical terms
- **Active voice:** "Click the button" not "The button should be clicked"
- **Short sentences:** <25 words per sentence
- **Headings:** Use semantic HTML (h1, h2, h3)
- **Lists:** Use bullet points for scannability
- **Examples:** Provide concrete examples
- **Alt text:** Describe images for screen readers

### Commit Message Style

```
<type>(<scope>): <subject>

<body>

<footer>
```

Example:
```
feat(nap): add sensory preference questions

Added 5 new questions to NAP inventory covering auditory,
visual, and tactile sensory preferences. Questions validated
through cognitive interviews with 10 neurodivergent participants.

Closes #123
Reviewed-by: NAB
```

## 🔍 Review Process

### Pull Request Review

All PRs go through multi-stage review:

1. **Automated Checks** (required to pass)
   - Tests pass
   - Linting passes
   - Accessibility tests pass
   - No merge conflicts

2. **Technical Review** (OSSC)
   - Code quality
   - Performance
   - Security
   - Maintainability

3. **Accessibility Review** (Accessibility Team)
   - Screen reader compatibility
   - Keyboard navigation
   - Color contrast
   - Cognitive load

4. **Neurodivergent Review** (NAB)
   - Alignment with neurodivergent-first principles
   - Sensory considerations
   - Executive function support
   - Community benefit

5. **Ethics Review** (CHAE, if applicable)
   - Safety implications
   - Privacy considerations
   - Informed consent
   - Data handling

### Review Timeline

- **Code PRs:** 3-5 business days
- **Documentation PRs:** 1-3 business days
- **Research proposals:** 1-2 weeks (includes NAB meeting)
- **Governance changes:** 2-4 weeks (includes community vote)

### Approval Requirements

- **Minor changes:** 1 OSSC approval
- **Major features:** 2 OSSC approvals + NAB approval
- **Research changes:** NAB majority + CGB approval
- **Governance changes:** NAB unanimous + community vote (>60% approval)

## 🏆 Recognition

We value all contributions! Contributors are recognized through:

1. **Contributors List** — Added to README.md
2. **Authorship** — Significant research contributions → co-authorship on papers
3. **Acknowledgments** — All contributions acknowledged in publications
4. **Community Badges** — Discord roles for active contributors
5. **Annual Awards** — "Neurodivergent Champion" and "Community Star" awards

## 🛡️ Neurodivergent-First Contribution Guidelines

### Sensory Accommodations

- **Async participation welcome** — No pressure to attend live meetings
- **Multiple communication channels** — Text, voice, video, or written
- **Flexible deadlines** — Request extensions anytime
- **Quiet collaboration** — Use "Do Not Disturb" mode freely

### Executive Function Support

- **Task breakdowns** — Large tasks split into smaller steps
- **Checklists provided** — Clear, actionable items
- **Reminders available** — Opt-in to deadline reminders
- **Pair programming** — Work with a buddy if helpful

### Communication Preferences

- **Direct communication** — Say what you mean; we won't read between lines
- **No small talk required** — Jump straight to the topic
- **Tone indicators** — Use `/s` (sarcasm), `/gen` (genuine), etc.
- **Ask for clarification** — No question is "stupid"

### Feedback Style

- **Specific and actionable** — "Add alt text to line 42" not "Improve accessibility"
- **Assume good intent** — We're all learning
- **Celebrate progress** — Acknowledge effort, not just outcomes
- **Private option** — Request private feedback if public feels overwhelming

## 🚨 Reporting Issues

### Bug Reports

Use the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md):
- Clear description
- Steps to reproduce
- Expected vs. actual behavior
- Screenshots (if applicable)
- Environment details (OS, browser, etc.)

### Feature Requests

Use the [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md):
- Problem statement
- Proposed solution
- Alternatives considered
- Neurodivergent impact assessment

### Security Vulnerabilities

**Do NOT open public issues for security vulnerabilities.**

Email: security@calsp.org with:
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will respond within 48 hours.

## 📜 Licensing

By contributing, you agree that your contributions will be licensed under:
- **Documentation:** CC BY 4.0
- **Code:** MIT License

You retain copyright but grant us permission to use, modify, and distribute your contributions.

## 🤝 Community Standards

### Expected Behavior

- **Be respectful** — Treat everyone with dignity
- **Be inclusive** — Welcome diverse perspectives
- **Be patient** — Everyone learns at their own pace
- **Be constructive** — Offer solutions, not just criticism
- **Be accessible** — Consider cognitive and sensory needs

### Unacceptable Behavior

- Harassment, discrimination, or hate speech
- Ableist language or assumptions
- Dismissing neurodivergent experiences
- Violating privacy or confidentiality
- Spamming or trolling

Violations will be addressed per our [Code of Conduct](community/CODE_OF_CONDUCT.md).

## 📞 Getting Help

Stuck? Need guidance? Reach out:

- **Discord:** #help channel
- **GitHub Discussions:** [Ask a Question](https://github.com/yourusername/constitutional-adaptive-learning/discussions/categories/q-a)
- **Email:** community@calsp.org
- **Office Hours:** Tuesdays 2-4pm ET (Zoom link in Discord)

## 🎓 Learning Resources

New to contributing? Check out:
- [First Contributions Guide](https://github.com/firstcontributions/first-contributions)
- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)
- [Accessibility for Developers](https://www.w3.org/WAI/tips/developing/)
- [Plain Language Guidelines](https://www.plainlanguage.gov/guidelines/)

## 🙏 Thank You!

Every contribution, no matter how small, makes this research better. Thank you for being part of our neurodivergent-first community!

---

**Questions?** Open a [Discussion](https://github.com/yourusername/constitutional-adaptive-learning/discussions) or join our [Discord](https://discord.gg/calsp).

**Last Updated:** 2026-06-23  
**Maintained by:** Community Manager & OSSC