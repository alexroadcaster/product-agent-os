# Desktop Local-First

Project: {project_name}
Profile: {profile_name}

## Inputs

- User goal:
- Desktop platform assumptions:
- Target OS scope:
- Filesystem permissions:
- Local data:
- Local DB:
- Indexing:
- Background jobs:
- Platform-native/local-helper option:
- Privacy:
- Build command:
- App logs:
- Screenshots:
- Recovery path:
- Rollback:
- Runtime evidence:
- Manual OS gap:
- Approval boundary:

## Process

1. Keep the workflow read-only until desktop platform assumptions, filesystem permissions, local data, build command, runtime log check, recovery path, rollback, and approval boundary are explicit.
2. Inventory desktop runtime files, package metadata, Electron/Tauri/native shell files, local DB files, storage locations, filesystem access points, background jobs, indexing paths, app logs, screenshots, and recovery docs.
3. Define acceptance scenarios before implementation: first run, restart, offline use, local data read/write, local DB migration, filesystem permission denied, background indexing, app crash/recovery, and rollback where applicable.
4. Record filesystem permissions, local data, local DB, indexing, background jobs, privacy, app logs, screenshots, and recovery path as `present_unverified` until desktop build/run evidence, app log evidence, screenshot evidence, or owner review confirms behavior.
5. Select verification from detected project files only: Electron command, Tauri command, native desktop build command, OS-specific run command, app logs, screenshots, local DB check, or manual OS check.
6. Prefer platform-native APIs, existing desktop framework primitives, current local storage helpers, and OS permission patterns before custom filesystem, background-job, indexing, or local-DB code.
7. Capture runtime evidence with command, exit code, OS version, app logs, screenshots, local data path, local DB state, recovery path result, rollback result, and manual OS gap when the local environment cannot run the app.
8. Do not claim desktop runtime behavior, do not claim filesystem behavior, and do not claim local data recovery from code inspection only.
9. Do not change filesystem access, local data retention, local DB migration, background autostart, telemetry, privacy-impacting storage, or destructive cleanup without explicit approval.
10. Do not package, sign, notarize, publish, or update desktop distribution metadata without explicit approval.

## Outputs

- Desktop local-first plan:
- Desktop platform assumptions:
- Target OS scope:
- Filesystem permissions:
- Local data:
- Local DB:
- Indexing:
- Background jobs:
- Platform-native/local-helper leverage decision:
- Privacy:
- Acceptance scenarios:
- Build command:
- App logs:
- Screenshots:
- Runtime log check:
- Runtime evidence:
- Recovery path:
- Rollback:
- Manual OS gap:
- Approval requirements:
- Residual risk:

## Verification

- Desktop platform assumptions include the target OS or name the unknown OS gap.
- Filesystem permissions, local data, local DB, privacy impact, background jobs, and indexing are explicit or marked `applicable_missing`.
- Build command is derived from detected project files or marked unavailable with reason.
- Runtime log check, app logs, screenshots, local data path, local DB state, recovery path, rollback, and manual OS gap are named before behavior claims.
- Runtime evidence records command, exit code, OS version, app logs, screenshots, local storage evidence, recovery evidence, rollback evidence, and residual risk.
- Custom desktop filesystem, indexing, background job, or local DB code records platform-native/current-helper alternatives and privacy impact.
- Filesystem access changes, local data deletion, privacy-impacting storage, background autostart, packaging, signing, notarization, publish, and external distribution operations remain blocked until explicit approval.

## Stop Conditions

- Desktop platform target is unknown.
- Build command is unknown for a runtime-affecting change.
- Filesystem permissions, local DB, local data deletion, privacy-impacting storage, or background autostart change lacks approval.
- Desktop runtime behavior, filesystem behavior, local data recovery, or rollback is requested as complete without current runtime evidence.
- Custom local storage, indexing, filesystem, background job, or local DB code is proposed before platform-native/framework/current-helper options are evaluated.
- App logs or screenshots are unavailable and no manual OS gap is recorded.
- The request asks to package, sign, notarize, publish, or mutate external distribution metadata without explicit approval.
