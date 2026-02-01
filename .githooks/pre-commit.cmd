@echo off
setlocal

set "HOOK_DIR=%~dp0"
set "PS=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"

if not exist "%PS%" (
  echo PowerShell not found at %PS%
  exit /b 1
)

"%PS%" -NoProfile -ExecutionPolicy Bypass -File "%HOOK_DIR%pre-commit.ps1" %*
exit /b %errorlevel%
