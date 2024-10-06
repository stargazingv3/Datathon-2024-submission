#!/bin/bash

# List of scripts to run
scripts=(
    "scripts/scrape.py"
    "scripts/combine-scrape.py"
    "scripts/cleanup.py"
    "scripts/add-county.py"
    "scripts/aggregate.py"
    "scripts/filter-pdp.py"
    "scripts/Task2.py"
)

# Run each script
for script in "${scripts[@]}"; do
    echo "Running $script..."
    python "$script"
    
    # Check if the last command was successful
    if [ $? -ne 0 ]; then
        echo "Error running $script"
        exit 1
    fi
done

echo "All scripts have been executed."
