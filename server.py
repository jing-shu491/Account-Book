from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
import json, threading, csv, io, os
import storage, records, stats, ai_analysis
LOCK = threading.Lock()
class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw): super().__init__(*a,directory=str(Path(__file__).parent/'static'),**kw)
    def reply(self, data, status=200):
        body=json.dumps(data,ensure_ascii=False).encode(); self.send_response(status); self.send_header('Content-Type','application/json; charset=utf-8'); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        u=urlparse(self.path)
        if u.path=='/api/records':
            try:
                rows=records.select(storage.read(),{k:v[0] for k,v in parse_qs(u.query).items()})
                self.reply(dict(records=rows,stats=stats.summarize(rows)))
            except (ValueError,ArithmeticError) as e: self.reply({'error':str(e)},400)
        elif u.path=='/api/export':
            body=json.dumps(storage.read(),ensure_ascii=False,indent=2).encode(); self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Disposition','attachment; filename="ledger-backup.json"'); self.end_headers(); self.wfile.write(body)
        else: super().do_GET()
    def do_POST(self):
        try:
            if urlparse(self.path).path=='/api/analyze':
                q={k:v[0] for k,v in parse_qs(urlparse(self.path).query).items()}
                self.reply({'analysis':ai_analysis.analyze(records.select(storage.read(),q))}); return
            if self.path!='/api/records': self.reply({'error':'接口不存在'},404); return
            data=json.loads(self.rfile.read(int(self.headers.get('Content-Length',0))))
            row=records.validate(data)
            with LOCK:
                rows=storage.read(); rows.append(row); storage.write(rows)
            self.reply(row,201)
        except (ValueError,KeyError,TypeError) as e: self.reply({'error':str(e)},400)
    def do_DELETE(self):
        ident=self.path.removeprefix('/api/records/')
        with LOCK:
            rows=storage.read(); storage.write([r for r in rows if r['id']!=ident])
        self.reply({'ok':True})
if __name__=='__main__':
    port=int(os.environ.get('PORT','8877'))
    server=ThreadingHTTPServer(('127.0.0.1',port),Handler)
    print(f'余白已启动：http://127.0.0.1:{port}',flush=True)
    server.serve_forever()
