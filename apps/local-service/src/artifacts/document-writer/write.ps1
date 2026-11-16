$ErrorActionPreference = 'Stop'
[Console]::InputEncoding = [Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
# Fixed trusted helper; JSON stdin is data, never PowerShell/C# source.
Add-Type -TypeDefinition @"
using System;
using System.IO;
using System.Text;
using System.Diagnostics;
using System.Security.Cryptography;
using System.Runtime.InteropServices;
using Microsoft.Win32.SafeHandles;
public static class PaosDocumentWrite {
 [StructLayout(LayoutKind.Sequential)] public struct Info {public uint Attributes;public System.Runtime.InteropServices.ComTypes.FILETIME Creation,Access,Write;public uint Volume,SizeHigh,SizeLow,Links,IndexHigh,IndexLow;}
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] public static extern SafeFileHandle CreateFile(string name,uint access,uint share,IntPtr security,uint disposition,uint flags,IntPtr template);
 [DllImport("kernel32.dll",SetLastError=true)] public static extern bool GetFileInformationByHandle(SafeFileHandle handle,out Info info);
 [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] public static extern uint GetFinalPathNameByHandle(SafeFileHandle handle,StringBuilder path,uint length,uint flags);
 static System.Threading.Timer timer;
 public static void Watch(int parent) {var start=Stopwatch.StartNew();timer=new System.Threading.Timer(delegate(object state){try{if(start.ElapsedMilliseconds>15000||Process.GetProcessById(parent).HasExited)Environment.Exit(3);}catch{Environment.Exit(3);}},null,1000,1000);}
 public static string[] Describe(SafeFileHandle handle,bool target) {Info info;if(!GetFileInformationByHandle(handle,out info))throw new Exception();if((info.Attributes & 0x400)!=0||target&&((info.Attributes & 0x10)!=0||info.Links!=1))throw new Exception();var text=new StringBuilder(32768);uint count=GetFinalPathNameByHandle(handle,text,32768,0);if(count==0||count>=32768)throw new Exception();return new string[]{text.ToString(),info.Volume.ToString(),(((ulong)info.IndexHigh<<32)|info.IndexLow).ToString(),info.Links.ToString(),(((ulong)info.SizeHigh<<32)|info.SizeLow).ToString(),(((ulong)(uint)info.Write.dwHighDateTime<<32)|(uint)info.Write.dwLowDateTime).ToString()};}
 public static byte[] Read(FileStream stream) {if(stream.Length>524288)throw new Exception();stream.Position=0;var bytes=new byte[(int)stream.Length];int at=0,n;while(at<bytes.Length&&(n=stream.Read(bytes,at,bytes.Length-at))>0)at+=n;if(at!=bytes.Length)throw new Exception();var value=new UTF8Encoding(false,true).GetString(bytes);if(value.IndexOf('\0')>=0)throw new Exception();return bytes;}
 public static string Hash(byte[] value) {using(var sha=SHA256.Create())return BitConverter.ToString(sha.ComputeHash(value)).Replace("-","").ToLowerInvariant();}
 public static void Write(FileStream stream,byte[] bytes) {if(bytes.Length>524288)throw new Exception();new UTF8Encoding(false,true).GetString(bytes);stream.Position=0;stream.Write(bytes,0,bytes.Length);stream.SetLength(bytes.Length);stream.Flush(true);}
}
"@
$handles = [System.Collections.Generic.List[Microsoft.Win32.SafeHandles.SafeFileHandle]]::new()
$stream = $null
$ownedHome = [IO.Path]::GetFullPath([Environment]::CurrentDirectory)
try {
 $line=[Console]::ReadLine();if($null -eq $line){exit 1};$request=$line | ConvertFrom-Json
 [PaosDocumentWrite]::Watch([int]$request.parentPid)
 $pins=@();$paths=@($request.paths)
 if($paths.Count -lt 2 -or $paths.Count -gt 34){throw 'scope'}
 for($i=0;$i -lt $paths.Count;$i++) {
  $target=$i -eq $paths.Count-1
  $handle=if($target){[PaosDocumentWrite]::CreateFile([string]$paths[$i],[uint32]3221225472,0,[IntPtr]::Zero,3,0x00200000,[IntPtr]::Zero)}else{[PaosDocumentWrite]::CreateFile([string]$paths[$i],[uint32]2147483648,1,[IntPtr]::Zero,3,0x02200000,[IntPtr]::Zero)}
  if($handle.IsInvalid){$handle.Dispose();throw 'busy'}
  $handles.Add($handle);$d=[PaosDocumentWrite]::Describe($handle,$target)
  $pins+=@{path=$d[0];volume=$d[1];fileId=$d[2];links=$d[3];size=$d[4];writeTicks=$d[5]}
 }
 $stream=[IO.FileStream]::new($handles[$handles.Count-1],[IO.FileAccess]::ReadWrite)
 $before=[PaosDocumentWrite]::Read($stream);$beforeHash=[PaosDocumentWrite]::Hash($before)
 if($beforeHash -ne [string]$request.expectedHash){throw 'drift'}
 [Console]::WriteLine((@{pins=$pins;beforeHash=$beforeHash;beforeBase64=[Convert]::ToBase64String($before)} | ConvertTo-Json -Compress -Depth 5));[Console]::Out.Flush()
 $line=[Console]::ReadLine();if([string]::IsNullOrEmpty($line)){exit 0};$commit=$line | ConvertFrom-Json
 if($commit.action -ne 'commit' -or $commit.expectedHash -ne $beforeHash -or [PaosDocumentWrite]::Hash([PaosDocumentWrite]::Read($stream)) -ne $beforeHash){throw 'commit'}
 $after=[Convert]::FromBase64String([string]$commit.afterBase64);$afterHash=[PaosDocumentWrite]::Hash($after)
 if($afterHash -ne $commit.afterHash){throw 'hash'}
 [PaosDocumentWrite]::Write($stream,$after)
 if([PaosDocumentWrite]::Hash([PaosDocumentWrite]::Read($stream)) -ne $afterHash){throw 'flush'}
 [Console]::WriteLine((@{beforeHash=$beforeHash;afterHash=$afterHash} | ConvertTo-Json -Compress));[Console]::Out.Flush()
} catch {[Console]::WriteLine('{"error":"DOCUMENT_NATIVE_FAILED"}');[Console]::Out.Flush();exit 1}
finally {
 if($null -ne $stream){$stream.Dispose()};foreach($handle in $handles){$handle.Dispose()}
 # EOF after parent death also removes only this empty private scratch directory.
 # No recursive deletion is performed by the helper.
 if([IO.Path]::GetFileName($ownedHome).StartsWith('paos-document-write-') -and $ownedHome -eq $env:HOME){
  try {$parentHome=[IO.Directory]::GetParent($ownedHome).FullName;Set-Location -LiteralPath $parentHome;[Environment]::CurrentDirectory=$parentHome;[IO.Directory]::Delete($ownedHome)} catch {}
 }
}
