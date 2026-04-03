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
                    #if ut.containsCapitalLetter(qs[key][0]):
                    #    linker_content = getHTMLDocument("blog/linker.html")
                    #    self.send_response(200)
                    #    self.send_header("Content-Type", "text/html; charset=utf-8")
                    #    self.end_headers()
                    #    self.wfile.write(linker_content.encode("utf-8")) # deprecated # query parameter of URL-https://.../new_task
                    #    return
                    #else:
                    phishing_content = M.applyMacros(getHTMLDocument("blog.html")).format(ut.generateRandomSequence(capitalize=True, length=4)) #, '__ADDITIONAL_TASK_PATH__', '__ADDITIONAL_TASK_KEY__', qs[key][0])
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
        elif path == "/blog/style.css":
            style_sheet = getHTMLDocument("style.css")
            self.send_response(200)
            self.send_header("Content-Type", "text/css; charset=utf-8")
            self.end_headers()
            self.wfile.write(style_sheet.encode("utf-8")) # deprecated # query parameter of URL-https://.../new_task
            return
        elif path == "/__HONEY_POT_PATH__":
            key2 = '__HONEY_POT_KEY__'
            try:
                print(qs[key2])
                if len(qs[key2][0]) == 4 and len(qs) == 2:
                    more_content = getHTMLDocument("destination.html")
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