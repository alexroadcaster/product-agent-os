param([Parameter(Mandatory=$true)][int]$OwnerPid)
$ErrorActionPreference = 'Stop'
# Inspect only our CLI's native-window child; never read the dialog body or pairing code.
Add-Type -TypeDefinition @'
using System;
using System.Text;
using System.Runtime.InteropServices;
public class PaosOwnedDialog {
 public delegate bool Callback(IntPtr h,IntPtr p);
 [DllImport("user32.dll")] public static extern bool EnumWindows(Callback callback,IntPtr data);
 [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h,out uint pid);
 [DllImport("user32.dll",CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h,StringBuilder text,int length);
 [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr h,uint message,IntPtr value,IntPtr data);
 public static bool Cancel(uint pid) {
  bool found=false;
  EnumWindows((h,p)=>{uint owner;GetWindowThreadProcessId(h,out owner);if(owner!=pid)return true;
   var title=new StringBuilder(80);GetWindowText(h,title,80);
   if(title.ToString()=="Product-Agent OS"){found=PostMessage(h,0x111,new IntPtr(2),IntPtr.Zero);return false;}return true;},IntPtr.Zero);
  return found;
 }
}
'@
$deadline=[DateTime]::UtcNow.AddSeconds(35)
while([DateTime]::UtcNow -lt $deadline){
 $children=Get-CimInstance Win32_Process -Filter "ParentProcessId = $OwnerPid" | Where-Object { $_.Name -eq 'powershell.exe' -and $_.CommandLine -like '*native-window.ps1*' }
 foreach($child in $children){if([PaosOwnedDialog]::Cancel([uint32]$child.ProcessId)){ @{windowObserved=$true;cancelRequested=$true;pairingRead=$false;target='owned_native_child'} | ConvertTo-Json -Compress;exit 0}}
 Start-Sleep -Milliseconds 100
}
throw 'OWNED_NATIVE_DIALOG_NOT_OBSERVED'
