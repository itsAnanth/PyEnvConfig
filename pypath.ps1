# Ask for Python installation directory
$pythonroot = Read-Host "Enter the path to the Python installation directory (e.g., C:\Python39)"

# Normalize path (removes trailing slashes, resolves relative paths)
try {
    $pythonroot = (Resolve-Path $pythonroot).Path
} catch {
    Write-Host "Invalid path provided. Exiting script."
    exit 1
}

$pythonexe  = Join-Path $pythonroot "python.exe"
$scriptsdir = Join-Path $pythonroot "Scripts"

if (!(Test-Path $pythonexe)) {
    Write-Host "Python executable not found at $pythonexe. Exiting script."
    exit 1
}

if (!(Test-Path $scriptsdir)) {
    Write-Host "Scripts directory not found at $scriptsdir. Attempting to create it using ensurepip."

    & $pythonexe -m pip install --upgrade pip setuptools wheel
    & $pythonexe -m ensurepip --upgrade
}

if (!(Test-Path $scriptsdir)) {
    Write-Host "Scripts directory still not found at $scriptsdir. Exiting script."
    exit 1
}

$pippath = Join-Path $scriptsdir "pip.exe"
if (!(Test-Path $pippath)) {
    Write-Host "pip executable not found at $pippath. Attempting to Bootstrap pip."

    Invoke-WebRequest https://bootstrap.pypa.io/get-pip.py -OutFile get-pip.py
    & $pythonexe get-pip.py
    Remove-Item get-pip.py
}

if (!(Test-Path $pippath)) {
    Write-Host "Failed to bootstrap pip at $pippath. Proceeding"
}

$olduserpath = [Environment]::GetEnvironmentVariable("Path", "User")

$existingPaths = @()
if (-not [string]::IsNullOrEmpty($olduserpath)) {
    $existingPaths = $olduserpath -split ';'
}

$pathstoadd = @($pythonroot, $scriptsdir)

$newPaths = @($existingPaths)

foreach ($pathtoadd in $pathstoadd) {
    if (-not ($newPaths | Where-Object { $_.TrimEnd('\') -ieq $pathtoadd.TrimEnd('\') })) {
        $newPaths += $pathtoadd
    }
}

$newuserpath = ($newPaths -join ';')

if ([string]::IsNullOrEmpty($newuserpath)) {
    Write-Error "New PATH is empty - aborting to prevent damage"
    exit 1
}

# Backup existing PATH
$olduserpath | Out-File (Join-Path $PSScriptRoot "path_backup.txt")


$confirmation = Read-Host "Do you want to set the new Path as:`n$newuserpath`n(y/n)"
if ($confirmation -ne "y") {
    Write-Host "Operation cancelled by user."
    exit 0
}

[Environment]::SetEnvironmentVariable("Path", $newuserpath, "User")

Write-Host "Python and pip set successfully."
Write-Host "Restart PowerShell to apply changes."
