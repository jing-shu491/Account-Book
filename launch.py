"""跨平台启动器：服务就绪后自动打开浏览器。"""
import os
import threading
import webbrowser
from http.server import ThreadingHTTPServer
from server import Handler

def main():
    port = int(os.environ.get('PORT', '8877'))
    try:
        server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    except OSError:
        print('端口 %s 已被占用。请关闭已启动的记账服务，或设置 PORT 后重试。' % port)
        return
    url = 'http://127.0.0.1:%s' % port
    print('余白已启动：' + url)
    print('保持此窗口开启；关闭窗口或按 Ctrl+C 停止服务。')
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
