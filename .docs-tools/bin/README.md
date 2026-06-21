# Standalone Docs Binary Boundary

This folder is reserved for project-local standalone documentation-check binaries after explicit approval.

`DOC-M37` installed Vale `3.15.1` locally from GitHub Releases. The binary is
ignored from git; `vale.sha256` records the local checksum for the installed
`vale.exe`.

`DOC-M38` installed lychee `0.24.2` and gitleaks `8.30.0` locally from GitHub
Releases. The binaries are ignored from git; `lychee.sha256` and
`gitleaks.sha256` record the local checksums.

Binary files and archives are ignored by default. If a future slice needs a
checked-in binary or vendored runtime, it must record source URL, license,
checksum, owner approval, rollback and smoke evidence before the artifact is
treated as usable.
