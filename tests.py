import urllib.request
import json
import sys
import pytest



# correct_request_payload = {"usd_summ": 1430}

def make_request(payload):
    myurl = "http://localhost:8080/usd-rub"
    req = urllib.request.Request(myurl, method='PUT')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(payload)
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)
    return response



def test_status_code_equals_200():
    response = make_request ({"initial_currency":"RUB", "initial_amount":1000})
    assert response.getcode() == 200

def test_check_content_type_equals_json():
    response = make_request ({"initial_currency":"RUB", "initial_amount":1000})
    assert response.headers['Content-Type'] == "application/json"

def test_check_incorrect_initial_currency():
    response = make_request ({"initial_currency":"RUBs", "initial_amount":1000})
    byte_f = response.read()
    json_f = json.loads(byte_f.decode('utf-8'))
    assert json_f['error'] == "Incorrect initial currency. Allowed are USD, RUB"

def test_belivable_rate():
    response = make_request ({"initial_currency":"USD", "initial_amount":1})
    byte_f = response.read()
    json_f = json.loads(byte_f.decode('utf-8'))
    exchange_rate = json_f['exchange_rate']
    assert exchange_rate > 0 and exchange_rate < 1000



