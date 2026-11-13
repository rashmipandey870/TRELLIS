# Helper script to sync the current trellis project state to Downloads/trellis.zip
param(
    [string]$Destination = "C:\Users\Rashm\Downloads\trellis.zip"
)

$Source = "C:\Users\Rashm\.gemini\antigravity\scratch\trellis"
Write-Host "Compressing $Source to $Destination..."
Get-ChildItem -Path $Source -Force | Compress-Archive -DestinationPath $Destination -Force
Write-Host "trellis.zip successfully updated at $(Get-Date)"
