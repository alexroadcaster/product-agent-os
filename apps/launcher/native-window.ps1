$ErrorActionPreference = 'Stop'
# Open the protected browser bootstrap directly. Session material never enters URL, clipboard or dialogs.
try {
 $inputData = [Console]::In.ReadToEnd() | ConvertFrom-Json
 $origin = [Uri]$inputData.origin
 if ($origin.Scheme -cne 'http' -or $origin.Host -cne '127.0.0.1' -or $origin.Port -lt 1 -or $origin.Port -gt 65535 -or $origin.AbsolutePath -ne '/' -or $origin.Query -or $origin.Fragment -or $origin.UserInfo) { throw 'origin' }
 $startInfo = New-Object System.Diagnostics.ProcessStartInfo
 $startInfo.FileName = $origin.AbsoluteUri + 'launch'; $startInfo.UseShellExecute = $true
 # An explicit owned browser profile permits native acceptance without touching the user's browser session.
 if ($inputData.browserExecutable -or $inputData.browserProfileDirectory) {
  $browser = [string]$inputData.browserExecutable; $profile = [string]$inputData.browserProfileDirectory
  if ($browser -notmatch '^[A-Za-z]:[\\/]' -or $profile -notmatch '^[A-Za-z]:[\\/]' -or $browser -match '["\r\n]' -or $profile -match '["\r\n]' -or -not [System.IO.File]::Exists($browser) -or -not [System.IO.Directory]::Exists($profile)) { throw 'browser' }
  $startInfo.FileName = $browser
  $startInfo.Arguments = '--user-data-dir="' + $profile.TrimEnd('\') + '" --no-first-run --no-default-browser-check --app=' + $origin.AbsoluteUri + 'launch'
 }
 [System.Diagnostics.Process]::Start($startInfo) | Out-Null
 [Console]::Out.Write('closed')
 exit 0
} catch { exit 1 }
