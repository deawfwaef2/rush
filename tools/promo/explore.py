#!/usr/bin/env python3
"""Camera exploration on a deterministic take: run the battle cheaply (low DPR) to chosen frames and render
still variants with pinned camera values at full resolution.

usage: python3 explore.py spec.json plan.json out_dir
  plan.json: [{"f": 440, "cams": [[x, zoom, tilt, y], ...]}, ...]   (x may be "bx+200", "ex-100", "xf+50" expressions)
Stills are named <out_dir>/f<frame>_<i>.jpg. The sim continues after each stop (stills cost no sim time, but the
extra zero-dt frames make the rest of the run diverge slightly from the real take - fine for looks, not for timing).
"""
import json, os, sys, time, base64
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import capture as C

def main():
    spec = json.load(open(sys.argv[1])); plan = json.load(open(sys.argv[2])); out = sys.argv[3]
    os.makedirs(out, exist_ok=True)
    fps = spec.get("fps", 30); dt = 1000.0 / fps
    vt = open(os.path.join(C.HERE, "vt.js")).read().replace("__SEED__", str(int(spec.get("seed", 1))))
    save = {**C.FLAGS, "lvl": spec["lvl"], "reserve": spec.get("men", 100) + spec.get("vets", 0) + 50, "vets": spec.get("vets", 0) + 10,
            "income": 400, "econ": 3, "day": 5, "lastPay": C.VT_EPOCH + 1000, "moraleT": C.VT_EPOCH + 1000}
    with sync_playwright() as p:
        br = p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
        ctx = br.new_context(viewport={"width": spec.get("w", 1920), "height": spec.get("h", 1080)}, device_scale_factor=spec.get("dsf", 1))
        ctx.add_init_script(vt + "\ntry{localStorage.setItem('charge_save_v3', JSON.stringify(%s));}catch(e){}" % json.dumps(save))
        pg = ctx.new_page(); errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(C.URL)
        pg.evaluate(C.SETUP_JS, spec)
        pg.evaluate("__VT.run(600,50)"); pg.evaluate("(()=>{ toPlan(); return 0; })()"); pg.evaluate("__VT.run(1700,50)")
        pg.evaluate("""(spec)=>{ setWave(0, spec.men||100, Math.min(spec.vets||0, S.vets)); const s=spec.sup||{}; for(const k in s){ used[k]=s[k]; } return 0; }""", spec)
        pg.evaluate("__VT.run(600,50)")
        if spec.get("cur"): pg.evaluate("(c)=>{ Object.assign(cur,c); return 0; }", spec["cur"])
        if spec.get("nowire"): pg.evaluate("(()=>{ belts.length=0; return 0; })()")
        if spec.get("mines") is not None: pg.evaluate("(n)=>{ mines.length=Math.min(mines.length,n); cur.mn=mines.length; return 0; }", spec["mines"])
        pg.evaluate(C.TRACK_JS, {**spec, "camtrack": [], "slow": spec.get("slow", [])})
        pg.evaluate("(()=>{ window.__F0=__VT.now; startCharge(); return 0; })()")
        low = spec.get("lowdpr", 0.34); pg.evaluate(C.SET_DPR_JS, low)
        f = 0; t0 = time.time()
        for stop in plan:
            while f < stop["f"]:
                pg.evaluate("(d)=>{ __VT.step(d); return 0; }", dt); f += 1
            st = json.loads(pg.evaluate(C.META_JS))
            print("at", f, {k: st.get(k) for k in ("mode", "bt", "alive", "e", "xf", "ex", "bx", "camx", "zoom")}, f"{time.time()-t0:.0f}s", flush=True)
            pg.evaluate(C.SET_DPR_JS, spec.get("dsf", 1))
            env = {"bx": st.get("bx") or 0, "ex": st.get("ex") or 0, "xf": st.get("xf") or st.get("camx"), "cx": st.get("camx")}
            for i, c in enumerate(stop["cams"]):
                x = eval(str(c[0]), {}, env) if isinstance(c[0], str) else c[0]
                pg.evaluate("(c)=>{ __CT.on=true; __CT.x=c[0]; __CT.zoom=c[1]; __CT.tilt=c[2]; __CT.y=c[3]||0; __VT.step(0); __VT.step(0); return 0; }", [x, c[1], c[2], c[3] if len(c) > 3 else 0])
                u = pg.evaluate("()=>cv.toDataURL('image/jpeg',0.85)")
                open(os.path.join(out, f"f{f}_{i}.jpg"), "wb").write(base64.b64decode(u.split(",", 1)[1]))
            pg.evaluate("(()=>{ __CT.on=false; return 0; })()")
            pg.evaluate(C.SET_DPR_JS, low)
        print("errs", errs[:3], pg.evaluate("__VT.errs.slice(0,3)"))
        br.close()

if __name__ == "__main__":
    main()
