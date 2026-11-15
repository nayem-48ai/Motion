import json, os, re, glob

ROOT = "/root/speakee-video"
T = json.load(open(os.path.join(ROOT, "build/timing.json")))
base_css = open(os.path.join(ROOT, "src/base.css")).read()

LOGO = '''<div class="logo"><svg width="48" height="48" viewBox="0 0 48 48" fill="none"><rect x="2" y="18" width="5" height="12" rx="2.5" fill="#5b4bff"/><rect x="11" y="11" width="5" height="26" rx="2.5" fill="#5b4bff"/><rect x="20" y="4" width="5" height="40" rx="2.5" fill="#16c7a3"/><rect x="29" y="14" width="5" height="20" rx="2.5" fill="#5b4bff"/><rect x="38" y="20" width="5" height="8" rx="2.5" fill="#16c7a3"/></svg><div><span class="word">speak<em>ee</em></span><span class="sub">Studio-grade AI voices</span></div></div>'''

# scene timing helpers
scenes = {s["id"]: s for s in T["scenes"]}
for f in sorted(glob.glob(os.path.join(ROOT, "src/scenes/*.html"))):
    scene_id = os.path.basename(f)[:-5]
    s = scenes[scene_id]
    b = {it["id"]: round(it["start"] - s["start"], 3) for it in s["items"]}
    d = {it["id"]: round(it["duration"], 3) for it in s["items"]}
    timing = {"start": s["start"], "dur": s["duration"], "b": b, "d": d}
    html = open(f).read()
    html = html.replace("/*__BASE__*/", base_css)
    html = html.replace("/*__TIMING__*/", json.dumps(timing, ensure_ascii=False))
    html = html.replace("<!--LOGO-->", LOGO)
    open(os.path.join(ROOT, "compositions", scene_id + ".html"), "w").write(html)
    print("scene", scene_id, s["duration"])

# index
hosts = []
for i, s in enumerate(T["scenes"]):
    hosts.append(f'''      <div
        id="{s['id']}"
        class="clip"
        data-composition-id="{s['id']}"
        data-composition-src="compositions/{s['id']}.html"
        data-start="{s['start']}"
        data-duration="{s['duration']}"
        data-track-index="{10+i}"
        data-track-kind="graphics"
        data-width="1920"
        data-height="1080"
      ></div>''')

audios = []
for s in T["scenes"]:
    for it in s["items"]:
        audios.append(f'''    <audio id="a-{it['id']}" class="clip" src="{it['file']}" data-start="{it['start']}" data-duration="{it['duration']}" data-track-index="70" data-volume="1"></audio>''')

# music + sfx
total = T["total"]
sfx = [
    ("riser", 0.15, 0.30, 2.6),
    ("impact", 1.45, 0.55, None),
    ("whoosh", scenes["what"]["start"], 0.35, None),
    ("whoosh", scenes["agenda"]["start"], 0.30, None),
    ("whoosh", scenes["library"]["start"], 0.35, None),
    ("whoosh", scenes["lang"]["start"], 0.30, None),
    ("whoosh", scenes["bn"]["start"], 0.35, None),
    ("whoosh", scenes["en"]["start"], 0.30, None),
    ("riser", scenes["models"]["start"] - 2.2, 0.24, 2.2),
    ("impact", scenes["models"]["start"] + 0.05, 0.45, None),
    ("whoosh", scenes["modeldemo"]["start"], 0.28, None),
    ("whoosh", scenes["studio"]["start"], 0.35, None),
    ("click", scenes["studio"]["start"] + scenes["studio"]["items"][1]["start"] - scenes["studio"]["start"] + 0.9, 0.40, None),
    ("whoosh", scenes["controls"]["start"], 0.28, None),
    ("pop", scenes["controls"]["start"] + 3.0, 0.30, None),
    ("whoosh", scenes["emotions"]["start"], 0.28, None),
    ("whoosh", scenes["script"]["start"], 0.30, None),
    ("typing", scenes["script"]["start"] + 1.4, 0.32, 2.6),
    ("click", scenes["generate"]["start"] + 3.2, 0.45, None),
    ("pop", scenes["generate"]["start"] + 4.6, 0.30, None),
    ("whoosh", scenes["recent"]["start"], 0.28, None),
    ("click", scenes["recent"]["start"] + 4.2, 0.35, None),
    ("click", scenes["recent"]["start"] + 5.4, 0.35, None),
    ("notification", scenes["recent"]["start"] + 7.2, 0.30, None),
    ("whoosh", scenes["api"]["start"], 0.35, None),
    ("typing", scenes["api"]["start"] + 1.6, 0.28, 3.4),
    ("pop", scenes["api"]["start"] + 8.1, 0.30, None),
    ("whoosh", scenes["tas"]["start"], 0.35, None),
    ("whoosh", scenes["tasts"]["start"], 0.25, None),
    ("whoosh", scenes["stt"]["start"], 0.25, None),
    ("whoosh", scenes["free"]["start"], 0.30, None),
    ("whoosh", scenes["install"]["start"], 0.28, None),
    ("typing", scenes["install"]["start"] + 1.4, 0.26, 3.0),
    ("whoosh", scenes["use"]["start"], 0.28, None),
    ("riser", scenes["outro"]["start"] - 1.8, 0.30, 1.8),
    ("sparkle", scenes["outro"]["start"] + 0.8, 0.35, None),
    ("impact", scenes["outro"]["start"] + 1.4, 0.45, None),
]
sfx_names = {"riser": "riser", "impact": "impact-bass-1", "whoosh": "whoosh-short", "click": "click-soft",
             "pop": "pop", "typing": "typing", "notification": "notification", "sparkle": "sparkle"}
audios.append(f'''    <audio id="bed" class="clip" src="assets/audio/bed.mp3" data-start="0" data-duration="{total}" data-track-index="85" data-volume="0.15"></audio>''')
for i, (name, start, vol, dur) in enumerate(sfx):
    extra = f' data-duration="{dur}"' if dur else ' data-duration="1.2"'

    audios.append(f'''    <audio id="sfx-{i}" class="clip" src="assets/sfx/{sfx_names[name]}.mp3" data-start="{round(start,3)}"{extra} data-track-index="80" data-volume="{vol}"></audio>''')

index = f'''<!doctype html>
<html lang="bn">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>Speakee — Feature Tour</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; background: #08080f; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}" data-width="1920" data-height="1080">
{chr(10).join(hosts)}
      <div id="ticker" class="clip" data-composition-id="ticker" data-composition-src="compositions/ticker.html" data-start="0" data-duration="{total}" data-track-index="60" data-width="1920" data-height="1080"></div>
{chr(10).join(audios)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
'''
open(os.path.join(ROOT, "index.html"), "w").write(index)

# ticker
ticker = f'''<template>
<style>
/*__BASE__*/
#root {{ position: absolute; inset: 0; background: transparent; overflow: hidden; }}
.ticker {{ position: absolute; left: 0; right: 0; bottom: 0; height: 54px; background: #08080f; display: flex; align-items: center; overflow: hidden; border-top: 2px solid #5b4bff; }}
.badge {{ flex: 0 0 auto; height: 100%; display: flex; align-items: center; gap: 10px; padding: 0 22px; background: #5b4bff; color: #fff; font-family: Outfit; font-weight: 800; font-size: 17px; letter-spacing: 0.18em; z-index: 2; }}
.dot {{ width: 9px; height: 9px; border-radius: 50%; background: #ff5a5a; }}
.track {{ display: flex; align-items: center; white-space: nowrap; will-change: transform; }}
.track span {{ font-family: "BN Sans", Outfit, sans-serif; font-weight: 600; font-size: 19px; letter-spacing: 0.06em; color: #d8d7e8; padding: 0 26px; }}
.track b {{ color: #16c7a3; font-weight: 700; }}
.track i {{ color: #6a5bff; font-style: normal; }}
.sep {{ color: #5b4bff; font-size: 15px; }}
</style>
<div id="root" data-composition-id="ticker" data-width="1920" data-height="1080" data-no-timeline>
  <div class="ticker">
    <div class="badge"><span class="dot"></span>SPEAKEE · LIVE</div>
    <div style="overflow:hidden;flex:1;height:100%;display:flex;align-items:center;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 46px,#000 calc(100% - 36px),transparent 100%);mask-image:linear-gradient(90deg,transparent 0,#000 46px,#000 calc(100% - 36px),transparent 100%)">
      <div class="track" id="track">
        <!--REPEAT-->
      </div>
    </div>
  </div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
tl.fromTo("#track", {{ xPercent: 0 }}, {{ xPercent: -50, duration: {total}, ease: "none" }}, 0);
window.__timelines["ticker"] = tl;
</script>
</template>'''
item = '<span><b>৪২টি ভাষা</b> <i class="sep">◆</i> <b>৮০০+ ভয়েস</b> <i class="sep">◆</i> <b>৫৮টি ইমোশন</b> <i class="sep">◆</i> NO SIGNUP <i class="sep">◆</i> NO API KEY <i class="sep">◆</i> SONIC 3.5 <i class="sep">◆</i> TAS SKILL <i class="sep">◆</i> TTS + STT <i class="sep">◆</i> ১০০% ফ্রি <i class="sep">◆</i></span>'
ticker = ticker.replace("/*__BASE__*/", base_css).replace("<!--REPEAT-->", item * 8)
ticker = ticker.replace('<div id="root" data-composition-id="ticker" data-width="1920" data-height="1080" data-no-timeline>', '<div id="root" data-composition-id="ticker" data-width="1920" data-height="1080">')
open(os.path.join(ROOT, "compositions/ticker.html"), "w").write(ticker)
print("total", total)
