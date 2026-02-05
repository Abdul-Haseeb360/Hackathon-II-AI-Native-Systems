#!/bin/bash

DESCRIPTION="$1"
NUMBER="$2"
SHORTNAME="$3"

# Extract the feature name for directory
FEATURE_DIR="${NUMBER}-${SHORTNAME}"
SPEC_PATH="specs/${FEATURE_DIR}/spec.md"

# Create directory if it doesn't exist
mkdir -p "specs/${FEATURE_DIR}"

# Create the spec file with basic template
cat > "$SPEC_PATH" << EOF
# Specification: $SHORTNAME

## Summary

[Feature summary goes here]

## User Scenarios & Testing

[User scenarios and testing approach]

## Functional Requirements

[Detailed functional requirements]

## Non-Functional Requirements

[Performance, security, scalability requirements]

## Success Criteria

[Measurable success criteria]

## Key Entities

[Data entities and relationships if applicable]

## Dependencies & Assumptions

[External dependencies and assumptions]

## Out of Scope

[Explicitly what is not included]
EOF

# Create the branch
BRANCH_NAME="${FEATURE_DIR}"
git checkout -b "$BRANCH_NAME"

echo "{\"BRANCH_NAME\": \"${BRANCH_NAME}\", \"SPEC_FILE\": \"${SPEC_PATH}\"}"