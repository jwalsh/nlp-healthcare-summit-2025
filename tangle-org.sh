#!/bin/bash
# tangle-org.sh - Tangle all org files in the repository to extract source code

echo "Tangling all org files to extract source code..."

# Make this script executable
chmod +x "$0"

# Check if emacs is available
if ! command -v emacs >/dev/null 2>&1; then
    echo "Error: Emacs is not installed or not in PATH"
    echo "Please install Emacs to use org-babel-tangle functionality."
    exit 1
fi

# Find all org files in the repository
ORG_FILES=$(find . -name "*.org" -type f | sort)

if [ -z "$ORG_FILES" ]; then
    echo "No org files found in the repository."
    exit 0
fi

# Create a temporary Elisp file to run org-babel-tangle
TMP_ELISP_FILE=$(mktemp)
cat > "$TMP_ELISP_FILE" <<'EOF'
(progn
  (require 'org)
  (require 'ob-tangle)
  
  (defun tangle-org-file (file)
    "Tangle FILE using org-babel-tangle."
    (find-file file)
    (message "Tangling %s..." file)
    (let ((tangle-files (org-babel-tangle)))
      (if tangle-files
          (progn
            (message "Tangled %d file(s) from %s:" (length tangle-files) file)
            (dolist (tangled-file tangle-files)
              (message "  - %s" tangled-file)))
        (message "No code blocks tangled from %s" file))))
  
  (dolist (file command-line-args-left)
    (tangle-org-file file))
  
  (kill-emacs 0))
EOF

# Run org-babel-tangle on each org file
echo "Tangling the following files:"
echo "$ORG_FILES" | sed 's/^/  - /'
echo

emacs --batch -Q -l "$TMP_ELISP_FILE" $ORG_FILES

# Cleanup
rm "$TMP_ELISP_FILE"

echo "Org-babel-tangle complete!"