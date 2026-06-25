#!/usr/bin/env bash

# 1️⃣ Ensure we're in the repo root
cd "$(git rev-parse --show-toplevel)" || exit 1

# 2️⃣ Back up the original requirements file
cp requirements.txt requirements.txt.bak

# 3️⃣ Remove the hard‑pin on sympy (replace with a minimum version)
sed -i.bak '/^sympy==1.12$/d' requirements.txt
echo "sympy>=1.13.3" >> requirements.txt

# 4️⃣ Clean the pip cache to avoid stale wheels
pip cache purge

# 5️⃣ Install all dependencies (will pick a torch that satisfies sympy>=1.13.3)
pip install -r requirements.txt

# 6️⃣ Verify the WebUI starts
cd ui && streamlit run app.py
