param(
  [switch]$SkipPython
)

$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
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

function Skip($name, $reason) {
  Write-Host "==> $name skipped ($reason)"
}

function Has($cmd) {
  return Get-Command $cmd -ErrorAction SilentlyContinue
}

function Get-GoBin {
  if (-not (Has "go")) {
    return $null
  }
  $goBin = (& go env GOBIN).Trim()
  if (-not $goBin) {
    $goPath = (& go env GOPATH).Trim()
    if ($goPath) {
      $goBin = Join-Path $goPath "bin"
    }
  }
  return $goBin
}

function Note-GoPath {
  $goBin = Get-GoBin
  if (-not $goBin) {
    return
  }
  $pathParts = $env:PATH -split ";"
  if ($pathParts -notcontains $goBin) {
    Write-Host "==> NOTE: add $goBin to PATH to use Go-installed tools."
  }
}

function Get-PythonCmd {
  if (Has "python") { return "python" }
  if (Has "python3") { return "python3" }
  if (Has "py") { return "py" }
  return $null
}

function Note-PythonPath($pythonCmd) {
  if (-not $pythonCmd) {
    return
  }
  try {
    $base = (& $pythonCmd -m site --user-base).Trim()
    if (-not $base) {
      return
    }
    $scripts = Join-Path $base "Scripts"
    $pathParts = $env:PATH -split ";"
    if ($pathParts -notcontains $scripts) {
      Write-Host "==> NOTE: add $scripts to PATH to use Python user-installed tools."
    }
  } catch {
    return
  }
}

if (Has "markdownlint-cli2") {
  Skip "markdownlint-cli2" "already installed"
} elseif (Has "npm") {
  Run "markdownlint-cli2" { npm install -g markdownlint-cli2 }
} else {
  Skip "markdownlint-cli2" "npm not installed"
  $fail = $true
}

if (Has "actionlint") {
  Skip "actionlint" "already installed"
} elseif (Has "go") {
  Run "actionlint" { go install github.com/rhysd/actionlint/cmd/actionlint@latest }
  Note-GoPath
} else {
  Skip "actionlint" "go not installed"
  $fail = $true
}

if (Has "kube-linter") {
  Skip "kube-linter" "already installed"
} elseif (Has "go") {
  Run "kube-linter" { go install golang.stackrox.io/kube-linter/cmd/kube-linter@latest }
  Note-GoPath
} else {
  Skip "kube-linter" "go not installed"
  $fail = $true
}

if ($SkipPython) {
  Skip "python tools" "SkipPython set"
} else {
  $pythonCmd = Get-PythonCmd
  if (Has "ruff") {
    Skip "ruff" "already installed"
  } elseif (Has "pipx") {
    Run "ruff" { pipx install ruff }
  } elseif ($pythonCmd) {
    Run "ruff" { & $pythonCmd -m pip install --user ruff }
    Note-PythonPath $pythonCmd
  } else {
    Skip "ruff" "python or pipx not installed"
    $fail = $true
  }

  if (Has "mypy") {
    Skip "mypy" "already installed"
  } elseif (Has "pipx") {
    Run "mypy" { pipx install mypy }
  } elseif ($pythonCmd) {
    Run "mypy" { & $pythonCmd -m pip install --user mypy }
    Note-PythonPath $pythonCmd
  } else {
    Skip "mypy" "python or pipx not installed"
    $fail = $true
  }
}

if ($fail) {
  Write-Host "==> One or more tools were not installed. See messages above."
  exit 1
}
