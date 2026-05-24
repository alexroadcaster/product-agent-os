# Native Mobile Feature

Project: {project_name}
Profile: {profile_name}

## Inputs

- User goal:
- Target platform assumptions:
- iOS surface:
- Android surface:
- Permissions:
- Offline state:
- Device or OS version assumptions:
- Simulator plan:
- Emulator plan:
- Build command:
- Logs:
- Screenshots:
- Manual device gap:
- Approval boundary:

## Process

1. Keep the workflow read-only until platform assumptions, permissions, build command, runtime evidence plan, and approval boundary are explicit.
2. Inventory iOS and Android project files, native modules, manifests, entitlements, build files, package metadata, and platform-specific docs.
3. Define acceptance scenarios before implementation: permission request, denied permission, offline state, background/foreground transition, install or upgrade path, and error recovery where applicable.
4. Record permissions and data access as `present_unverified` until platform build/run evidence, owner review, or device evidence confirms behavior.
5. Select verification from detected project files only: Android Gradle build, iOS Xcode build, Flutter command, React Native command, simulator, emulator, device, logs, screenshots, or manual check.
6. Capture runtime evidence with command, exit code, app logs, device logs, simulator/emulator name, OS version, screenshots, and manual device gap when the local environment cannot run a device.
7. Do not claim runtime behavior, do not claim permission behavior, and do not claim offline behavior from code inspection only.
8. Do not change permissions, signing, entitlements, store metadata, production profiles, or device enrollment without explicit approval.
9. Do not publish to App Store, Play Store, TestFlight, internal tracks, or external device management without explicit approval.

## Outputs

- Native mobile feature plan:
- Platform assumptions:
- iOS scope:
- Android scope:
- Permission impact:
- Offline state:
- Acceptance scenarios:
- Build command:
- Simulator plan:
- Emulator plan:
- Device plan:
- Logs:
- Screenshots:
- Runtime evidence:
- Manual device gap:
- Approval requirements:
- Residual risk:

## Verification

- Platform assumptions include iOS, Android, or both and name any unknown platform gap.
- Permissions and offline state are explicit or marked `applicable_missing`.
- Build command is derived from detected project files or marked unavailable with reason.
- Simulator, emulator, device, logs, screenshots, and manual device gap are named before runtime claims.
- Runtime evidence records command, exit code, logs, screenshots, device or simulator/emulator target, OS version, and residual risk.
- Permission changes, signing, store publish, external device management, and production operations remain blocked until explicit approval.

## Stop Conditions

- Platform target is unknown.
- Build command is unknown for a runtime-affecting change.
- Permission or entitlement change lacks approval.
- Runtime, permission, or offline behavior is requested as complete without current platform evidence.
- Simulator/emulator or device evidence is unavailable and no manual device gap is recorded.
- The request asks to publish, sign for production, or mutate external store metadata without explicit approval.
