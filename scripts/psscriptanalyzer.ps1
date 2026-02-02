[CmdletBinding()]
param (
    [Parameter(Mandatory=$true, Position=0, ValueFromRemainingArguments=$true)]
    [string[]]$Path
)

$ErrorActionPreference = "Stop"

if (-not (Get-Module -ListAvailable -Name PSScriptAnalyzer)) {
    Write-Warning "PSScriptAnalyzer module not found info. Attempting to import..."
    Import-Module PSScriptAnalyzer -ErrorAction SilentlyContinue
}

Write-Host "Running PSScriptAnalyzer on $($Path.Count) files..."

$results = Invoke-ScriptAnalyzer -Path $Path

if ($results) {
    $results | Format-Table
    Write-Error "PSScriptAnalyzer found issues."
    exit 1
} else {
    Write-Host "No issues found."
    exit 0
}
