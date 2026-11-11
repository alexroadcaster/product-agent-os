$ErrorActionPreference = 'Stop'
# Native user interaction is explicit; pairing data arrives only on stdin, never process arguments or logs.
try {
 $inputData = [Console]::In.ReadToEnd() | ConvertFrom-Json
 $origin = [Uri]$inputData.origin
 if ($origin.Scheme -cne 'http' -or $origin.Host -cne '127.0.0.1' -or $origin.Port -lt 1 -or $origin.Port -gt 65535 -or $origin.AbsolutePath -ne '/' -or $origin.Query -or $origin.Fragment -or $origin.UserInfo) { throw 'origin' }
 Add-Type -AssemblyName PresentationFramework
 $pairing = if ($inputData.pairingCode) { "Pairing code: $($inputData.pairingCode)" } else { 'Use the pairing code shown by the original launcher.' }
 $text = "Product-Agent OS local preview`n$pairing`nRuntime: $($inputData.runtime)`nOpen the local UI?"
 $choice = [System.Windows.MessageBox]::Show($text, 'Product-Agent OS', 'OKCancel', 'Information')
 if ($choice -ne 'OK') { [Console]::Out.Write('quit'); exit 0 }
 $startInfo = New-Object System.Diagnostics.ProcessStartInfo
 $startInfo.FileName = $origin.AbsoluteUri; $startInfo.UseShellExecute = $true
 [System.Diagnostics.Process]::Start($startInfo) | Out-Null
 if ($inputData.owner -eq $true) {
  # Keep the pairing code visible while the owner explicitly controls service lifetime.
  $quitChoice = [System.Windows.MessageBox]::Show("$pairing`nOK: Quit and close local sessions.`nCancel: keep the service running; use the paired browser Quit control later.", 'Product-Agent OS - Quit', 'OKCancel', 'Information')
  if ($quitChoice -eq 'OK') { [Console]::Out.Write('quit') } else { [Console]::Out.Write('closed') }
 } else { [Console]::Out.Write('closed') }
 exit 0
} catch { exit 1 }
