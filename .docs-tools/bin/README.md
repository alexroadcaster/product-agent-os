# Standalone Docs Binary Boundary

This folder is reserved for project-local standalone documentation-check binaries after explicit approval.

`DOC-M37` installed Vale `3.15.1` locally from GitHub Releases. The binary is
ignored from git; `vale.sha256` records the local checksum for the installed
`vale.exe`.

Planned future tools include lychee and gitleaks. Binary files and archives are
ignored by default. If a future slice needs a checked-in binary or vendored
runtime, it must record source URL, license, checksum, owner approval, rollback
and smoke evidence before the artifact is treated as usable.
