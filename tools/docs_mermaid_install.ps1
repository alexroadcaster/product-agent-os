param(
    [switch]$Install,
    [switch]$AllowNetwork,
    [string]$MermaidVersion = "10.9.6",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$VendorDir = Join-Path $Root "docs\assets\javascripts\vendor"
$TargetFileName = "mermaid-$MermaidVersion.min.js"
$TargetPath = Join-Path $VendorDir $TargetFileName
$HashPath = Join-Path $VendorDir "$TargetFileName.sha256"
$LicensePath = Join-Path $VendorDir "mermaid-$MermaidVersion.LICENSE.txt"
$PackageMetadataPath = Join-Path $VendorDir "mermaid-$MermaidVersion.package.json"
$BaseUrl = "https://unpkg.com/mermaid@$MermaidVersion"
$AssetUrl = "$BaseUrl/dist/mermaid.min.js"
$LicenseUrl = "https://raw.githubusercontent.com/mermaid-js/mermaid/v$MermaidVersion/LICENSE"
$PackageUrl = "$BaseUrl/package.json"

$Plan = [ordered]@{
    tool = "mermaid"
    version = $MermaidVersion
    source = "npm package via pinned UNPKG URL"
    asset_url = $AssetUrl
    license_url = $LicenseUrl
    package_metadata_url = $PackageUrl
    target = "docs/assets/javascripts/vendor/$TargetFileName"
    hash_file = "docs/assets/javascripts/vendor/$TargetFileName.sha256"
    license_file = "docs/assets/javascripts/vendor/mermaid-$MermaidVersion.LICENSE.txt"
    package_metadata_file = "docs/assets/javascripts/vendor/mermaid-$MermaidVersion.package.json"
    install_requested = [bool]$Install
    allow_network = [bool]$AllowNetwork
    browser_proof_enabled = $false
    root_site_freshness_claim_enabled = $false
}

if (-not $Install) {
    $Plan | ConvertTo-Json -Depth 5
    exit 0
}

if (-not $AllowNetwork) {
    throw "Refusing to download Mermaid without -AllowNetwork."
}

New-Item -ItemType Directory -Path $VendorDir -Force | Out-Null

if ((Test-Path -LiteralPath $TargetPath) -and -not $Force) {
    $Hash = Get-FileHash -Path $TargetPath -Algorithm SHA256
    Set-Content -Path $HashPath -Value "$($Hash.Hash.ToLowerInvariant())  $TargetFileName" -Encoding ASCII
    [ordered]@{
        result = "already_installed"
        version = $MermaidVersion
        target = "docs/assets/javascripts/vendor/$TargetFileName"
        sha256 = $Hash.Hash.ToLowerInvariant()
        browser_proof_enabled = $false
        root_site_freshness_claim_enabled = $false
    } | ConvertTo-Json -Depth 5
    exit 0
}

$Headers = @{ "User-Agent" = "codex-docs-doc-m39" }
Invoke-WebRequest -Uri $AssetUrl -OutFile $TargetPath -Headers $Headers
Invoke-WebRequest -Uri $LicenseUrl -OutFile $LicensePath -Headers $Headers
Invoke-WebRequest -Uri $PackageUrl -OutFile $PackageMetadataPath -Headers $Headers

$PackageMetadata = Get-Content -Path $PackageMetadataPath -Raw | ConvertFrom-Json
if ($PackageMetadata.version -ne $MermaidVersion) {
    throw "Downloaded Mermaid package metadata version '$($PackageMetadata.version)' did not match expected '$MermaidVersion'."
}
if ($PackageMetadata.license -ne "MIT") {
    throw "Downloaded Mermaid package metadata license '$($PackageMetadata.license)' did not match expected MIT."
}

$Hash = Get-FileHash -Path $TargetPath -Algorithm SHA256
Set-Content -Path $HashPath -Value "$($Hash.Hash.ToLowerInvariant())  $TargetFileName" -Encoding ASCII

[ordered]@{
    result = "installed"
    version = $MermaidVersion
    source_url = $AssetUrl
    license_url = $LicenseUrl
    package_metadata_url = $PackageUrl
    target = "docs/assets/javascripts/vendor/$TargetFileName"
    sha256 = $Hash.Hash.ToLowerInvariant()
    license = $PackageMetadata.license
    browser_proof_enabled = $false
    root_site_freshness_claim_enabled = $false
} | ConvertTo-Json -Depth 5
