import yaml
import subprocess
import os
import sys

# Validasi file YAML
yaml_path = "releases.yaml"

if not os.path.exists(yaml_path):
    print("❌ releases.yaml not found")
    sys.exit(1)

with open(yaml_path) as f:
    try:
        data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print("❌ YAML parse error:", e)
        sys.exit(1)

if not isinstance(data, dict) or "releases" not in data:
    print("❌ Invalid structure: 'releases' key not found")
    sys.exit(1)

for entry in data["releases"]:
    tag = entry.get("tag")
    url = entry.get("url")

    if not tag or not url:
        print(f"❌ Skipping invalid entry: {entry}")
        continue

    print(f"🚀 Processing {tag} from {url}")

    try:
        subprocess.run(f"gdown --fuzzy {url} -O downloaded_file", shell=True, check=True)

        subprocess.run(
            f"gh release create {tag} downloaded_file --title {tag} --notes 'Automated release for {tag}' --repo {os.environ['REPO']}",
            shell=True,
            check=True
        )

        os.remove("downloaded_file")
        print(f"✅ Done uploading {tag}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Error processing {tag}: {e}")
