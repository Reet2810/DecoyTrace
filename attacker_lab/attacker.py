import os
import requests

TARGET_DIR = os.path.dirname(os.path.abspath(__file__))

interesting_keywords = ["credential", "password", "secret", "key", "token", "username"]

print("[+] Simulated attack started")
print("[*] Beginning reconnaissance...")

files = os.listdir(TARGET_DIR)

print("[+] Resource found:")

for file in files:
    if file != "attacker.py":
        print(f"    - {file}")

print("\n[*] Inspecting discovered resources...")

for file in files:
    if file != "attacker.py":
        file_path = os.path.join(TARGET_DIR, file)
        with open(file_path, 'r') as f:
            content = f.read()

        found_keywords = []
        for keyword in interesting_keywords:
            if keyword.lower() in content.lower():
                found_keywords.append(keyword)

        if found_keywords:
            print(f"[!] Interesting resource found: {file}")
            print(f"    Keywords detected: {found_keywords}")
            if "token" in content.lower():
                for line in content.splitlines():
                    if "token" in line.lower():
                        token = line.split(":", 1)[-1].strip()
                        print(f"    Honeytoken extracted: {token}")
                        target_url = f"http://127.0.0.1:5000/decoy/{token}"
                        response = requests.get(target_url)

                        print(f"[+] HTTP request sent to {target_url}")
                        print(f"[+] Response: {response.status_code}")
        else:
            print(f"[-] {file} does not appear interesting")