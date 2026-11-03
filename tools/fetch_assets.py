#!/usr/bin/env python3
"""Fetch a book's binary assets (images) from Google Drive by file id, verify sha256, extract in place.

Usage: fetch_assets.py assets.manifest.json   (run inside books/<slug>/)
Auth (first match wins):
  GDRIVE_SA_JSON       service-account JSON (contents or path) with read access to the files
  GDRIVE_ACCESS_TOKEN  OAuth access token
  (none)               public download (works only if the Drive files are shared "anyone with link")
Exit 0 = assets ready; exit 78 = assets unavailable (no credentials / no access) -> caller may skip.
"""
import hashlib, io, json, os, sys, tarfile, urllib.request, urllib.error

def sha(b): return hashlib.sha256(b).hexdigest()

def present_ok(m, key='files'):
    for f in m.get(key, []):
        if not os.path.exists(f['path']): return False
    return all(sha(open(f['path'], 'rb').read()) == f['sha256'] for f in m.get(key, []))

def token():
    if os.environ.get('GDRIVE_ACCESS_TOKEN'): return os.environ['GDRIVE_ACCESS_TOKEN']
    sa = os.environ.get('GDRIVE_SA_JSON', '').strip()
    if not sa: return None
    info = json.load(open(sa)) if os.path.exists(sa) else json.loads(sa)
    from google.oauth2 import service_account          # pip install google-auth requests
    import google.auth.transport.requests as tr
    c = service_account.Credentials.from_service_account_info(info, scopes=['https://www.googleapis.com/auth/drive.readonly'])
    c.refresh(tr.Request()); return c.token

def get(fid, tok):
    if tok:
        req = urllib.request.Request(f'https://www.googleapis.com/drive/v3/files/{fid}?alt=media&supportsAllDrives=true',
                                     headers={'Authorization': f'Bearer {tok}'})
    else:
        req = urllib.request.Request(f'https://drive.usercontent.google.com/download?id={fid}&export=download&confirm=t')
    with urllib.request.urlopen(req, timeout=600) as r: return r.read()

def main():
    m = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'assets.manifest.json'))
    if present_ok(m) and present_ok(m, 'extra_files'):
        print(f"assets: {m['book']} already present ({len(m['files'])} files)"); return 0
    tok = token()
    if not tok: print('assets: no GDRIVE_SA_JSON / GDRIVE_ACCESS_TOKEN; trying public Drive download')
    for f in m.get('extra_files', []):
        try: data = get(f['drive_file_id'], tok)
        except (urllib.error.URLError, OSError) as e:
            print(f"::warning::assets for {m['book']} unavailable ({f['path']}: {e}). Set repo secret GDRIVE_SA_JSON or share the Drive files; see README."); return 78
        if sha(data) != f['sha256']:
            print(f"::warning::assets for {m['book']}: {f['path']} sha256 mismatch (no access?)"); return 78
        os.makedirs(os.path.dirname(f['path']) or '.', exist_ok=True); open(f['path'], 'wb').write(data)
    if present_ok(m): print(f"assets: {m['book']} ready"); return 0
    buf = io.BytesIO()
    for p in m['archive']['parts']:
        try: data = get(p['drive_file_id'], tok)
        except (urllib.error.URLError, OSError) as e:
            print(f"::warning::assets for {m['book']} unavailable ({p['name']}: {e}). "
                  "Set repo secret GDRIVE_SA_JSON or share the Drive files; see README.")
            return 78
        if sha(data) != p['sha256']:
            print(f"::warning::assets for {m['book']}: {p['name']} sha256 mismatch (no access / HTML page returned?)"); return 78
        buf.write(data)
    buf.seek(0)
    with tarfile.open(fileobj=buf) as t: t.extractall('.', filter='data')
    if not present_ok(m): print('assets: extracted files fail sha256 check'); return 1
    print(f"assets: {m['book']} fetched {len(m['files'])} files"); return 0

if __name__ == '__main__': sys.exit(main())
