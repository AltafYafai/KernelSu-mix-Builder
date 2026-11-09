#!/usr/bin/env python3
import os
import sys
import html
import hashlib
import urllib.request
import urllib.parse
import json

def get_file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def send_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

def upload_document(token, chat_id, file_path, caption=""):
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    boundary = "----TelegramBoundary" + os.urandom(16).hex()
    filename = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    body = bytearray()

    # chat_id field
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n'.encode())

    # parse_mode field
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(b'Content-Disposition: form-data; name="parse_mode"\r\n\r\nHTML\r\n')

    # caption field
    if caption:
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="caption"\r\n\r\n{caption}\r\n'.encode())

    # document field
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(f'Content-Disposition: form-data; name="document"; filename="{filename}"\r\n'.encode())
    body.extend(b'Content-Type: application/vnd.android.package-archive\r\n\r\n')
    body.extend(file_bytes)
    body.extend(b'\r\n')

    body.extend(f"--{boundary}--\r\n".encode())

    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))

def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    tag = os.environ.get("TAG_NAME", "").strip() or "v1.0.5"
    repo = os.environ.get("GITHUB_REPOSITORY", "AltafYafai/KernelSu-mix-Builder")
    release_url = f"https://github.com/{repo}/releases/tag/{tag}"

    if not token or not chat_id:
        print("INFO: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not configured.")
        print("To enable Telegram notifications and APK uploads, add these secrets to your repository settings:")
        print("  - TELEGRAM_BOT_TOKEN: Bot token from @BotFather")
        print("  - TELEGRAM_CHAT_ID: Target Channel ID or Chat ID (e.g. @your_channel or -100xxxxxxxxxx)")
        sys.exit(0)

    print(f"Sending Telegram notification for release {tag} to chat {chat_id}...")

    # Extract changelog
    changelog_snippet = ""
    notes_file = "dist/RELEASE_NOTES.md"
    if os.path.exists(notes_file):
        try:
            with open(notes_file, "r", encoding="utf-8") as f:
                content = f.read()
            # Find What's New section
            import re
            m = re.search(r"#### What's New.*?:(.*?)(?=---|\Z)", content, re.DOTALL)
            if m:
                raw_snippet = m.group(1).strip()
                # Limit length to avoid exceeding Telegram message size
                lines = [l.strip() for l in raw_snippet.splitlines() if l.strip()]
                shortened = lines[:15]
                changelog_snippet = "\n".join(shortened)
        except Exception as e:
            print(f"Warning: could not parse release notes: {e}")

    if not changelog_snippet:
        changelog_snippet = "• Routine bugfixes, upstream synchronization, and enhancements."

    msg = f"""🚀 <b>KernelSu-mix Release {html.escape(tag)} is out!</b>

📱 <b>Manager Version:</b> <code>v3.4.2 (33497-6)</code>
⚡ <b>Kernel UAPI:</b> <code>v6</code>
🛡️ <b>Inbuilt Features:</b>
• <b>Zygisk API v4</b> (Native Userspace)
• <b>SUSFS</b> Root &amp; Mount Path Cloaking
• <b>Play Integrity Fix (PIF 4.9)</b> Auto-Fetch
• <b>Tricky Addon Keybox</b> Browser &amp; Injector
• <b>TEE Emulator</b> (Hardware Keystore Bypass)
• <b>Play Store Detach</b> Engine

📝 <b>Changelog:</b>
<pre>{html.escape(changelog_snippet)}</pre>

🔗 <a href="{release_url}">View on GitHub Releases</a>"""

    try:
        resp = send_message(token, chat_id, msg)
        print("Message sent successfully:", resp.get("ok"))
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

    # Search for manager APK to upload
    apk_candidates = [
        "dist/KernelSu-mix-Manager.apk",
        "dist/KernelSu_mix_v3.4.2_33497-release.apk"
    ]
    apk_path = None
    for cand in apk_candidates:
        if os.path.exists(cand):
            apk_path = cand
            break

    if not apk_path and os.path.exists("dist"):
        for f in os.listdir("dist"):
            if f.endswith(".apk") and "unsigned" not in f:
                apk_path = os.path.join("dist", f)
                break

    if apk_path and os.path.exists(apk_path):
        size_mb = os.path.getsize(apk_path) / (1024 * 1024)
        sha256 = get_file_sha256(apk_path)
        caption = f"📦 <b>KernelSu-mix Manager</b> (<code>{html.escape(tag)}</code>)\n" \
                  f"📏 <b>Size:</b> {size_mb:.2f} MB\n" \
                  f"🔑 <b>SHA-256:</b> <code>{sha256[:16]}...{sha256[-8:]}</code>\n" \
                  f"#KernelSu #Release #Manager"
        print(f"Uploading APK {apk_path} ({size_mb:.2f} MB) to Telegram...")
        try:
            doc_resp = upload_document(token, chat_id, apk_path, caption)
            print("APK uploaded successfully:", doc_resp.get("ok"))
        except Exception as e:
            print(f"Error uploading APK to Telegram: {e}")
    else:
        print("Notice: No APK file found in dist/ to upload.")

if __name__ == "__main__":
    main()
