#!/bin/bash
# load_env.sh - Export local .env keys into the Pixi environment session

# Make the repo root importable as a package (e.g. `from src.db.connection import ...`)
# regardless of which script's directory Streamlit/pytest/python prepend to sys.path.
export PYTHONPATH="$PIXI_PROJECT_ROOT${PYTHONPATH:+:$PYTHONPATH}"

ENV_FILE="$PIXI_PROJECT_ROOT/.env"

if [ -f "$ENV_FILE" ]; then
    # Filter out comments and blank lines, then export variables
    while IFS= read -r line || [ -n "$line" ]; do
        # Ignore lines starting with # or empty lines
        [[ "$line" =~ ^#.*$ ]] && continue
        [[ -z "$line" ]] && continue
        
        # Export the variable
        export "$line"
    done < "$ENV_FILE"
fi

