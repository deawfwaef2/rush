#!/usr/bin/env python3
"""Build the portal ZIPs from the repo (index.html + audio/ + CREDITS.md).

    python3 tools/build_zips.py [out_dir]        (default: ../zips next to the repo - never commit the ZIPs)

Outputs
  rush-crazygames.zip  window.PLATFORM="crazygames" + CrazyGames HTML5 SDK v3
  rush-playgama.zip    window.PLATFORM="playgama"   + Playgama Bridge v2 (CDN) + playgama-bridge-config.json
  rush-web.zip         window.PLATFORM="web"        no SDK at all (offline, double-click index.html)

index.html must contain the <!--PLATFORM:BEGIN ... PLATFORM:END--> block; it is replaced per build.
"""
import os, re, sys, zipfile, json, datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(os.path.join(REPO, "..", "zips"))

BLOCKS = {
    "crazygames": '<script>window.PLATFORM="crazygames";</script>\n'
                  '<script src="https://sdk.crazygames.com/crazygames-sdk-v3.js"></script>',
    "playgama":   '<script>window.PLATFORM="playgama";</script>\n'
                  '<script src="https://bridge.playgama.com/v2/stable/playgama-bridge.js"></script>',
    "web":        '<script>window.PLATFORM="web";</script>',
}
EXTRA = {"playgama": {"playgama-bridge-config.json": os.path.join(REPO, "tools", "playgama-bridge-config.json")}}
INCLUDE_FILES = ["CREDITS.md"]
INCLUDE_DIRS = ["audio"]


def build(name, html):
    pat = re.compile(r"<!--PLATFORM:BEGIN.*?-->.*?<!--PLATFORM:END-->", re.S)
    if not pat.search(html):
        sys.exit("PLATFORM marker block not found in index.html")
    stamp = datetime.date.today().isoformat()
    page = pat.sub(lambda m: f"<!--PLATFORM build: {name} ({stamp})-->\n" + BLOCKS[name], html, count=1)
    path = os.path.join(OUT, f"rush-{name}.zip")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        z.writestr("index.html", page)
        for f in INCLUDE_FILES:
            p = os.path.join(REPO, f)
            if os.path.exists(p):
                z.write(p, f)
        for d in INCLUDE_DIRS:
            for root, _, files in os.walk(os.path.join(REPO, d)):
                for f in sorted(files):
                    full = os.path.join(root, f)
                    z.write(full, os.path.relpath(full, REPO))
        for arc, src in EXTRA.get(name, {}).items():
            json.load(open(src, encoding="utf-8"))  # must be valid JSON
            z.write(src, arc)
    return path


def main():
    os.makedirs(OUT, exist_ok=True)
    html = open(os.path.join(REPO, "index.html"), encoding="utf-8").read()
    for name in BLOCKS:
        p = build(name, html)
        with zipfile.ZipFile(p) as z:
            n = len(z.namelist())
            assert "index.html" in z.namelist()
        print(f"{os.path.basename(p):24s} {os.path.getsize(p)/1e6:5.2f} MB  {n} files")


if __name__ == "__main__":
    main()
