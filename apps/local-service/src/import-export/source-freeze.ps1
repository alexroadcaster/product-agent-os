$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
Set-StrictMode -Version Latest
$stream = $null
$hasher = $null
$exitCode = 1
try {
    $line = [Console]::In.ReadLine()
    if ($null -eq $line -or $line.Length -gt 32768) { throw 'Invalid request' }
    $request = ConvertFrom-Json -InputObject $line
    if (@($request.PSObject.Properties).Count -ne 2 -or $request.workspaceRoot -isnot [string] -or $request.sourcePath -isnot [string]) {
        throw 'Invalid request'
    }
    $root = [IO.Path]::GetFullPath($request.workspaceRoot)
    $source = [IO.Path]::GetFullPath($request.sourcePath)
    if ($root -notmatch '^[A-Za-z]:\\' -or $source -notmatch '^[A-Za-z]:\\') { throw 'Local drive required' }
    $rootPrefix = $root.TrimEnd([IO.Path]::DirectorySeparatorChar) + [IO.Path]::DirectorySeparatorChar
    if (-not $source.StartsWith($rootPrefix, [StringComparison]::OrdinalIgnoreCase)) { throw 'Source outside root' }
    $current = $root
    if (([IO.File]::GetAttributes($current) -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'Linked root' }
    foreach ($part in $source.Substring($rootPrefix.Length).Split([IO.Path]::DirectorySeparatorChar)) {
        $current = [IO.Path]::Combine($current, $part)
        if (([IO.File]::GetAttributes($current) -band [IO.FileAttributes]::ReparsePoint) -ne 0) { throw 'Linked ancestor' }
    }
    $null = Add-Type -TypeDefinition @'
using System;
using System.ComponentModel;
using System.Runtime.InteropServices;
using System.Text;
using Microsoft.Win32.SafeHandles;
public static class PaosFrozenSourceNative {
    [StructLayout(LayoutKind.Sequential)]
    public struct FileInformation {
        public uint Attributes;
        public System.Runtime.InteropServices.ComTypes.FILETIME CreationTime;
        public System.Runtime.InteropServices.ComTypes.FILETIME LastAccessTime;
        public System.Runtime.InteropServices.ComTypes.FILETIME LastWriteTime;
        public uint VolumeSerialNumber;
        public uint FileSizeHigh;
        public uint FileSizeLow;
        public uint NumberOfLinks;
        public uint FileIndexHigh;
        public uint FileIndexLow;
    }
    [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    public static extern uint GetFinalPathNameByHandleW(SafeFileHandle handle, StringBuilder path, uint size, uint flags);
    [DllImport("kernel32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    public static extern bool GetFileInformationByHandle(SafeFileHandle handle, out FileInformation information);
    public static string FinalPath(SafeFileHandle handle) {
        var path = new StringBuilder(1024);
        uint length = GetFinalPathNameByHandleW(handle, path, (uint)path.Capacity, 0);
        if (length >= path.Capacity && length < 32768) {
            path = new StringBuilder((int)length + 1);
            length = GetFinalPathNameByHandleW(handle, path, (uint)path.Capacity, 0);
        }
        if (length == 0 || length >= path.Capacity) throw new Win32Exception();
        return path.ToString();
    }
    public static void Verify(SafeFileHandle handle) {
        FileInformation information;
        if (!GetFileInformationByHandle(handle, out information)) throw new Win32Exception();
        if (information.NumberOfLinks != 1 || (information.Attributes & (0x10u | 0x400u)) != 0)
            throw new InvalidOperationException();
    }
}
'@
    # FileShare.Read denies concurrent writer and delete/rename handles for this source.
    $stream = [IO.FileStream]::new($source, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::Read)
    [PaosFrozenSourceNative]::Verify($stream.SafeFileHandle)
    $finalPath = [PaosFrozenSourceNative]::FinalPath($stream.SafeFileHandle)
    if ($finalPath.StartsWith('\\?\')) { $finalPath = $finalPath.Substring(4) }
    if (-not $finalPath.Equals($source, [StringComparison]::OrdinalIgnoreCase) -or
        -not $finalPath.StartsWith($rootPrefix, [StringComparison]::OrdinalIgnoreCase)) { throw 'Changed source identity' }
    if ($stream.Length -gt 1048576) { throw 'Source too large' }
    $hasher = [Security.Cryptography.SHA256]::Create()
    $hash = [BitConverter]::ToString($hasher.ComputeHash($stream)).Replace('-', '').ToLowerInvariant()
    $observation = @{ sha256 = $hash; byteSize = $stream.Length } | ConvertTo-Json -Compress
    [Console]::Out.WriteLine($observation)
    [Console]::Out.Flush()
    $release = [Console]::In.ReadLineAsync()
    if (-not $release.Wait(30000) -or $release.Result -cne 'release') { throw 'Release required' }
    $exitCode = 0
} catch {
    # Paths, source content and exception text never enter stdout, stderr or logs.
    $exitCode = 1
} finally {
    if ($null -ne $hasher) { $hasher.Dispose() }
    if ($null -ne $stream) { $stream.Dispose() }
}
exit $exitCode
