# Changelog

All notable changes to **KernelSu-mix** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to Semantic Versioning.

---

## [v1.0.6] - 2026-11-09

### Fixed
- **Zygisk Framework Detection for Module Installers**: Fixed Zygisk module flashing failure (such as HMA-OSS aborting with *"No known Zygisk frameworks (e.g. ZygiskNext) is found"*). Exported `ZYGISK_ENABLED=1` in the module installation environment and automatically provisioned framework metadata and daemon markers in `/data/adb/modules/zygisk_mix` when inbuilt Zygisk is enabled.
- **Keybox Auto-Fetch Resilience**: Bundled a verified, authentic 6-certificate hardware keybox (`assets/keybox.xml`) directly into the Manager APK. The "Auto-Fetch Keybox" button now reliably installs valid certificates even when upstream raw URLs are blocked or moved.
- **Accurate Keybox State Detection**: Prevented empty or corrupted 0-certificate files from falsely displaying *"Hardware Keybox: Installed (Strong Integrity)"*. Only valid keyboxes with parsed certificates (> 0) report as active.
- **T.A.K.R. WebView Download Interceptor**: Overhauled the in-app Keybox Repository WebView (`https://keybox.kowx712.cc/en`) with `window.open` trapping, `setDownloadListener`, `shouldOverrideUrlLoading`, and cookie inheritance, allowing keyboxes like TAKR 36 to be downloaded and installed directly in-app after human verification.
- **Automated GMS Target Configuration**: Importing or fetching a keybox now automatically adds or upgrades `com.google.android.gms!` and `com.google.android.gms.unstable!` to Keybox Generate mode (`!`) in `target.txt` and terminates GMS attestation processes to force immediate certificate re-issuance.

### Added
- **Telegram Bot Integration**: Added automated Telegram notifications with formatted HTML changelog and direct `KernelSu-mix-Manager.apk` document upload to configured channels/chats on every GitHub release.

---

## [v1.0.5] - 2026-11-09

### Fixed
- **Manager UAPI v6 Alignment**: Fixed `get_manager_uapi_version()` in `ksu.cc` returning `KERNEL_SU_UAPI_VERSION` (`6`) instead of `5`, eliminating the red *"The current KernelSu-mix manager version 5 is too low for KernelSu-mix to work properly. Please upgrade manager to version 6 or higher!"* warning banner.
- **Manager and LKM Full Harmony**: Manager version string now reflects `v3.4.2 (33497-6)`, matching the kernel module UAPI v6 protocol perfectly.

### Added
- **Automated Specific Release Changelogs**: Integrated CI release notes generator that automatically extracts release-specific changelogs and computes SHA-256 checksums tables for all release artifacts.

---

## [v1.0.4] - 2026-11-09

### Fixed
- **LKM and Manager Version Synchronization**: Dynamically synchronized Manager APK `versionCode` (`33497`) and `versionName` (`v3.4.2`) directly from the bundled GKI LKM binary (`welcome to KernelSU version 33497`).
- **Update Banner Mismatch**: Eliminated the false *"A newer bundled LKM is available. Tap to update"* banner on the Home dashboard by matching the Manager's version comparison logic to the bundled LKM.
- **UI KMI Detection**: Fixed an unresolved reference crash in `MixFeatures.kt` by using `getCurrentKmi()` instead of `getKernelVersion().kmi`.

### Changed
- **Compiler Cleanliness**: Cleaned up redundant module imports (`pif`, `tricky`, `zygisk`, `detach`) in `ksud/src/cli.rs`.

---

## [v1.0.3] - 2026-11-09

### Added
- **Play Integrity Fix 4.9 Integration**:
  - Support for parsing both `pif.json` and line-by-line `pif.prop` (`KEY=VALUE`) formats.
  - Automatic extraction of `BRAND`, `PRODUCT`, `DEVICE`, `ID`, `INCREMENTAL`, `TYPE`, and `TAGS` from `FINGERPRINT` string.
  - Complete injection coverage across `android.os.Build` and `android.os.Build.VERSION` (including `SECURITY_PATCH` and integer `DEVICE_INITIAL_SDK_INT`).
  - Updated certified fallback profile to Google Pixel 6a Canary (`bluejay_beta`, `ZP11.260918.007`).
  - Added one-click online profile fetcher in UI and `ksud` daemon (`ksud pif fetch`) pulling from verified upstream repositories and killing GMS unstable process automatically.
- **Tricky Addon Keybox Auto-Fetch & Browser**:
  - Built-in Tricky Addon Keybox Repository (T.A.K.R.) WebView browser dialog supporting official `postMessage` handshake protocol (`https://keybox.kowx712.cc/en`).
  - Added URL mirror fallback keybox auto-fetch (`ksud tricky fetch [url]`).
  - Added "Add GMS (!)" quick preset for target packages.

---

## [v1.0.2] - 2026-11-09

### Added
- **Kernel UAPI v6 Support**: Upgraded Manager and LKM protocol communication to UAPI v6, resolving the *"Version 5 is too low for the manager"* error.
- **Bundled Upstream Dev GKI LKMs**: Integrated latest official KernelSU-Next dev LKMs across all 8 supported kernel versions:
  - `android12-5.10`, `android13-5.10`, `android13-5.15`, `android14-5.15`
  - `android14-6.1`, `android15-6.1`, `android15-6.6`, and `android-mainline`
- **Automated Signature Patcher**: Automated CI patcher script modifying certificate SHA-256 hash and APK size across all bundled LKMs without altering executable code sections.

### Changed
- **Full Localization Rebranding**: Updated app name to "KernelSu-mix" across all 24 localized `values-*/strings.xml` resource directories.

---

## [v1.0.1] - 2026-11-09

### Fixed
- **Boot Panic & Kernel Trap 0x34 Fix**:
  - Replaced raw assembly jump hook in `is_manager_apk` with zero-code-modification `.rodata` SHA-256 string and APK size comparison patch.
  - Fully preserved ARM64 BTI (Branch Target Identification), PAC, SCS (Shadow Call Stack), and CFI integrity across all LKMs.
- **Boot Image Patcher**: Fixed empty KMI list on Select Boot by adding GKI KMI fallback detection in `getSupportedKmis()`.

### Added
- **Tricky Store Management**: Added interactive keybox deletion, target list manager (`target.txt`), and mode toggles (`!` Keybox Generate vs `?` Leaf Hack).
- **CLI Commands**: Added `ksud tricky remove-keybox`, `add-target`, and `remove-target`.

---

## [v1.0.0] - 2026-11-09

### Added
- **Initial Release of KernelSu-mix Suite**:
  - **Inbuilt Zygisk Runtime**: Native Zygisk API v4 injection subsystem built directly into `ksud` and Manager.
  - **SUSFS Kernel Cloaking**: Built-in support for SUSFS kernel-level root and injection hiding.
  - **Play Integrity Fix (PIF)**: Built-in fingerprint spoofing and hardware attestation bypass.
  - **Tricky Store / Keybox Support**: Built-in keybox.xml injection for Strong Integrity attestation.
  - **TEE Emulator**: Built-in broken TEE bypass for devices with degraded hardware trust environments.
  - **Play Store Detach**: Built-in SQLite package detacher to prevent unwanted app auto-updates.
  - **Custom Manager Signature Bypass**: Initial implementation for authenticating custom manager builds with GKI LKMs.
