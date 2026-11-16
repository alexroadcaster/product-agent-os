$ErrorActionPreference = 'Stop'
# Trusted fixed helper. The first stdin line contains paths; EOF or a second line releases all handles.
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
using System.Text;
using Microsoft.Win32.SafeHandles;
public static class PaosDatabaseLease {
 [StructLayout(LayoutKind.Sequential)] public struct Info {public uint Attributes;public System.Runtime.InteropServices.ComTypes.FILETIME Creation,Access,Write;public uint Volume,SizeHigh,SizeLow,Links,IndexHigh,IndexLow;}
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] public static extern SafeFileHandle CreateFile(string name,uint access,uint share,IntPtr security,uint disposition,uint flags,IntPtr template);
 [DllImport("kernel32.dll",SetLastError=true)] public static extern bool GetFileInformationByHandle(SafeFileHandle handle,out Info info);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] public static extern uint GetFinalPathNameByHandle(SafeFileHandle handle,StringBuilder path,uint length,uint flags);
 public static string[] Describe(SafeFileHandle handle) {Info info;if(!GetFileInformationByHandle(handle,out info))throw new Exception("DATABASE_LEASE_IDENTITY");if((info.Attributes & 0x400)!=0)throw new Exception("DATABASE_LEASE_REPARSE");var text=new StringBuilder(32768);uint count=GetFinalPathNameByHandle(handle,text,32768,0);if(count==0||count>=32768)throw new Exception("DATABASE_LEASE_PATH");return new string[]{text.ToString(),info.Volume.ToString(),(((ulong)info.IndexHigh<<32)|info.IndexLow).ToString(),info.Links.ToString()};}
}
"@
$handles = [System.Collections.Generic.List[Microsoft.Win32.SafeHandles.SafeFileHandle]]::new()
try {
 $inputLine=[Console]::ReadLine();if($null -eq $inputLine){exit 1};$request=$inputLine | ConvertFrom-Json
 $pins=@()
 foreach($path in $request.paths) {
  $handle=[PaosDatabaseLease]::CreateFile([string]$path,[uint32]2147483648,1,[IntPtr]::Zero,3,0x02200000,[IntPtr]::Zero)
  if($handle.IsInvalid){$handle.Dispose();throw 'DATABASE_LEASE_BUSY'}
  $handles.Add($handle);$description=[PaosDatabaseLease]::Describe($handle)
  $pins+=@{path=$description[0];volume=$description[1];fileId=$description[2];links=$description[3]}
 }
 [Console]::WriteLine((@{pins=$pins} | ConvertTo-Json -Compress -Depth 4));[Console]::Out.Flush()
 [void][Console]::ReadLine()
} catch {[Console]::WriteLine('{"error":"DATABASE_LEASE_DENIED"}');[Console]::Out.Flush();exit 1}
finally {foreach($handle in $handles){$handle.Dispose()}}
