#!/usr/bin/env python3
"""Cut captured takes into a promo clip + rebuild the soundtrack from the game's own sound calls.

usage: python3 edit.py edl.json
EDL keys:
  w,h,fps          output size (frames of a take are scaled/cropped to fit: "cover")
  takes_dir        where capture.py wrote the takes (default /var/tmp/promo)
  segments         [{take, from, len, zoom:[z0,z1], cx, cy, flash, sfx(0/1), sfx_gain, crop:[x,y,w,h] (source px)}]
  music            {file, start, gain, fade_in, fade_out}
  amb              {sample: gain} constant ambience beds
  extra            [{t (output s), k (sample), v, rate, off, dur, lp}]
  out              output path WITHOUT extension; writes <out>.mp4 (with sound) and <out>_silent.mp4
  alt_crop         optional [{suffix, x, y, w, h}] extra silent crops of the finished video (e.g. 2:3 from 9:16)
"""
import sys, json, os, subprocess, math, random
import numpy as np
from PIL import Image, ImageEnhance

SR = 44100
SFX_DIR = "/var/tmp/promo/sfx"
_cache = {}


def wav(k):
    if k not in _cache:
        p = os.path.join(SFX_DIR, k + ".wav") if not k.startswith("/") else k
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", p, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"],
                             capture_output=True, check=True).stdout
        _cache[k] = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()
    return _cache[k]


def lowpass(x, fc):
    if not fc or fc >= SR / 2: return x
    from scipy.signal import butter, lfilter
    b, a = butter(2, fc / (SR / 2))
    return lfilter(b, a, x, axis=0).astype(np.float32)


def place(bus, x, t, gain, pan=0.0):
    i0 = int(round(t * SR))
    if i0 >= len(bus): return
    if i0 < 0: x = x[-i0:]; i0 = 0
    n = min(len(x), len(bus) - i0)
    if n <= 0: return
    l = math.cos((pan + 1) * math.pi / 4) * math.sqrt(2); r = math.sin((pan + 1) * math.pi / 4) * math.sqrt(2)
    bus[i0:i0 + n, 0] += x[:n, 0] * gain * l
    bus[i0:i0 + n, 1] += x[:n, 1] * gain * r


def render_event(ev, rng):
    k = ev["k"]
    if k.startswith("@"):
        if k == "@tone" and ev.get("f", 0) == 300:   # barrage 'incoming' whistle -> real recording
            k = rng.choice(["inc1", "inc2"]); ev = {**ev, "k": k, "v": 0.5, "dur": 0}
        else:
            return None
    try:
        x = wav(k)
    except Exception:
        return None
    off = ev.get("off", 0) or 0
    if off: x = x[int(off * SR):]
    rate = (ev.get("rate", 1) or 1) * (1 if ev.get("fixed") else (0.93 + rng.random() * 0.14))
    if abs(rate - 1) > 1e-3:
        n = int(len(x) / rate); idx = np.arange(n) * rate
        i = np.minimum(idx.astype(np.int64), len(x) - 2); fr = (idx - i)[:, None].astype(np.float32)
        x = x[i] * (1 - fr) + x[i + 1] * fr
    dur = ev.get("dur", 0) or 0
    if dur:
        n = int(dur * SR); x = x[:n].copy()
        f = min(len(x), int(0.05 * SR))
        if f > 0: x[-f:] *= np.linspace(1, 0, f, dtype=np.float32)[:, None]
    if ev.get("lp"): x = lowpass(x.copy(), ev["lp"])
    return x


def reverb_ir(sec=2.2, seed=3):
    r = np.random.default_rng(seed); n = int(sec * SR)
    env = (1 - np.arange(n) / n) ** 3.2
    return (r.uniform(-1, 1, (n, 2)) * env[:, None]).astype(np.float32)


def fftconv(x, h):
    n = len(x) + len(h) - 1; N = 1 << (n - 1).bit_length(); out = np.zeros((len(x), 2), dtype=np.float32)
    for c in range(2):
        y = np.fft.irfft(np.fft.rfft(x[:, c], N) * np.fft.rfft(h[:, c], N), N)[:len(x)]
        out[:, c] = y
    return out


def main():
    E = json.load(open(sys.argv[1]))
    W, H, fps = E["w"], E["h"], E.get("fps", 30)
    tdir = E.get("takes_dir", "/var/tmp/promo")
    segs = E["segments"]
    total = sum(s["len"] for s in segs)
    dur = total / fps
    out = E["out"]
    os.makedirs(os.path.dirname(out), exist_ok=True)
    rng = random.Random(7)

    # ---------------- AUDIO ----------------
    N = int(dur * SR) + SR
    sfx = np.zeros((N, 2), dtype=np.float32)
    t_out = 0.0
    for s in segs:
        if s.get("sfx", 1):
            meta0 = None
            with open(os.path.join(tdir, s["take"], "meta.jsonl")) as fh:
                for i, line in enumerate(fh):
                    if i == s["from"]: meta0 = json.loads(line); break
            L = json.load(open(os.path.join(tdir, s["take"], "sfx.json")))
            ts0 = meta0["t"] / 1000.0; ts1 = ts0 + s["len"] / fps
            g = s.get("sfx_gain", 1.0); skip = set(s.get("skip", []))
            for ev in L:
                te = ev["t"] / 1000.0 + (ev.get("d", 0) or 0)
                if ts0 - s.get("pre", 0.0) <= te < ts1 - 0.05 and ev["k"] not in skip:
                    x = render_event(ev, rng)
                    if x is None: continue
                    pan = ev["pan"] if ev.get("pan") is not None else (rng.random() - 0.5) * 0.6
                    if te < ts0:   # started just before the cut: keep its tail
                        x = x[int((ts0 - te) * SR):]; te = ts0
                    # hard cut: sounds end with the shot unless they are long 'tails'
                    keep = s.get("tail", 0.35)
                    n = int((ts1 - te + keep) * SR)
                    if n < len(x):
                        x = x[:n].copy(); f = min(len(x), int(keep * SR * 0.9) or 1)
                        x[-f:] *= np.linspace(1, 0, f, dtype=np.float32)[:, None]
                    place(sfx, x, t_out + (te - ts0), ev.get("v", 1) * g, pan)
        t_out += s["len"] / fps
    for ex in E.get("extra", []):
        x = render_event({"fixed": 1, **ex}, rng)
        if x is not None: place(sfx, x, ex["t"], ex.get("v", 1), ex.get("pan", 0))
    # room reverb like the game (dry + 0.32 wet)
    wet = fftconv(sfx, reverb_ir()) * 0.32 / 40.0
    bus = sfx * 0.8 + wet * 0.8
    # ambience beds
    for k, g in (E.get("amb") or {}).items():
        x = wav(k); reps = int(math.ceil(N / len(x))) + 1; x = np.tile(x, (reps, 1))[:N]
        bus += x * g
    # music
    mus = np.zeros_like(bus)
    if E.get("music"):
        M = E["music"]; x = wav(M["file"])[int(M.get("start", 0) * SR):][:N].copy()
        fi, fo = M.get("fade_in", 0), M.get("fade_out", 0.8)
        if fi: n = int(fi * SR); x[:n] *= np.linspace(0, 1, n, dtype=np.float32)[:, None]
        end = int(dur * SR)
        if fo: n = int(fo * SR); x[end - n:end] *= np.linspace(1, 0, n, dtype=np.float32)[:, None]; x[end:] = 0
        mus[:len(x)] = x * M.get("gain", 0.6)
        for d in M.get("duck", []):      # [t0,t1,gain]
            a, b = int(d[0] * SR), int(d[1] * SR); mus[a:b] *= d[2]
    mix = bus + mus
    mix = mix[:int(dur * SR)]
    # gentle fade in/out on the whole mix
    n = int(0.03 * SR); mix[:n] *= np.linspace(0, 1, n, dtype=np.float32)[:, None]
    n = int(E.get("end_fade", 0.6) * SR); mix[-n:] *= np.linspace(1, 0, n, dtype=np.float32)[:, None]
    raw = os.path.join(os.path.dirname(out), os.path.basename(out) + "_raw.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-af", "acompressor=threshold=-16dB:ratio=3:attack=5:release=120,loudnorm=I=-14:TP=-1.5:LRA=9,alimiter=limit=0.89",
                    "-ar", str(SR), raw], input=mix.astype(np.float32).tobytes(), check=True)
    print("audio", raw, f"{dur:.2f}s", flush=True)

    # ---------------- VIDEO ----------------
    silent = out + "_silent.mp4"
    enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(fps),
                            "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", str(E.get("crf", 17)), "-pix_fmt", "yuv420p",
                            "-profile:v", "high", "-movflags", "+faststart", silent], stdin=subprocess.PIPE)
    fo = 0
    for s in segs:
        z0, z1 = (s.get("zoom") or [1, 1])
        for i in range(s["len"]):
            p = os.path.join(tdir, s["take"], f"f{s['from'] + i:05d}.jpg")
            im = Image.open(p).convert("RGB")
            if s.get("crop"):
                x, y, w, h = s["crop"]; im = im.crop((x, y, x + w, y + h))
            sw, sh = im.size
            k = i / max(1, s["len"] - 1); ez = k * k * (3 - 2 * k) if s.get("ease", 1) else k
            z = z0 + (z1 - z0) * ez
            sc = max(W / sw, H / sh) * z                  # cover + zoom
            cw, ch = W / sc, H / sc
            cxp = s.get("cx", 0.5) + (s.get("cx1", s.get("cx", 0.5)) - s.get("cx", 0.5)) * ez
            cyp = s.get("cy", 0.5) + (s.get("cy1", s.get("cy", 0.5)) - s.get("cy", 0.5)) * ez
            x0 = min(max(0, cxp * sw - cw / 2), sw - cw); y0 = min(max(0, cyp * sh - ch / 2), sh - ch)
            im = im.resize((W, H), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))
            fl = s.get("flash", 0)
            if fl and i < 4:
                a = fl * (1 - i / 4)
                im = Image.blend(im, Image.new("RGB", (W, H), (255, 248, 232)), a)
            if s.get("bright"):
                im = ImageEnhance.Brightness(im).enhance(s["bright"])
            enc.stdin.write(im.tobytes()); fo += 1
    enc.stdin.close(); enc.wait()
    print("video", silent, fo, "frames", flush=True)
    final = out + ".mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-i", raw, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", final], check=True)
    print("final", final, flush=True)
    for a in E.get("alt_crop", []):
        o = out + a["suffix"] + ".mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", silent, "-vf", f"crop={a['w']}:{a['h']}:{a['x']}:{a['y']}",
                        "-c:v", "libx264", "-preset", "slow", "-crf", str(E.get("crf", 17)), "-pix_fmt", "yuv420p", "-an",
                        "-movflags", "+faststart", o], check=True)
        print("alt", o, flush=True)


if __name__ == "__main__":
    main()
