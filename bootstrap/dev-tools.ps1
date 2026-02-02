[Diagnostics.CodeAnalysis.SuppressMessageAttribute('PSAvoidUsingWriteHost', '')]
$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $root

function Has($cmd) {
  return Get-Command $cmd -ErrorAction SilentlyContinue
}

Write-Host "==> Setting up pre-commit..."

if (Has "pre-commit") {
  Write-Host "==> pre-commit already installed"
} else {
  if (Has "pipx") {
    Write-Host "==> Installing pre-commit via pipx..."
    pipx install pre-commit
  } elseif (Has "pip") {
    Write-Host "==> Installing pre-commit via pip..."
    pip install pre-commit
  } elseif (Has "python") {
    Write-Host "==> Installing pre-commit via python -m pip..."
    python -m pip install pre-commit
  } else {
    Write-Host "==> Error: Python/pip required to install pre-commit." -ForegroundColor Red
    exit 1
  }
}

if (Has "pre-commit") {
  Write-Host "==> Installing git hooks..."
  pre-commit install
} else {
  # Try to find it in user scripts
  try {
    if (Has "python") {
        $base = (& python -m site --user-base).Trim()
        $scripts = Join-Path $base "Scripts"
        $env:PATH += ";$scripts"
    }
  } catch {
    Write-Verbose "Failed to determine Python user base: $_"
  }

  if (Has "pre-commit") {
    Write-Host "==> Installing git hooks..."
    pre-commit install
  } else {
    Write-Host "==> Error: pre-commit installed but not found in PATH." -ForegroundColor Red
    exit 1
  }
}

Write-Host "==> Setup complete!" -ForegroundColor Green
