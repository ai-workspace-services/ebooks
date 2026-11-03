#!/usr/bin/env python3
"""Fetch a book's binary assets (images) from Google Drive by file id, verify sha256, extract in place.

Usage: fetch_assets.py assets.manifest.json   (run inside books/<slug>/)
Auth (first match wins):
  GDRIVE_SA_JSON       service-account JSON (contents or path) with read access to the files
  GDRIVE_ACCESS_TOKEN  OAuth access token
  (none)               public HTTPS download, incl. large-file confirm token (works only if the Drive files are shared "anyone with link")
Exit 0 = assets ready; exit 78 = assets unavailable (no credentials / no access) -> caller may skip.
"""
import hashlib, html, json, os, re, sys, tarfile, tempfile, time, urllib.error, urllib.parse, urllib.request

def sha(b): return hashlib.sha256(b).hexdigest()

def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        while chunk := f.read(1 << 20): h.update(chunk)
    return h.hexdigest()

def present_ok(m, key='files'):
    for f in m.get(key, []):
        if not os.path.exists(f['path']): return False
        if sha_file(f['path']) != f['sha256']: return False
    return True

def token():
    if os.environ.get('GDRIVE_ACCESS_TOKEN'): return os.environ['GDRIVE_ACCESS_TOKEN']
    sa = os.environ.get('GDRIVE_SA_JSON', '').strip()
    if not sa: return None
    info = json.load(open(sa)) if os.path.exists(sa) else json.loads(sa)
    from google.oauth2 import service_account          # pip install google-auth requests
    import google.auth.transport.requests as tr
    c = service_account.Credentials.from_service_account_info(info, scopes=['https://www.googleapis.com/auth/drive.readonly'])
    c.refresh(tr.Request()); return c.token

UA = {'User-Agent': 'ebooks-fetch-assets/1.0'}

def _open(url, headers):
    return urllib.request.urlopen(urllib.request.Request(url, headers={**UA, **headers}), timeout=600)

def _public(fid):
    """Anonymous download of an 'anyone with the link' file, handling the large-file virus-scan confirm page."""
    url = f'https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t'
    r = _open(url, {})
    if 'text/html' in r.headers.get('Content-Type', ''):
        page = r.read().decode('utf-8', 'replace')
        form = re.search(r'<form[^>]+action="([^"]+)"', page)
        fields = dict(re.findall(r'name="([^"]+)" value="([^"]*)"', page))
        if not form or 'confirm' not in fields:
            raise OSError('Drive returned an HTML page (file not shared publicly?)')
        r = _open(html.unescape(form.group(1)) + '?' + urllib.parse.urlencode(fields), {})
        if 'text/html' in r.headers.get('Content-Type', ''):
            raise OSError('Drive confirm step returned HTML')
    return r

def get(fid, tok, dest):
    """Stream one Drive file to dest; return its sha256. Retries 3x."""
    for attempt in range(3):
        try:
            r = (_open(f'https://www.googleapis.com/drive/v3/files/{fid}?alt=media&supportsAllDrives=true',
                       {'Authorization': f'Bearer {tok}'}) if tok else _public(fid))
            h = hashlib.sha256()
            with open(dest, 'wb') as out:
                while chunk := r.read(1 << 20):
                    h.update(chunk); out.write(chunk)
            return h.hexdigest()
        except (urllib.error.URLError, OSError) as e:
            if attempt == 2: raise
            print(f'assets: retry {fid} after {e}'); time.sleep(5 * (attempt + 1))

def main():
    m = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'assets.manifest.json'))
    if present_ok(m) and present_ok(m, 'extra_files'):
        print(f"assets: {m['book']} already present ({len(m['files'])} files)"); return 0
    tok = token()
    if not tok: print('assets: no GDRIVE_SA_JSON / GDRIVE_ACCESS_TOKEN -> public mode (Drive files must be shared "anyone with the link")')
    for f in m.get('extra_files', []):
        if os.path.exists(f['path']) and sha(open(f['path'], 'rb').read()) == f['sha256']: continue
        os.makedirs(os.path.dirname(f['path']) or '.', exist_ok=True)
        try: got = get(f['drive_file_id'], tok, f['path'])
        except (urllib.error.URLError, OSError) as e:
            print(f"::warning::assets for {m['book']} unavailable ({f['path']}: {e}). Set repo secret GDRIVE_SA_JSON or share the Drive files; see README."); return 78
        if got != f['sha256']:
            os.remove(f['path']); print(f"::warning::assets for {m['book']}: {f['path']} sha256 mismatch"); return 78
    if present_ok(m) and present_ok(m, 'extra_files'):
        print(f"assets: {m['book']} ready ({len(m['files'])} files)"); return 0
    tmp = tempfile.mkdtemp(prefix='assets-', dir='.')
    tar = os.path.join(tmp, 'reassembled.tar')
    try:
        with open(tar, 'wb') as whole:
            for i, p in enumerate(m['archive']['parts']):
                part = os.path.join(tmp, f'part-{i:02d}.bin')
                t0 = time.time()
                try: got = get(p['drive_file_id'], tok, part)
                except (urllib.error.URLError, OSError) as e:
                    print(f"::warning::assets for {m['book']} unavailable ({p['name']}: {e}). "
                          "Set repo secret GDRIVE_SA_JSON or share the Drive files; see README.")
                    return 78
                if got != p['sha256']:
                    print(f"::warning::assets for {m['book']}: {p['name']} sha256 mismatch"); return 78
                print(f"assets: {p['name']} {os.path.getsize(part)/1e6:.0f} MB in {time.time()-t0:.0f}s")
                with open(part, 'rb') as src:
                    while chunk := src.read(1 << 20): whole.write(chunk)
                os.remove(part)
        if m['archive'].get('sha256') and sha_file(tar) != m['archive']['sha256']:
            print('assets: reassembled archive sha256 mismatch'); return 1
        with tarfile.open(tar) as t: t.extractall('.', filter='data')
    finally:
        import shutil; shutil.rmtree(tmp, ignore_errors=True)
    if not present_ok(m): print('assets: extracted files fail sha256 check'); return 1
    print(f"assets: {m['book']} fetched {len(m['files'])} files"); return 0

if __name__ == '__main__': sys.exit(main())
