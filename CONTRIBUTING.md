# Contributing to CropVanta.AI 

Thank you for your interest in contributing to CropVanta.AI.  
We welcome improvements in AI models, agricultural analytics, performance optimization, documentation, UI enhancements, and system architecture.

This document provides a structured overview of how to contribute effectively and professionally.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Ways to Contribute](#ways-to-contribute)
- [Add or Improve Features](#add-or-improve-features)
- [Improve Models](#improve-models)
- [Update Data Pipelines](#update-data-pipelines)
- [Reporting Issues](#reporting-issues)
- [Development Workflow](#development-workflow)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Commit Message Standards](#commit-message-standards)
- [Security & Data Policy](#security--data-policy)
- [Code of Conduct](#code-of-conduct)

---

## Project Structure

Main directories in this repository:

- [`assets/`](https://github.com/dhakarshailendra829/CropVanta.AI/tree/main/assets)
- [`data/`](https://github.com/dhakarshailendra829/CropVanta.AI/tree/main/data)
- [`images/`](https://github.com/dhakarshailendra829/CropVanta.AI/tree/main/images)
- [`logs/`](https://github.com/dhakarshailendra829/CropVanta.AI/tree/main/logs)
- [`models/`](https://github.com/dhakarshailendra829/CropVanta.AI/tree/main/models)
- [`modules/`](https://github.com/dhakarshailendra829/CropVanta.AI/tree/main/modules)
- [`pages/`](https://github.com/dhakarshailendra829/CropVanta.AI/tree/main/pages)
- [`scripts/`](https://github.com/dhakarshailendra829/CropVanta.AI/tree/main/scripts)
- [`uploaded_papers/`](https://github.com/dhakarshailendra829/CropVanta.AI/tree/main/uploaded_papers)

Key files:

- [`app.py`](https://github.com/dhakarshailendra829/CropVanta.AI/blob/main/app.py) – Main application entry point  
- [`Modelcode.py`](https://github.com/dhakarshailendra829/CropVanta.AI/blob/main/Modelcode.py) – Core ML logic  
- [`requirements.txt`](https://github.com/dhakarshailendra829/CropVanta.AI/blob/main/requirements.txt) – Dependencies  
- [`styles.css`](https://github.com/dhakarshailendra829/CropVanta.AI/blob/main/styles.css) – UI styling  
- [`README.md`](https://github.com/dhakarshailendra829/CropVanta.AI/blob/main/README.md)  
- [`LICENSE`](https://github.com/dhakarshailendra829/CropVanta.AI/blob/main/LICENSE)

⚠️ Do not commit runtime-generated files inside `logs/` or large temporary outputs.

---

## 🚀 Ways to Contribute

You can contribute by:

- Improving AI/ML models
- Enhancing crop prediction accuracy
- Optimizing preprocessing pipelines
- Fixing bugs
- Improving UI/UX pages
- Refactoring modules for performance
- Enhancing documentation
- Adding research-backed agricultural insights

---

## 🌱 Add or Improve Features

If you want to add a feature:

1. Open an issue first describing:
   - What the feature does
   - Why it is useful
   - Technical approach

2. Create a new branch:

```bash
git checkout -b feature/feature-name
```
---

## 🌱 Feature Branch Examples

When creating a new feature branch, follow this format:

```
feature/short-description
```

### Examples:

- `feature/agri-metrics-dashboard`
- `feature/disease-detection-upgrade`

---

## 🤖 Improve Models

If contributing to AI/ML models:

- Maintain reproducibility
- Document dataset source clearly
- Provide evaluation metrics:
  - Accuracy
  - F1-score
  - Precision / Recall
- Compare results with baseline model
- Ensure no data leakage
- Validate proper training/testing splits

🚫 **Do NOT commit trained model weights or large datasets unless explicitly approved.**  
Use external storage or model hosting if required.

Model-related work usually involves:

```
models/
Modelcode.py
data/
```

---

## 🔄 Update Data Pipelines

If modifying preprocessing or pipeline logic:

- Avoid hardcoded paths
- Keep dataset structure consistent
- Ensure compatibility with `app.py`
- Validate outputs
- Maintain clean modular structure

Pipeline logic may involve:

```
scripts/
modules/
data/
```

---

## 🐛 Reporting Issues

When reporting a bug, include:

- Clear description
- Steps to reproduce
- Expected vs actual behavior

### Environment Details:

- Python version
- Operating System (OS)
- Library versions
- GPU/CPU (if ML-related)

Before opening a new issue, please check existing issues.

---

## 🛠 Development Workflow

1. Fork the repository  
2. Clone your fork  
3. Install dependencies:

```
pip install -r requirements.txt
```

4. Create a new branch:

```
git checkout -b feature/short-description
```

5. Make changes  
6. Test locally  
7. Submit a Pull Request  

---

## 📥 Pull Request Guidelines

When submitting a PR:

- Provide a clear description
- Mention related issue (if any)
- Include model performance comparison (if applicable)
- Ensure no breaking changes
- Keep PR focused (avoid unrelated bulk changes)

---

## ✅ PR Checklist

- [ ] Code runs successfully
- [ ] No debug prints
- [ ] Documentation updated
- [ ] Tested locally
- [ ] No unnecessary files committed

---

## 📝 Commit Message Standards

Use professional and meaningful commit messages.

### Format:

Short summary (max 72 characters)

### Good Examples:

- Improve crop yield prediction accuracy
- Optimize preprocessing memory usage
- Fix hashing reset bug
- Refactor authentication module

### ❌ Avoid:

- update
- fix
- changes

---

## 🔒 Security & Data Policy

- Do not upload private datasets
- Do not commit API keys or `.env` secrets
- Follow dataset licensing rules
- Ensure ethical AI usage
- Avoid biased agricultural predictions
- Do not commit large log files

If you find a security issue, report it privately to the maintainer.

---

Thank you for helping improve CropVanta.AI 🌾🚀
