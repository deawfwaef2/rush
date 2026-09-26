#!/usr/bin/env python3
"""Frame-exact capture of real gameplay for the promo videos.

The page runs on a virtual clock (vt.js): every output frame advances the game by exactly 1/fps s,
then the canvas is grabbed. Slow software rendering therefore never causes stutter or time drift.
Outputs to <outdir>/<name>/: f00000.jpg ..., meta.jsonl (game state per frame), sfx.json (every
sound the game asked for, with virtual timestamps; the soundtrack is rebuilt from it offline).

usage: python3 capture.py '<json take spec>'
  spec keys: name, lvl, men, vets, sup{art,snp,smk,tnk}, w, h, fps, seed, dur (s after CHARGE),
             tail (s to keep after the win), portrait (K: view scale = H*K/1100, 16/9 = crop-equivalent),
             clean (hide in-canvas UI marks), noinsets, nobars (montage without letterbox), outdir, q (jpeg q)
"""
import sys, json, os, time, base64
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
URL = "file://" + os.path.join(ROOT, "index.html")

FLAGS = {"tut": 1, "perfTut": 1, "gfx": "h", "lang": "en", "morale": 95, "snd": 1, "mus": 1,
         **{f"seenCG{i}": 1 for i in range(5)}, **{f"seenCh{i}": 1 for i in range(5)}, **{f"seenSub{i}": 1 for i in range(5)},
         "seenM": {k: 1 for k in ["mg", "mn", "sh", "wr", "gs", "sn", "fl", "art", "snp", "smk", "tnk", "eng", "flare", "off"]},
         "supU": {"art": 1, "snp": 1, "smk": 1, "tnk": 1}}

META_JS = """(()=>{ const r={t:__VT.now, mode, slow:slowmo, camx:Math.round(cam.x), zoom:+cam.zoom.toFixed(3), shake:+(cam.shake||0).toFixed(2),
  mont: montage?+montage.t.toFixed(2):-1, fr: flagRaise?+flagRaise.t.toFixed(2):-1};
  try{ r.vfx = (typeof vfx!=="undefined"&&vfx)?+vfx.t.toFixed(2):-1; }catch(e){}
  if(battle){ const b=battle; r.bt=+b.t.toFixed(2); r.mel=b.melee?1:0; r.over=b.over?1:0; r.dead=b.dead; r.e=b.e; r.reached=b.reached;
    let al=0, run=0, xs=[]; for(const m of men){ if(!m.alive)continue; al++; if(!m.intrench&&m.state!=="crouch"){ run++; xs.push(m.x); } }
    xs.sort((a,b)=>a-b); r.alive=al; r.run=run; r.xf = xs.length? Math.round(xs[Math.floor(xs.length*0.8)]) : null;
    r.ex=trenchX(S.lvl+(mode==="result"?0:1)); r.bx=trenchX(S.lvl-(mode==="result"?1:0)); }
  return JSON.stringify(r); })()"""

SETUP_JS = """(spec)=>{
  // audio off (deterministic; the soundtrack is rebuilt offline from the log below)
  AU.init=function(){};
  const L=window.__SFXLOG=[]; const last={};
  SFX.play=function(k,vol,o){ vol=vol==null?1:vol; o=o||{}; const t=__VT.now;
    if(o.gap){ if(last[k]!=null && t-last[k]<o.gap*1000) return true; last[k]=t; }
    L.push({t, k, v:vol, d:o.delay||0, dur:o.dur||0, off:o.off||0, rate:o.rate||1, fixed:o.fixed?1:0, lp:o.lp||0, pan:(o.pan==null?null:o.pan), mode}); return true; };
  const ot=AU.tone; AU.tone=function(t,f,dur,vol,type,out,f2){ L.push({t:__VT.now,k:"@tone",f,dur,v:vol,f2:f2||0,mode}); };
  const ob=BGM.play.bind(BGM); BGM.play=function(k){ L.push({t:__VT.now,k:"@bgm:"+k,mode}); };
  if(spec.clean){ drawEvTags=function(){}; drawAimMarks=function(){}; drawUnitMarks=function(){}; }
  if(spec.nobubbles){ drawBubbles=function(){ bubbles.length=0; }; }
  if(spec.noinsets){ drawInsets=function(){ insets.length=0; }; }
  if(spec.nobars||spec.pmontage){ let src=drawMontage.toString();
    if(spec.nobars) src=src.replace("bar=H*0.11","bar=0").replace("W/2,H-bar/2+5","W/2,H+99");
    if(spec.pmontage){ src=src.replace("const S_=ih/200","const S_=Math.min(ih,W)/200").replace("R_=ih*0.36","R_=Math.min(ih*0.36,W*0.4)")
                              .replace("const lx=W*0.42, lw=W*0.16;","const lw=Math.max(W*0.16,S_*60), lx=Math.min(W*0.42,W*0.5-lw/2);"); }
    drawMontage=(0,eval)("("+src+")"); }
  window.perfTick=function(){}; perfTick=function(){};
  if(spec.portrait){ const K=spec.portrait; scaleZ=function(z){ const b=(H*K/1100)*cam.zoom; return b*(0.36+1.44*Math.pow(Math.max(0,z),1.08)); }; }
  QUAL=2; resize();
  return 0; }"""

# director: optional camera override per phase (offsets in world units; null/absent = keep the game's own camera)
DIRECTOR_JS = """(spec)=>{
  let tgt=null; const d=spec.director||{};
  Object.defineProperty(cam,'tx',{configurable:true, get(){ return tgt!=null?tgt:this._tx; }, set(v){ this._tx=v; }});
  __VT.pre=function(){
    tgt=null;
    if(mode==="barrage"){ if(d.barrage!=null) tgt=trenchX(S.lvl+1)+d.barrage; return; }
    if((mode==="charge"||mode==="melee")&&battle){ const b=battle, ex=trenchX(S.lvl+1), bx=trenchX(S.lvl);
      if(montage || b.t<(d.holdT!=null?d.holdT:1.2)){ if(d.start!=null) tgt=bx+d.start; return; }
      if(b.mel.length>6 || b.over){ if(d.melee!=null) tgt=ex+d.melee; return; }
      if(d.follow==null) return;
      const xs=[]; for(const m of men){ if(m.alive&&!m.intrench&&m.state!=="crouch") xs.push(m.x); }
      if(!xs.length) return; xs.sort((a,c)=>a-c); const q=d.q!=null?d.q:0.8;
      tgt=Math.min(ex+(d.melee!=null?d.melee:-70), xs[Math.floor((xs.length-1)*q)]+d.follow); return; }
    if(mode==="result"&&d.win!=null){ tgt=trenchX(S.lvl)+d.win; return; }
  };
  return 0; }"""


def main():
    spec = json.loads(sys.argv[1])
    name = spec["name"]; fps = spec.get("fps", 30); w = spec.get("w", 1920); h = spec.get("h", 1080)
    out = os.path.join(spec.get("outdir", "/var/tmp/promo"), name); os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        if f.endswith(".jpg"): os.remove(os.path.join(out, f))
    vt = open(os.path.join(HERE, "vt.js")).read().replace("__SEED__", str(int(spec.get("seed", 1))))
    save = {**FLAGS, "lvl": spec["lvl"], "reserve": spec.get("men", 100) + spec.get("vets", 0) + 50, "vets": spec.get("vets", 0) + 10,
            "income": 400, "econ": 3, "day": 5, "lastPay": int(time.time() * 1000), "moraleT": int(time.time() * 1000)}
    q = spec.get("q", 0.92)
    t0 = time.time()
    with sync_playwright() as p:
        br = p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required", "--use-gl=swiftshader", "--enable-unsafe-swiftshader",
                                      "--disable-background-timer-throttling", "--disable-renderer-backgrounding"])
        ctx = br.new_context(viewport={"width": w, "height": h}, device_scale_factor=spec.get("dsf", 1))
        ctx.add_init_script(vt + "\ntry{localStorage.setItem('charge_save_v3', JSON.stringify(%s));}catch(e){}" % json.dumps(save))
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.goto(URL)
        pg.evaluate(SETUP_JS, spec)
        pg.evaluate("__VT.run(600,50)")
        pg.evaluate("(()=>{ toPlan(); return 0; })()")
        pg.evaluate("__VT.run(1700,50)")
        pg.evaluate("""(spec)=>{ const o=document.getElementById('ov'); if(o&&!o.classList.contains('hide')){ const b=o.querySelector('button'); if(b)b.click(); }
            setWave(0, spec.men||100, Math.min(spec.vets||0, S.vets)); const s=spec.sup||{}; for(const k in s){ used[k]=s[k]; }
            if(spec.waves){ /* extra waves: [[r,v,d],...] */ }
            return 0; }""", spec)
        pg.evaluate("__VT.run(600,50)")
        if spec.get("director"):
            pg.evaluate(DIRECTOR_JS, spec)
        if spec.get("cur"):
            pg.evaluate("(c)=>{ Object.assign(cur,c); return 0; }", spec["cur"])
        if spec.get("nowire"):
            pg.evaluate("(()=>{ belts.length=0; return 0; })()")
        if spec.get("mines") is not None:
            pg.evaluate("(n)=>{ mines.length=Math.min(mines.length,n); cur.mn=mines.length; return 0; }", spec["mines"])
        info = pg.evaluate("JSON.stringify({mode, lvl:S.lvl, sendN, used, gr:cur.gr, mg:cur.mg, W, H, DPR, QUAL})")
        print("setup", info, "errs", errs[:3], f"{time.time()-t0:.1f}s", flush=True)
        pg.evaluate("(()=>{ startCharge(); return 0; })()")
        meta = open(os.path.join(out, "meta.jsonl"), "w")
        dt = 1000.0 / fps
        nmax = int(spec.get("dur", 40) * fps); tail = int(spec.get("tail", 6) * fps)
        won_at = None; f = 0; tl = time.time()
        grab = "(a)=>{ __VT.step(a[0]); const u=a[2]?cv.toDataURL('image/jpeg',a[1]):''; return [u, %s]; }" % META_JS
        every = spec.get("grab_every", 1); g0 = spec.get("grab_from", 0)
        stopf = os.path.join(spec.get("outdir", "/var/tmp/promo"), name + ".stop")
        def dump():
            open(os.path.join(out, "sfx.json"), "w").write(pg.evaluate("JSON.stringify(window.__SFXLOG||[])"))
        while f < nmax:
            want = f >= g0 and (f - g0) % every == 0
            u, m = pg.evaluate(grab, [dt, q, want])
            if u:
                with open(os.path.join(out, f"f{f:05d}.jpg"), "wb") as fh:
                    fh.write(base64.b64decode(u.split(",", 1)[1]))
            if f % 150 == 0: dump(); meta.flush()
            if os.path.exists(stopf): os.remove(stopf); print("stop file", flush=True); break
            md = json.loads(m); md["f"] = f; meta.write(json.dumps(md) + "\n")
            if won_at is None and md.get("mode") == "result":
                won_at = f
            if won_at is not None and f - won_at >= tail:
                break
            f += 1
            if f % 60 == 0:
                print(f"frame {f} t={md['t']/1000:.1f}s mode={md['mode']} bt={md.get('bt')} alive={md.get('alive')} e={md.get('e')} "
                      f"{(time.time()-tl)/60*1000:.0f}ms/f", flush=True); tl = time.time()
        meta.close()
        dump()
        vterr = pg.evaluate("__VT.errs.slice(0,5)")
        print("done frames", f, "won_at", won_at, "errs", errs[:3], vterr, f"{time.time()-t0:.0f}s total", flush=True)
        br.close()


if __name__ == "__main__":
    main()
