import os

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
        else:
            print(f"[-] {file} does not appear interesting")