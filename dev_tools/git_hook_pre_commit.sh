#!/bin/bash

is_venv_activated() {
    [[ "$VIRTUAL_ENV" != "" ]]
}

# Call the function to check if the virtual environment is activated
if is_venv_activated; then
    echo "✅ Virtual environment is activated: $VIRTUAL_ENV"
else
    echo "🚨 Virtual environment is not activated."
    exit 1
fi

# 🗑️ Delete unused imports
autoflake .

# 🚦 Sort imports
isort .

# 👔 Code formatting
yapf --in-place --recursive .

# 👔 HTML formatting
djlint --reformat ./app

# ➕ Readd all changed files
git add .
