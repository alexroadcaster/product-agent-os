# Filesystem and root identity

Source status: repository_source / static_source_review; 2026-11-15.

Owner: security/runtime owner + docs-maintainer. Scope: PAOS source at `259977f3b257ba7fc0e932396f8963262bd327ad`; update with guards, tests or policy changes. Linked tests are verification routes, not a new run. No real profiles, credentials or provider calls were examined.

## Registration and reads

[project-sources](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/adapters/project-sources.ts) accepts a local absolute path and binds the canonical root to directory identity (device/inode); before reading fixed control-plane files it rechecks the binding, regular file, absence of symbolic and hard links, 1 MiB limit, open handle identity, and changes during the read. The digest represents raw bytes while displayed text can be redacted. This is a bounded reader, not a complete project explorer.

[app-agent-files](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/runtime/app-agent-files.mts) observes pinned task files only: at most 32 files, 64 KiB each and 512 KiB total. It excludes private paths, links and binary/private-key content, checks path and handle and rebinds the root; the diff is bounded and redacted. Failure or excluded means no permitted observation, not proof that nothing changed.

[profile identity](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/apps/local-service/src/connections/profile-identity.mts) separately checks profile directory identity and credential-store namespace. Admission checking is not an atomic filesystem lock. Changes require [project source tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/project-sources.test.mts), [file tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/app-agent-files.test.mts), [profile tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/web/profile-identity.test.mts), and the relevant user-surface check; these links do not mean those tests ran now. No real project was scanned here; the full file directory and future integrations are planned, not established by this reader.
