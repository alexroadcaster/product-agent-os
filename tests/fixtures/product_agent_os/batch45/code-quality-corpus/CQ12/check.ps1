param([string]$Candidate)
$ErrorActionPreference='Stop'
. $Candidate
if ((Join-Words @('one','two')) -cne 'one two' -or (Join-Words @()) -cne '') { throw 'join regression' }
