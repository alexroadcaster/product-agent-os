param(
    [switch]$AllowNetworkAudit,
    [ValidateSet("low", "moderate", "high", "critical")]
    [string]$AuditLevel = "high",
    [switch]$WriteReport
)

$ErrorActionPreference = "Stop"

$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptPath "..")
$PythonExe = Join-Path $RepoRoot ".venv-docs\Scripts\python.exe"
$NodeRoot = Join-Path $RepoRoot ".docs-tools\node"
$ReportsRoot = Join-Path $RepoRoot ".docs-tools\reports"

function Invoke-JsonCommand {
    param(
        [Parameter(Mandatory = $true)]
        [scriptblock]$Command
    )

    $raw = & $Command | Out-String
    return $raw | ConvertFrom-Json
}

function Test-RecordedHash {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$ChecksumPath
    )

    $actual = (Get-FileHash $Path -Algorithm SHA256).Hash.ToLowerInvariant()
    $recorded = (Get-Content $ChecksumPath -Raw).Trim().Split(" ")[0].ToLowerInvariant()
    return [ordered]@{
        path = Resolve-Path -Relative $Path
        checksum_path = Resolve-Path -Relative $ChecksumPath
        sha256 = $actual
        matches_recorded = ($actual -eq $recorded)
    }
}

if (-not (Test-Path $PythonExe)) {
    throw "Missing docs Python runtime at $PythonExe"
}

if (-not (Test-Path (Join-Path $NodeRoot "package.json"))) {
    throw "Missing Node docs tooling package.json at $NodeRoot"
}

$previousEncoding = $env:PYTHONIOENCODING
$env:PYTHONIOENCODING = "utf-8"
try {
    $pipList = Invoke-JsonCommand { & $PythonExe -m pip list --format=json }
    $pipInspect = Invoke-JsonCommand { & $PythonExe -m pip inspect --local }
}
finally {
    $env:PYTHONIOENCODING = $previousEncoding
}

$pipCheckOutput = & $PythonExe -m pip check | Out-String
$pipCheckExitCode = $LASTEXITCODE

$nodeLs = Invoke-JsonCommand { & npm.cmd --prefix $NodeRoot ls --depth=0 --json }
$nodeSbom = Invoke-JsonCommand { & npm.cmd --prefix $NodeRoot sbom --json --sbom-format=cyclonedx }

$npmAudit = [ordered]@{
    status = "skipped_approval_required"
    audit_level = $AuditLevel
    vulnerabilities = $null
    command = "npm.cmd --prefix .docs-tools\node audit --audit-level=$AuditLevel --json"
}

if ($AllowNetworkAudit) {
    $auditRaw = & npm.cmd --prefix $NodeRoot audit "--audit-level=$AuditLevel" --json | Out-String
    $audit = $auditRaw | ConvertFrom-Json
    $npmAudit = [ordered]@{
        status = "ran_network_audit"
        audit_level = $AuditLevel
        exit_code = $LASTEXITCODE
        vulnerabilities = $audit.metadata.vulnerabilities
        command = "npm.cmd --prefix .docs-tools\node audit --audit-level=$AuditLevel --json"
    }
}

$hashChecks = @(
    Test-RecordedHash `
        -Path (Join-Path $RepoRoot ".docs-tools\bin\vale.exe") `
        -ChecksumPath (Join-Path $RepoRoot ".docs-tools\bin\vale.sha256")
    Test-RecordedHash `
        -Path (Join-Path $RepoRoot ".docs-tools\bin\lychee.exe") `
        -ChecksumPath (Join-Path $RepoRoot ".docs-tools\bin\lychee.sha256")
    Test-RecordedHash `
        -Path (Join-Path $RepoRoot ".docs-tools\bin\gitleaks.exe") `
        -ChecksumPath (Join-Path $RepoRoot ".docs-tools\bin\gitleaks.sha256")
    Test-RecordedHash `
        -Path (Join-Path $RepoRoot "docs\assets\javascripts\vendor\mermaid-10.9.6.min.js") `
        -ChecksumPath (Join-Path $RepoRoot "docs\assets\javascripts\vendor\mermaid-10.9.6.min.js.sha256")
)

$report = [ordered]@{
    schema_version = "docs_dependency_audit_helper_v1"
    generated_by = "tools/docs_dependency_audit.ps1"
    python = [ordered]@{
        package_count = $pipList.Count
        requested_packages = @(
            $pipInspect.installed |
                Where-Object { $_.requested } |
                ForEach-Object {
                    [ordered]@{
                        name = $_.metadata.name
                        version = $_.metadata.version
                    }
                }
        )
        pip_check = [ordered]@{
            exit_code = $pipCheckExitCode
            output = $pipCheckOutput.Trim()
        }
        pip_audit_status = "not_installed_approval_required"
    }
    node = [ordered]@{
        direct_dependencies = $nodeLs.dependencies.PSObject.Properties.Name
        sbom = [ordered]@{
            format = $nodeSbom.bomFormat
            spec_version = $nodeSbom.specVersion
            component_count = $nodeSbom.components.Count
            dependency_entries = $nodeSbom.dependencies.Count
            tool = $nodeSbom.metadata.tools[0]
        }
        npm_audit = $npmAudit
    }
    binary_and_vendor_hashes = $hashChecks
    unsupported_claims = @(
        "Python vulnerability audit clean",
        "complete repository SBOM",
        "standalone binary SBOM",
        "Mermaid vulnerability audit",
        "dependency remediation performed",
        "legal or compliance approval",
        "release readiness"
    )
}

if ($WriteReport) {
    New-Item -ItemType Directory -Path $ReportsRoot -Force | Out-Null
    $ReportPath = Join-Path $ReportsRoot "doc-m40-dependency-audit-helper-summary.json"
    $report | ConvertTo-Json -Depth 10 | Set-Content -Path $ReportPath -Encoding UTF8
    Write-Output "Wrote report: $ReportPath"
}

$report | ConvertTo-Json -Depth 10
