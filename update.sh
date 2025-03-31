#!/bin/bash
# update.sh - Update all documents and generate outputs for NLP Summit Healthcare 2025

echo "Updating NLP Summit Healthcare 2025 repository..."

# Make this script executable (just in case)
chmod +x "$0"

# Activate Poetry environment if it exists, otherwise create it
if [ -d .venv ]; then
    source .venv/bin/activate || source .venv/Scripts/activate
else
    echo "Setting up Poetry environment..."
    poetry install
    poetry shell
fi

# Process org files to generate tangled output (if emacs is available)
if command -v emacs >/dev/null 2>&1; then
    echo "Processing org files with Emacs..."
    find . -name "*.org" -exec emacs --batch -l org {} -f org-babel-tangle \;
else
    echo "Emacs not found. Skipping org-mode tangling."
    echo "Install Emacs and org-mode for full functionality."
fi

# Run Python processors
echo "Running Python processors..."
mkdir -p docs

# Process sessions
echo "Processing sessions..."
python -m nlp_healthcare_summit_2025.scripts.process_sessions

# Process contacts
echo "Processing contacts..."
python -m nlp_healthcare_summit_2025.scripts.process_contacts

# Process knowledge base
echo "Processing knowledge base..."
python -m nlp_healthcare_summit_2025.scripts.process_knowledge

echo "Update complete!"
