#! /usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from schedule import get_schedule
from datetime import datetime
from base64 import b64encode
from urllib import parse
import traceback

# Fall semester, 2017
start_date = datetime(2017, 9, 7)


with open('template.html', 'r') as f:
    template = f.read()


class Server(SimpleHTTPRequestHandler):

    def write_template(self, output):
        self.wfile.write(template.replace(
            '{CONTENTS}', output).encode('utf-8'))

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self._set_headers()
            with open('homepage.html', 'r') as f:
                homepage = f.read()
            self.write_template(homepage)
        else:
            SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        self.send_response(200)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_data = {k: v for k, v in (
            x.split('=') for x in post_data.decode('utf-8').split('&'))}
        error, schedule, warnings = None, None, None
        try:
            schedule, warnings = get_schedule(
                post_data['username'], parse.unquote(post_data['password']), start_date)
        except Exception as e:
            traceback.print_exc()
            error = e
        if schedule:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            encoded_schedule = 'data:application/octet-stream;base64,' + \
                b64encode(str(schedule).encode('utf-8')).decode('utf-8')
            output = '<h1>Schedule created '
            if warnings:
                output += 'with %s warning%s!</h1><ul>' % (
                    len(warnings), '' if len(warnings) == 1 else 's')
                for warning in warnings:
                    output += '<li>' + warning + '</li>'
                output += '</ul>'
            else:
                output += 'successfully!</h1>'
            output += '<h2><a class="button" download="%s" href="%s" title="Download Schedule">Download Schedule</a></h2>' % (
                post_data['username'] + '.ics', encoded_schedule)
            output += '<a href="/"">go back</a>'

            self.write_template(output)
        else:
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            if not error:
                output = '<h1>Incorrect username or password!</h1>'
            else:
                output = "<h1>An internal error occured</h1><pre>" + str(error) + "</pre>"
                print(error)
            output += '<p><a href="/"">go back</a></p>'
            self.write_template(output)


def run(server_class=HTTPServer, handler_class=Server, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
