$ErrorActionPreference = "Stop"

$root = git rev-parse --show-toplevel
Set-Location $root

$fail = $false

function Run($name, $script) {
  Write-Host "==> $name"
  try {
    & $script
    Write-Host "==> $name ok"
  } catch {
    Write-Host "==> $name failed"
    $script:fail = $true
  }
}

function Run-In($name, $dir, $script) {
  Write-Host "==> $name"
  try {
    Push-Location $dir
    & $script
    Write-Host "==> $name ok"
  } catch {
    Write-Host "==> $name failed"
    $script:fail = $true
  } finally {
    Pop-Location
  }
}

function Skip($name, $reason) {
  Write-Host "==> $name skipped ($reason)"
}

function Has($cmd) {
  return Get-Command $cmd -ErrorAction SilentlyContinue
}

if (Has "markdownlint-cli2") {
  Run "markdownlint" { markdownlint-cli2 "**/*.md" }
} else {
  Skip "markdownlint" "markdownlint-cli2 not installed"
}

if (Has "actionlint") {
  Run "actionlint" { actionlint -color }
} else {
  Skip "actionlint" "actionlint not installed"
}

if (Has "kube-linter") {
  Run "kube-linter" { kube-linter lint . --config .kube-linter.yaml }
} else {
  Skip "kube-linter" "kube-linter not installed"
}

$pyDir = "apps/_examples/demo-backend/app"
if (Test-Path $pyDir) {
  if (Has "ruff") {
    Run-In "ruff" $pyDir { ruff check . }
  } else {
    Skip "ruff" "ruff not installed"
  }

  if (Has "mypy") {
    Run-In "mypy" $pyDir { mypy . }
  } else {
    Skip "mypy" "mypy not installed"
  }
} else {
  Skip "python lint" "directory not found: $pyDir"
}

if ($fail) {
  Write-Host "Commit blocked due to failed checks."
  exit 1
}
