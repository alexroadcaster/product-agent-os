param(
    [switch]$Install,
    [switch]$AllowNetwork,
    [string]$OfflineWheelhouse = ""
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$VenvPath = Join-Path $RepoRoot ".venv-docs"
$RequirementsPath = Join-Path $RepoRoot "requirements.txt"
$PythonPath = Join-Path $VenvPath "Scripts\python.exe"

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,
        [Parameter(ValueFromRemainingArguments = $true)]
        [string[]]$Arguments
    )

    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed with exit code ${LASTEXITCODE}: $FilePath $($Arguments -join ' ')"
    }
}

if (-not $Install) {
    Write-Output "DOC-M35 plan only: no environment created and no dependencies installed."
    Write-Output "Target venv: $VenvPath"
    Write-Output "Requirements: $RequirementsPath"
    Write-Output "Run with -Install plus either -AllowNetwork or -OfflineWheelhouse <path> after approval."
    exit 0
}

if (-not $AllowNetwork -and [string]::IsNullOrWhiteSpace($OfflineWheelhouse)) {
    throw "DOC-M35 install requires explicit source: pass -AllowNetwork or -OfflineWheelhouse <path>."
}

if (-not (Test-Path -LiteralPath $RequirementsPath)) {
    throw "Missing requirements.txt at $RequirementsPath"
}

if (-not (Test-Path -LiteralPath $VenvPath)) {
    Invoke-Checked "python" "-m" "venv" $VenvPath
}

Invoke-Checked $PythonPath "-m" "pip" "install" "--upgrade" "pip"

if (-not [string]::IsNullOrWhiteSpace($OfflineWheelhouse)) {
    Invoke-Checked $PythonPath "-m" "pip" "install" "--no-index" "--find-links" $OfflineWheelhouse "-r" $RequirementsPath
} else {
    Invoke-Checked $PythonPath "-m" "pip" "install" "-r" $RequirementsPath
}

Invoke-Checked $PythonPath "-m" "mkdocs" "--version"
