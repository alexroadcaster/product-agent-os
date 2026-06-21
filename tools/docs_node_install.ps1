param(
    [switch]$Install,
    [switch]$AllowNetwork,
    [string]$OfflineCache = ""
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$NodeToolsPath = Join-Path $RepoRoot ".docs-tools\node"
$PackageJsonPath = Join-Path $NodeToolsPath "package.json"
$BinPath = Join-Path $NodeToolsPath "node_modules\.bin"

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
    Write-Output "DOC-M36 plan only: no Node packages installed."
    Write-Output "Target folder: $NodeToolsPath"
    Write-Output "Package manifest: $PackageJsonPath"
    Write-Output "Run with -Install plus either -AllowNetwork or -OfflineCache <path> after approval."
    exit 0
}

if (-not $AllowNetwork -and [string]::IsNullOrWhiteSpace($OfflineCache)) {
    throw "DOC-M36 install requires explicit source: pass -AllowNetwork or -OfflineCache <path>."
}

if (-not (Test-Path -LiteralPath $PackageJsonPath)) {
    throw "Missing package.json at $PackageJsonPath"
}

Get-Command "npm.cmd" -ErrorAction Stop | Out-Null

$installArgs = @(
    "install",
    "--prefix", $NodeToolsPath,
    "--save-dev",
    "--save-exact",
    "markdownlint-cli2",
    "prettier",
    "@redocly/cli"
)

if (-not [string]::IsNullOrWhiteSpace($OfflineCache)) {
    $installArgs += @("--cache", $OfflineCache, "--offline")
}

Invoke-Checked "npm.cmd" @installArgs

Invoke-Checked (Join-Path $BinPath "markdownlint-cli2.cmd") "--version"
Invoke-Checked (Join-Path $BinPath "prettier.cmd") "--version"
Invoke-Checked (Join-Path $BinPath "redocly.cmd") "--version"
