param([string]$Candidate)
$ErrorActionPreference='Stop'
. $Candidate
if (-not (Test-Within 'tree/x' 'tree') -or -not (Test-Within 'tree' 'tree') -or (Test-Within 'tree2/x' 'tree') -or (Test-Within 'Tree/x' 'tree')) { throw 'path boundary regression' }
