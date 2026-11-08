# KernelSu-mix Builder & Releases

<div align="center">

![KernelSu-mix](https://raw.githubusercontent.com/KernelSU-Next/KernelSU-Next/dev/assets/ksunext.png)

### The All-In-One Root & Environment Evasion Platform
**Inbuilt Zygisk • SUSFS • Play Integrity Fix • Tricky Store • TEE Emulator • Detach**

[![Build Release](https://github.com/AltafYafai/KernelSu-mix-Builder/actions/workflows/build.yml/badge.svg)](https://github.com/AltafYafai/KernelSu-mix-Builder/actions/workflows/build.yml)
[![Releases](https://img.shields.io/github/v/release/AltafYafai/KernelSu-mix-Builder?style=flat-square)](https://github.com/AltafYafai/KernelSu-mix-Builder/releases)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

</div>

---

## 🌟 What is KernelSu-mix?

**KernelSu-mix** is an advanced fork of **KernelSU-Next** that unifies the most requested root evasion, mounting, and injection features into a single, cohesive ecosystem. Instead of requiring users to hunt down, download, and troubleshoot conflicting external Zygisk modules, companion apps, and terminal scripts, KernelSu-mix bundles them natively.

### 🚀 Key Integrated Features

1. **⚡ Inbuilt Zygisk Runtime (API v4)**
   * Stealth Zygote injection powered by custom linker resolution and ptrace.
   * Full backward compatibility with the official Zygisk API (v2, v3, v4) for running third-party modules like LSPosed.
   * Internal hooks run first for zero-overhead performance.

2. **🛡️ Native SUSFS Kernel Cloaking**
   * Built-in kernel-space VFS and OverlayFS mount cloaking.
   * Inode metadata spoofing (`kstat`), open redirection, and `/proc/modules` symbol hiding.
   * Real-time driver status and auto-load toggle directly in the Manager app.

3. **🔒 Play Integrity Fix (PIF) Injector**
   * Automatically injected into Google Play Services (`com.google.android.gms.unstable`).
   * Spoofs certified `Build` fields, hardware models, and verified boot parameters (`ro.boot.flash.locked=1`, `ro.boot.verifiedbootstate=green`).
   * Dynamic profile editor and one-tap `pif.json` importer in the Manager.

4. **🔑 Tricky Store & Strong Integrity**
   * Intercepts `android.security.keystore` and KeyMint Binder calls.
   * **Leaf Hack mode**: Patches verified boot state and security level in the hardware leaf certificate.
   * **Keybox mode**: Injects custom `keybox.xml` certificates for passing Strong Integrity.

5. **⚙️ TEE Emulator (Broken TEE Bypass)**
   * Specifically crafted for unlocked devices (e.g. OnePlus, ASUS, Pixel) where OEM firmware disables hardware Keymaster key generation.
   * Seamlessly falls back to software keystore key generation (`KM_SECURITY_LEVEL_SOFTWARE`), preventing app crashes.

6. **🚫 Play Store Detach**
   * Intercepts Google Play Store (`com.android.vending`) package inventory transactions.
   * Prevents modded or patched applications (e.g., YouTube ReVanced) from being detected or automatically updated.

---

## 📥 Downloads & Installation

Get the latest pre-compiled builds from the **[Releases Tab](https://github.com/AltafYafai/KernelSu-mix-Builder/releases)**:

* **KernelSu-mix-Manager.apk**: The unified management application.
* **ksud Standalone Binaries**: Multi-arch userspace daemons (`arm64`, `x86_64`, `riscv64`).
* **Kernel Flashables / Boot Images**: Pre-patched boot images with KernelSu-mix + SUSFS.

---

## 🛠️ GitHub Actions CI/CD Pipeline

This repository acts as the public builder and automated release pipeline for the private source repository.

### Required Secrets (Repository Settings -> Secrets and variables -> Actions)

To trigger automated builds, configure the following repository secrets:

| Secret Name | Description |
| :--- | :--- |
| `ACCESS_TOKEN` | Personal Access Token (classic) with `repo` scope to clone the private source repo (`AltafYafai/KernelSu-mix`) |
| `KEYSTORE_BASE64` | Base64-encoded release signing keystore (`.p12` or `.jks`) |
| `KEYSTORE_PASSWORD` | Keystore password |
| `KEY_ALIAS` | Key alias |
| `KEY_PASSWORD` | Key password |
| `EXPECTED_MANAGER_SIZE` | Signing certificate size in hex (e.g. `0x567`) |
| `EXPECTED_MANAGER_HASH` | Signing certificate SHA-256 fingerprint |

*(Note: Run `./scripts/sign.sh generate` in the source repository to automatically generate all of these secrets at once).*

### Triggering a Build

1. Go to the **Actions** tab in this repository.
2. Select **Build & Release KernelSu-mix**.
3. Click **Run workflow**, choose your target options, and click **Run**.
4. Once completed, the signed Manager APK and binaries will appear in the workflow artifacts and release assets!

---

## 👥 Authors & Acknowledgements

KernelSu-mix is made possible by the incredible work of the open-source Android root community:

* **[Weishu (tiann)](https://github.com/tiann)** - Original author of KernelSU
* **[Rifat Azad (rifsxd)](https://github.com/rifsxd)** - Lead Developer of KernelSU-Next
* **[Simon Punk (simonpunk)](https://gitlab.com/simonpunk)** - Author of the SUSFS driver
* **[chiteroman](https://github.com/chiteroman)** - Author of PlayIntegrityFix
* **[5ec1cff](https://github.com/5ec1cff)** - Author of Tricky Store
* **[j-hc](https://github.com/j-hc)** - Author of Zygisk Detach
* **[PerformanC](https://github.com/PerformanC)** - Author of ReZygisk
* **[Altaf Yafai](https://github.com/AltafYafai)** - Maintainer & integrator of KernelSu-mix

---

## 📄 License

KernelSu-mix is distributed under the terms of the GNU General Public License v3 (GPL-3.0). See [LICENSE](LICENSE) for details.
