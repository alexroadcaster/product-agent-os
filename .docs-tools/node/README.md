# Node Docs Tooling Boundary

This folder is reserved for project-local Node documentation tools.

Allowed checked-in files are `package.json`, `package-lock.json` and small
config files after the corresponding G1.1 slice is approved.

`node_modules/`, npm caches and generated outputs are local-only and ignored.

Installed DOC-M36 tools:

- `markdownlint-cli2`
- Prettier
- Redocly CLI

Redocly remains `not_applicable` until an OpenAPI source contract exists.

Use `tools/docs_node_install.ps1` from the repository root. Without `-Install`,
the helper prints the plan and does not install packages.
