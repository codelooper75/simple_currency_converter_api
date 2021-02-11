import http.server
import importlib
import json
import os
import re
import shutil
import sys
import urllib.request
import urllib.parse

import logging
import sys


# LOGGING SETTINGS
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')


file_handler = logging.FileHandler('api.log') #logs to file
file_handler.setLevel(logging.INFO) #will allow to include ERROR level event in log
file_handler.setFormatter(formatter)


stream_handler = logging.StreamHandler() #will log to stdout
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.CRITICAL)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


from exchange_rate_parser import get_exchange_rate

importlib.reload(sys)

here = os.path.dirname(os.path.realpath(__file__))

success_response = {}

def service_worker():
    pass


def usd_rub(handler):


    payload = handler.get_payload()
    initial_currency = payload['initial_currency']
    init_amount = payload['initial_amount']
    exchange_rate = get_exchange_rate()  # todo rename to get_exchage_rate
    # print('inside try')

    try:
        init_amount = int(init_amount)
    except:
        error = "Please provide initial amount as integer"
        logger.info(f'initial_currency: {initial_currency}, init_amount:{init_amount} '
                    f'exchange_rate:{exchange_rate}')
        return ({"error": error})

    if initial_currency == 'USD':
        final_currency = 'RUB'
        final_amount = init_amount * exchange_rate

    elif initial_currency == 'RUB':
        final_currency = 'USD'
        final_amount = init_amount * 1 / exchange_rate

    else:
        error = "Incorrect initial currency. Allowed are USD, RUB"
        logger.info(f'initial_currency: {initial_currency}, init_amount:{init_amount} '
                    f'exchange_rate:{exchange_rate}')
        return ({"error": error})

    success_response["initial_currency"] = initial_currency
    success_response["init_amount"] = init_amount
    success_response["exchange_rate"] = exchange_rate
    success_response["final_currency"] = final_currency
    success_response["final_amount"] = final_amount

    logger.info(f'initial_currency: {initial_currency}, init_amount:{init_amount} '
                f'exchange_rate:{exchange_rate}, final_currency:{final_currency}, final_amount:{final_amount} ')

    return success_response

routes = {
    r'^/usd-rub': {'PUT': usd_rub, 'media_type': 'application/json'},

    }

poll_interval = 0.1

def rest_call_json(url, payload=None, with_payload_method='PUT'):
    'REST call with JSON decoding of the response and JSON payloads'
    if payload:
        if not isinstance(payload, str):
            payload = json.dumps(payload)
        # PUT or POST
        response = urllib.request.urlopen(
            MethodRequest(url, payload.encode(), {'Content-Type': 'application/json'}, method=with_payload_method))

        response = response.read().decode()
        return json.loads(response)


class MethodRequest(urllib.request.Request):
    'See: https://gist.github.com/logic/2715756'

    def __init__(self, *args, **kwargs):
        if 'method' in kwargs:
            self._method = kwargs['method']
            del kwargs['method']
        else:
            self._method = None
        return urllib.request.Request.__init__(self, *args, **kwargs)

    def get_method(self, *args, **kwargs):
        return self._method if self._method is not None else urllib.request.get_method(self, *args, **kwargs)


class RESTRequestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.routes = routes

        return http.server.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)


    def do_PUT(self):
        self.handle_method('PUT')

    def get_payload(self):
        payload_len = int(self.headers.get('content-length', 0))
        payload = self.rfile.read(payload_len)
        payload = json.loads(payload.decode())
        return payload

    def handle_method(self, method):
        route = self.get_route()
        if route is None:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Route not found\n'.encode())
        else:
            if method in route:
                content = route[method](self)
                if content is not None:
                    self.send_response(200)
                    if 'media_type' in route:
                        self.send_header('Content-type', route['media_type'])
                    self.end_headers()
                    if method != 'DELETE':
                        self.wfile.write(json.dumps(content).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write('Not found\n'.encode())
            else:
                self.send_response(405)
                self.end_headers()
                self.wfile.write(method + ' is not supported\n'.encode())

    def get_route(self):
        for path, route in self.routes.items():
            if re.match(path, self.path):
                return route
        return None


def rest_server(port):
    'Starts the REST server'
    http_server = http.server.HTTPServer(('', port), RESTRequestHandler)
    http_server.service_actions = service_worker
    print('Starting HTTP server at port %d' % port)
    try:
        http_server.serve_forever(poll_interval)
    except KeyboardInterrupt:
        pass
    print('Stopping HTTP server')
    http_server.server_close()


def main(argv):
    rest_server(8080)


if __name__ == '__main__':
    main(sys.argv[1:])
