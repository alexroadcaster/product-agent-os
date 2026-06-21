param(
    [switch]$Install,
    [switch]$AllowNetwork,
    [string]$Version = "3.15.1",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$BinDir = Join-Path $Root ".docs-tools\bin"
$ValeExe = Join-Path $BinDir "vale.exe"
$HashFile = Join-Path $BinDir "vale.sha256"
$ReleaseApi = "https://api.github.com/repos/vale-cli/vale/releases/tags/v$Version"

New-Item -ItemType Directory -Path $BinDir -Force | Out-Null

$Plan = [ordered]@{
    tool = "Vale"
    version = $Version
    source = "GitHub Releases"
    release_api = $ReleaseApi
    target = ".docs-tools/bin/vale.exe"
    hash_file = ".docs-tools/bin/vale.sha256"
    install_requested = [bool]$Install
    allow_network = [bool]$AllowNetwork
    advisory_only = $true
}

if (-not $Install) {
    $Plan | ConvertTo-Json -Depth 4
    exit 0
}

if (-not $AllowNetwork) {
    throw "Refusing to download Vale without -AllowNetwork."
}

if ((Test-Path -LiteralPath $ValeExe) -and -not $Force) {
    $VersionText = & $ValeExe --version
    $Hash = Get-FileHash -Path $ValeExe -Algorithm SHA256
    Set-Content -Path $HashFile -Value "$($Hash.Hash.ToLowerInvariant())  vale.exe" -Encoding ASCII
    [ordered]@{
        result = "already_installed"
        version_output = $VersionText
        target = ".docs-tools/bin/vale.exe"
        sha256 = $Hash.Hash.ToLowerInvariant()
    } | ConvertTo-Json -Depth 4
    exit 0
}

$Headers = @{ "User-Agent" = "codex-docs-doc-m37" }
$Release = Invoke-RestMethod -Uri $ReleaseApi -Headers $Headers
$Asset = $Release.assets |
    Where-Object {
        $_.name -match "Windows" -and
        $_.name -match "(64-bit|amd64|x86_64)" -and
        $_.name -match "\.zip$"
    } |
    Select-Object -First 1

if (-not $Asset) {
    throw "Could not find a Windows 64-bit Vale zip asset for v$Version."
}

$ZipPath = Join-Path $BinDir "vale_$Version.zip"
$ExtractDir = Join-Path $BinDir "_vale_extract"

Invoke-WebRequest -Uri $Asset.browser_download_url -OutFile $ZipPath -Headers $Headers

if (Test-Path -LiteralPath $ExtractDir) {
    Remove-Item -LiteralPath $ExtractDir -Recurse -Force
}
New-Item -ItemType Directory -Path $ExtractDir -Force | Out-Null
Expand-Archive -LiteralPath $ZipPath -DestinationPath $ExtractDir -Force

$ExtractedVale = Get-ChildItem -Path $ExtractDir -Recurse -Filter "vale.exe" | Select-Object -First 1
if (-not $ExtractedVale) {
    throw "Downloaded archive did not contain vale.exe."
}

Copy-Item -LiteralPath $ExtractedVale.FullName -Destination $ValeExe -Force
$VersionText = & $ValeExe --version
$Hash = Get-FileHash -Path $ValeExe -Algorithm SHA256
Set-Content -Path $HashFile -Value "$($Hash.Hash.ToLowerInvariant())  vale.exe" -Encoding ASCII

Remove-Item -LiteralPath $ZipPath -Force
Remove-Item -LiteralPath $ExtractDir -Recurse -Force

[ordered]@{
    result = "installed"
    version_output = $VersionText
    source_asset = $Asset.name
    source_url = $Asset.browser_download_url
    target = ".docs-tools/bin/vale.exe"
    sha256 = $Hash.Hash.ToLowerInvariant()
    advisory_only = $true
} | ConvertTo-Json -Depth 4
