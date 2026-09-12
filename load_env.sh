#!/bin/bash
# load_env.sh - Export local .env keys into the Pixi environment session

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

