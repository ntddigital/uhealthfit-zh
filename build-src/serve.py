#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本機預覽伺服器：模擬 Cloudflare Pages 的行為，讓建好的靜態網站在本機也能用乾淨網址瀏覽。
用法：python3 build-src/serve.py [port]（預設 8766，或環境變數 PORT），然後開 http://localhost:8766/
- /about、/products/calmoon → 對應的 .html；/blog/ → blog/index.html
- /about.html → 308 轉址到 /about（Cloudflare 也是這樣）
- 不存在的網址 → 以 404.html 回應 HTTP 404
追蹤碼只在 us.uhealthfit.com 啟用，本機預覽不會把資料送進 GA4／GTM／Meta。
"""
import os, sys, posixpath
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

DIST = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=DIST, **kw)

    def _exists(self, rel):
        return os.path.isfile(os.path.join(DIST, rel.lstrip('/')))

    def do_GET(self):
        u = urlsplit(self.path); path = posixpath.normpath(u.path) if u.path != '/' else '/'
        query = ('?' + u.query) if u.query else ''
        # .html 網址 → 308 到乾淨網址
        if path.endswith('/index.html') or path == '/index.html':
            return self._redirect(path[:-len('index.html')] + query)
        if path.endswith('.html') and path != '/404.html':
            return self._redirect(path[:-len('.html')] + query)
        if u.path.endswith('/') and path != '/': path += '/'
        if path.endswith('/'):
            if self._exists(path + 'index.html'):
                self.path = path + 'index.html' + query; return super().do_GET()
        elif self._exists(path) and not os.path.isdir(os.path.join(DIST, path.lstrip('/'))):
            self.path = path + query; return super().do_GET()
        elif self._exists(path + '.html'):
            self.path = path + '.html' + query; return super().do_GET()
        elif os.path.isdir(os.path.join(DIST, path.lstrip('/'))):
            return self._redirect(path + '/' + query)
        return self._not_found()

    def _redirect(self, to):
        self.send_response(308); self.send_header('Location', to); self.end_headers()

    def _not_found(self):
        page = os.path.join(DIST, '404.html')
        if not os.path.isfile(page): return self.send_error(404)
        body = open(page, 'rb').read()
        self.send_response(404); self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get('PORT', 8766))
    print(f'serving {DIST} at http://localhost:{port}/  (clean URLs + 404.html, no tracking)')
    ThreadingHTTPServer(('', port), Handler).serve_forever()
