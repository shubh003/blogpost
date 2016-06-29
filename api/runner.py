#!/usr/bin/env python

import json
from urlparse import parse_qs
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

from data_handler import DataHandler
from settings import PORT_NUMBER, GET_URL_MAPPER, POST_URL_MAPPER, DELETE_URL_MAPPER

dat_handler = DataHandler()

class RequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def _extract_params(self):
        params_parsed = {}

        split_params = self.path.split('?')
        if len(split_params) > 1:
            params_parsed = parse_qs(split_params[1])

        return params_parsed

    def _extract_data(self):
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(data_string)

        return data

    def _check_authentication(self):
        global key
        is_admin = False
        if self.headers.getheader('Authorization'):
            auth_header = self.headers.getheader('Authorization')
            key = auth_header.split('Token ')[1]

            if key in dat_handler.admin_dict.values():
                is_admin = True

        return is_admin

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        for url, func in GET_URL_MAPPER.items():
            matched = url.match(self.path)
            if not matched:
                continue

            # Get url embedded variables
            args_dict = matched.groupdict()

            # Get params
            params = self._extract_params()

            args_dict.update(**params)

            # Fetch results
            result_list = getattr(dat_handler, func)(**args_dict)
            results = {"results": result_list}

            # Create response with data
            self._set_headers()
            self.wfile.write(json.dumps(results))
            return

        self.send_error(404, 'Invalid URL: %s' % (self.path, ))

    def do_POST(self):
        for url, func in POST_URL_MAPPER.items():
            matched = url.match(self.path)

            if not matched:
                continue

            # Get url embedded variables
            args_dict = matched.groupdict()

            # Get post data
            data = self._extract_data()

            # Get params
            params = self._extract_params()

            # Merge all args
            args_dict.update(**data)
            args_dict.update(**params)

            # Admin Check
            args_dict['is_admin'] = self._check_authentication()

            # Send data to sql
            response = getattr(dat_handler, func)(**args_dict)
            if 'admin_error' in response:
                self.do_AUTHHEAD()
            else:
                self._set_headers()

            self.wfile.write(json.dumps(response))
            return
        
        self.send_error(404, 'Invalid URL: %s' % self.path)

    def do_DELETE(self):
        for url, func in DELETE_URL_MAPPER.items():
            matched = url.match(self.path)

            if not matched:
                continue

            # Get url embedded variables
            args_dict = matched.groupdict()

            # Get params
            params = self._extract_params()

            # Merge all args
            args_dict.update(**params)

            # Admin Check
            args_dict['is_admin'] = self._check_authentication()

            # Send data to sql
            response = getattr(dat_handler, func)(**args_dict)
            if 'admin_error' in response:
                self.do_AUTHHEAD()
            else:
                self._set_headers()

            self.wfile.write(json.dumps(response))
            return
        
        self.send_error(404, 'Invalid URL: %s' % self.path)


if __name__ == '__main__':
    try:
        server = HTTPServer(('', PORT_NUMBER), RequestHandler)
        print 'Started httpserver on port ' , PORT_NUMBER
        
        #Wait forever for incoming http requests
        server.serve_forever()

    except KeyboardInterrupt:
        print '^C received, shutting down the web server'
        server.socket.close()