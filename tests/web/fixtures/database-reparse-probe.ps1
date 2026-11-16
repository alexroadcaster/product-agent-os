$ErrorActionPreference='Stop'
Add-Type -TypeDefinition @"
using System;
using System.Text;
using System.Runtime.InteropServices;
using Microsoft.Win32.SafeHandles;
public static class SyntheticReparseProbe {
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] static extern SafeFileHandle CreateFile(string name,uint access,uint share,IntPtr security,uint disposition,uint flags,IntPtr template);
 [DllImport("kernel32.dll",SetLastError=true)] static extern bool DeviceIoControl(SafeFileHandle file,uint code,byte[] input,uint size,IntPtr output,uint outputSize,out uint written,IntPtr overlap);
 public static string SetJunction(string path,string target){
  using(var handle=CreateFile(path,0x40000000,7,IntPtr.Zero,3,0x02200000,IntPtr.Zero)){
   if(handle.IsInvalid)return "OPEN_DENIED:"+Marshal.GetLastWin32Error();
   var sub=Encoding.Unicode.GetBytes(@"\??\"+target);var print=Encoding.Unicode.GetBytes(target);var buffer=new byte[20+sub.Length+print.Length];
   Array.Copy(BitConverter.GetBytes(0xA0000003u),0,buffer,0,4);Array.Copy(BitConverter.GetBytes((ushort)(buffer.Length-8)),0,buffer,4,2);
   Array.Copy(BitConverter.GetBytes((ushort)sub.Length),0,buffer,10,2);Array.Copy(BitConverter.GetBytes((ushort)(sub.Length+2)),0,buffer,12,2);Array.Copy(BitConverter.GetBytes((ushort)print.Length),0,buffer,14,2);
   Array.Copy(sub,0,buffer,16,sub.Length);Array.Copy(print,0,buffer,18+sub.Length,print.Length);uint written;
   return DeviceIoControl(handle,0x000900A4,buffer,(uint)buffer.Length,IntPtr.Zero,0,out written,IntPtr.Zero)?"REPARSE_SET":"REPARSE_FAILED:"+Marshal.GetLastWin32Error();
  }
 }
}
"@
$job=[Console]::ReadLine() | ConvertFrom-Json
[Console]::WriteLine([SyntheticReparseProbe]::SetJunction([string]$job.path,[string]$job.target))
