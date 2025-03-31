#!/bin/bash
# lint-org.sh - Lint all org files in the repository using emacs org-lint

echo "Linting all org files with org-lint..."

# Make this script executable
chmod +x "$0"

# Check if emacs is available
if ! command -v emacs >/dev/null 2>&1; then
    echo "Error: Emacs is not installed or not in PATH"
    echo "Please install Emacs to use org-lint functionality."
    exit 1
fi

# Find all org files in the repository
ORG_FILES=$(find . -name "*.org" -type f | sort)

if [ -z "$ORG_FILES" ]; then
    echo "No org files found in the repository."
    exit 0
fi

# Create a temporary Elisp file to run org-lint
TMP_ELISP_FILE=$(mktemp)
cat > "$TMP_ELISP_FILE" <<'EOF'
(progn
  (require 'org)
  (require 'org-lint)
  
  (defun lint-org-file (file)
    "Run org-lint on FILE and output results."
    (find-file file)
    (message "Linting %s..." file)
    (let ((lint-results (org-lint)))
      (if lint-results
          (progn
            (message "Found %d issues in %s:" (length lint-results) file)
            (dolist (result lint-results)
              (message "  - %s: %s" (car result) (cadr result))))
        (message "No issues found in %s" file))))
  
  (dolist (file command-line-args-left)
    (lint-org-file file))
  
  (kill-emacs 0))
EOF

# Run org-lint on each org file
echo "Running org-lint on the following files:"
echo "$ORG_FILES" | sed 's/^/  - /'
echo

emacs --batch -Q -l "$TMP_ELISP_FILE" $ORG_FILES

# Cleanup
rm "$TMP_ELISP_FILE"

echo "Org-lint check complete!"