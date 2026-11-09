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

$Offline = -not [string]::IsNullOrWhiteSpace($OfflineWheelhouse)
if ($Offline -and -not (Test-Path -LiteralPath $OfflineWheelhouse -PathType Container)) {
    throw "Offline wheelhouse directory not found: $OfflineWheelhouse"
}

if (-not (Test-Path -LiteralPath $VenvPath)) {
    # venv uses bundled ensurepip; never request --upgrade-deps in offline mode.
    Invoke-Checked "python" "-m" "venv" $VenvPath
}

if ($Offline) {
    # Offline takes precedence even when -AllowNetwork was also supplied.
    try {
        Invoke-Checked $PythonPath "-m" "pip" "install" "--no-index" "--find-links" $OfflineWheelhouse "-r" $RequirementsPath
    } catch {
        throw "Offline wheelhouse install failed. Supply all compatible wheels locally; no network fallback was attempted. $($_.Exception.Message)"
    }
} else {
    Invoke-Checked $PythonPath "-m" "pip" "install" "--upgrade" "pip"
    Invoke-Checked $PythonPath "-m" "pip" "install" "-r" $RequirementsPath
}

Invoke-Checked $PythonPath "-m" "mkdocs" "--version"
