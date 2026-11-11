$ErrorActionPreference = 'Stop'
# Current-user Credential Manager; no registry, policy, profile, or filesystem persistence.
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class PaosCredentials {
 [StructLayout(LayoutKind.Sequential, CharSet=CharSet.Unicode)]
 public struct Credential {
  public UInt32 Flags; public UInt32 Type; public string TargetName; public string Comment;
  public System.Runtime.InteropServices.ComTypes.FILETIME LastWritten;
  public UInt32 CredentialBlobSize; public IntPtr CredentialBlob; public UInt32 Persist;
  public UInt32 AttributeCount; public IntPtr Attributes; public string TargetAlias; public string UserName;
 }
 [DllImport("advapi32.dll", EntryPoint="CredWriteW", CharSet=CharSet.Unicode, SetLastError=true)]
 public static extern bool Write(ref Credential credential, UInt32 flags);
 [DllImport("advapi32.dll", EntryPoint="CredReadW", CharSet=CharSet.Unicode, SetLastError=true)]
 public static extern bool Read(string target, UInt32 type, UInt32 flags, out IntPtr credential);
 [DllImport("advapi32.dll", EntryPoint="CredDeleteW", CharSet=CharSet.Unicode, SetLastError=true)]
 public static extern bool Delete(string target, UInt32 type, UInt32 flags);
 [DllImport("advapi32.dll")] public static extern void CredFree(IntPtr value);
}
"@
try {
 $request = [Console]::In.ReadToEnd() | ConvertFrom-Json
 if ($request.target -cnotmatch '^PAOS/[A-Za-z0-9_-]{1,100}/[A-Za-z0-9_-]{1,100}$') { throw 'target' }
 $result = @{ok=$true}
 switch ($request.operation) {
  'write' {
   $bytes = [System.Text.Encoding]::UTF8.GetBytes([string]$request.secret)
   if ($bytes.Length -eq 0 -or $bytes.Length -gt 2560) { throw 'size' }
   $pointer = [Runtime.InteropServices.Marshal]::AllocHGlobal($bytes.Length)
   try {
    [Runtime.InteropServices.Marshal]::Copy($bytes, 0, $pointer, $bytes.Length)
    $credential = New-Object PaosCredentials+Credential
    $credential.Type = 1; $credential.TargetName = $request.target
    $credential.CredentialBlobSize = $bytes.Length; $credential.CredentialBlob = $pointer
    $credential.Persist = 2; $credential.UserName = 'PAOS'
    if (-not [PaosCredentials]::Write([ref]$credential, 0)) { throw 'write' }
   } finally {
    for ($index = 0; $index -lt $bytes.Length; $index++) { [Runtime.InteropServices.Marshal]::WriteByte($pointer, $index, 0) }
    [Runtime.InteropServices.Marshal]::FreeHGlobal($pointer); [Array]::Clear($bytes, 0, $bytes.Length)
   }
  }
  'read' {
   $pointer = [IntPtr]::Zero
   if ([PaosCredentials]::Read($request.target, 1, 0, [ref]$pointer)) {
    try {
     $credential = [Runtime.InteropServices.Marshal]::PtrToStructure($pointer, [type][PaosCredentials+Credential])
     if ($credential.CredentialBlobSize -gt 2560) { throw 'size' }
     $bytes = New-Object byte[] $credential.CredentialBlobSize
     [Runtime.InteropServices.Marshal]::Copy($credential.CredentialBlob, $bytes, 0, $bytes.Length)
     $result.secret = [Text.Encoding]::UTF8.GetString($bytes)
     [Array]::Clear($bytes, 0, $bytes.Length)
    } finally { [PaosCredentials]::CredFree($pointer) }
   } elseif ([Runtime.InteropServices.Marshal]::GetLastWin32Error() -ne 1168) { throw 'read' }
  }
  'delete' {
   if (-not [PaosCredentials]::Delete($request.target, 1, 0) -and [Runtime.InteropServices.Marshal]::GetLastWin32Error() -ne 1168) { throw 'delete' }
  }
  default { throw 'operation' }
 }
 [Console]::Out.Write(($result | ConvertTo-Json -Compress)); exit 0
} catch { [Console]::Out.Write('{"ok":false}'); exit 1 }
