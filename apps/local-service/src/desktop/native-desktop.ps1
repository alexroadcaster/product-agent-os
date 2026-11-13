$ErrorActionPreference = 'Stop'
[Console]::InputEncoding = New-Object System.Text.UTF8Encoding($false)
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
try {
 $inputData = [Console]::In.ReadToEnd() | ConvertFrom-Json
 if ($inputData.action -eq 'codex') {
  $uri = [Uri]$inputData.url
  if ($uri.Scheme -cne 'codex' -or $uri.Host -cne 'new' -or $uri.UserInfo -or $uri.Fragment -or $uri.AbsoluteUri.Length -gt 24000) { throw 'uri' }
  $start = New-Object System.Diagnostics.ProcessStartInfo
  $start.FileName = $uri.AbsoluteUri; $start.UseShellExecute = $true
  [System.Diagnostics.Process]::Start($start) | Out-Null
  [Console]::Out.Write('{"opened":true}'); exit 0
 }
 if ($inputData.action -ne 'folder') { throw 'action' }
 # IFileOpenDialog is the modern Explorer folder picker; the user can create a folder in its toolbar.
 Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class PaosProjectFolder {
 [ComImport, Guid("DC1C5A9C-E88A-4DDE-A5A1-60F82A20AEF7")] class FileOpenDialog {}
 [ComImport, Guid("D57C7288-D4AD-4768-BE02-9D969532D960"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
 interface IFileOpenDialog {
  [PreserveSig] int Show(IntPtr owner);
  void SetFileTypes(uint count,IntPtr specs);void SetFileTypeIndex(uint index);void GetFileTypeIndex(out uint index);
  void Advise(IntPtr events,out uint cookie);void Unadvise(uint cookie);void SetOptions(uint options);void GetOptions(out uint options);
  void SetDefaultFolder(IShellItem item);void SetFolder(IShellItem item);void GetFolder(out IShellItem item);void GetCurrentSelection(out IShellItem item);
  void SetFileName([MarshalAs(UnmanagedType.LPWStr)] string name);void GetFileName(out IntPtr name);
  void SetTitle([MarshalAs(UnmanagedType.LPWStr)] string title);void SetOkButtonLabel([MarshalAs(UnmanagedType.LPWStr)] string label);
  void SetFileNameLabel([MarshalAs(UnmanagedType.LPWStr)] string label);void GetResult(out IShellItem item);
 }
 [ComImport, Guid("43826D1E-E718-42EE-BC55-A1E261C37BFE"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
 interface IShellItem {
  void BindToHandler(IntPtr context,ref Guid handler,ref Guid iid,out IntPtr result);void GetParent(out IShellItem parent);
  void GetDisplayName(uint type,out IntPtr name);void GetAttributes(uint mask,out uint attributes);void Compare(IShellItem other,uint hint,out int order);
 }
 [DllImport("shell32.dll",CharSet=CharSet.Unicode,PreserveSig=false)]
 static extern void SHCreateItemFromParsingName(string path,IntPtr context,ref Guid iid,[MarshalAs(UnmanagedType.Interface)] out IShellItem item);
 public static string Choose(string title,string initialDirectory) {
  var dialog=(IFileOpenDialog)new FileOpenDialog();
  try {
   uint options;dialog.GetOptions(out options);
   // PICKFOLDERS | FORCEFILESYSTEM | PATHMUSTEXIST | NOCHANGEDIR | DONTADDTORECENT.
   dialog.SetOptions(options|0x20u|0x40u|0x800u|0x8u|0x2000000u);dialog.SetTitle(title);
   if(!String.IsNullOrEmpty(initialDirectory)){IShellItem initial;Guid iid=new Guid("43826D1E-E718-42EE-BC55-A1E261C37BFE");SHCreateItemFromParsingName(initialDirectory,IntPtr.Zero,ref iid,out initial);try{dialog.SetFolder(initial);}finally{Marshal.ReleaseComObject(initial);}}
   int hr=dialog.Show(IntPtr.Zero);if(hr==unchecked((int)0x800704C7))return null;if(hr<0)Marshal.ThrowExceptionForHR(hr);
   IShellItem item;dialog.GetResult(out item);
   try {IntPtr path;item.GetDisplayName(0x80058000u,out path);try{return Marshal.PtrToStringUni(path);}finally{Marshal.FreeCoTaskMem(path);}}
   finally {Marshal.ReleaseComObject(item);}
  } finally {Marshal.ReleaseComObject(dialog);}
 }
}
'@
 $selected = [PaosProjectFolder]::Choose([string]$inputData.title,[string]$inputData.initialDirectory)
 if ($null -eq $selected) { [Console]::Out.Write('{"cancelled":true}') }
 else { [Console]::Out.Write((@{cancelled=$false;workspaceRoot=$selected} | ConvertTo-Json -Compress)) }
 exit 0
} catch { exit 1 }
