# Install the OpsWatch agent as a Windows Scheduled Task (runs every 5 min as SYSTEM).
# Usage (admin PowerShell): .\scripts\install_agent.ps1
$ErrorActionPreference = "Stop"

$InstallDir = "C:\ProgramData\OpsWatch"
$RepoRoot   = Split-Path -Parent $PSScriptRoot

New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
Copy-Item -Recurse -Force "$RepoRoot\agent\opswatch_agent" $InstallDir
if (-not (Test-Path "$InstallDir\config.yaml")) {
    Copy-Item "$RepoRoot\agent\config.example.yaml" "$InstallDir\config.yaml"
}

python -m venv "$InstallDir\.venv"
& "$InstallDir\.venv\Scripts\pip.exe" install -q -r "$RepoRoot\agent\requirements.txt"

$Action  = New-ScheduledTaskAction -Execute "$InstallDir\.venv\Scripts\python.exe" `
           -Argument "-m opswatch_agent.cli --config config.yaml --once" -WorkingDirectory $InstallDir
$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5)
Register-ScheduledTask -TaskName "OpsWatchAgent" -Action $Action -Trigger $Trigger `
    -User "SYSTEM" -RunLevel Highest -Force | Out-Null

Write-Host "Installed. Edit $InstallDir\config.yaml to point at your server."
