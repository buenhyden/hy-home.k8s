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
  $mdFiles = @(git diff --name-only --cached --diff-filter=ACMR -- "*.md")
  $mdFiles = $mdFiles | Where-Object { $_ -notmatch '(^|/)\.history/' }
  if ($mdFiles.Count -eq 0) {
    Skip "markdownlint" "no markdown files staged"
  } else {
    Run "markdownlint" { markdownlint-cli2 @mdFiles }
  }
} else {
  Skip "markdownlint" "markdownlint-cli2 not installed"
}

if (Has "actionlint") {
  Run "actionlint" { actionlint -color }
} else {
  Skip "actionlint" "actionlint not installed"
}

if (Has "kube-linter") {
  $yamlFiles = @(git diff --name-only --cached --diff-filter=ACMR -- "*.yml" "*.yaml")
  $yamlFiles = $yamlFiles | Where-Object { $_ -notmatch '(^|/)\.history/' }
  $chartDirs = $yamlFiles |
    Where-Object { $_ -match '(^|/)Chart\.yaml$' } |
    ForEach-Object { Split-Path $_ -Parent } |
    Where-Object { $_ -and $_ -ne "." }
  $rootCharts = $yamlFiles | Where-Object { $_ -match '^(\\./)?Chart\.yaml$' }
  $manifestFiles = $yamlFiles | Where-Object { $_ -notmatch '(^|/)Chart\.yaml$' }
  $targets = @($manifestFiles + $chartDirs + $rootCharts | Sort-Object -Unique)
  if ($targets.Count -eq 0) {
    Skip "kube-linter" "no yaml files staged"
  } else {
    foreach ($target in $targets) {
      Run "kube-linter ($target)" { kube-linter lint $target --config .kube-linter.yaml }
    }
  }
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
