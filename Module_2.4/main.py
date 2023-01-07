from http.server import HTTPServer, BaseHTTPRequestHandler
import mimetypes
import pathlib
import urllib.parse
import socket
import threading
from datetime import datetime
import json

UDP_IP = '127.0.0.1'
UDP_PORT = 5000
HTTP_PORT = 3000


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('front-init/index.html')
        elif pr_url.path == '/message.html':
            self.send_html_file('front-init/message.html')
        else:
            if pathlib.Path().joinpath(
                    pathlib.Path('front-init', pr_url.path[1:])
            ).exists():
                self.send_static('front-init')
            else:
                self.send_html_file('front-init/error.html', 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        self.send_to_socket(data)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self, path_prefix: str, status=200):
        self.send_response(status)
        path = pathlib.Path().joinpath(
            pathlib.Path(path_prefix, self.path[1:]))
        mt = mimetypes.guess_type(path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'{path}', 'rb') as file:
            self.wfile.write(file.read())

    def send_to_socket(self, message):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server = UDP_IP, UDP_PORT
        sock.sendto(message, server)
        print(f'Sending data: {message.decode()} to server: {server}\n')
        response, address = sock.recvfrom(1024)
        print(f'Response: {response.decode()} from server: {address}')
        sock.close()


class Http_Server():
    def run_server(self, server_class=HTTPServer, handler_class=HttpHandler):
        server_address = ('', HTTP_PORT)
        http = server_class(server_address, handler_class)
        try:
            http.serve_forever()
        except KeyboardInterrupt:
            http.server_close()


class Socket_Server():
    def run_server(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server = UDP_IP, UDP_PORT
        sock.bind(server)
        try:
            while True:
                data, address = sock.recvfrom(1024)
                sock.sendto(b'OK', address)
                data_parse = urllib.parse.unquote_plus(data.decode())
                data_dict = {key: value for key, value in [
                    el.split('=') for el in data_parse.split('&')]}
                print(f'Parsed received data: {data_dict} from: {address}\n')
                path = pathlib.Path().joinpath(pathlib.Path('storage\data.json'))
                if path.exists():
                    self.save_data_to_json(data_dict, path)
        except KeyboardInterrupt:
            print(f'Dismiss server')
        finally:
            sock.close()

    def save_data_to_json(self, data_dict, file_path):
        data = {}
        data[str(datetime.now())] = data_dict
        with open(file_path, 'r+') as file:
            file_data = json.load(file)
            file_data.update(data)
            file.seek(0)
            json.dump(file_data, file)


if __name__ == '__main__':
    http_server = Http_Server()
    socket_server = Socket_Server()
    http_thread = threading.Thread(target=http_server.run_server)
    socket_thread = threading.Thread(target=socket_server.run_server)
    http_thread.start()
    socket_thread.start()
