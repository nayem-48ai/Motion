import json, subprocess, os

ROOT = "/root/speakee-video"
audio = json.load(open(os.path.join(ROOT, "build/audio.json")))
spec = json.load(open(os.path.join(ROOT, "build/timeline_spec.json")))

def dur(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", path], capture_output=True, text=True)
    return round(float(r.stdout.strip()), 3)

extra = {"demo-dialog": "assets/audio/demo-dialog.mp3"}
for k, p in extra.items():
    audio[k] = {"file": p, "duration": dur(os.path.join(ROOT, p))}

scenes = []
cursor = 0.0
for i, s in enumerate(spec["scenes"]):
    start = cursor + (0 if i == 0 else spec["gap"])
    t = start + s["lead"]
    items = []
    for it in s["items"]:
        a = audio[it["id"]]
        pre = it.get("pre", 0.12)
        post = it.get("post", 0.22)
        st = t + pre
        items.append({"id": it["id"], "kind": it.get("kind", "vo"),
                      "start": round(st, 3), "end": round(st + a["duration"], 3),
                      "duration": a["duration"], "file": a["file"]})
        t = st + a["duration"] + post
    end = t + s["tail"]
    scenes.append({"id": s["id"], "start": round(start, 3), "end": round(end, 3),
                   "duration": round(end - start, 3), "items": items})
    cursor = end

total = cursor
out = {"total": round(total, 3), "scenes": scenes, "audio": audio}
json.dump(out, open(os.path.join(ROOT, "build/timing.json"), "w"), ensure_ascii=False, indent=2)
for s in scenes:
    print(f'{s["id"]:10} {s["start"]:7.2f} -> {s["end"]:7.2f}  ({s["duration"]:5.2f}s)')
print("TOTAL", total, f"{int(total//60)}:{total%60:05.2f}")
