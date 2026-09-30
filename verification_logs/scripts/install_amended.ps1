# install_amended.ps1
$ErrorActionPreference = "Continue"

Write-Output "=== 1. Installing amended requirements ==="
$logFile = "..\verification_logs\step1_amended_install.log"
& .\venv\Scripts\pip.exe install -r ..\verification_logs\requirements.amended.txt 2>&1 | Out-File -FilePath $logFile -Encoding utf8
$installExit = $LASTEXITCODE
Write-Output "pip install exit code: $installExit"

Write-Output "=== 2. pip show finnhub-python ==="
& .\venv\Scripts\pip.exe show finnhub-python

Write-Output "=== 3. pip freeze ==="
$freezeFile = "..\verification_logs\step1_pip_freeze.log"
& .\venv\Scripts\pip.exe freeze | Out-File -FilePath $freezeFile -Encoding utf8
$freezeExit = $LASTEXITCODE
Write-Output "pip freeze exit code: $freezeExit"
