"""Mirror channel logos into logos/ (some logo hosts, e.g. imgur, are blocked in RU/BY).
Usage: python3 fetch_logos.py <playlist.m3u>  -> downloads missing logos as logos/<sha1>.png"""
import hashlib, io, os, re, sys, urllib.request
from PIL import Image
root = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(root, 'logos'); os.makedirs(out, exist_ok=True)
urls = sorted(set(re.findall(r'tvg-logo="(https?://[^"]+)"', open(sys.argv[1], encoding='utf-8').read())))
ok = fail = 0
for u in urls:
    if 'raw.githubusercontent.com/Zhnec91477' in u: continue
    fn = os.path.join(out, hashlib.sha1(u.encode()).hexdigest()[:16] + '.png')
    if os.path.exists(fn): continue
    try:
        m = re.match(r'https://upload\.wikimedia\.org/wikipedia/(\w+)/(\w)/(\w\w)/([^/]+\.svg)$', u)
        src = f'https://upload.wikimedia.org/wikipedia/{m[1]}/thumb/{m[2]}/{m[3]}/{m[4]}/256px-{m[4]}.png' if m else u
        req = urllib.request.Request(src, headers={'User-Agent': 'IPTV-playlist-logo-mirror/1.0 (github.com/Zhnec91477/IPTV)'})
        data = urllib.request.urlopen(req, timeout=20).read()
        try:
            im = Image.open(io.BytesIO(data)); im.load()
        except Exception:
            if b'<svg' not in data[:3000]: raise
            import subprocess, tempfile
            with tempfile.TemporaryDirectory() as td:
                src = os.path.join(td, 'in.svg'); dst = os.path.join(td, 'out.png')
                open(src, 'wb').write(data)
                subprocess.run(['convert', '-background', 'none', '-density', '200', src, '-resize', '256x256', dst], check=True, timeout=60)
                im = Image.open(dst); im.load()
        im = im.convert('RGBA'); im.thumbnail((256, 256))
        im.save(fn, 'PNG', optimize=True); ok += 1
    except Exception as e:
        fail += 1; print('fail', u, e, file=sys.stderr)
print('logos downloaded', ok, 'failed', fail)
