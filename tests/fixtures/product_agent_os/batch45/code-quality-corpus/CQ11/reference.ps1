function Test-Within($Path,$Root) { return ($Path -ceq $Root) -or $Path.StartsWith($Root + '/', [System.StringComparison]::Ordinal) }
