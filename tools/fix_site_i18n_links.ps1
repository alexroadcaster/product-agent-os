param(
    [string]$SiteDir = "site"
)

$resolved = Resolve-Path -LiteralPath $SiteDir
$siteRoot = $resolved.Path.TrimEnd("\")
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$changed = 0

Get-ChildItem -LiteralPath $siteRoot -Recurse -Filter "*.html" | ForEach-Object {
    $fullPath = $_.FullName
    $relative = $fullPath.Substring($siteRoot.Length).TrimStart("\", "/").Replace("\", "/")
    $depth = [Math]::Max(($relative.Split("/").Count - 1), 0)
    $prefix = if ($depth -gt 0) { "../" * $depth } else { "" }

    $text = [System.IO.File]::ReadAllText($fullPath, [System.Text.Encoding]::UTF8)
    $updated = [System.Text.RegularExpressions.Regex]::Replace(
        $text,
        'href="(?:\.\./)*en/index\.html"',
        'href="' + $prefix + 'en/index.html"'
    )
    $updated = $updated.Replace('href="/en/"', 'href="' + $prefix + 'en/index.html"')
    $updated = $updated.Replace('href="/"', 'href="' + $prefix + 'index.html"')
    $updated = [System.Text.RegularExpressions.Regex]::Replace(
        $updated,
        '[ \t]+(\r?\n)',
        '$1'
    )
    $updated = [System.Text.RegularExpressions.Regex]::Replace($updated, '[ \t]+\z', '')

    if ($updated -ne $text) {
        [System.IO.File]::WriteAllText($fullPath, $updated, $utf8NoBom)
        $script:changed += 1
    }
}

Get-ChildItem -LiteralPath $siteRoot -Recurse -Filter "*.js" | ForEach-Object {
    $fullPath = $_.FullName
    $text = [System.IO.File]::ReadAllText($fullPath, [System.Text.Encoding]::UTF8)
    $updated = [System.Text.RegularExpressions.Regex]::Replace(
        $text,
        '[ \t]+(\r?\n)',
        '$1'
    )
    $updated = [System.Text.RegularExpressions.Regex]::Replace($updated, '[ \t]+\z', '')

    if ($updated -ne $text) {
        [System.IO.File]::WriteAllText($fullPath, $updated, $utf8NoBom)
        $script:changed += 1
    }
}

Write-Output "updated_files=$changed"
