#!/bin/bash

is_venv_activated() {
    [[ "$VIRTUAL_ENV" != "" ]]
}

# Call the function to check if the virtual environment is activated
if is_venv_activated; then
    echo "Virtual environment is activated."
else
    echo "Virtual environment is not activated."
fi

# Check if VIRTUAL_ENV variable is set
if [ -n "$VIRTUAL_ENV" ]; then
    # Print the path of the virtual environment
    echo "Virtual environment is activated: $VIRTUAL_ENV"
else
    # Print a warning message and exit with non-zero status
    echo "Warning: Virtual environment is not activated!"
fi
