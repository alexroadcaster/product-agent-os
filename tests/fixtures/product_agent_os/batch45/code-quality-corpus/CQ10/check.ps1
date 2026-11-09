param([string]$Candidate)
$ErrorActionPreference='Stop'
. $Candidate
if ((Get-Enabled $false) -ne $false -or (Get-Enabled $null) -ne $true) { throw 'boolean default regression' }
