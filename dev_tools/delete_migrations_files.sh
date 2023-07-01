#!/bin/bash

delete_migrations_files() {
  # Loop through all directories and subdirectories
  for directory in "$1"/*/; do
    if [ -d "$directory" ]; then
      # Check if the directory is named "migrations"
      if [ "$(basename "$directory")" == "migrations" ]; then
        echo "Found 'migrations' folder: $directory"
        echo "Deleting files in $directory"

        # Loop through all files in the migrations folder
        for file in "$directory"/*; do
          if [ -f "$file" ] && [ "$(basename "$file")" != "__init__.py" ]; then
            echo "Deleting $(basename "$file")"
            rm "$file"
          fi
        done

        echo "File deletion completed in $directory"
        echo
      fi

      # Recursively call the function for subdirectories
      delete_migrations_files "$directory"
    fi
  done
}

# Start the file deletion from the current directory
delete_migrations_files "."

echo "File deletion process completed."
