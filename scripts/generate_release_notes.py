#!/usr/bin/env python3
import os
import re
import subprocess

def main():
    tag = os.environ.get('TAG_NAME', '').strip()
    custom = os.environ.get('CUSTOM_NOTES', '').strip()
    clean_tag = tag.lstrip('v')

    changelog_section = ''

    if custom:
        print('Using user-provided custom changelog notes')
        changelog_section = custom
    else:
        if os.path.exists('CHANGELOG.md'):
            try:
                with open('CHANGELOG.md', 'r', encoding='utf-8') as f:
                    content = f.read()
                pattern = rf'## \[v?{re.escape(clean_tag)}\](.*?)(?=\n## \[|\Z)'
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    text = match.group(1).strip()
                    lines = text.splitlines()
                    if lines and lines[0].strip().startswith('- '):
                        lines = lines[1:]
                    changelog_section = '\n'.join(lines).strip()
                    print(f'Extracted changelog section for {tag} from CHANGELOG.md')
            except Exception as e:
                print(f'Error reading CHANGELOG.md: {e}')

        if not changelog_section:
            print('Deriving changelog from git commits...')
            try:
                prev_tags = subprocess.check_output(['git', 'tag', '--sort=-creatordate'], text=True).splitlines()
                prev_tag = next((t for t in prev_tags if t != tag and t), None)
                if prev_tag:
                    rev = f'{prev_tag}..HEAD'
                else:
                    rev = 'HEAD~10..HEAD'
                commits = subprocess.check_output(['git', 'log', rev, '--no-merges', '--pretty=format:* %s (%h)'], text=True).strip()
                changelog_section = commits if commits else '* Continuous integration maintenance and upstream synchronization.'
            except Exception as e:
                changelog_section = '* Continuous integration maintenance and upstream synchronization.'

    lkm_version = '33497'
    ko_sample = 'userspace/ksud/bin/aarch64/android15-6.6_kernelsu.ko'
    if os.path.exists(ko_sample):
        try:
            out = subprocess.check_output(['strings', ko_sample], text=True)
            for line in out.splitlines():
                m = re.search(r'welcome to KernelSU version (\d+)', line)
                if m:
                    lkm_version = m.group(1)
                    break
        except Exception:
            pass

    checksum_rows = []
    if os.path.exists('dist'):
        for fname in sorted(os.listdir('dist')):
            fpath = os.path.join('dist', fname)
            if os.path.isfile(fpath) and fname != 'RELEASE_NOTES.md':
                h = subprocess.check_output(['sha256sum', fpath], text=True).split()[0]
                checksum_rows.append(f'| `{fname}` | `{h}` |')
    checksum_table = '| File | SHA-256 Checksum |\n| :--- | :--- |\n' + '\n'.join(checksum_rows) if checksum_rows else 'N/A'

    release_body = f'''### KernelSu-mix Release {tag}

#### What's New in {tag}:
{changelog_section}

---

#### Built-in Mix Enhancements:
* **Inbuilt Zygisk Runtime (API v4)**: Native userspace Zygisk injection without external modules.
* **SUSFS Kernel Cloaking**: Inbuilt root and path cloaking support.
* **Play Integrity Fix (PIF 4.9)**: Online profile auto-fetch, parsing both `pif.prop` and `pif.json`, with Pixel 6a Canary certified fallback.
* **Tricky Addon Keybox Integration**: Online keybox fetcher & embedded Tricky Addon Keybox Repository (T.A.K.R.) WebView browser dialog.
* **TEE Broken Emulator**: Built-in bypass for devices with corrupted hardware keystore.
* **Play Store Package Detach**: SQLite database detacher preventing app auto-updates.

---

#### Bundled LKM Information:
* **LKM Version**: `v3.4.2 ({lkm_version}-6)` (Kernel UAPI v6)
* **Supported Kernels**: `android12-5.10`, `android13-5.10`, `android13-5.15`, `android14-5.15`, `android14-6.1`, `android15-6.1`, `android15-6.6`, and `android-mainline`.
* **Security & Integrity**: Authenticated with KernelSu-mix production keystore with BTI, PAC, SCS, and CFI fully preserved.

---

#### Checksums & Verification:
{checksum_table}
'''

    os.makedirs('dist', exist_ok=True)
    with open('dist/RELEASE_NOTES.md', 'w', encoding='utf-8') as out_f:
        out_f.write(release_body)
    print('Successfully generated dist/RELEASE_NOTES.md')

if __name__ == '__main__':
    main()
