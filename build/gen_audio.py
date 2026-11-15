import json, subprocess, os, sys

ROOT = "/root/speakee-video"
TAS = os.path.expanduser("~/.config/opencode/skills/tas/scripts/tas.py")
OUT = os.path.join(ROOT, "assets/audio")
os.makedirs(OUT, exist_ok=True)
data = json.load(open(os.path.join(ROOT, "build/lines.json")))
narr = data["narrator"]

def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", path], capture_output=True, text=True)
    return round(float(r.stdout.strip()), 3) if r.stdout.strip() else None

def gen(entry, default_voice):
    out = os.path.join(OUT, entry["id"] + ".mp3")
    if os.path.exists(out):
        print("skip", entry["id"], dur(out))
        return
    cmd = [sys.executable, TAS, "tts", entry["vo"],
           "-l", entry.get("lang", "bn"),
           "-m", entry.get("model", "sonic-3.5"),
           "-v", entry.get("voice", default_voice),
           "-s", str(entry.get("speed", 1.08)),
           "-e", entry.get("emotion", "neutral"),
           "-o", out]
    print("gen", entry["id"], entry.get("voice", default_voice), entry.get("model", "sonic-3.5"))
    r = subprocess.run(cmd, capture_output=True, text=True)
    print((r.stdout or "").strip().splitlines()[-1] if r.stdout else "", end=" | ")
    print((r.stderr or "").strip()[-200:])
    if r.returncode != 0:
        raise SystemExit(f"failed {entry['id']}")

for e in data["lines"]:
    gen(e, narr["voice"])
for e in data["demos"]:
    gen(e, narr["voice"])

manifest = {}
for e in data["lines"] + data["demos"]:
    p = os.path.join(OUT, e["id"] + ".mp3")
    manifest[e["id"]] = {"file": "assets/audio/" + e["id"] + ".mp3", "duration": dur(p), **e}
json.dump(manifest, open(os.path.join(ROOT, "build/audio.json"), "w"), ensure_ascii=False, indent=2)
total = sum(v["duration"] or 0 for k, v in manifest.items() if k in [x["id"] for x in data["lines"]])
print(f"narrator total {total:.1f}s, {len(manifest)} clips")
