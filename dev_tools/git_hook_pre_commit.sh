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

make ff

# ➕ Readd all changed files
git add .
