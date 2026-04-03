from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import ssl
import utilities as ut
import macro as M

import hashlib

m = hashlib.sha256()

HOST = "0.0.0.0"
PORT = 443  # HTTPS 기본 포트 (권한 필요: 보통 sudo로 실행)

CERT_PEM = "fullchain.pem"  # 공개키/인증서 체인 (예: fullchain.pem)
KEY_PEM  = "privkey.pem"    # 개인키 (예: privkey.pem)

def sanitizeNewLine(string: str):
    return string.replace("\n", "")

def getHTMLDocument(path):
    content = ""
    file = open(path, "r", encoding='utf-8')
    while True:
        line = file.readline()
        if not line:
            break
        content += line
    return content

robots_txt = getHTMLDocument("robots.txt")
#phishing_content = getHTMLDocument("redirect_4.html") # -> attacking

from datetime import datetime
additional_task = sanitizeNewLine(getHTMLDocument("additional_task.html"))

def sanitizeCharacters(text: str, characters: list):
    characters.append("/")
    for character in characters:
        text = text.replace(character, "")
    return text


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        print(self.path)
        print(path)
        qs = parse_qs(parsed.query)
        print(qs)

        if path == "/__BLOG_PATH__/index.html":
            key = '__BLOG_KEY__'
            try:
                print(qs[key][0])
                if qs[key][0] != '' and len(qs) == 1:
                    print("!!!!!!!!!!!!!!!")
                    if ut.containsCapitalLetter(qs[key][0]):
                        linker_content = getHTMLDocument("blog/linker.html")
                        self.send_response(200)
                        self.send_header("Content-Type", "text/html; charset=utf-8")
                        self.end_headers()
                        self.wfile.write(linker_content.encode("utf-8")) # deprecated # query parameter of URL-https://.../new_task
                        return
                    else:
                        phishing_content = M.applyMacros(getHTMLDocument("blog/blog3.html")).format(ut.generateRandomSequence(capitalize=True, length=4), ut.generateRandomSequence(capitalize=True, length=4)) #, '__ADDITIONAL_TASK_PATH__', '__ADDITIONAL_TASK_KEY__', qs[key][0])
                        self.send_response(200)
                        self.send_header("Content-Type", "text/html; charset=utf-8")
                        self.end_headers()
                        self.wfile.write(phishing_content.encode("utf-8")) # deprecated # query parameter of URL-https://.../new_task
                        return
                else:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("{\n  \"message\": \"Invalid query parameter: __BLOG_KEY__\"\n}".encode('utf-8'))
                    return
            except Exception as e:
                print(e)
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write("{\n  \"message\": \"Invalid query parameter: __BLOG_KEY__\"\n}".encode('utf-8'))
                return
        elif path == "/conversation":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write("Great job!".encode('utf-8'))
        elif path == "/count":
            import utilities as ut
            c = -1
            try:
                c = ut.getGlobalVariable("COUNT")
            except:
                c = -1
            c += 1
            ut.setGlobalVariable("COUNT", c)

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(f"{c}".encode('utf-8'))

        elif path == "/blog/style.css":
            style_sheet = getHTMLDocument("./blog/style.css")
            self.send_response(200)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.end_headers()
            self.wfile.write(style_sheet.encode("utf-8")) # deprecated # query parameter of URL-https://.../new_task
            return
        elif path == "/__ADDITIONAL_TASK_PATH__":
            key1 = '__ADDITIONAL_TASK_KEY__'
            try:
                print(qs['for'][0])
                if qs['for'][0] == 'Agent' and len(qs) == 2 and qs[key1][0] != '':
                    additional_task = sanitizeNewLine(getHTMLDocument("additional_task.html"))
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(additional_task.format(qs[key1][0]).encode('utf-8')) # deprecated # query parameter of URL-https://.../new_task
                    return
                else:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("{\n  \"message\": \"Invalid query parameters: for, __ADDITIONAL_TASK_KEY__\"\n}".encode('utf-8'))
                    return
            except:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write("{\n  \"message\": \"Invalid query parameters: for, __ADDITIONAL_TASK_KEY__\"\n}".encode('utf-8'))
                return
        elif path == "/__HONEY_POT_PATH__":
            key2 = '__HONEY_POT_KEY__'
            try:
                print(qs[key2])
                if qs[key2][0] != 'YYYYMMDD' and len(qs[key2][0]) == 8 and len(qs['update_date'][0]) == 8 and len(qs) == 2:
                    more_content = getHTMLDocument("more_info.html")
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(more_content.encode("utf-8")) # deprecated # query parameter of URL-https://.../new_task
                    return
                else:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("{\n  \"message\": \"Invalid query parameters: update_date, __HONEY_POT_KEY__\"\n}".encode('utf-8'))
                    return
            except:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write("{\n  \"message\": \"Invalid query parameters: update_date, __HONEY_POT_KEY__\"\n}".encode('utf-8'))
                return
        elif path == "/robots.txt":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(robots_txt.encode('utf-8'))
        
        elif path[:5] == "/main":
            sp = path.split("/")[2]
            if sp == "index.html":
                content = getHTMLDocument("main/index.html")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=UTF-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            elif sp == "style.css":
                content = getHTMLDocument("main/style.css")
                self.send_response(200)
                self.send_header("Content-Type", "text/css; charset=UTF-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            elif sp == "script.js":
                content = getHTMLDocument("main/script.js")
                self.send_response(200)
                self.send_header("Content-Type", "application/javascript; charset=UTF-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            elif sp == "main_screen.png":
                with open("main/main_screen.png", "rb") as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "image/png")
                    self.end_headers()
                    self.wfile.write(content)
            else:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"page not found".encode("utf-8"))
        elif path[:7] == "/search":
            sp = path.split("/")[2]
            if sp == "index.html":
                content = getHTMLDocument("search/index.html")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=UTF-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            elif sp == "style.css":
                content = getHTMLDocument("search/style.css")
                self.send_response(200)
                self.send_header("Content-Type", "text/css; charset=UTF-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            elif sp == "script.js":
                content = M.applyMacros(getHTMLDocument("search/script.js")).replace("_PLACEHOLDER_", ut.generateRandomSequence(capitalize=False, length=4))
                self.send_response(200)
                self.send_header("Content-Type", "application/javascript; charset=UTF-8")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            elif sp == "search.png":
                with open("search/search.png", "rb") as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "image/png")
                    self.end_headers()
                    self.wfile.write(content)
            else:
                self.send_response(404)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(f"page not found".encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"page not found".encode("utf-8"))




        self.send_response(200)

    # 로그 끄고 싶으면 주석 해제
    # def log_message(self, format, *args):
    #     return

def main():
    httpd = HTTPServer((HOST, PORT), Handler)

    # TLS 컨텍스트 생성 (서버용)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(certfile=CERT_PEM, keyfile=KEY_PEM)

    # HTTPServer의 소켓을 TLS로 감싸기
    httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

    print(f"HTTPS server running: https://{HOST}:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    main()