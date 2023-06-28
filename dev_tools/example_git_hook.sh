#!/bin/bash
# ./.git/hooks/pre-commit

is_venv_activated() {
    [[ "$VIRTUAL_ENV" != "" ]]
}

# Call the function to check if the virtual environment is activated
if is_venv_activated; then
    echo "🚨 Virtual environment is activated."
else
    echo "✅ Virtual environment is not activated."
    exit 1
fi

# 🗑️ Delete unused imports
autoflake -i -r --remove-all-unused-imports .

# 🚦 Sort imports
isort .

# 👔 Code formatting
yapf --in-place --recursive .
# black -l 120 .

# ➕ Readd all changed files
git add .
