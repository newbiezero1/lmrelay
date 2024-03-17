import time
import hashlib
import hmac
import requests
import json


class Gateio(object):
    def __init__(self, key: str, secret: str):
        self.key = key  # api_key
        self.secret = secret  # api_secret
        self.host = "https://api.gateio.ws"
        self.prefix = "/api/v4"
        self.common_headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}

    def gen_sign(self, method, url, query_string=None, payload_string=None):
        t = time.time()
        m = hashlib.sha512()
        m.update((payload_string or "").encode('utf-8'))
        hashed_payload = m.hexdigest()
        s = '%s\n%s\n%s\n%s\n%s' % (method, url, query_string or "", hashed_payload, t)
        sign = hmac.new(self.secret.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()
        return {'KEY': self.key, 'Timestamp': str(t), 'SIGN': sign}

    def req(self, method: str, url:str, param: dict, query: str = None):
        data = None
        if param:
            #request_content = json.dumps(param)
            sign_headers = self.gen_sign(method, self.prefix + url, "", param)
            data = param
        elif query is not None:
            sign_headers = self.gen_sign('GET', self.prefix + url, query)
            sign_headers.update(sign_headers)

        #sign_headers.update(self.common_headers)
        headers= self.common_headers.copy()
        headers.update(sign_headers)
        print('signature headers: %s' % headers)
        res = requests.request(method, self.host + self.prefix + url, headers=headers, data=data)
        print(res.json())
        return res.json()

    def get_positions(self) -> list:
        param = ''
        positions = self.req('GET', '/futures/usdt/positions', {}, param)
        return positions

    def get_positions_history(self, from_t=0) -> list:
        param = ''
        positions = self.req('GET', '/futures/usdt/position_close', {}, param)
        return positions

    def get_bars(self, pair: str, interval: str) -> list:
        param = f'contract={pair}_USDT&interval={interval}&limit=3'
        bars = self.req('GET', f'/futures/usdt/candlesticks?{param}', {}, param)
        return bars

    def close_position(self, pair: dict) -> None:
        url = '/futures/usdt/orders'
        body='{"contract":"'+pair+'_USDT","size":0,"close":true,"price":0,"tif":"ioc"}'
        print(body)
        r = self.req('POST', url, body)

