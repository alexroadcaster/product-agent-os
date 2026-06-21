param(
    [switch]$Install,
    [switch]$AllowNetwork,
    [string]$LycheeVersion = "0.24.2",
    [string]$GitleaksVersion = "8.30.0",
    [switch]$Force
)

$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$BinDir = Join-Path $Root ".docs-tools\bin"
$LycheeExe = Join-Path $BinDir "lychee.exe"
$GitleaksExe = Join-Path $BinDir "gitleaks.exe"
$LycheeHashFile = Join-Path $BinDir "lychee.sha256"
$GitleaksHashFile = Join-Path $BinDir "gitleaks.sha256"
$LycheeReleaseApi = "https://api.github.com/repos/lycheeverse/lychee/releases/tags/lychee-v$LycheeVersion"
$GitleaksReleaseApi = "https://api.github.com/repos/gitleaks/gitleaks/releases/tags/v$GitleaksVersion"

New-Item -ItemType Directory -Path $BinDir -Force | Out-Null

$Plan = [ordered]@{
    tools = @(
        [ordered]@{
            tool = "lychee"
            version = $LycheeVersion
            source = "GitHub Releases"
            release_api = $LycheeReleaseApi
            target = ".docs-tools/bin/lychee.exe"
            hash_file = ".docs-tools/bin/lychee.sha256"
        },
        [ordered]@{
            tool = "gitleaks"
            version = $GitleaksVersion
            source = "GitHub Releases"
            release_api = $GitleaksReleaseApi
            target = ".docs-tools/bin/gitleaks.exe"
            hash_file = ".docs-tools/bin/gitleaks.sha256"
        }
    )
    install_requested = [bool]$Install
    allow_network = [bool]$AllowNetwork
    broad_scans_enabled = $false
    external_url_crawl_enabled = $false
    report_retention_enabled = $false
}

if (-not $Install) {
    $Plan | ConvertTo-Json -Depth 5
    exit 0
}

function Select-ReleaseAsset {
    param(
        [Parameter(Mandatory = $true)]
        $Assets,
        [Parameter(Mandatory = $true)]
        [string[]]$RequiredPatterns,
        [string[]]$RejectedPatterns = @()
    )

    foreach ($Asset in $Assets) {
        $Name = $Asset.name
        $MatchesAll = $true
        foreach ($Pattern in $RequiredPatterns) {
            if ($Name -notmatch $Pattern) {
                $MatchesAll = $false
                break
            }
        }
        if (-not $MatchesAll) {
            continue
        }
        foreach ($Pattern in $RejectedPatterns) {
            if ($Name -match $Pattern) {
                $MatchesAll = $false
                break
            }
        }
        if ($MatchesAll) {
            return $Asset
        }
    }
    return $null
}

function Expand-DownloadedAsset {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ToolName,
        [Parameter(Mandatory = $true)]
        $Asset,
        [Parameter(Mandatory = $true)]
        [string]$DownloadPath,
        [Parameter(Mandatory = $true)]
        [string]$TargetExe
    )

    if ($Asset.name -match "\.exe$") {
        Copy-Item -LiteralPath $DownloadPath -Destination $TargetExe -Force
        return
    }

    $ExtractDir = Join-Path $BinDir "_${ToolName}_extract"
    if (Test-Path -LiteralPath $ExtractDir) {
        Remove-Item -LiteralPath $ExtractDir -Recurse -Force
    }
    New-Item -ItemType Directory -Path $ExtractDir -Force | Out-Null

    if ($Asset.name -match "\.zip$") {
        Expand-Archive -LiteralPath $DownloadPath -DestinationPath $ExtractDir -Force
    } elseif ($Asset.name -match "\.tar\.gz$") {
        & tar -xzf $DownloadPath -C $ExtractDir
        if ($LASTEXITCODE -ne 0) {
            throw "tar extraction failed for $($Asset.name)."
        }
    } else {
        throw "Unsupported $ToolName asset extension: $($Asset.name)"
    }

    $ExtractedExe = Get-ChildItem -Path $ExtractDir -Recurse -Filter "$ToolName.exe" | Select-Object -First 1
    if (-not $ExtractedExe) {
        throw "Downloaded $ToolName archive did not contain $ToolName.exe."
    }

    Copy-Item -LiteralPath $ExtractedExe.FullName -Destination $TargetExe -Force
    Remove-Item -LiteralPath $ExtractDir -Recurse -Force
}

function Install-DocsTool {
    param(
        [Parameter(Mandatory = $true)]
        [string]$ToolName,
        [Parameter(Mandatory = $true)]
        [string]$Version,
        [Parameter(Mandatory = $true)]
        [string]$ReleaseApi,
        [Parameter(Mandatory = $true)]
        [string]$TargetExe,
        [Parameter(Mandatory = $true)]
        [string]$HashFile,
        [Parameter(Mandatory = $true)]
        [string[]]$RequiredAssetPatterns,
        [string[]]$RejectedAssetPatterns = @()
    )

    if ((Test-Path -LiteralPath $TargetExe) -and -not $Force) {
        $VersionText = if ($ToolName -eq "gitleaks") { & $TargetExe version } else { & $TargetExe --version }
        $Hash = Get-FileHash -Path $TargetExe -Algorithm SHA256
        Set-Content -Path $HashFile -Value "$($Hash.Hash.ToLowerInvariant())  $ToolName.exe" -Encoding ASCII
        return [ordered]@{
            result = "already_installed"
            tool = $ToolName
            version_output = ($VersionText -join "`n")
            target = ".docs-tools/bin/$ToolName.exe"
            sha256 = $Hash.Hash.ToLowerInvariant()
        }
    }

    if (-not $AllowNetwork) {
        throw "Refusing to download $ToolName without -AllowNetwork."
    }

    $Headers = @{ "User-Agent" = "codex-docs-doc-m38" }
    $Release = Invoke-RestMethod -Uri $ReleaseApi -Headers $Headers
    $Asset = Select-ReleaseAsset -Assets $Release.assets -RequiredPatterns $RequiredAssetPatterns -RejectedPatterns $RejectedAssetPatterns
    if (-not $Asset) {
        throw "Could not find a Windows x64 $ToolName asset for $Version."
    }

    $DownloadPath = Join-Path $BinDir $Asset.name
    Invoke-WebRequest -Uri $Asset.browser_download_url -OutFile $DownloadPath -Headers $Headers
    Expand-DownloadedAsset -ToolName $ToolName -Asset $Asset -DownloadPath $DownloadPath -TargetExe $TargetExe

    $VersionText = if ($ToolName -eq "gitleaks") { & $TargetExe version } else { & $TargetExe --version }
    $Hash = Get-FileHash -Path $TargetExe -Algorithm SHA256
    Set-Content -Path $HashFile -Value "$($Hash.Hash.ToLowerInvariant())  $ToolName.exe" -Encoding ASCII
    Remove-Item -LiteralPath $DownloadPath -Force

    return [ordered]@{
        result = "installed"
        tool = $ToolName
        version_output = ($VersionText -join "`n")
        source_asset = $Asset.name
        source_url = $Asset.browser_download_url
        target = ".docs-tools/bin/$ToolName.exe"
        sha256 = $Hash.Hash.ToLowerInvariant()
    }
}

$Results = @()
$Results += Install-DocsTool `
    -ToolName "lychee" `
    -Version $LycheeVersion `
    -ReleaseApi $LycheeReleaseApi `
    -TargetExe $LycheeExe `
    -HashFile $LycheeHashFile `
    -RequiredAssetPatterns @("(?i)^lychee-", "(?i)windows", "(?i)(x86_64|x64|amd64)", "(?i)(\.exe$|\.zip$|\.tar\.gz$)") `
    -RejectedAssetPatterns @("(?i)\.sha256$", "(?i)\.sig$")

$Results += Install-DocsTool `
    -ToolName "gitleaks" `
    -Version $GitleaksVersion `
    -ReleaseApi $GitleaksReleaseApi `
    -TargetExe $GitleaksExe `
    -HashFile $GitleaksHashFile `
    -RequiredAssetPatterns @("(?i)^gitleaks_", "(?i)windows", "(?i)(x64|x86_64|amd64)", "(?i)\.zip$") `
    -RejectedAssetPatterns @("(?i)\.sha256$", "(?i)\.sig$")

[ordered]@{
    result = "installed_or_present"
    tools = $Results
    broad_scans_enabled = $false
    external_url_crawl_enabled = $false
    report_retention_enabled = $false
} | ConvertTo-Json -Depth 5
