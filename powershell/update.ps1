# Download and execute the install script with -Update flag
$scriptContent = Invoke-RestMethod -Uri "https://raw.githubusercontent.com/itsAnanth/pvm/main/powershell/install.ps1"
$scriptBlock = [ScriptBlock]::Create($scriptContent)
& $scriptBlock -Update