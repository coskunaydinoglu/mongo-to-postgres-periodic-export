#!/bin/bash

# Load environment variables
set -a  # Automatically export all variables
source /app/.env
set +a

# Now run your Python script
python /app/script.py
