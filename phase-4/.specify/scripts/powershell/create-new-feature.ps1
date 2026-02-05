# PowerShell script to create a new feature branch and spec file
param(
    [Parameter(Mandatory=$true)]
    [string]$Description,

    [Parameter(Mandatory=$true)]
    [int]$Number,

    [Parameter(Mandatory=$true)]
    [string]$ShortName
)

# Extract the feature name for directory
$featureDir = "${Number}-${ShortName}"
$specPath = "specs/${featureDir}/spec.md"

# Create directory if it doesn't exist
if (!(Test-Path "specs")) {
    New-Item -ItemType Directory -Path "specs" -Force
}

if (!(Test-Path "specs/${featureDir}")) {
    New-Item -ItemType Directory -Path "specs/${featureDir}" -Force
}

# Create the spec file with basic template
@"
# Specification: $ShortName

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
"@ | Out-File -FilePath $specPath -Encoding UTF8

# Create the branch
$branchName = "${Number}-${ShortName}"
git checkout -b $branchName

Write-Output "{""BRANCH_NAME"": ""${branchName}"", ""SPEC_FILE"": ""${specPath}""}"